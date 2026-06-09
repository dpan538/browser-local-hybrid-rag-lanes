import * as webllm from "https://esm.run/@mlc-ai/web-llm";

const DETERMINISTIC_FIELDS = [
  "source",
  "rights_label",
  "reuse_permission",
  "public_domain_status"
];
const PLACEHOLDER = "[not provided in source]";
const CONDITIONS = ["all_generation", "hybrid_without_refusal", "full_hybrid"];

const state = {
  health: null,
  promptPack: null,
  runtimeRows: [],
  evalRows: new Map(),
  engine: null,
  modelLoadMs: null,
  webgpu: null,
  records: [],
  requestCount: 0,
  wasBackgrounded: false,
  longTaskCount: 0,
  lastLongTaskCount: 0
};

const el = (id) => document.getElementById(id);

if ("PerformanceObserver" in window) {
  try {
    const observer = new PerformanceObserver((list) => {
      state.longTaskCount += list.getEntries().length;
    });
    observer.observe({ type: "longtask", buffered: true });
  } catch (_error) {
    // Long Task API is optional.
  }
}

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") state.wasBackgrounded = true;
});

function log(message) {
  const stamp = new Date().toLocaleTimeString();
  el("logBox").textContent += `[${stamp}] ${message}\n`;
  el("logBox").scrollTop = el("logBox").scrollHeight;
}

function setBadge(id, text, kind = "") {
  const node = el(id);
  node.textContent = text;
  node.className = `badge ${kind}`.trim();
}

