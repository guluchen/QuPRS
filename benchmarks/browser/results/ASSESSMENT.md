# QuPRS browser port: isolated benchmark assessment

The canonical screen completed **220 cells / 892 trials** on the original **73 paper input pairs** (110 mode/input pairs), with a 200-second whole-request cap. All 24 before/after anchors pass the 10% check (range 0.939443–1.027042). There are **zero status/distance discrepancies on completed native/WASM comparisons and repeated results**. Unresolved cells are retained; this is not a claim that every numerical answer is independently certified.

| Mode | Native adapter reports | Browser reports | Native distances | Browser distances |
|---|---:|---:|---:|---:|
| Hybrid | 30/37 | 30/37 | 13/37 | 13/37 |
| WMC | 26/37 | 28/37 | 10/37 | 11/37 |
| Reduction only | 36/36 | 36/36 | 35/36 | 35/36 |

One reduction report is **unknown** in each build. Thus there are 91 native and 93 browser numerical decisions, versus 92/94 completed reports. The browser produces a finite distance on 59/110 mode/input pairs. Numerical tolerance acceptance need not compute a distance; printed counts outside the unitary range receive no fabricated zero. The existing PathsumWMC interval workbench remains a separate option.

Browser/native whole-request geometric means are **2.159x Hybrid (6 pairs), 2.437x WMC (10 pairs), and 1.980x reduction (3 pairs)** on paired completed cells whose native request is at least 100 ms. Each cell is a conditional five-repeat median when its first successful request is below two seconds, otherwise a single screening trial. These are selected timing subsets, not full-suite speed ratios. No timeout is replaced by an artificial time.

The native baseline is **this same browser capture/replay adapter compiled natively**, not the unmodified single-pass upstream CLI. Both profiles run original QuPRS v0.16.0 and the original MPFR GPMC. The separate historical comparison used paper-era Python QuPRS and cannot be substituted as this baseline. WASM32/native64 ordering and search differences can change which cases finish; more browser completions do not establish a universal browser speed advantage.

Every WASM trial launches a fresh browser/page and waits for complete closure before the following sample. Launch/cleanup are recorded separately, outside request timing. This prevents transient asynchronous worker cleanup from contaminating native or subsequent WASM requests. The first reused-browser screen and its retries are excluded from timing claims and remain archived only as historical evidence. The real active-timeout audit also caught a disabled-termination mutant and measured zero settled/closed CPU in the working implementation.

The release passed 125 core tests, 48 enumerated weighted CNFs, eight MPFR phase references including 1e-400, 24 native/browser circuit comparisons with 18 real GPMC invocations, and actual Chromium UI checks. Published assets match 15/15 tested file hashes. Source-phase weights use the original upstream C MPFR bridge at 96–1024 bits; complex counting uses 30 decimal digits. Results are **numerical estimates, not ball-arithmetic certificates**.

[Full table](RESULTS.md), [CSV](results.csv), [summary](summary.json), [methods](../METHODS.md), [raw evidence and checksums](https://github.com/guluchen/QuPRS/releases/tag/browser-benchmark-isolated-20261115), [tested assets/complete sources/frozen native binaries](https://github.com/guluchen/QuPRS/releases/tag/web-mpfr-20261115), [browser](https://guluchen.github.io/QuPRS/).
