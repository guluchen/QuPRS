"""Replace exactly predeclared noisy shards; preserve both original and rerun evidence."""
import json,pathlib,shutil,sys
base,retry1,retry2,out=map(pathlib.Path,sys.argv[1:5]);out.mkdir(parents=True,exist_ok=True)
plan={6:retry1,8:retry1,18:retry2};audit={'rule':'One predefined replacement of each original anchor failure; no fastest-of-runs selection','replacements':[]}
for i in range(24):
 original=base/f'benchmark-{i}';d=json.loads((original/'results.json').read_text());chosen=original
 if i in plan:
  chosen=plan[i]/f'benchmark-{i}';r=json.loads((chosen/'results.json').read_text())
  assert d['complete'] and r['complete'];assert d['binary_sha256']==r['binary_sha256']
  key=lambda c:(c['id'],c['mode'],c['engine'])
  assert {key(c) for c in d['cells']}=={key(c) for c in r['cells']}
  status=lambda c:sorted({t.get('report',{}).get('status','ERROR') for t in c['trials']})
  old={key(c):status(c) for c in d['cells']};new={key(c):status(c) for c in r['cells']}
  audit['replacements'].append({'shard':i,'original_anchor_ratio':d['anchor_ratio'],'replacement_anchor_ratio':r['anchor_ratio'],'replacement_drift_pass':.9<=r['anchor_ratio']<=1.1,'source':str(chosen),'outcome_changes':[{'cell':k,'old':v,'new':new[k]} for k,v in old.items() if v!=new[k]]})
 shutil.copytree(chosen,out/f'benchmark-{i}')
(out/'RERUN-AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
