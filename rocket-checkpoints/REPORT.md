# Astra with ROCKET: completed checkpoint integration pilot

6 October 2026. **The real Astra→ROCKET→Minecraft path works, but this pilot does not demonstrate a performance gain.** A narrow log goal produced useful approach/break behavior; a full-trunk goal did not. Merely offering the tool did not cause Astra to use it. These findings make goal granularity, delegation policy and controller cadence concrete integration questions.

All five episodes restored the same saved Minecraft 1.16.1 tree checkpoint. The planner was **gpt-6-astra, medium effort, through Codex CLI 0.160.1 using the existing ChatGPT login on the Mac**. This is not Vals AI's complete proprietary agent. Minecraft and ROCKET ran on DTU; no Qualia compute was used.

| Episode | Controller condition | Outcome | Wall time | Completed tool calls |
|---|---|---|---:|---:|
| baseline-r0 | Astra ordinary look/act | 3 logs collected | 45.31 s | 5 |
| rocket-r0 | ROCKET available, same task prompt | 3 logs collected; ROCKET never called | 97.53 s | 6 |
| rocket-required-r0 | Explicitly require one ROCKET attempt, whole-trunk box | 3 logs collected; Astra finished with ordinary actions | 53.31 s | 4 |
| rocket-singleblock-r0 | Explicitly require one ROCKET attempt, lowest-log box | 3 logs collected; Astra finished with ordinary actions | 41.92 s | 6 |
| baseline-r1 | Repeated ordinary-action baseline | 3 logs collected | 110.00 s | 7 |

The rows are execution order. Every episode had full health and no death throughout grader polls. This artificial flat platform had no mobs or meaningful hazards. The two baselines alone varied from 45 to 110 seconds. One checkpoint, five episodes, adaptive prompt changes and variable planner latency cannot establish speedup, improved reliability, or navigation safety. No significance test is appropriate here. Token/API cost is unavailable: the external grader interrupted each CLI after completion, before a normal completed-turn usage record. Tool count is not a substitute for token cost.

## What happened inside the helper

Astra selected every goal from the player screenshot; no human drew these boxes. The service retained each original reference frame, avoiding the old-box/new-image bug while Astra thought.

- Whole trunk: box `[584,151,697,496]`, event ID 2, five-second budget. ROCKET produced 37 action samples; 36 were issued, all with attack and none with forward. The first cold result was too old and dropped. The helper did not approach or harvest; Astra subsequently completed the task itself.
- Single lowest log: after observing the previous failure, the prompt specified one block instead of the whole trunk. Astra chose `[585,383,698,497]`, ID 2, five seconds. All 44 samples were issued; 17 included forward and 19 attack. The resulting image shows approach and log breaking. Astra then finished collection with ordinary actions.

This supports a **goal-interface hypothesis**, not a controlled causal conclusion: mask size, repeated runtime state, sampling and timing also differ. Both interventions were logged as separate conditions. Neither five-second option completed the full three-log collection unaided. The optional-tool run is evidence about tool adoption, not evidence about ROCKET's motor performance.

The controller reached only 7.4/8.8 samples per second in these two options, including capture/inference/decoding and an additional 50 ms sleep. Each issued action had a 50 ms lease, so keys could expire between slow decisions. This conservative implementation is not the earlier 14–20 Hz direct probe. Profile and improve the cadence/lease design before attributing all losses to the model. The independent watchdog still bounds held inputs; do not pause Minecraft to conceal inference latency. The logged capture-through-decoding medians, 71.5/66.2 ms, include CPU synchronization and are not isolated GPU inference times.

## What is implemented and verified

The new `pixel_service.py` exposes only rendered RGB and whitelisted OS keyboard/mouse controls, with bearer authentication, a separate input-expiry process, a maximum five-second call budget, bounded image-reference storage and explicit reference expiry. It imports no game bridge. Its optional ROCKET endpoint uses current RGB, the selected historical RGB/rectangle, numeric event ID and previous issued actions. ID 6 has attack/use suppressed as a declared constrained approach variant; this pilot exercised ID 2 only.

The Mac `pixel_mcp.py` exposes look/act and optionally `rocket_option`. A separately audited invocation-local Codex configuration removes shell, file editing, web, memory, plugins and other tools. Generic resource helpers cannot obtain anything from this MCP server: it exposes no resources and rejects those methods. Auth files, credentials and the generated model catalogue were not published. The exact prompts, launch arguments, isolation manifests and provider transcripts are preserved.

