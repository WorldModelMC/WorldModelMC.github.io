# Live SAM survival diagnostic — 6 October 2026

Main question: does adding same-frame SAM observations help Astra survive a real historical recovery situation? Four predeclared episodes ran on DTU A100 allocation29616292 with gpt-6-astra/medium running through isolated Codex on the Mac. All used a copied converted Astra step425 checkpoint, Minecraft1.16.1, Easy, FOV70 and continuous20TPS. This is a26.3→1.16.1 reconstruction, not exact replay. The original October1 pit/hill starts remain unavailable.

## Observed outcomes

| Episode | Survived120s | Wall seconds | Accumulated health loss | SAM observations |
|---|---|---:|---:|---:|
| baseline-0 | yes | 120.82 | 9.73 | 0 |
| sam-0 | yes | 120.79 | 2.50 | 16 |
| sam-1 | no | 68.45 | 22.57 | 10 |
| baseline-1 | yes | 120.73 | 9.50 | 0 |

Both baselines survived; one of two SAM runs survived. The failing SAM run's death screen says “hit the ground too hard.” All four runs visibly pillar out of the shaft in the reviewed recording samples. Survival is the primary outcome; the old restrictive y≥67 escape rule no longer stops play. We did not compute a terrain-aware escape time.

This is too small to establish a performance difference or reliability rate. The first SAM run took less damage, but no useful mob localization was delivered that would justify attributing it to SAM. The second died. No benefit is demonstrated for this fixed configuration.

## What SAM actually supplied

Both SAM arms received their original image plus a640×360 annotated image on every completed look/action response. Four fixed prompts: minecraft zombie, minecraft spider, minecraft creeper, minecraft grass block; threshold0.5. No helper failures occurred across26 delivered observations. All seven positive proposals were labelled grass block. Visual inspection of all five positive-observation images showed held or placed cobblestone, not useful terrain classification. There were zero positive mob proposals; this is not a recall estimate because camera coverage and ground truth were not established.

The median added helper round trip was0.573s and0.473s in the two SAM runs, totalling9.05s and5.27s respectively. The game continued throughout. These include transport and inference on shared GPU hardware and are not isolated GPU latency measurements.

## Validation and limits

All sampled scorer states were Easy,20TPS, unpaused and unfrozen. Raw video frame counts match per-frame timing records; video/game/wall durations agree within1.5seconds. Restore pose/health and exact inventory/equipment checks passed; preparation clock advances were+2,+3,+3,+4ticks. This is not deterministic replay. Both baselines' final action requests received409 at the end-of-episode control gate; those calls are retained, not hidden. No SAM helper errors were recorded. Player process interruption after grading is expected.

Health loss is the sum of observed downward health changes at0.5s polling, so it can exceed20 with regeneration and can miss changes between polls. Contact-sheet review samples12frames per episode plus final frames; it is not exhaustive frame-by-frame annotation. Four episodes and one converted save cannot generalize to other pits, mobs or terrain. The survival instruction differs from the earlier ROCKET pilot, so those runs are not controls for this experiment.

The converter's losses and original checkpoint hashes are preserved in the merged rocket3-failure-checkpoints-20261006 report/archive. Source and complete raw traces/video are included here. No direct game state reaches the actor or SAM; privileged data appear only in preparation and scoring artifacts. CPU/GPU/game processes and dedicated tunnels were closed after the four episodes.

Next useful intervention: explicit active-looking after visible damage and/or a terrain-depth/foothold method, tested separately from SAM. Merely adding these four semantic masks has not solved the failure.
