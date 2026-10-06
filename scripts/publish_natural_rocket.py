"""Copy reviewed, credential-free experiment artifacts into canonical GitHub Pages."""
from pathlib import Path
import json,html,shutil,argparse
p=argparse.ArgumentParser();p.add_argument('--site',type=Path,required=True);p.add_argument('--bundle',nargs=3,action='append',metavar=('SLUG','TITLE','PATH'),required=True);a=p.parse_args();root=a.site
esc=html.escape
header='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/comparisons/style.css"><script defer src="/comparisons/player.js"></script><title>{title} · Minecraft perception lab</title></head><body><header><strong><a href="/comparisons/">Minecraft perception lab</a></strong><a href="/comparisons/#sam">SAM</a><a href="/comparisons/#rocket">ROCKET-3</a><a href="/legacy/">Legacy</a></header><main>'
footer='<footer>6 October 2026 · Compute: DTU HPC / Jonathan’s Mac. <a href="https://github.com/WorldModelMC/minecraft-perception-lab/tree/main/research/rocket3-real-terrain-20261006">Implementation, constitution checks and reports</a>.</footer></main></body></html>'
all_rows=[]
for slug,title,source in a.bundle:
 src=Path(source);rows=json.loads((src/'summary.json').read_text());validation=json.loads((src/'validation.json').read_text());assert validation['status']=='passed'
 dest=root/'comparisons/rocket-natural-media'/slug;dest.mkdir(parents=True,exist_ok=True)
 for name in ['summary.json','validation.json','REPORT.md','source-selection.json']:
  if (src/name).exists():shutil.copy2(src/name,dest/name)
 for row in rows:
  ep=row['episode'];sd=src/'episodes'/ep;out=dest/ep;out.mkdir(exist_ok=True)
  for name in ['game-browser.mp4','policy-panels.mp4','initial.png','result.json','review.jpg']:
   shutil.copy2(sd/name,out/name)
  for name in ['prompt.txt','calls.json']:shutil.copy2(src/'players'/ep/name,out/name)
  row=dict(row,bundle=slug,bundle_title=title,base=f'/comparisons/rocket-natural-media/{slug}/{ep}',result=json.loads((sd/'result.json').read_text()))
  all_rows.append(row)
