# Historical shaft rescue: bounded ROCKET diagnostic

Both clean Astra trials reached above the shaft rim, and both subsequently died by Zombie. The assigned ROCKET option produced camera movements but no attack, forward or use input. This pair provides no evidence that ROCKET helped the recovery. It does expose a useful distinction: getting out of a hole is not the same as reaching safety, and the planner's own completion message is not a reliable success signal.

## What was actually recovered

Lucas's now-readable DTU backup contains 366 manifests, all Minecraft 26.3, ending September 30. The October 1 flooded-pit and terraced-hill starts are absent. Their historical Astra results—2/12 for the flooded pit and 0/10 for the hill—remain relevant priorities, but are not reproduced here. Source: [WorldModelMC experiment report](https://github.com/WorldModelMC/docs/blob/5226f03/docs/experiments/harness-auto-research1.md).

We copied September 27 Astra checkpoint 425, created 21:35:34+02, verified all four manifest hashes, and left Lucas's originals untouched. It precedes the later historical death sequence. The copied player stands at the bottom of a four-to-five-block shaft, looking upward, with full health and food, cobblestone, dirt and tools.

The benchmark converter at commit 1272adf5a5d045b92b005c017cc3882d2edb3310 rebuilt 289 chunks for 1.16.1. Structural validation passed. Among retained non-air blocks, 94.7% retained identity, 5.1% used explicit fallbacks and 0.2% were removed. It retained 108 entities and dropped 50, 44 outside the supported height interval. The adjacent conversion report records the losses, including modern-block and item substitutions. Terrain outside the radius is newly generated 1.16 terrain.

**This is a converted reconstruction, not an exact historical replay.** Game mechanics, AI intentions and paths, discarded entities, item/block substitutions and boundary terrain differ. No original October 1 pit/hill checkpoint was invented or substituted without disclosure.

## Runtime verification and protocol

DTU preflight job 29614958 confirmed restored pose, inventory, health, food, air, experience and selected slot against the converted source. Easy survival, default FOV 70 (`fov:0.0`), sensitivity 0.5 and `pauseOnLostFocus:false` were verified. The normal rendered HUD has no F3 overlay. The historical source frame containing F3 is retained as source evidence only and is not shown to an actor.

Preparation-only queries found a nearby zombie, creeper and spider. A 15.4-second no-input check advanced 308 ticks with health 20→20. This establishes neither inevitable nor immediate historical death. These hidden observations never enter the actor interface.

The new selected task is: “Escape this shaft onto the surrounding open ground safely. Stop once you are out.” Exact `gpt-6-astra`, medium, runs through the isolated local Codex launcher, with rendered-image and ordinary keyboard/mouse tools. The second arm additionally requires an initial event 2 ROCKET attempt on a block selected from pixels; Astra may orient/select tools beforehand and resume normal actions afterward. It chose a two-second option. Neither arm receives RAM/API/file-derived game state or audio; both use pixels only.

The independently recorded scorer allowed 120 wall seconds and required alive/on-ground/y≥67/at least two horizontal blocks from the start for three continuously observed seconds. Death is failure. All scored polls verify 20 TPS, Easy, unpaused and unfrozen. Preparation freezing is outside scored play. No controller latency or planner reasoning time is removed from the wall clock.

The loader advances initialization ticks before applying rate 0. One strict clock check was rejected before inference; a second host startup exceeded the initial two-tick assumption and was also rejected. We then explicitly permitted at most 20 preparation ticks while preserving exact inventory/mode/equipment checks and pose/health tolerance 0.02. The baseline restore advanced **three ticks** (clock 22557); the ROCKET restore advanced **two ticks** (clock 22556). This one-tick difference is retained as a limitation, not described as an identical-clock replay. The initial host boot advanced 15 ticks; its world was discarded before every scored restore. All clock offsets are recorded, rather than corrected invisibly.

## Results

| Clean condition | Outcome | Wall time | First observed damage | ROCKET calls |
|---|---|---:|---:|---:|
| Astra ordinary actions | Died by Zombie |59.97s|47.28s|0|
| Astra with initial ROCKET option | Died by Zombie |54.50s|46.23s|1|

Video review shows the baseline opening inventory, selecting cobblestone and pillaring above the shaft. An explosion appears after it reaches the surface; it falls into the damaged terrain and is killed by a zombie. The ROCKET arm also pillars up using Astra's ordinary actions, moves across visible surrounding terrain and dies by a zombie. Both normal death screens explicitly name Zombie. Neither outcome is inferred from the model's text.

The option made 10 predictions, issued 9 camera-only actions, and dropped its first prediction because inference took 0.83s, exceeding the 0.25s freshness bound. Its reference screenshot was 9.44s old when the option started. There were **zero issued attack, forward and use inputs**, so no block was broken by the ROCKET attempt. This short cold-start option is not a fair throughput or upper-bound policy-capability test. Subsequent prediction latency was roughly 0.036–0.096s, plus the existing 50ms loop sleep; this adapter is not a continuous 20Hz controller.

One additional baseline attempt is explicitly excluded: a stale readiness marker allowed startup before the new pixel service was listening. Astra made two failed look calls and no inputs, then the grader timed out. The service-ready check now requires a ready event newer than the current process launch. Its raw timeout result is retained for audit but is **not a model performance result**. The earlier rejected restore is retained separately as setup_error.

## What the scorer does and does not establish

The fixed y≥67 criterion was chosen from the shaft's neighbouring rim before the trials. Surrounding terrain descends to y66; therefore this geometric criterion is too restrictive as a general definition of physical escape. We do not label these videos “failed to leave the shaft.” Both visibly emerge, and both die afterward. That survival failure is independently supported even though the egress predicate needs improvement.

The ROCKET-arm planner says it escaped and stopped, but the continuing game subsequently kills it. A future scenario should grade physical egress separately from a predefined post-egress survival window, using a terrain-aware destination region. It should expose no hidden scorer data to the policy. The current results must not be retrospectively rescored into a success claim.

## Practical conclusion

For this reconstruction, forcing a short mining option did not address the actual hazard. The useful next comparison is a recovery planner that keeps observing after egress, detects threats from pixels, and continues to a safe destination, with bounded low-level options only when they serve that plan. Warm up ROCKET before the scored start, refresh target imagery when necessary, and measure controller cadence; otherwise a two-second command spends a large fraction of its budget on setup.

Keep the original flooded-pit and hill starts as explicit missing assets. Their lower-step excavation and terrace-climbing requirements remain better targeted tests for motor assistance once the actual checkpoints become available. The present pair supports this direction, not a claim of improved reliability, speed or a reproduced historical trajectory.

## Evidence and cleanup

The complete local evidence is `outputs/rocket3-failures/`: original copied 26.3 checkpoint, converted 1.16.1 start, manifest hashes, loss report, preparation checks, source scripts, exact prompts, isolated launch manifests, raw provider/tool events, independent scorer traces, raw videos with per-frame wall timestamps, browser videos and contact sheets. The gallery explicitly separates excluded setup attempts from the clean pair. Automated validation checks decoded video frame counts, 1280×720 raw resolution, monotonic times, 20TPS/unpaused/Easy observations, clean tool calls and matching game/video/wall durations within 1.5s. Sampled visual review confirms normal HUD, upward pillaring, outdoor views and both zombie death screens.

Compute used only the Mac and DTU. The dedicated game, service and GPU allocation were stopped, and only this experiment's 18776 SSH forward was removed; the shared SSH master remains available. No credentials or generated private model catalogue are included in published evidence.
