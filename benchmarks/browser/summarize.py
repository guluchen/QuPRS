"""Summarize complete, disjoint frozen browser timing shards; no timeout imputation."""
import collections,csv,hashlib,json,math,pathlib,statistics,sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
shards=[json.loads(p.read_text()) for p in sorted(root.glob('benchmark-*/results.json'))]
assert len(shards)==24 and {s['shard'] for s in shards}==set(range(24)),len(shards)
assert all(s['complete'] for s in shards)
cells=[c for s in shards for c in s['cells']];keys=[(c['id'],c['mode'],c['engine']) for c in cells]
assert len(keys)==len(set(keys))==220,len(keys)
assert len({json.dumps(s['binary_sha256'],sort_keys=True) for s in shards})==1
rows=[];conflicts=[]
for c in cells:
 reports=[t['report'] for t in c['trials'] if 'report' in t and not t.get('error')]
 statuses=sorted({r['status'] for r in reports})
 if len(statuses)>1:conflicts.append({'kind':'repeat-status','cell':keys[cells.index(c)],'statuses':statuses})
 ds=[r['distance_estimate'] for r in reports if r.get('distance_estimate') is not None]
 row={k:c[k] for k in ['id','family','mode','engine','successes']};row.update(trials=len(c['trials']),complete=c['successes']==len(c['trials']),status='|'.join(statuses),median_request_ms=c.get('median_request_ms'),median_whole_ms=c.get('median_whole_ms'),distance_available=len(ds)==len(c['trials']),distance_median=statistics.median(ds) if ds else None,rr_approximate=any(r.get('rr_approximate') for r in reports),errors=' | '.join(sorted({t.get('error','') for t in c['trials'] if t.get('error')})))
 rows.append(row)
by={(r['id'],r['mode'],r['engine']):r for r in rows};ratios=collections.defaultdict(list)
for r in rows:
 if r['engine']!='native':continue
 w=by[(r['id'],r['mode'],'wasm')]
 if r['complete'] and w['complete']:
  if r['status']!=w['status']:conflicts.append({'kind':'native-wasm-status','id':r['id'],'mode':r['mode'],'native':r['status'],'wasm':w['status']})
  if r['distance_median'] is not None and w['distance_median'] is not None and abs(r['distance_median']-w['distance_median'])>1e-8:conflicts.append({'kind':'native-wasm-distance','id':r['id'],'mode':r['mode'],'native':r['distance_median'],'wasm':w['distance_median']})
  if r['median_whole_ms']>=100:ratios[r['mode']].append(w['median_whole_ms']/r['median_whole_ms'])
summary={'cells':len(cells),'trials':sum(len(c['trials']) for c in cells),'pairs':73,'mode_pairs':110,'conflicts':conflicts,'binaries':shards[0]['binary_sha256'],'anchor_ratios':{s['shard']:s['anchor_ratio'] for s in shards},'groups':[],'geomean_wasm_native_whole_request_native_at_least_100ms':{mode:{'pairs':len(rs),'ratio':math.exp(statistics.mean(map(math.log,rs)))} for mode,rs in ratios.items()}}
for mode in ['hybrid','wmc','reduction']:
 for engine in ['native','wasm']:
  rs=[r for r in rows if r['mode']==mode and r['engine']==engine]
  summary['groups'].append({'mode':mode,'engine':engine,'cells':len(rs),'completed':sum(r['complete'] for r in rs),'distance_available':sum(r['distance_available'] for r in rs),'statuses':dict(collections.Counter(r['status'] for r in rs))})
with (out/'results.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(out/'results.json').write_text(json.dumps({'summary':summary,'cells':cells,'shards':[{k:v for k,v in s.items() if k!='cells'} for s in shards]},indent=2)+'\n')
text=['# QuPRS v0.16.0 native / browser screen','', 'Pinned original paper input pairs; 200-second whole-request cap, Difference strategy. Five repeats only when the first successful whole request takes less than two seconds; all others are single-trial screens. Timing medians from one trial are not five-repeat estimates. No timeout imputation. Results are numerical estimates, not certified intervals. This Rust v0.16 fork is distinct from the earlier paper-era Python comparison.','',f'{len(cells)} cells, {summary["trials"]} trials, 73 input pairs / 110 mode pairs.','', '| Mode | Engine | Completed / cells | Distance available |','|---|---|---:|---:|']
for g in summary['groups']:text.append(f'| {g["mode"]} | {g["engine"]} | {g["completed"]} / {g["cells"]} | {g["distance_available"]} |')
text+=['','A completed report can be indeterminate or a tolerance-based reduction acceptance without a computed distance. Status counts and all errors are retained in JSON/CSV. Small circuit/GPMC enumeration tests provide separate correctness evidence; repeated benchmark timings alone do not establish ground truth.','',f'Native/WASM or repeat discrepancies: **{len(conflicts)}**. See summary.json for every discrepancy.','', 'Native processes use a 4 GiB address-space cap and 16 MiB stack. Each WASM module has a 512 MiB linear-memory maximum, with browser overhead outside that limit. Same-host native/WASM requests run serially on one pinned core; order is rotated. Page/server startup and browser launch are excluded; worker startup, core loading/instantiation and local-HTTP fetches remain inside browser requests. Native whole times include process startup. These timings are not public-network page-load measurements.','', '## Browser/native timing ratio','', 'Only paired successful cells with native whole-request time >=100 ms enter these geometric means. A ratio above one means browser slower. Exact zero/near-zero native startup cases are omitted from this ratio only, never from coverage.']
for mode,r in summary['geomean_wasm_native_whole_request_native_at_least_100ms'].items():text.append(f'- {mode}: {r["ratio"]:.3f}x ({r["pairs"]} pairs).')
rat=list(summary['anchor_ratios'].values());text+=['',f'Within-shard SHA256 drift-anchor range: {min(rat):.3f}–{max(rat):.3f}. Anchors are diagnostic and no time has been drift-corrected. Shards on different CI hosts are not a common CPU for cross-input ranking; each reported native/browser ratio is paired within its own host.','', 'Input sources/hashes: manifest.json, PhysicsQoo/QuPRS paper-era 60bcb250; original MQTBench and Feynman pairs without regeneration or angle normalization. Engine: upstream QuPRS 0b287366; original GPMC 93cae8db; source-phase weights via the upstream C MPFR bridge, tolerance-selected 96–1024 bits, original counter at 30 decimal digits. Raw binary hashes, CPU/browser metadata and individual results are preserved.']
(out/'RESULTS.md').write_text('\n'.join(text)+'\n')
print(json.dumps(summary,indent=2))
