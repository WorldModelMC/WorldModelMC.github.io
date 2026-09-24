const scenarioSelect = document.getElementById('scenario-select');
const versionSelect = document.getElementById('version-select');
const trialSelect = document.getElementById('trial-select');
const paceSelect = document.getElementById('playback-pace');
const maskToggle = document.getElementById('show-masks');
const playAllButton = document.getElementById('play-all');
const video = document.getElementById('trial-video');
const status = document.getElementById('recording-status');
const links = document.querySelector('.video-links');
const infoList = document.getElementById('model-info-list');
let catalog;
let playAll = false;

function option(value, label) {
  const item = document.createElement('option');
  item.value = value;
  item.textContent = label;
  return item;
}

function scenario() {
  return catalog.scenarios.find(item => item.id === scenarioSelect.value);
}

function version() {
  return catalog.versions[versionSelect.value];
}

function addInfo(label, value) {
  const term = document.createElement('dt');
  const description = document.createElement('dd');
  term.textContent = label;
  description.textContent = value == null ? '—' : String(value);
  infoList.append(term, description);
}

function addSourceInfo(commit) {
  const term = document.createElement('dt');
  const description = document.createElement('dd');
  const link = document.createElement('a');
  term.textContent = 'Source commit';
  link.href = `https://github.com/WorldModelMC/minecraft-perception-lab/commit/${encodeURIComponent(commit)}`;
  link.textContent = commit;
  description.append(link);
  infoList.append(term, description);
}

function showInfo() {
  infoList.replaceChildren();
  const selectedScenario = scenario();
  const selectedVersion = version();
  if (!selectedVersion) return;
  const run = selectedVersion.runs[Number(trialSelect.value) || 0];
  addInfo('Scenario', selectedScenario.label);
  addInfo('Mob equipment', selectedScenario.equipment);
  addInfo('Policy', selectedVersion.policy);
  addInfo('Combat actions', selectedVersion.condition);
  addInfo('Segmentation', selectedVersion.segmentation);
  addInfo('Target selection', selectedVersion.targeting);
  addInfo('Detector threshold', selectedVersion.detector_threshold);
  addInfo('Visual-aim age limit', selectedVersion.visual_aim_age);
  addInfo('Controller additions', selectedVersion.changes.join('; '));
  addInfo('Model inputs', catalog.shared_inputs);
  addSourceInfo(selectedVersion.source);
  if (run) {
    addInfo('HPC job', run.hpc_job);
    addInfo('Outcome', `${run.kills} kills · ${run.deaths} deaths · ${run.steps} steps`);
    addInfo('Final health', run.final_health == null ? '—' : run.final_health);
    addInfo('Target / scan steps', `${run.target_steps ?? '—'} / ${run.scan_steps ?? '—'}`);
    addInfo('Recorded wall time', run.wall_seconds == null ? '—' : `${run.wall_seconds.toFixed(1)} seconds`);
  } else {
    addInfo('Recording status', selectedVersion.status);
  }
}

function setPlaybackPace(run) {
  const wall = paceSelect.querySelector('option[value="wall"]');
  const available = run?.wall_seconds > 0;
  wall.disabled = !available;
  wall.textContent = available
    ? `Measured average wall-clock pace · ${(run.steps / run.wall_seconds).toFixed(1)} steps/s`
    : 'Measured wall-clock pace unavailable';
  if (!available && paceSelect.value === 'wall') paceSelect.value = 'game';
  const rate = paceSelect.value === 'wall' ? run.steps / (20 * run.wall_seconds) : 1;
  video.defaultPlaybackRate = rate;
  video.playbackRate = rate;
}

function populateVersions() {
  versionSelect.replaceChildren();
  for (const key of scenario().versions) {
    versionSelect.append(option(key, catalog.versions[key].label));
  }
  populateTrials();
}

function populateTrials() {
  trialSelect.replaceChildren();
  const selectedVersion = version();
  if (selectedVersion) {
    selectedVersion.runs.forEach((run, index) => {
      const noun = run.kills === 1 ? 'kill' : 'kills';
      trialSelect.append(option(String(index), `Trial ${index + 1} · ${run.kills} ${noun}`));
    });
  }
  trialSelect.disabled = !selectedVersion || !selectedVersion.runs.length;
  playAllButton.disabled = trialSelect.disabled;
  selectVideo();
}

function selectVideo(keepTime = false, autoplay = false) {
  const selectedVersion = version();
  const run = selectedVersion?.runs[Number(trialSelect.value) || 0];
  const time = keepTime ? video.currentTime : 0;
  const resume = keepTime && !video.paused;
  video.pause();
  if (!run) {
    setPlaybackPace(null);
    video.removeAttribute('src');
    video.load();
    video.hidden = true;
    links.hidden = true;
    status.hidden = false;
    status.textContent = selectedVersion?.status || 'No recording available.';
    showInfo();
    return;
  }
  video.hidden = false;
  setPlaybackPace(run);
  links.hidden = false;
  status.hidden = true;
  video.src = `${run.base}${maskToggle.checked ? '-masks' : ''}.mp4`;
  video.setAttribute('aria-label', `${scenario().label}, ${selectedVersion.label}, trial ${Number(trialSelect.value) + 1}`);
  document.getElementById('screen-link').href = `${run.base}.mp4`;
  document.getElementById('masks-link').href = `${run.base}-masks.mp4`;
  if (keepTime || autoplay) {
    video.addEventListener('loadedmetadata', () => {
      if (keepTime) video.currentTime = Math.min(time, video.duration || time);
      if (resume || autoplay) video.play().catch(() => {});
    }, { once: true });
  }
  showInfo();
}

scenarioSelect.addEventListener('change', () => { playAll = false; populateVersions(); });
versionSelect.addEventListener('change', () => { playAll = false; populateTrials(); });
trialSelect.addEventListener('change', () => { playAll = false; selectVideo(); });
maskToggle.addEventListener('change', () => selectVideo(true));
paceSelect.addEventListener('change', () => setPlaybackPace(version()?.runs[Number(trialSelect.value) || 0]));
playAllButton.addEventListener('click', () => {
  playAll = true;
  trialSelect.value = '0';
  selectVideo(false, true);
});
video.addEventListener('ended', () => {
  if (!playAll) return;
  const next = Number(trialSelect.value) + 1;
  if (next >= version().runs.length) { playAll = false; return; }
  trialSelect.value = String(next);
  selectVideo(false, true);
});

fetch('/current/player-catalog.json')
  .then(response => { if (!response.ok) throw new Error(`Catalog HTTP ${response.status}`); return response.json(); })
  .then(data => {
    catalog = data;
    for (const item of catalog.scenarios) scenarioSelect.append(option(item.id, item.label));
    populateVersions();
  })
  .catch(error => {
    video.hidden = true;
    links.hidden = true;
    status.hidden = false;
    status.textContent = `Could not load recording catalog: ${error.message}`;
  });