for task,slug,title,lead in [('navigate','rocket-approach','Navigate through natural terrain','Astra chooses a visible destination, then uses ordinary controls or repeatedly refreshed ROCKET goals to reach a higher tree.'),('harvest','rocket-harvesting','Gather several logs from real trees','Astra chooses trees and log blocks from pixels, continuing until four new logs are collected.')]:
 rows=[r for r in all_rows if r['task']==task];sections=[]
 for bundle,btitle,_ in a.bundle:
  rs=[r for r in rows if r['bundle']==bundle]
  if not rs:continue
  table='<div class="table"><table><thead><tr><th>Condition</th><th>Outcome</th><th>Wall seconds</th><th>New logs</th><th>Health lost</th><th>ROCKET calls</th>'
  if task=='navigate':table+='<th>Reached tree distance*</th><th>Reached tree rise*</th>'
  table+='</tr></thead><tbody>'
  for r in rs:
   table+=f'<tr><td>{"Astra ordinary controls" if r["arm"]=="baseline" else "Astra + ROCKET"}</td><td>{esc(r["outcome"])}</td><td>{r["wall_seconds"]:.2f}</td><td>{r["logs_gained"]}</td><td>{r["health_lost"]:.2f}</td><td>{len(r["rocket_options"])}</td>'
   if task=='navigate':
    goal=r['result'].get('navigation_root');start=r['result']['before']['player']
    table+=f'<td>{goal["distance_from_start"]:.2f} blocks</td><td>+{goal["y"]-start["y"]:.1f} blocks</td>' if goal else '<td>Not reached</td><td>Not reached</td>'
   table+='</tr>'
  table+='</tbody></table></div>'
  vids='<section><h3>Complete task videos</h3><div class="controls"><button data-play>Play both from start</button><button data-pause>Pause both</button></div><div class="videos">'
  for r in rs:
   b=r['base'];label='Astra ordinary controls' if r['arm']=='baseline' else 'Astra + ROCKET'
   vids+=f'<figure><h3>{label}</h3><video controls playsinline preload="none" style="aspect-ratio:960/584" poster="{b}/initial.png" src="{b}/game-browser.mp4"></video><figcaption>Full wall-time attempt, including reasoning and waiting. <a href="{b}/prompt.txt">Exact task prompt</a> · <a href="{b}/calls.json">Actions and selected goals</a> · <a href="{b}/result.json">Independent score</a></figcaption></figure>'
  vids+='</div></section>'
  for r in rs:
   if r['arm']!='rocket':continue
   b=r['base'];vids+=f'<h3>ROCKET’s input and goal-mask overlay</h3><figure><video controls playsinline preload="none" style="aspect-ratio:960/880" src="{b}/policy-panels.mp4"></video><figcaption>Full task. During each option: original reference RGB, fixed goal-mask overlay, current 224×224 policy input, event ID, reference age and action. The fixed mask belongs to its original image; it is not a live tracked segmentation. Between options, the panels explicitly show no active ROCKET call.</figcaption></figure>'
   vids+='<details><summary>Every autonomous ROCKET goal and issued action counts</summary><div class="table"><table><tr><th>Call</th><th>Event</th><th>Goal age at start</th><th>Predicted / issued</th><th>Forward</th><th>Jump</th><th>Attack</th><th>Use</th></tr>'
   for n,o in enumerate(r['rocket_options'],1):vids+=f'<tr><td>{n}</td><td>{o["event_id"]}</td><td>{o["reference_age_s"]:.2f}s</td><td>{o["predictions"]} / {o["issued"]}</td><td>{o["forward"]}</td><td>{o["jump"]}</td><td>{o["attack"]}</td><td>{o["use"]}</td></tr>'
   vids+='</table></div><p>Counts are issued action predictions, not time or unique movements. Multiple keys may occur in one action.</p></details>'
  sections.append(f'<h2>{esc(btitle)}</h2>'+table+vids+f'<p><a href="/comparisons/rocket-natural-media/{bundle}/summary.json">Results JSON</a> · <a href="/comparisons/rocket-natural-media/{bundle}/REPORT.md">Source, preparation and full report</a> · <a href="/comparisons/rocket-natural-media/{bundle}/validation.json">Validation</a></p>')
 criteria='Success: a different rooted tree at least 10 horizontal blocks from the start and at least 2 blocks higher; player displacement ≥8 blocks and rise ≥2; standing on ground within 2.5 horizontal blocks and 1.5 vertical blocks of that trunk for 2 seconds. *Tree geometry is measured from the starting position, not path length. Autonomous agents may select different endpoints, so elapsed times are not an equal-distance controller-speed comparison.' if task=='navigate' else 'Success: four net-new collected log items. Breaking four blocks without collecting their drops does not pass. Repeated ROCKET options remain bounded to five seconds; Astra can retarget, select tools, collect drops or recover with ordinary controls.'
 body=header.format(title=esc(title))+f'<div class="eyebrow">ROCKET-3 · autonomous natural-terrain pilot</div><h1>{title}</h1><p class="lead">{lead}</p><p class="note">All goal boxes in these new runs are selected by Astra from rendered pixels. No human-selected masks. These are copied historical worlds converted to Minecraft 1.16.1; they are not exact replays of the original sessions.</p><p>{criteria}</p>'+''.join(sections)
 body+='<h2>Conditions and limits</h2><p>GPT-6 Astra, medium; Minecraft 1.16.1, Easy, FOV70, continuous 20TPS during reasoning and inference; 150-second deadline. Same saved start per pair, with independent autonomous target choices. Scoring uses privileged state outside the actor. Preparation and conversion changes are documented in the source reports. One run per condition per checkpoint; no reliability, statistical advantage or general-navigation claim.</p><p>ROCKET is warmed before scoring. Inputs expire after at most 150ms, with a 250ms watchdog ceiling and at least 50ms between prediction starts. Event6 navigation suppresses attack/use; this is a constrained controller configuration. Event2 harvesting allows attack. Whole-task video is resampled from recorded capture timestamps to preserve wall time; it includes delays.</p>'
 legacy='rocket-flat-approach' if task=='navigate' else 'rocket-harvesting'
 body+=f'<p><a href="/legacy/2026-10-06/{legacy}/">Earlier controlled diagnostic and human-mask probes</a> · <a href="/comparisons/rocket-recovery/">What happened in the shaft</a></p>'+footer
 out=root/'comparisons'/slug;out.mkdir(exist_ok=True);(out/'index.html').write_text(body)
(root/'comparisons/rocket-natural-media/index.json').write_text(json.dumps([{k:v for k,v in r.items() if k!='result'} for r in all_rows],indent=2))
