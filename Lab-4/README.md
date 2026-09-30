# Lab 4 – VibeCoding: Lunar Lander (repo 32_lunarLander)

**Student GitHub:** SUKRUTH-ES
**Assigned repo:** https://github.com/SETAPESU26/32_lunarLander (cloned only – no PR raised to SETAPESU26, as the handout requires)
**AI tool used:** Notion AI (chat agent)

## Contents of this folder

| File | What it is |
|---|---|
| `game.py` | Updated game with the bug fix and all three features (every change is tagged `# TASK n`) |
| `before.mp4` | 10 s gameplay with the **original** code – sideways landing (Vx = 60 > MAX_SPEED_X = 25) is counted as "Perfect landing!" |
| `after.mp4` | 10 s gameplay with the **updated** code – same sideways landing now crashes ("drifting sideways too fast"), hull turns red on low fuel, fireworks on the x3 pad, "BONUS LIFE!" at 1500 points |
| `Chat_History_Lab4.pdf` | Exported chat history with the AI assistant |
| `changes.diff` | Git diff of `game.py` vs the original repo |
| `record_demo.py` | Auto-play script used to record both videos (saves frames, stitches with ffmpeg) |

## Changes made (search for `# TASK`)

### Task 1 – Touchdown validation bug (fixed)
`touchdown()` checked `MAX_SPEED_Y` and `MAX_ANGLE` but never `MAX_SPEED_X`, so a ship could slam down sideways at any horizontal speed and still land "perfectly".
- Added `abs(self.vel.x) <= MAX_SPEED_X` to the success condition.
- Added a crash reason: when horizontal speed is the cause, the message is **"Crashed: drifting sideways too fast!"** (vertical-speed crashes still say "too fast").

### Task 2 – `ship_color(fuel_ratio)`
Linearly blends the hull from white `(230, 230, 240)` at full fuel to red `(255, 30, 30)` at empty, so the ship gradually turns red as fuel runs low.

### Task 3 – `on_landing(score)`
- Spawns a particle/fireworks burst at the landing spot: 60 gold/white sparks on the x1 pad, 180 multi-coloured, faster sparks on the x3 pad.
- Plays a short synthesized beep (higher pitch on x3). Wrapped in `try/except`, so the game never crashes when no audio device is available.
- Small supporting additions: an `FX` state dict, `Game.__init__` registers the game in `FX` (so `on_landing` knows the ship position), and `draw()` calls `draw_effects()` to animate the particles.

### Task 4 – `bonus_life_threshold()`
Returns `1500`. The existing bookkeeping awards the life; one added line starts a ~1.5 s **"BONUS LIFE!"** banner, drawn by `draw_effects()`.

Everything else in the game is unchanged.

## How it was tested
- Headless unit checks (original vs updated): sideways touchdown at Vx = 60 → original `landed`, updated `crashed: drifting sideways too fast`; gentle landings still succeed; particle counts 60 (x1) / 180 (x3); `ship_color` = (230,230,240) / (242,130,135) / (255,30,30) at 100 % / 50 % / 0 % fuel; score 1600 → lives 3 → 4 with banner shown.
- The real `main()` loop was run headless (SDL dummy video/audio) without errors, confirming the beep fails silently without audio.
- Videos recorded with `record_demo.py` (fixed random seed, scripted inputs; for the demo the score is preset to 1300 and fuel to 100 so the bonus life and low-fuel colour appear within 10 s).

## Run it
```bash
pip install pygame
python game.py
```
Controls: Left/Right rotate, Up thrust, R reset, Space continue.

Re-record the videos: `python record_demo.py game.py after.mp4` (needs ffmpeg).
