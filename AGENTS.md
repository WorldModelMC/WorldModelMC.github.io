# Constitution

1. Do not use privileged information during final inference: models and controllers may use only rendered game pixels plus game audio (what a player sees and hears), never direct game state from RAM, APIs or files. Additionally, we will never pause the game, and always keep the game difficulty on Easy. Privileged data is permitted for dataset creation and training.
2. Use Minecraft **1.16.1**, chosen for its common use in speedrunning and compatibility with our Minecraft 1.16 research tooling.
3. Ensure that findings and project information eventually reside in a repository in our [GitHub organization](https://github.com/WorldModelMC) or in our [Drive folder](https://drive.google.com/drive/folders/1lVd1fIp2F-CLqtppMRSUyTghZCk0AjoN).
4. The default field of view is **70** (the game default, `fov:0.0` in options.txt), the setting of VPT's recordings and the MineStudio simulator: run every test, evaluation, data recording and policy at it, with field-of-view effects left at the game default. Quake Pro (110) was considered on 2026-10-01 and dropped.
