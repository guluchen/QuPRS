# QuPRS v0.16.0 native / browser screen

The native comparator is this same capture/replay browser adapter compiled natively, not the unmodified single-pass upstream CLI. See METHODS.md. Pinned original paper input pairs; 200-second whole-request cap, Difference strategy. Five repeats only when the first successful whole request takes less than two seconds; all others are single-trial screens. Timing medians from one trial are not five-repeat estimates. No timeout imputation. Results are numerical estimates, not certified intervals. This Rust v0.16 fork is distinct from the earlier paper-era Python comparison.

220 cells, 892 trials, 73 input pairs / 110 mode pairs.

| Mode | Engine | Completed / cells | Distance available |
|---|---|---:|---:|
| hybrid | native | 30 / 37 | 13 |
| hybrid | wasm | 30 / 37 | 13 |
| wmc | native | 26 / 37 | 10 |
| wmc | wasm | 28 / 37 | 11 |
| reduction | native | 36 / 36 | 35 |
| reduction | wasm | 36 / 36 | 35 |

A completed report can be indeterminate or a tolerance-based reduction acceptance without a computed distance. Status counts and all errors are retained in JSON/CSV. Small circuit/GPMC enumeration tests provide separate correctness evidence; repeated benchmark timings alone do not establish ground truth.

Native/WASM or repeat discrepancies: **0**. See summary.json for every discrepancy.

Native processes use a 4 GiB address-space cap and 16 MiB stack. Each WASM module has a 512 MiB linear-memory maximum, with browser overhead outside that limit. Same-host native/WASM requests run serially on one pinned core; order is rotated. Every WASM trial uses a fresh Chromium process and HTTP server; both are closed before the next native or WASM sample, preventing asynchronous worker teardown from contaminating it. Browser launch and cleanup are timed separately, excluded from request latency. Page/server startup and browser launch are excluded; worker startup, core loading/instantiation and local-HTTP fetches remain inside browser requests. Native whole times include process startup. These timings are not public-network page-load measurements.

## Browser/native timing ratio

Only paired successful cells with native whole-request time >=100 ms enter these geometric means. A ratio above one means browser slower. Exact zero/near-zero native startup cases are omitted from this ratio only, never from coverage.
- hybrid: 2.159x (6 pairs).
- wmc: 2.437x (10 pairs).
- reduction: 1.980x (3 pairs).

Pairs from shards whose anchors exceed 10% are excluded from this additional quality-qualified timing subset only; all coverage cells and all raw diagnostic ratios above remain available. This is a subset screen, not a full-suite gate.
- Anchor-qualified hybrid: 2.159x (6 pairs).
- Anchor-qualified wmc: 2.437x (10 pairs).
- Anchor-qualified reduction: 1.980x (3 pairs).

Timing quality: PASS (all anchors within 10%).
Within-shard SHA256 drift-anchor range: 0.939–1.027. Anchors are diagnostic and no time has been drift-corrected. Shards on different CI hosts are not a common CPU for cross-input ranking; each reported native/browser ratio is paired within its own host.

Input sources/hashes: manifest.json, PhysicsQoo/QuPRS paper-era 60bcb250; original MQTBench and Feynman pairs without regeneration or angle normalization. Engine: upstream QuPRS 0b287366; original GPMC 93cae8db; source-phase weights via the upstream C MPFR bridge, tolerance-selected 96–1024 bits, original counter at 30 decimal digits. Raw binary hashes, CPU/browser metadata and individual results are preserved.