A separate operator/scorer process creates and restores the checkpoint. Before each episode it checks pose, health, food, inventory, mode and difficulty; any mismatch is a setup error. It then starts continuous 20 TPS and independently scores three gained oak logs. Scorer state never enters an actor observation or a motor stopping rule. At the end of the entire scored episode it disables further control, releases inputs and stops the player; only afterward may the world freeze for preparation. The user-facing tool receives no inventory counts, coordinates or grader status. The model chooses when to invoke or stop its bounded options from pixels.

Actual options verified: FOV `0.0` (70 degrees), mouse sensitivity `0.5`, `pauseOnLostFocus:false`; default FOV effects. All grader polls were Easy/20 TPS/unpaused/unfrozen. All five raw videos decode with frame counts matching their timestamp logs, and captured/game/wall durations agree within 1.5 seconds. Browser clips are H.264 derivatives; nominal 20-fps playback is approximate, with exact capture timestamps retained. All five 12-frame contact sheets were reviewed, plus the checkpoint, helper outputs and both assigned-arm final frames. This is a sampled visual audit, not a frame-by-frame review.

Four transport tests pass: action whitelist/budget, authentication and absence of privileged routes, episode-gate failure behavior, and reference-frame expiry. Code compilation and whitespace checks pass. DTU job 29612989 completed; the game quit cleanly and the dedicated SSH forwarding was removed. The shared SSH connection was preserved. Earlier job 29612970 was a launch-wrapper no-op; 29612982 failed before any episode due to a missing upstream import path. Setup logs remain separate from the five valid results.

## Historical situations for newly validated tasks

**Upstream correction (6 October 2026):** [benchmark commit `1009e107`](https://github.com/WorldModelMC/benchmark/blob/1009e1071a3df6aedb5533c755885bcc7d85455f/bench/tasks/archived/README.md) archives all six `r1-*` tasks because their grading was unreliable and explicitly says their results must not be used. The historical pit **2/12** and hill **0/10** counts are retained here only to identify the superseded report; they are not valid capability estimates, baselines, or quantitative evidence for prioritizing one intervention. The recordings remain inspectable historical evidence, and saved starts remain usable for newly defined, independently validated tasks. Do not reuse the archived criteria unchanged.

The superseded [1 October report](https://github.com/WorldModelMC/docs/blob/5226f03/docs/experiments/harness-auto-research1.md) and clips describe a flooded bank and a hill with two- or three-block terraces. Those scenes can motivate new recovery/climbing tasks based on visible behavior, without relying on the invalid scores. The old runs also used half game speed, so their timing is not a matched baseline for our 20-TPS pilot. Easy log collection does not cover either situation.

After access to the relevant checkpoint worlds is available, prioritize **bank escape** and **step climbing**: let Astra select a concrete bank/step block, test bounded ID 2 modification followed by bounded approach, and compare against ordinary controls from identical starts. Score actual escape/arrival, damage, wrong-block changes, time and interruptions. A route must be judged from pixels; privileged target coordinates belong only in the grader. ROCKET is not established as a drowning rescue policy.

The earlier permission-denied check is superseded: `/work3/s234842/claudeplay-backup` is now readable. The [DTU recheck at 20:04:38 UTC on 6 October](https://github.com/WorldModelMC/minecraft-perception-lab/blob/main/research/checkpoint-status-20261006/access-recheck.json) found no `starts`, `r1-water`, `r1-navigate` or `2026-10*` directories in that backup, and the checked Git tree contains no start-world assets. The last manifest inventory contains 366 Minecraft 26.3 checkpoints through September 30. The original October 1 pit/hill starts are therefore still missing from the inspected locations, not blocked by permissions; this does not establish that no other copy exists. Continuation with the original pit/hill worlds requires another readable saved-start location. Never label a reconstruction as the original checkpoint. The [root SAM findings](https://github.com/WorldModelMC/minecraft-perception-lab/blob/main/research/sam-paired-20261006/FINDINGS.md) separately examine those actual failure clips; this tree pilot only validates the helper integration and exposes its limitations.

See [gallery](index.html), [summary](summary.json), [validation](validation.json), and [option trace summary](option-summary.json). Complete raw evidence and the reusable checkpoint are packaged separately for GitHub release.
