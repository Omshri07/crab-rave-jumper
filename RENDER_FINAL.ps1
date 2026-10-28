# Re-renders the entry video from the saved checkpoint, skin and scene.
# Usage (from the project root):  .\RENDER_FINAL.ps1 [-Out file.mp4] [-Vertical]
# Never run while training: both slow down.
param(
  [string]$Out = "1_FINAL_VIDEOS\crab_rave_dance_rerender.mp4",
  [switch]$Vertical
)
$root = $PSScriptRoot
Set-Location "$root\jumper"
if (-not (Test-Path "assets\jumper\jumper_neon.xml")) {
  Copy-Item "$root\3_SKIN\jumper_neon.xml" "assets\jumper\jumper_neon.xml"
}
$w, $h, $d = 1280, 720, 1.0
if ($Vertical) { $w, $h, $d = 720, 1280, 1.1 }
& .\.venv\Scripts\python.exe scripts/play.py --task jumper.dance --model assets/jumper/jumper_neon.xml `
  --checkpoint "$root\4_TRAINING\run_2026-10-28_02-10-18\model_1499.pt" `
  --backend native --device cpu --num_envs 1 --headless --steps 2000 --stop-on-done `
  --video "$root\$Out" --video-width $w --video-height $h --video-fps 30 `
  --scene "$root\2_SCENE\crab_rave.map" --no-video-follow --video-azimuth 150 `
  --video-elevation -10 --video-distance $d --video-lookat-height 0.15
Set-Location $root
