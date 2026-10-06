# SAM live-checkpoint handoff

Merged source: PR15, branch head03f296698cb28406d1c215454fdea4544309e0f3. Use the merged source, not the stale remote scenario_host.py (the current-process readiness fix was committed after the final live run).

## Verified existing assets

- DTU copied start: `/work3/s216136/rocket3-failures-20261006/starts/astra425-converted116` (world.zip SHA256 `9ee0f5ca2107dae7af7f7c19c8f1602243633ead9d348089c006bc4832716c63`). Copy this entire checkpoint directory into a new experiment root's `starts/`; do not modify it or Lucas originals.
- DTU benchmark code/deps: `/work3/s216136/rocket3-failures-20261006/benchmark` (converter upstream1272adf; custom harness does not depend on patched shared Grader).
- Python: `/work3/s216136/rocket2/venv-rocket3/bin/python`.
- Shared assets: `/work3/s216136/sam-eval-20261005`; Python deps `/work3/s216136/rocket3-research-20261006/deps`.
- Local merged scripts: `research/rocket3-failure-checkpoints-20261006/{scenario_host.py,run_player.py}`; package `rocket2-hpc/rocket_hpc`.
- Mac isolation helper: `/Users/jonathantybirk/Documents/Codex/2026-10-05/check/work/decisions-api/research/decisions-api-20261006/isolate_codex.py`.
- SSH: socket `/Users/jonathantybirk/Documents/Codex/2026-09-21/sta/work/dtu.sock`, host`s216136@login1.gbar.dtu.dk`.

## Minimal SAM-specific edits in your own copy

1. `scenario_host.py`: remove the service argv pair `--checkpoint`, `/work3/s216136/rocket2/checkpoints/rocket3.ckpt`. The pixel service then needs no ROCKET GPU/model and exposes only pixels/action transport. Keep all release, control-file deadline, current-process readiness and separate scorer logic. Use your own `--root`, display and port. For the default Mac launcher, keep port18776 (now free). Display176 is free; separate display is fine.
2. `run_player.py`: add arm `sam` to argparse choices. Immediately after its local `env={PIXEL_URL...,PIXEL_TOKEN_FILE...}` declaration, for `a.arm=='sam'`, set `env['PIXEL_SAM_URL']='http://127.0.0.1:18777'` and `env['PIXEL_SAM_PROMPTS']=json.dumps(YOUR_FROZEN_PROMPT_LIST)`. These must be in the explicit MCP server env dictionary; exporting only the parent shell env is not a reliable substitute under isolation. Keep tools exactly `look,act` in both baseline and SAM. Do not enable `PIXEL_ROCKET`. Model/effort remain exactgpt-6-astra/medium.
3. The MCP client already adds original image + same-frame SAM annotation on every look/act. It POSTs `/segment` with `{image:BASE64_JPEG,prompts:[...]}`; accepts annotation `image` or `annotated_image`; records helper_wall_s, and warns that predictions are uncertain. Root's SAM service should run in venv-sam. Check MIME compatibility (client emits image/jpeg), warm it up before scored play, and keep its tunnel alive. A failed SAM annotation falls back to original pixels and must be counted/reported as helper-unavailable, not silently called a successful SAM trial.
4. Repair/prespecify grading before a new live test: the current `y>=67` predicate misses valid lower surrounding terrain. Both prior actors physically emerged, so it is not a universal egress measure. Grade physical egress and a subsequent survival interval separately. You can keep it unchanged only if explicitly presenting the restrictive prior criterion. Keep death grading and continuous play. Do not retrospectively modify old results.

## Launch sequence

On DTU create a NEW root, for example `/work3/s216136/sam-live-shaft-20261006`, copy the existing checkpoint and benchmark into it, then rsync your patched scenario_host.py and `rocket_hpc/` package there. Never copy token, STOP, request.json, active.json or ready.json from the ROCKET root. The new host creates a fresh0600 token.

Create a remote shell script containing:

```sh
#!/bin/bash
exec /work3/s216136/rocket2/venv-rocket3/bin/python /work3/s216136/sam-live-shaft-20261006/scenario_host.py --root /work3/s216136/sam-live-shaft-20261006 --seconds 120 --display :178 --port 18776
```

Start the CPU game/pixel host with an LSF compute allocation (do not run on login):

```sh
source /etc/profile.d/lsf.sh
bsub -Is -q hpc -n 4 -W 20 -R 'span[hosts=1] rusage[mem=4GB]' /bin/bash /work3/s216136/sam-live-shaft-20261006/run-host.sh
```

Use a separate suitable GPU allocation for the warmed SAM service in venv-sam. Obtain actual compute hostnames from `ready.json` / SAM readiness output, then on Mac forward18776 to the GAME_HOST:18776 and18777 to SAM_HOST:18777 using the shared SSH master. Example (substitute actual hostnames):

```sh
ssh -S /Users/jonathantybirk/Documents/Codex/2026-09-21/sta/work/dtu.sock -O forward -L 18776:GAME_HOST:18776 s216136@login1.gbar.dtu.dk
ssh -S /Users/jonathantybirk/Documents/Codex/2026-09-21/sta/work/dtu.sock -O forward -L 18777:SAM_HOST:18777 s216136@login1.gbar.dtu.dk
```

Copy only the new root's token into a private Mac directory (never print it). Run your adapted local launcher twice sequentially, changing arm and episode:

```sh
python3 PATH_TO_YOUR_RUN_PLAYER.py --episode sam-shaft-baseline-r0 --arm baseline --root /work3/s216136/sam-live-shaft-20261006 --output PATH_TO_PUBLIC_RESULTS/players --helper /Users/jonathantybirk/Documents/Codex/2026-10-05/check/work/decisions-api/research/decisions-api-20261006/isolate_codex.py --mcp PATH_TO_MERGED_REPO/rocket2-hpc/rocket_hpc/pixel_mcp.py --token PATH_TO_PRIVATE/token --private PATH_TO_PRIVATE --socket /Users/jonathantybirk/Documents/Codex/2026-09-21/sta/work/dtu.sock
```

For the second run use `--episode sam-shaft-helper-r0 --arm sam`. The launcher writes a request, waits for a valid restore and active status, then starts isolated Astra. It watches the independent result and interrupts the player after grading. With120s host limit its145s local watchdog is adequate; change both if using a longer task. Each episode directory must be new. Never issue overlapping requests.

Afterward create NEW_ROOT/STOP, wait for clean game/service shutdown, remove only these two exact SSH forwards with `-O cancel -L ...`, preserve the shared master. Validate all raw scorer polls, videos and actual helper calls.

## Non-negotiable interpretation and restore caveats

This is a26.3→1.16.1 converted reconstruction, not original historical replay and not the missing October1 flooded-pit/hill world. Conversion losses and runtime preflight are in PR15. All actor inference is rendered pixels/issued-action history; prep/scorer API data stay outside MCP.

The engine advances initialization ticks before applying the frozen preparation rate. The harness rejects clock drift outside0–20ticks and verifies pose/health within0.02, exact inventory/equipment/mode, and Easy. Both old clean arms differed by one initialization tick (+3 baseline,+2 ROCKET). This is disclosed, not deterministic replay. Record fresh offsets and all restore differences. The initial boot's world is discarded before each scored arm. All scoring starts after publish/rate20, includes model/tool latency, and remains unpaused. Normal HUD/defaultFOV70 was verified in the source runtime; verify your new HOME options too.
