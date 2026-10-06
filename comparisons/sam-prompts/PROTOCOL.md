# Focused SAM3.1 study — 6 October 2026

Status: setup, not new results. Supersedes the broad prompt/gallery matrix and the planned terraced-hill/bank-escape SAM continuation. Primary uses: mob discovery/tracking, exposed ore tracking, visible structure tracking. Walking hazard detection is a secondary study. GitHub Pages is the canonical presentation.

## Decision sequence

1. Validate capture and scorer on two short development clips before model comparison. Reject underground cameras, incomplete loading, unwanted particle carryover and missing render timestamps. Keep rejected setup attempts outside policy scores.
2. Compare at most three prompt candidates per class: `minecraft <class>`, the plain class as a development control, and one Minecraft-specific visual description. Do not cross prompts with model, confidence, resolution and seed sweeps. Native SAM3.1, output threshold 0.5, fixed resolution and propagation settings throughout this screen.
3. Use two development route families per cohort, with visible positives, partial occlusions, held-item/menu distractors and at least 60 seconds of verified target-absent exposure. Store exact text, class mapping, checkpoint revision and scorer version. A prompt must have precision ≥0.90, at most one false detection per evaluated minute, and at least 20 matched instances/object observations across two independent clips to pass the *development* gate. These are engineering gates, not population guarantees. Report counts and uncertainty.
4. Pick the passing prompt with highest recall, breaking ties by fewer false detections, then the Minecraft-prefixed candidate. If none passes, mark that class unresolved; do not silently choose a generic label. Select no more than two prompts for a class. A second prompt is considered only if the first misses a reviewed visual subtype; test one prespecified complement on the same development set. Evaluate the deduplicated union, require ≥5 percentage-point recall gain while preserving both false-positive gates. Never sum separate prompt counts.
5. Freeze selected text and its source-data hash in a lock file. Run only that bank on disjoint evaluation worlds/routes. No prompt tuning on evaluation videos. Failed evaluation remains a result; a revised prompt requires a new study version and new holdout.

The small historical static SAM3 screen is background evidence only, not a SAM3.1 prompt lock. It localized 7/30 targets with plain labels and17/30 with Minecraft-prefixed labels at0.5. Other Minecraft-prefixed prompts produced false labels on held blocks. Prefixing is a justified candidate, not a universal correctness rule.

## Primary mob test: continuous approach and discovery

Start with two cohorts: overworld (`zombie`, `skeleton`, `creeper`, `spider`, `enderman`, `cow`) and Nether (`blaze`, `ghast`, `piglin`, `magma cube`). Separate capture sessions use the appropriate dimension and lighting. Baby variants are identified in teacher metadata and reported as subgroups, not automatically new labels.

For prompt development, record120-second continuous approaches with at least600 timestamped inference frames at5Hz and a continuous20FPS review video. Targets move from approximately48 to3blocks; actual visible pixel size and occlusion, not nominal distance, determine the scored denominators. Include later arrivals and periods when targets are absent. Three class panels may be shown side by side as synchronized displays from separate captures, without pretending they are one shared world.

After prompt lock, evaluate four disjoint120-second mixed-species routes (two per cohort), then two300-second exploration routes (one per cohort). Movement, turning, partial/full occlusion, re-entry, varied lighting and similar-looking instances must occur. Use more than one instance per class in mixed scenes. Keep a fixed seed/route list and no adaptive stopping. Three density levels (6/12/24 spawned mobs) are separate prespecified sections of the mixed routes, not a separate prompt matrix.

The inference scheduler loads one model checkpoint and uses independent class prompt/track state. Verify the upstream multi-prompt semantics before merging prompts into a session; session IDs alone do not prove independent class labels. If separate sessions are required, share loaded weights where supported and measure the whole prompt-bank pass. A rotating class schedule and per-frame tracking are acceptable only with recorded revisit latency. No privilege-driven choice of which prompt to run. An ore/structure policy must not query only when a teacher reports that object.

“All mobs” means a registered target inventory with per-class denominators. The first ten-class cohort is not all1.16.1 mobs. Teacher records every visible mob, including out-of-bank classes; publish taxonomy coverage and unmatched/uncovered classes. Extend the bank through the same bounded screen for additional classes encountered in the intended task distribution, with new development clips. Generic `minecraft mob` is not a substitute for this accounting.

## Teacher and scoring boundary

