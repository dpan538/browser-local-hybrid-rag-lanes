# Parallel Research Hybrid Lane Related Work Matrix

Generated: 2026-06-08

Scope: primary-source matrix for the parallel hybrid answer-lane research
branch. This matrix is for paper framing and does not imply archive product or
runtime changes.

| Theme | Primary Source | What It Covers | Relevance To Hybrid Answer Lanes | Remaining Gap |
|---|---|---|---|---|
| Browser-local LLM inference | WebLLM paper: https://arxiv.org/abs/2412.15803 | In-browser LLM inference using WebGPU and WebAssembly | Establishes browser-local generation as feasible | Does not specify which answer lanes should bypass generation |
| Browser-local LLM runtime | WebLLM repo: https://github.com/mlc-ai/web-llm | OpenAI-compatible API, streaming, JSON mode, WebGPU, workers, cache backends | Supports the implementation context for local Qwen/WebLLM RAG | Runtime capability is not a generation policy |
| WebLLM deployment docs | MLC WebLLM docs: https://llm.mlc.ai/docs/deploy/webllm.html | WebGPU acceleration, model records, custom model deployment | Shows browser execution is configurable and componentized | No archive-specific contract or lane taxonomy |
| Browser WebGPU runtime comparison | ONNX Runtime WebGPU: https://onnxruntime.ai/docs/tutorials/web/ep-webgpu.html | WebGPU execution provider, graph capture, GPU tensor paths | Research-only comparison path for browser inference | Not focused on text-generation answer semantics |
| Browser ML runtime comparison | Transformers.js WebGPU: https://huggingface.co/docs/transformers.js/guides/webgpu | WebGPU acceleration via `device: "webgpu"` | Confirms broader browser-local ML ecosystem | Does not address rights-aware RAG contracts |
| WebGPU LLM systems | LlamaWeb: https://arxiv.org/abs/2605.20706 | Memory-efficient, portable WebGPU inference for `llama.cpp` | Places WebGPU LLM inference in systems research | Not about answer-lane routing or deterministic evidence delivery |
| Browser-local retrieval | MeMemo project: https://zijie.wang/papers/mememo/ | Browser HNSW dense retrieval using IndexedDB and Web Workers | Direct neighbor for private browser-local RAG | Retrieval layer does not define generation/no-generation lanes |
| Browser-local retrieval | MeMemo paper: https://arxiv.org/abs/2407.01972 | On-device retrieval augmentation and RAG Playground | Supports private/personalized local RAG motivation | No source/rights deterministic lane design |
| RAG foundation | RAG: https://arxiv.org/abs/2005.11401 | Parametric plus non-parametric memory, provenance, updatable knowledge | Grounds the archive evidence-packet motivation | Still assumes generation as the answer surface |
| RAG evaluation | RAGAS: https://arxiv.org/abs/2309.15217 | Context relevance, faithful use of retrieved context, generation quality | Supports multi-dimensional RAG evaluation | Does not separate deterministic evidence rendering from generation |
| RAG evaluation | ARES: https://arxiv.org/abs/2311.09476 | Context relevance, answer faithfulness, answer relevance | Useful for contract plus answer-quality framing | Mostly evaluates generated answers |
| Citation faithfulness | ALCE: https://arxiv.org/abs/2305.14627 and https://github.com/princeton-nlp/ALCE | Fluency, correctness, citation quality | Supports source-backed answer evaluation | Citation quality is not the same as exact rights-field preservation |
| Verifiability | Evaluating Verifiability in Generative Search Engines: https://arxiv.org/abs/2304.09848 | Citation recall and precision in generated search answers | Supports provenance and citation precision framing | Does not study local deterministic refusal/source rendering |
| Retrieval adaptivity | Self-RAG: https://arxiv.org/abs/2310.11511 | Adaptive retrieval and self-critique to improve factuality/citation accuracy | Shows not every query should use retrieval uniformly | Still keeps the LM central to critique/generation |
| Retrieval correction | Corrective RAG: https://arxiv.org/abs/2401.15884 | Retrieval-quality evaluation and corrective actions | Supports evidence sufficiency as a runtime decision | Does not ask whether exact evidence fields should skip generation |
| Neuro-symbolic systems | MRKL: https://arxiv.org/abs/2205.00445 | Modular LMs plus discrete tools and reasoning modules | Conceptual basis for model/runtime division of labor | Not browser-local, not archive rights-aware |
| Programmable guardrails | NeMo Guardrails: https://arxiv.org/abs/2310.10501 | Runtime rails independent of the underlying LLM | Supports deterministic/programmable controls around LLMs | Guardrails do not directly define answer-lane latency accounting |
| Structured LLM programs | SGLang: https://arxiv.org/abs/2312.07104 | Structured LM programs and runtime optimizations | Supports multi-step structured generation and runtime co-design | Optimizes generation rather than bypassing it for exact lanes |
| LLM programming | LMQL: https://arxiv.org/abs/2212.06094 and https://github.com/lmql-lang/lmql | Prompt programming, constraints, control flow, efficient calls | Useful for constrained generation comparisons | Constrained generation is still generation |
| Logical control | Ctrl-G: https://arxiv.org/abs/2406.13892 | Logical constraints over LLM generation | Supports reliable output control | Does not cover deterministic field rendering as the preferred path |
| Constrained decoding | NeuroLogic A*esque: https://arxiv.org/abs/2112.08726 | Constraint-satisfying decoding with lookahead heuristics | Useful structured-generation related work | More complex than needed for exact source/rights field copying |
| Structured-output evaluation | Structured output benchmark: https://arxiv.org/abs/2501.10868 | JSON-schema constrained decoding behavior | Helps explain why syntax guarantees are not enough | Rights/source correctness is semantic and evidentiary, not just schema validity |
| Mixed-initiative UI | Horvitz mixed-initiative UI: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/chi99horvitz.pdf | Coupling automated services with direct manipulation | Supports UI/runtime as an active mediator | Predates LLM RAG and browser-local inference |
| Human-AI guidelines | Microsoft HAI guidelines: https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/ | Human-AI interaction guidelines for AI-infused systems | Supports communicating uncertainty, user control, and appropriate trust | General guidelines, not an archive RAG methodology |
| Transparent LLM workflows | AI Chains: https://arxiv.org/abs/2110.01691 | Decomposed LLM prompt chains for transparent/control workflows | Supports decomposing AI behavior into inspectable steps | Still prompt-chain oriented rather than deterministic evidence-field delivery |
| LLM serving latency | vLLM / PagedAttention: https://arxiv.org/abs/2309.06180 | Throughput/latency tradeoffs and KV-cache memory management | Normalizes precise serving metrics | Server-side serving results do not transfer directly to browser-local WebGPU |
| LLM latency phases | DistServe: https://arxiv.org/abs/2401.09670 | Prefill/decode disaggregation, TTFT and TPOT objectives | Supports phase-specific latency accounting | Does not include deterministic UI/runtime assembly as a first-class phase |
| WebGPU overhead | WebGPU dispatch overhead: https://arxiv.org/abs/2604.02344 | Batch-size-1 WebGPU overhead across browsers/backends/GPU vendors | Directly relevant to local WebGPU latency interpretation | Studies model execution, not answer-lane policy |
| Tool-use latency | Chain-of-Abstraction: https://arxiv.org/abs/2401.17464 | More efficient tool use in LLM agents | Supports measuring model/tool interaction costs | Tool latency is related but not identical to deterministic answer rendering |
| Cultural-heritage rights | RightsStatements.org: https://rightsstatements.org/en/ | Standardized rights statements for online cultural heritage | Establishes rights fields as machine/human-readable evidence | Does not address LLM/RAG answer generation |
| Cultural-heritage rights | Europeana rights statements: https://pro.europeana.eu/page/available-rights-statements | Rights statements for digital objects and reuse conditions | Supports source-authoritative rights metadata | Does not specify AI assistant behavior over rights metadata |

## Matrix Interpretation

The closest prior-work cluster is not one source; it is the intersection of
browser-local inference, browser-local retrieval, RAG provenance, programmable
rails, mixed-initiative UI, and latency accounting.

The independent gap is:

No primary source above directly studies answer-lane-specific decisions about
what a browser-local small-model RAG system should not generate, especially
under rights-aware archive evidence contracts.

## Paper-Useful Related-Work Buckets

1. Browser-local inference and retrieval.
2. Grounded RAG and citation faithfulness.
3. Refusal, abstention, and retrieval sufficiency.
4. Guardrails, neuro-symbolic systems, and structured generation.
5. UI/runtime-mediated human-AI systems.
6. Latency accounting and phase-specific LLM systems measurement.
7. Cultural-heritage rights metadata and source authority.
