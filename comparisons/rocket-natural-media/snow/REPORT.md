# Snowy terrain: whole-task navigation and gathering

The second natural checkpoint produced a navigation success with repeated ROCKET options where the ordinary-control baseline timed out. Both gathering arms collected four new logs without an axe. This completes a bounded eight-trial batch across two historical terrain starts, one run per arm/task/start.

| Task | Ordinary controls | ROCKET-assisted | Actual helper contribution |
|---|---|---|---|
| Reach a higher tree | Timeout, 150.88s; 2 cumulative health lost | Success, 49.93s; no damage | Four event6 options (5, 5, 4, 5 seconds); all movement after one ordinary camera turn used ROCKET. |
| Collect four new logs | Success, 108.59s; no damage | Success, 87.56s; no damage | Eight options: two event6 approaches and six event2 calls, with 366 issued attack actions. Ordinary controls supplied two camera turns. |

The baseline navigation did climb: maximum player height was 86.17 from a start at 78. It then descended into a hollow, lost two health points around 71.36s, regenerated, and attempted to return through snowy steps. It never satisfied the complete grounded, intact-tree proximity condition for two seconds. The ROCKET arm reached a rooted spruce 38.35 horizontal blocks from the saved start, with its root six blocks higher; final player height was 85. These are independently selected journeys, not a fixed-destination controller-speed comparison. Gathering elapsed time likewise includes Astra observation/reasoning, target choice, movement and collection, not just policy execution.

## Source and verified preparation

The copied source is `pc/runs/2026-09-25_sonnet-5/checkpoints/2026-09-25_sonnet-5_step000025` in Lucas's backup. All four source manifest hashes passed. The source's actor was Sonnet; the experimental actor in **both** arms is isolated Codex `gpt-6-astra`, medium reasoning, using the subscription launcher. ROCKET uses the pinned `rocket3.ckpt` SHA256 `e484da8c417f5fa18767e669222575d8c61ee135e022de3953cad12a226dc259`.

The documented benchmark converter at upstream commit `1272adf5a5d045b92b005c017cc3882d2edb3310` reconstructs 26.3 into 1.16.1 with radius eight chunks. Structural validation passed for 289 chunks; the complete conversion loss report is retained. This is a converted reconstruction, not exact historical replay. No source files were modified.

The saved start preserves position (-9.0907, 78, 4.5780), orientation, health/food and source inventory: **one spruce log and one dirt, no axe**. The harvest prompt says “Use whatever tools you have”; no stone-axe claim was used in this batch. Fifteen pre-existing item drops were removed during preparation, with no terrain block edits. Consequently success requires inventory to rise from one to at least five logs. A fifteen-second live idle check showed no damage. All four restores passed pose/inventory/mode checks; two or three initialization ticks elapsed before preparation freezing. Runtime configuration verified Easy, survival, FOV70/default effects; every scored state was unpaused, unfrozen and 20TPS. Privileged preparation/scoring never enters the actor's MCP.

The unchanged scorer requires navigation to an intact rooted tree at least ten horizontal blocks away and two blocks above the start, with player displacement at least eight, player rise at least two, grounded within 2.5 horizontal/1.5 vertical blocks of the root for two consecutive observed seconds. Gathering requires four net-new log inventory items. Wall-time budget is 150s; polling/termination overhead accounts for the baseline's 150.88s. Setup failures are distinct from task outcomes.

## Inputs, control and evidence

Astra selects and updates every goal box from returned pixels. No human goal mask or privileged target catalogue is supplied. Calls are bounded to five seconds, and repeated as needed. Event6 suppresses attack/use. Event2 can attack and may disturb nearby terrain while approaching the chosen log; a successful whole-task outcome does not mean every option cleanly achieved its intended block. The gathering video shows an early dirt strike before later successful trunk harvesting.

The same warmed-up controller and 150ms expiring input leases as the forest batch are used. Every option resets recurrent state and stores its original reference RGB, exact binary mask, actual resized 224×224 reference inputs, every current RGB consumed by policy, reference age, event ID and action issuance. Separate video panels tint the exact mask on its **fixed reference**, never on a later frame. The large game view is unmodified. Whole-task browser videos preserve elapsed wall-time by holding frames according to recorded capture timestamps; original raw videos remain available.

Automated checks passed for all four runs: scored-state settings, valid restores, no actor tool errors, policy image shapes, event6 restrictions, issued observation age ≤250ms/lease ≤150ms, raw frame/timestamp counts, and game/wall/video duration agreement. Sampled contact sheets and a policy-panel frame confirm natural snow-covered slopes, the baseline's hollow, repeated tree-block harvesting, and a correctly positioned fixed-reference mask. The archive includes all exact prompts, calls, scorer traces, source/checkpoint files, conversion losses, and code. All compute was Mac/DTU; the host/game exited and the private SSH forward was removed after completion.

## What the eight trials establish

Forest: both navigation arms succeeded (37.94s baseline, 80.56s assisted), and both gathered four logs (93.52s, 104.10s). The forest navigation destinations differed markedly: baseline 10.38 blocks away/root +5; assisted 36.81/root +18. Snow: the results above add meaningful terrain and inventory variation. Together they demonstrate autonomous repeated-option integration for useful navigation and multi-block gathering on two reconstructed natural starts. They do not establish general reliability or a causal speed advantage.

Next justified expansion is repeated, pixel-defined shared destinations and obstacle/recovery checkpoints, including the original flooded-pit and terraced-hill starts when those exact assets become available. Passive hunting, structures and Nether combat were not evaluated in this batch. Missing original October 1 pit/hill checkpoints remain a limitation; these natural starts do not silently substitute for those failures.
