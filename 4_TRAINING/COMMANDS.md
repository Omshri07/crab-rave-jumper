# Exact commands used (Windows, PowerShell, from the project root)

## 1. Get the code at the pinned commits
```powershell
git clone https://github.com/KingKongRobotics/jumper.git jumper
git -C jumper checkout b2e58669848a3ba4f209597cd6bebdfe9d0533a4
$env:GIT_LFS_SKIP_SMUDGE = 1
git clone https://github.com/KingKongRobotics/jumper-design.git jumper-design
git -C jumper-design checkout 918d192857fcea1678c2a40b339501004a94d838
# jumper-design needs only these large files:
git -C jumper-design lfs pull --include="robots/jumper/**,library/skins/jumper-original.skin"
```

## 2. Environments (Python 3.11, CPU only)
This laptop reaches PyPI very slowly; the Tsinghua mirror was about 40x faster.
```powershell
$idx = "https://pypi.tuna.tsinghua.edu.cn/simple"
cd jumper
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -i $idx --upgrade pip
.\.venv\Scripts\python.exe -m pip install -i $idx torch==2.9.1 torchvision==0.24.1
.\.venv\Scripts\python.exe -m pip install -i $idx -e ".[dev]"     # ended with torch 2.14.1+cpu
cd ..\jumper-design
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -i $idx --upgrade pip
.\.venv\Scripts\python.exe -m pip install -i $idx -e ".[sim,dev]"
```
Exact resulting versions: `requirements-jumper-lock.txt`, `requirements-design-lock.txt`.

## 3. Train (about 2 h 31 min on the laptop)
```powershell
cd jumper
.\.venv\Scripts\python.exe scripts/train.py --task jumper.dance --backend native --device cpu --num_envs 256 --max-iterations 1500 --headless
```
Measured speed: 2.1 s/iteration at 64 envs, 6.0 s at 256, 13.5 s at 512. Checkpoints every
50 iterations land in `jumper/logs/jumper/jumper.dance/<timestamp>/`. The final one is
`4_TRAINING/run_2026-10-28_02-10-18/model_1499.pt`.

## 4. Scene (map)
```powershell
py -3.11 2_SCENE\make_crab_rave.py 2_SCENE\crab_rave.scene.json     # regenerates the source
cd jumper-design
.\.venv\Scripts\python.exe scripts/shellflow.py export-map ..\2_SCENE\crab_rave.scene.json --id crab-rave --title "Crab Rave" --default-skin library/skins/jumper-original.skin --profile robots/jumper/profile.json --output ..\2_SCENE\crab_rave.map
.\.venv\Scripts\python.exe scripts/shellflow.py verify-package ..\2_SCENE\crab_rave.map --profile robots/jumper/profile.json --capability rigid --capability jumper --mujoco
```
Spawn support check passed (floor at 0.01 m); native MuJoCo compile passed. This does not
prove a policy can walk on it; the replay did.

## 5. Skin
```powershell
py -3.11 3_SKIN\make_neon_skin.py jumper\assets\jumper\jumper.xml 3_SKIN\jumper_neon.xml
copy 3_SKIN\jumper_neon.xml jumper\assets\jumper\jumper_neon.xml
```

## 6. Final video
`RENDER_FINAL.ps1` in the project root runs this for you. The command it uses:
```powershell
cd jumper
.\.venv\Scripts\python.exe scripts/play.py --task jumper.dance --model assets/jumper/jumper_neon.xml --checkpoint ..\4_TRAINING\run_2026-10-28_02-10-18\model_1499.pt --backend native --device cpu --num_envs 1 --headless --steps 2000 --stop-on-done --video OUT.mp4 --video-width 1280 --video-height 720 --video-fps 30 --scene ..\2_SCENE\crab_rave.map --no-video-follow --video-azimuth 150 --video-elevation -10 --video-distance 1.0 --video-lookat-height 0.15
```
Vertical version: `--video-width 720 --video-height 1280 --video-distance 1.1`.
Replay adds observation noise by default, so a re-render is not guaranteed to be pixel-identical.
