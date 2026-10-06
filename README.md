# Minecraft combat lab

This repository contains the public [Minecraft combat evaluation site](https://worldmodelmc.github.io/).
GitHub Pages publishes the root of `main` after each push. Group members can edit the
HTML and site assets here, or propose changes through a pull request.

The simulation runner and research source remain in the private
`WorldModelMC/minecraft-perception-lab` repository. Only results intended for the
public website belong here. New recordings and result JSON can be copied into this
repository and pushed to `main` to publish them.

## Use-case comparisons

[Browse SAM and ROCKET comparisons](https://worldmodelmc.github.io/comparisons/). Videos and statistics are grouped by use case with exact model and test-condition labels. GitHub Pages is the canonical publication.

## Active presentation

The homepage and `/comparisons/` show the focused SAM3.1 study and current-session ROCKET results. `/legacy/` contains earlier and retired exploratory directions. Keep old media URLs for provenance. Do not restore the old broad comparison generator as the homepage. New study cards must say setup until actual results exist, and show exact prompts/model versions beside videos. Publish here on GitHub Pages, never the legacy ChatGPT Site.

ROCKET goal overlays always belong to the original reference image. Do not paste a fixed reference mask onto later gameplay frames as if it were tracked. Distinguish human-selected diagnostic masks from autonomous Astra-selected goals.