SAM receives only rendered RGB video, exact selected text and its own history. The teacher/scorer can read UUIDs, types, poses, block states and camera matrices. These streams must be stored separately; inference manifests contain no teacher path or state. Privileged data never selects or updates the detector's live target list.

A world-space bounding box or nearby entity is not visible ground truth. Use a teacher visibility pass with camera projection plus depth/occlusion checks, then visually audit sampled frames and every claimed false positive/miss in the prompt-selection set. If only projected boxes are available, label them geometric proxies and keep ambiguous/fully occluded references out of visible recall. Do not report mask IoU without verified instance masks. Keep teacher render passes offline so they cannot change the actor camera/game timing.

Per class and route report: distinct visible instances; fraction discovered within1second of first eligible visibility; time to first correct detection; visible object-time coverage; false positive detections/minute and false track duration; semantic confusion; identity switches/fragmentation; re-acquisition after occlusion; box/mask localization under the stated teacher; combined prompt-bank latency, memory and effective frames/s. Count wrong-class detections as a false positive for the predicted class and a miss for the true class. Cross-prompt duplicate masks need deduplication with original proposals retained. Confidence is not correctness. Report units and denominators rather than treating adjacent frames as independent trials.

Initial eligibility: verified visible reference with ≥64 image pixels; report smaller instances separately rather than dropping them silently. Threshold0.5 is frozen for the first screen. Continuous20TPS / Easy / Minecraft1.16.1 / FOV70 and default FOV effects. Menu intervals remain explicit negative/distractor intervals, not hidden exclusions.

## Ore tracking

Develop prompts for exposed coal, iron, gold, redstone, lapis, diamond, emerald, Nether quartz, Nether gold and ancient debris. Do not label buried ore as a miss. Record approach, camera turns, look-away/revisit and partial mining under varied illumination. Teacher instance key: dimension plus block position, changing when the block is removed. Stone/dirt, held blocks, particles and inventory ore icons are negatives. Freeze per-class prompts before four disjoint90-second routes (two Overworld, two Nether). Score visible-vein discovery and block-level tracking separately; adjacent ore blocks are not automatically one instance.

## Structure tracking

Start with Nether fortress, bastion remnant, village, ruined portal and mineshaft. Use Minecraft-specific structural labels, with block-material labels only as tested complements. Teacher structure membership is not visibility. Score visible components and site-level discovery separately; lava/red terrain/caves are negatives. Four disjoint120-second walking/viewpoint routes, including distance/occlusion transitions. Never call a camera offset from `/locate` the distance to a visible structure. No path planning or traversal success is attributed to masks.

## Secondary moving-hazard test

Develop `minecraft hole in the ground`, `minecraft cave opening`, and `minecraft cliff edge` families on two development routes, with continuous forward/turning motion. Then six held-out60-second routes: three distinct natural hazards and three traversable controls. Compare a fixed movement script with/without the frozen mask-stop rule from the same starts. Measure warning lead time, actual falls/damage, false stops/minute and stopped time. A stopped guard run is not forced to keep moving into the hole. No stationary camera accuracy proxy replaces this experiment. Do not tune the stopping region on the evaluation routes.

## Presentation

Active pages: prompt selection; approaching/mixed/long-horizon mobs; ore tracking; structure tracking; walking hazards. Exact prompt strings and threshold beside every video, with model and timing mode. Keep the simple crossing/occlusion demonstration as a baseline within the mob page. Old static prompt comparisons, all-zombie stress clips, recorded hill/bank labels and shaft helper pilot move into the archive. Keep today's ROCKET noncombat/integration results separate, pending the user's review; older combat sweeps are archive material.

All training/evaluation compute: Jonathan's Mac or DTU HPC only. No new experiments are claimed by this setup. Start the bounded prompt screen before allocating the main evaluation matrix.

## Implementation status

`study.json` specifies candidates and boundaries; `capture-plan.json` fixes route IDs, splits, seeds and durations. `select_prompts.py` implements the bounded development selection gate and records a source SHA256. Six selector tests cover holdout rejection, false-positive gates, evidence minimums and union handling. The new capture/visibility scorer and SAM3.1 multi-prompt scheduling still require implementation and runtime validation before this matrix runs. Existing native forward-propagation code is offline; its throughput must never be reported as causal live latency. A live implementation may consume only frames available at decision time, and must record buffering, skipped frames and state resets. No new prompt is labeled selected until reviewed development evidence exists.
