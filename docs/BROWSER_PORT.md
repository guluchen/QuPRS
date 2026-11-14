# QuPRS browser integration

This is a fork of the original QuPRS Rust v0.16.0 implementation, not another independently written quantum-verification algorithm. The upstream path-sum reduction, WMC construction and numerical classification remain in use. The upstream MIT license and NOTICE are retained. Browser integration is attributed to Codex and guluchen; MIT worker/clock integration from PathsumWMC is credited separately.

## Execution boundary

The additive `browser-transport` feature captures a weighted problem at the native subprocess boundary. The browser runs the real GPMC WASM counter in a disposable worker. Finishing a request replays the upstream verifier and accepts the returned stdout only when the canonical prepared problem matches and the result is consumed exactly once. Sessions restore their thread-local state on errors and nested calls. Ordinary native calls outside a transport session retain the original subprocess path.

The browser build does not link native MPFR into its Rust WASM core. Instead it sends original rational phase descriptors through private CNF comments. The C++ worker adapter runs the **original upstream C MPFR phase-weight function**, with the same exact-Clifford shortcuts and the same 96–1024-bit tolerance-dependent input policy. It creates a private temporary input and replaces every positive phase placeholder before counting. A count without an explicit phase-weight acknowledgment is rejected. An old or unmodified counter therefore cannot silently count placeholder weights. The source-weight adapter, C bridge and complete GNU dependencies are included in the source archive.

Counting uses the original GPMC v1.0.2 MPFR complex engine at its upstream default 30 decimal digits. Its Boolean search is unchanged. The small portability shim substitutes worker-local elapsed wall time and a linear-memory proxy for unavailable OS CPU/RSS APIs. These proxies must not be reported as OS measurements. Compile-time MPFR working precision and printed count precision are numerical policies, not certified error bounds.

## Output and limits

The displayed distance is the normalized Frobenius distance after minimizing global phase:

`min_phi ||U - exp(i phi) V||_F / sqrt(2^n)`.

Zero means closest under this convention, and the metric ranges up to `sqrt(2)`. This is an average matrix distance, not a worst-case input-state error. A numerical estimate of zero does not certify exact equality. If reduction only accepts within tolerance, no distance is invented. A printed count outside the unitary range is not assigned a distance. Every report says `certified_distance_interval: false`; the separate PathsumWMC workbench retains its ball-arithmetic interval interface.

The port supports upstream restricted unitary QASM 2/3, Hybrid/WMC/reduction modes and the four exposed upstream strategies. It has a 200-second worker limit and a 512 MiB linear-memory maximum **per WASM module**, with additional Chromium memory outside those limits. Stop and timeout terminate the root worker and all counter workers. Versioned JS/WASM URLs prevent a source-weight bridge from being mixed with cached prototype assets. The fork exposes GPMC as its browser counter; GANAK is installed only for the upstream native regression suite.

## Evidence and reproduction

The `web-build.yml` workflow builds immutable native/WASM artifacts. `web-publish.yml` verifies source identity and counter checksums, then runs core tests, a brute-force counter ladder, upstream C phase-weight references and actual Chromium tests before Pages deployment. The published release includes complete corresponding sources, GNU source tarballs, build instructions, tested assets, QA evidence and hashes. Frozen native benchmark binaries and their separate provenance are archived alongside them.

The release passed 125 core tests, 48 enumerated small weighted CNFs, eight native/WASM source-phase references including `1e-400`, and 24 native/WASM circuit checks with 18 actual GPMC invocations. QASM 3, invalid input, upload/download, Stop, timeout and 390px layout also passed. These checks do not turn arbitrary numerical benchmark answers into certificates.

The paper-corpus screen and its baseline limitations are documented in [benchmark methods](../benchmarks/browser/METHODS.md). In particular, its native comparator is this same capture/replay adapter compiled natively, and the earlier paper-era Python comparison remains a separate experiment.