async function getJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${path} returned ${res.status}`);
  return res.json();
}

function selectedQuery() {
  const queryId = el("querySelect").value;
  return state.runtimeRows.find((row) => row.query_id === queryId);
}

function firstRecord(row) {
  return row?.evidence_packet?.records?.[0] || {};
}

function deterministicFields(row) {
  const record = firstRecord(row);
  const output = {};
  for (const field of DETERMINISTIC_FIELDS) {
    output[field] = String(record[field] ?? PLACEHOLDER);
  }
  return output;
}

function shouldRefuse(row) {
  const evidenceState = row.routing_inputs?.evidence_state;
  const intentSignal = row.routing_inputs?.intent_signal;
  if (intentSignal === "refusal_required" && ["partial", "missing", "contradictory"].includes(evidenceState)) {
    return true;
  }
  return ["missing", "contradictory"].includes(evidenceState);
}

function executionModeFor(row, condition) {
  const intentSignal = row.routing_inputs?.intent_signal;
  if (condition === "all_generation") return "generative_answer";
  if (condition === "full_hybrid" && shouldRefuse(row)) return "deterministic_refusal";
  if (intentSignal === "mixed") return "compound_answer";
  if (["source/rights", "source_rights", "rights_only"].includes(intentSignal)) {
    return "deterministic_render";
  }
  return "generative_answer";
}

function outputFormatFor(executionMode) {
  if (executionMode === "compound_answer") return "structured_fields_plus_natural_language";
  if (executionMode === "generative_answer") return "bounded_natural_language";
  if (executionMode === "deterministic_refusal") return "refusal_template";
  return "structured_fields";
}

function approxTokens(text) {
  return String(text || "").split(/\s+/).filter(Boolean).length;
}

function tokensPerSecond(outputTokens, totalMs, ttftMs) {
  const decodeMs = Math.max(1, Number(totalMs || 0) - Number(ttftMs || 0));
  if (!outputTokens || !totalMs) return null;
  return outputTokens / (decodeMs / 1000);
}

function stripThinking(text) {
  const raw = String(text || "");
  if (!raw.includes("<think>")) return raw.trim();
  if (raw.includes("</think>")) {
    return raw.split("</think>").slice(1).join("</think>").trim();
  }
  return raw.replace(/<think>[\s\S]*$/i, "").trim();
}

function parseGeneratedJson(text) {
  const raw = stripThinking(text);
  const unfenced = raw.replace(/^```(?:json)?/i, "").replace(/```$/i, "").trim();
  try {
    const parsed = JSON.parse(unfenced);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch (_error) {
    return {};
  }
}

function buildPrompt(row, condition) {
  const promptPack = state.promptPack || {};
  const conditionPrompt = promptPack.conditions?.[condition] || {};
  const answerKeys = [
    "source",
    "rights_label",
    "reuse_permission",
    "public_domain_status",
    "research_guidance",
    "refusal",
    "caveats"
  ];
  return [
    "You are running a research-only browser-local Qwen RAG experiment.",
    "Generated text is not archive evidence.",
    "Use only the supplied evidence packet.",
    "Do not output hidden reasoning, chain-of-thought, or <think> tags.",
    "Return one JSON object only. Do not wrap it in markdown.",
    `Required keys: ${answerKeys.join(", ")}.`,
    "Use null for refusal when the answer should not refuse. Use an array for caveats.",
    "",
    `Condition: ${condition}`,
    `Condition instruction: ${conditionPrompt.prompt_template || ""}`,
    `Model role: ${conditionPrompt.model_role || ""}`,
    "",
    `Question: ${row.query?.text || ""}`,
    "",
    "Global constraints:",
    ...(promptPack.global_constraints || []).map((line) => `- ${line}`),
    "",
    "Runtime routing inputs:",
    JSON.stringify(row.routing_inputs || {}, null, 2),
    "",
    "Evidence packet:",
    JSON.stringify(row.evidence_packet || {}, null, 2)
  ].join("\n");
}

async function probeWebGPU() {
  const result = {
    status: "unavailable",
    has_navigator_gpu: Boolean(navigator.gpu),
    adapter_info: null,
    error: null
  };
  try {
    if (!navigator.gpu) {
      result.error = "navigator.gpu is not available";
      return result;
    }
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) {
      result.error = "requestAdapter returned null";
      return result;
    }
    result.status = "available";
    if (adapter.info) result.adapter_info = adapter.info;
    if (typeof adapter.requestAdapterInfo === "function") {
      result.adapter_info = await adapter.requestAdapterInfo();
    }
  } catch (error) {
    result.status = "error";
    result.error = error?.message || String(error);
  }
  return result;
}

async function loadEngine() {
  if (state.engine) {
    setBadge("engineBadge", "WebLLM loaded", "good");
    log("WebLLM engine already loaded; reusing warm engine.");
    return;
  }
  const appConfig = {
    model_list: [
      {
        model: el("modelUrl").value.trim(),
        model_id: el("modelId").value.trim(),
        model_lib: el("modelLibUrl").value.trim(),
        overrides: {
          context_window_size: 4096
        }
      }
    ]
  };
  setBadge("engineBadge", "loading", "warn");
  log("Loading Qwen WebLLM runtime. Browser may download/cache model artifacts outside the repo.");
  const started = performance.now();
  state.engine = await webllm.CreateMLCEngine(el("modelId").value.trim(), {
    appConfig,
    initProgressCallback: (report) => {
      if (report?.text) log(report.text);
    }
  });
  state.modelLoadMs = performance.now() - started;
  setBadge("engineBadge", `loaded ${Math.round(state.modelLoadMs)} ms`, "good");
  log(`Engine loaded in ${Math.round(state.modelLoadMs)} ms.`);
}

async function streamCompletion(prompt) {
  if (!state.engine) throw new Error("Load Qwen WebLLM before running a generative lane.");
  const started = performance.now();
  let firstTokenAt = null;
  let answerText = "";
  const completion = await state.engine.chat.completions.create({
    messages: [
      {
        role: "system",
        content: "You are a cautious rights-aware archive research assistant. Preserve evidence caveats and return JSON only."
      },
      { role: "user", content: prompt }
    ],
    temperature: Number(el("temperature").value || 0.2),
    max_tokens: Number(el("maxTokens").value || 160),
    extra_body: {
      enable_thinking: false,
      chat_template_kwargs: {
        enable_thinking: false
      }
    },
    stream: true
  });

  for await (const chunk of completion) {
    const delta = chunk.choices?.[0]?.delta?.content || "";
    if (!delta) continue;
    if (firstTokenAt === null) firstTokenAt = performance.now();
    answerText += delta;
    el("answerBox").textContent = [
      "PROMPT",
      prompt,
      "",
      "STREAMING ANSWER",
      stripThinking(answerText)
    ].join("\n");
  }
  const ended = performance.now();
  const cleaned = stripThinking(answerText);
  const outputTokens = approxTokens(cleaned);
  const ttftMs = firstTokenAt === null ? null : firstTokenAt - started;
  const totalMs = ended - started;
  return {
    raw_answer_text: answerText,
    cleaned_answer_text: cleaned,
    parsed_answer: parseGeneratedJson(cleaned),
    ttft_ms: ttftMs,
    total_latency_ms: totalMs,
    output_tokens: outputTokens,
    tokens_per_second: tokensPerSecond(outputTokens, totalMs, ttftMs)
  };
}

function answerRefused(answer) {
  const value = String(answer.refusal || "").trim().toLowerCase();
  return Boolean(value && value !== "none" && value !== "null");
}

function fieldState(row, field) {
  return row.evidence_packet?.field_checklist?.[field] || "not_applicable";
}

function checkContract(record, runtimeRow, evalRow) {
  const answer = record.answer || {};
  const condition = record.condition;
  const sourceRecord = firstRecord(runtimeRow);
  const didRefuse = answerRefused(answer);
  const results = {};
  for (const field of DETERMINISTIC_FIELDS) {
    if (didRefuse) {
      results[`${field}_rendered`] = "n/a";
      results[`${field}_mutation`] = "n/a";
      continue;
    }
    const value = String(answer[field] || "");
    const expected = String(sourceRecord[field] ?? PLACEHOLDER);
    if (fieldState(runtimeRow, field) === "absent") {
      results[`${field}_rendered`] = value === PLACEHOLDER ? "pass" : "warning";
    } else {
      results[`${field}_rendered`] = value.trim() ? "pass" : "fail";
    }
    if (["hybrid_without_refusal", "full_hybrid"].includes(condition)) {
      results[`${field}_mutation`] = value === expected ? "pass" : "fail";
    } else {
      results[`${field}_mutation`] = "n/a";
    }
  }
  if (didRefuse) {
    results.source_pointer_preserved = "n/a";
  } else {
    const sourceValue = String(answer.source || "");
    const expectedSource = String(sourceRecord.source || "");
    results.source_pointer_preserved = expectedSource && sourceValue.includes(expectedSource) ? "pass" : "warning";
  }
  const rightsMutated = results.rights_label_mutation === "fail";
  const statusMutated = results.public_domain_status_mutation === "fail";
  results.rights_label_upgrade = rightsMutated || statusMutated ? "warning" : "pass";

  const checklist = runtimeRow.evidence_packet?.field_checklist || {};
  const hasConflict = Object.values(checklist).some((value) => value === "present_but_conflicting");
  if (hasConflict) {
    const text = JSON.stringify(answer).toLowerCase();
    results.conflict_surfaced = ["conflict", "contradict", "inconsistent"].some((term) => text.includes(term)) ? "pass" : "fail";
  } else {
    results.conflict_surfaced = "n/a";
  }

  const meta = evalRow?.evaluation_labels?.fixture_meta || {};
  if (meta.refusal_expected) {
    results.refusal_expected_alignment = didRefuse ? "pass" : "fail";
  } else {
    results.refusal_expected_alignment = didRefuse ? "warning" : "pass";
  }
  for (const field of DETERMINISTIC_FIELDS) {
    if (!didRefuse && fieldState(runtimeRow, field) === "absent") {
      results[`${field}_placeholder_used`] = String(answer[field] || "") === PLACEHOLDER ? "pass" : "warning";
    }
  }
  return results;
}

function contractMetrics(autoContract) {
  return {
    contract_failure: Object.values(autoContract).some((value) => value === "fail"),
    contract_warning: Object.values(autoContract).some((value) => value === "warning"),
    field_omission_count: Object.entries(autoContract).filter(([key, value]) => key.endsWith("_rendered") && value === "fail").length,
    field_mutation_count: Object.entries(autoContract).filter(([key, value]) => key.endsWith("_mutation") && value === "fail").length,
    unsupported_upgrade_count: ["warning", "fail"].includes(autoContract.rights_label_upgrade) ? 1 : 0,
    unsupported_claims: 0,
    hallucination_count: 0,
    hallucination_severity: null,
    refusal_false_positive: autoContract.refusal_expected_alignment === "warning",
    refusal_false_negative: autoContract.refusal_expected_alignment === "fail"
  };
}

function envFlags(warmState) {
  state.requestCount += 1;
  const longTaskDelta = Math.max(0, state.longTaskCount - state.lastLongTaskCount);
  state.lastLongTaskCount = state.longTaskCount;
  return {
    cold_start: state.requestCount === 1 || warmState === "cold_start",
    warmup: warmState === "warmup",
    warm: warmState === "warm",
    tab_backgrounded: document.visibilityState === "hidden" || state.wasBackgrounded,
    long_task_gc: Boolean(longTaskDelta || state.longTaskCount),
    network_variance: false,
    manual_interruption: false,
    client_environment: {
      visibility_state: document.visibilityState,
      was_backgrounded: state.wasBackgrounded,
      long_task_count: state.longTaskCount,
      long_task_count_delta: longTaskDelta,
      user_agent: navigator.userAgent,
      webgpu: state.webgpu,
      model_id: el("modelId").value.trim(),
      model_url: el("modelUrl").value.trim(),
      model_lib_url: el("modelLibUrl").value.trim()
    }
  };
}

function baseAnswer(executionMode) {
  return {
    output_mode: executionMode,
    source: "",
    rights_label: "",
    reuse_permission: "",
    public_domain_status: "",
    research_guidance: "",
    refusal: null,
    caveats: ["evidence_correctness_requires_source_audit"]
  };
}

function renderRecord(record) {
  el("answerBox").textContent = JSON.stringify(record.answer, null, 2);
  el("metricsBox").textContent = JSON.stringify({
    latency: record.latency,
    auto_contract: record.auto_contract,
    env_flags: record.env_flags
  }, null, 2);
  el("recordsBox").textContent = state.records.map((row) => JSON.stringify(row)).join("\n");
  setBadge("recordBadge", `${state.records.length} records`, state.records.length ? "good" : "");
  el("saveBtn").disabled = state.records.length === 0;
}

async function runCondition(row, condition) {
  const executionMode = executionModeFor(row, condition);
  const warmState = el("warmState").value;
  const runId = el("runId").value.trim() || "qwen_webllm_smoke_v0";
  const started = performance.now();
  const timings = {
    retrieval_latency_ms: 0.0,
    deterministic_assembly_latency_ms: 0.0,
    qwen_generation_latency_ms: 0.0,
    hybrid_system_latency_ms: 0.0,
    ttft_ms: null,
    tokens_per_second: null,
    latency_saved_by_deterministic_ms: null,
    warm_state: warmState
  };
  const answer = baseAnswer(executionMode);
  let generated = null;
  let prompt = "";

  if (executionMode === "deterministic_refusal") {
    const detStarted = performance.now();
    answer.refusal = "I cannot answer this from the provided evidence.";
    answer.caveats.push("deterministic_refusal_missing_or_contradictory_evidence");
    timings.deterministic_assembly_latency_ms = performance.now() - detStarted;
  } else {
    if (["hybrid_without_refusal", "full_hybrid"].includes(condition)) {
      const detStarted = performance.now();
      Object.assign(answer, deterministicFields(row));
      timings.deterministic_assembly_latency_ms = performance.now() - detStarted;
    }
    const needsGeneration = executionMode === "generative_answer" || executionMode === "compound_answer" || condition === "all_generation";
    if (needsGeneration) {
      prompt = buildPrompt(row, condition);
      const genStarted = performance.now();
      generated = await streamCompletion(prompt);
      timings.qwen_generation_latency_ms = performance.now() - genStarted;
      timings.ttft_ms = generated.ttft_ms;
      timings.tokens_per_second = generated.tokens_per_second;
      const parsed = generated.parsed_answer || {};
      answer.research_guidance = String(parsed.research_guidance || generated.cleaned_answer_text || "");
      answer.refusal = parsed.refusal === undefined ? null : parsed.refusal;
      answer.caveats = Array.isArray(parsed.caveats)
        ? [...parsed.caveats, "evidence_correctness_requires_source_audit"]
        : answer.caveats;
      if (condition === "all_generation") {
        answer.source = String(parsed.source || generated.cleaned_answer_text || "");
        answer.rights_label = String(parsed.rights_label || generated.cleaned_answer_text || "");
        answer.reuse_permission = String(parsed.reuse_permission || generated.cleaned_answer_text || "");
        answer.public_domain_status = String(parsed.public_domain_status || generated.cleaned_answer_text || "");
      }
    }
    if (condition === "full_hybrid" && !answer.refusal) answer.refusal = "none";
  }

  timings.hybrid_system_latency_ms = performance.now() - started;
  const evalRow = state.evalRows.get(row.query_id);
  const draftRecord = {
    run_id: runId,
    query_id: row.query_id,
    condition,
    intent_label: row.routing_inputs?.intent_signal || "",
    execution_mode: executionMode,
    rule_match: {
      rule_version: row.routing_inputs?.rule_version || "lane_rules_v1",
      rule_name: null,
      routing_undefined: false,
      routing_notes: "browser_qwen_webllm_smoke_v0"
    },
    evidence_state: row.routing_inputs?.evidence_state || "not_applicable",
    field_state_checklist: row.evidence_packet?.field_checklist || {},
    latency: timings,
    contract_metrics: {
      contract_failure: false,
      contract_warning: false,
      field_omission_count: 0,
      field_mutation_count: 0,
      unsupported_upgrade_count: 0,
      unsupported_claims: 0,
      hallucination_count: 0,
      hallucination_severity: null,
      refusal_false_positive: false,
      refusal_false_negative: false
    },
    format: {
      output_format: outputFormatFor(executionMode),
      format_consistency_score: null,
      compound_answer: executionMode === "compound_answer"
    },
    protocol_artifacts: {},
    answer: {
      ...answer,
      model_meta: generated ? {
        producer: "webllm_qwen3_5_0_8b_research_runtime",
        primary_model_identity: "Qwen/Qwen3.5-0.8B",
        model_id: el("modelId").value.trim(),
        model_url: el("modelUrl").value.trim(),
        model_lib_url: el("modelLibUrl").value.trim(),
        model_load_ms: state.modelLoadMs,
        raw_answer_text: generated.raw_answer_text,
        prompt_chars: prompt.length,
        prompt_tokens_est: Math.ceil(prompt.length / 4),
        output_tokens: generated.output_tokens
      } : {
        producer: "deterministic_hybrid_system_v1",
        primary_model_identity: "Qwen/Qwen3.5-0.8B",
        qwen_invoked: false
      }
    },
    auto_contract: {},
    env_flags: envFlags(warmState),
    timestamp_utc: new Date().toISOString()
  };
  draftRecord.auto_contract = checkContract(draftRecord, row, evalRow);
  draftRecord.contract_metrics = contractMetrics(draftRecord.auto_contract);
  state.records.push(draftRecord);
  renderRecord(draftRecord);
  log(`Completed ${row.query_id} ${condition} as ${executionMode}.`);
  return draftRecord;
}

async function runSelectedCondition() {
  const row = selectedQuery();
  if (!row) return;
  const condition = el("conditionSelect").value;
  el("runOneBtn").disabled = true;
  try {
    await runCondition(row, condition);
  } catch (error) {
    log(`ERROR: ${error?.message || String(error)}`);
    el("metricsBox").textContent = String(error?.message || error);
  } finally {
    el("runOneBtn").disabled = false;
  }
}

async function runThreeConditions() {
  const row = selectedQuery();
  if (!row) return;
  el("runThreeBtn").disabled = true;
  try {
    for (const condition of CONDITIONS) {
      await runCondition(row, condition);
    }
  } catch (error) {
    log(`ERROR: ${error?.message || String(error)}`);
    el("metricsBox").textContent = String(error?.message || error);
  } finally {
    el("runThreeBtn").disabled = false;
  }
}

async function saveRecords({ allowOverwrite = false } = {}) {
  if (!state.records.length) return;
  el("saveBtn").disabled = true;
  try {
    const runId = el("runId").value.trim() || "qwen_webllm_smoke_v0";
    const res = await fetch("/api/runs/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        run_id: runId,
        records: state.records,
        allow_overwrite: allowOverwrite
      })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `save returned ${res.status}`);
    log(`Saved ${data.records} records to ${data.path}.`);
  } catch (error) {
    log(`SAVE ERROR: ${error?.message || String(error)}`);
  } finally {
    el("saveBtn").disabled = state.records.length === 0;
  }
}

async function runBatch(start, limit, runId) {
  const rows = state.runtimeRows.slice(start - 1, start - 1 + limit);
  if (!rows.length) throw new Error("No rows selected for batch.");
  el("runScopeBtn").disabled = true;
  el("run10Btn").disabled = true;
  el("run50Btn").disabled = true;
  el("runOneBtn").disabled = true;
  el("runThreeBtn").disabled = true;
  el("runId").value = runId;
  state.records = [];
  renderRecord({
    answer: { status: "batch_started", rows: rows.length },
    latency: {},
    auto_contract: {},
    env_flags: {}
  });
  log(`Starting batch ${runId}: rows ${start}-${start + rows.length - 1}, ${rows.length} queries x ${CONDITIONS.length} conditions.`);
  try {
    for (const row of rows) {
      el("querySelect").value = row.query_id;
      for (const condition of CONDITIONS) {
        el("conditionSelect").value = condition;
        await runCondition(row, condition);
      }
    }
    await saveRecords({ allowOverwrite: false });
    log(`Batch ${runId} completed and save was requested.`);
  } finally {
    el("runScopeBtn").disabled = false;
    el("run10Btn").disabled = false;
    el("run50Btn").disabled = false;
    el("runOneBtn").disabled = false;
    el("runThreeBtn").disabled = false;
  }
}

async function runCustomBatch() {
  const start = Math.max(1, Number(el("batchStart").value || 1));
  const limit = Math.max(1, Number(el("batchLimit").value || 10));
  const runId = `qwen_webllm_batch_${limit}_v0`;
  try {
    await runBatch(start, limit, runId);
  } catch (error) {
    log(`BATCH ERROR: ${error?.message || String(error)}`);
  }
}

async function runFirst10() {
  try {
    await runBatch(1, 10, "qwen_webllm_pilot10_v0");
  } catch (error) {
    log(`PILOT10 ERROR: ${error?.message || String(error)}`);
  }
}

async function runFirst50() {
  try {
    await runBatch(1, 50, "qwen_webllm_scale50_v0");
  } catch (error) {
    log(`SCALE50 ERROR: ${error?.message || String(error)}`);
  }
}

function clearRecords() {
  state.records = [];
  el("recordsBox").textContent = "[]";
  setBadge("recordBadge", "0 records", "");
  el("saveBtn").disabled = true;
  log("Cleared in-page records.");
}

async function loadData() {
  state.health = await getJson("/api/health");
  state.promptPack = await getJson("/api/prompt-pack");
  state.runtimeRows = await getJson("/api/fixtures/runtime");
  const evalRows = await getJson("/api/fixtures/evaluation");
  state.evalRows = new Map(evalRows.map((row) => [row.query_id, row]));
  setBadge("healthBadge", `API ok · ${state.runtimeRows.length} rows`, "good");
  const select = el("querySelect");
  select.innerHTML = "";
  for (const row of state.runtimeRows) {
    const option = document.createElement("option");
    option.value = row.query_id;
    option.textContent = `${row.query_id} · ${row.routing_inputs?.intent_signal || ""}`;
    select.append(option);
  }
  log(`Loaded ${state.runtimeRows.length} runtime rows and ${evalRows.length} eval rows.`);
}

el("probeWebgpuBtn").addEventListener("click", async () => {
  el("probeWebgpuBtn").disabled = true;
  try {
    state.webgpu = await probeWebGPU();
    const kind = state.webgpu.status === "available" ? "good" : "bad";
    setBadge("webgpuBadge", `WebGPU ${state.webgpu.status}`, kind);
    log(`WebGPU probe: ${JSON.stringify(state.webgpu)}`);
  } finally {
    el("probeWebgpuBtn").disabled = false;
  }
});

el("loadWebllmBtn").addEventListener("click", async () => {
  el("loadWebllmBtn").disabled = true;
  try {
    await loadEngine();
  } catch (error) {
    setBadge("engineBadge", "load failed", "bad");
    log(`LOAD ERROR: ${error?.message || String(error)}`);
  } finally {
    el("loadWebllmBtn").disabled = false;
  }
});

el("runOneBtn").addEventListener("click", runSelectedCondition);
el("runThreeBtn").addEventListener("click", runThreeConditions);
el("runScopeBtn").addEventListener("click", runCustomBatch);
el("run10Btn").addEventListener("click", runFirst10);
el("run50Btn").addEventListener("click", runFirst50);
el("saveBtn").addEventListener("click", () => saveRecords({ allowOverwrite: false }));
el("clearBtn").addEventListener("click", clearRecords);

loadData().catch((error) => {
  setBadge("healthBadge", "API error", "bad");
  log(`INIT ERROR: ${error?.message || String(error)}`);
});
