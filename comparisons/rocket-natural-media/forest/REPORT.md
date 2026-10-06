# Real-forest whole-task pilot

All four trials completed their tasks without observed damage: baseline and ROCKET-assisted navigation to a different higher tree, and baseline and ROCKET-assisted collection of four new logs. Astra selected every target from rendered pixels. ROCKET was used repeatedly across the useful task, not stopped after one option.

| Task | Ordinary controls | ROCKET-assisted | Helper contribution |
|---|---:|---:|---|
| Reach a higher tree |37.94s, success|80.56s, success|Six event6 options; subsequent movement and climbing after initial camera/back-up actions used ROCKET.|
| Gather four new logs |93.52s, success|104.10s, success|Seven options: one event6 approach and six event2 attempts, including133 issued attack actions. Astra also oriented, inspected inventory and collected drops with ordinary controls.|

These are different autonomous journeys, not equal-distance speed trials. The baseline navigation endpoint was10.38 horizontal blocks from the saved start with a root5 blocks higher. The ROCKET endpoint was36.81 blocks away with its root18 blocks higher. No controller speed advantage or reliability estimate is established by one trial per arm. A second checkpoint is being evaluated separately to broaden coverage.

## Actual terrain, source and scoring

Source: copied `2026-09-30_gpt-6.1-sol_step000050` from Lucas's readable backup. All four source manifest hashes passed. The documented converter reconstructs Minecraft1.16.1 from26.3; the full loss report is included. This is not exact historical replay. The start is natural spruce forest with uneven ground, foliage and hills, full health/food and a stone axe. Preparation removes16 existing item-drop entities so collecting historical dropped logs cannot satisfy gathering. No blocks are added or changed. Natural rooted trees are catalogued for the separate scorer; the actor never receives that catalogue or game state.

Navigation was prespecified as reaching a rooted tree at least10 horizontal blocks from the start and at least2 blocks higher, while the player moves at least8 blocks, rises at least2, stands on ground within2.5 horizontal and1.5 vertical blocks of the trunk for2 observed seconds. At least three vertical trunk logs must remain. Harvesting requires four net-new log items in inventory. Both tasks have150 wall seconds, Easy difficulty, default FOV70 and continuous20TPS. All four runtime restores passed pose/inventory/mode checks and advanced three initialization ticks before preparation freezing.

## Implemented feedback

The controller now warms up before scored play without issuing inputs. This pilot uses150ms expiring input leases, bounded by the independent250ms watchdog, and50ms minimum start-to-start pacing. Previous studies used50ms leases plus post-inference sleeps. Therefore these are a documented integration variant, not repetitions of the earlier adapter.

Every option stores the exact original reference RGB and binary mask, the actual224×224 reference RGB/mask after upstream resizing, and every224×224 current RGB consumed by ROCKET. Logs retain eventID, reference age, previous action input, each issued action, observation latency and lease duration. Event6 explicitly suppresses attack/use. Goal selection and retargeting are performed by Astra. A fixed reference mask is not a tracker.

## Evidence and validation

`episodes/*/game-browser.mp4` are whole-task plain videos; `policy-panels.mp4` retain the whole task with separate fixed-reference RGB, tinted exact mask on that original reference, and current-policy-input panels. No mask is projected onto the main game view or a later policy image. Videos are resampled onto actual elapsed wall-time from capture timestamps; original raw1280×720 recordings and timestamps remain archived. Per-option raw masks are retained.

Automated checks passed: all scored polls Easy/20TPS/unpaused/unfrozen; no actor tool errors; reference/current/mask files224×224; event6 attack/use absent; issued predictions at most250ms old and leases at most150ms; raw decoded frames match capture logs; wall/game/video durations agree. Sampled visual review confirms forest traversal, repeated hill climbing, tree-block breaking, inventory inspection and four collected logs. Exact endpoints and per-option counts are in `summary.json` and scorer results.

A preliminary preparation start was rejected before actor inference after panorama commands shifted its position by0.3 blocks. The corrected start restores explicit original coordinates and verifies pose after preparation. This setup issue is not a task failure. Compute used only the Mac and DTU.
