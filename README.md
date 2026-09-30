# SE_LAB4_32_Lunar_Lander – Lunar Lander Repair Lab

> **Lab 4 (VibeCoding) submission by SUKRUTH-ES.** Based on the assigned repo [SETAPESU26/32_lunarLander](https://github.com/SETAPESU26/32_lunarLander) (cloned only – no PR raised to SETAPESU26). The bug fix and all three features are done; the updated code and videos are in [`Lab-4/`](Lab-4/) (details in [`Lab-4/README.md`](Lab-4/README.md)). AI tool used: Notion AI.

This project is a single-file Lunar Lander-lite clone using **Pygame**. It introduces students to vector physics, procedural terrain generation, and multi-condition landing validation using a small, readable object-oriented codebase.

---

## What's Provided

A working Lunar Lander-lite game with:

- A ship with rotation, thrust, gravity, and limited fuel, wrapping horizontally around the screen
- Procedurally generated terrain with two landing pads of different point multipliers
- Touchdown validation based on speed and angle, with a full HUD showing live telemetry
- Levels, lives, and scoring for successful landings

The original build had **one deliberate bug** and **three optional features** left as empty functions. In this submission the bug is fixed and all three features are implemented with the help of an AI assistant (every change in `Lab-4/game.py` is tagged `# TASK 1` … `# TASK 4`).

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
cd Lab-4
python game.py
```

**Controls:** Left/Right to rotate, Up to thrust, `R` to reset, Space to continue after landing or crashing.

---

## Tasks to Complete

All four tasks are complete ✅. Each section below keeps the original task text, followed by what was done.

### Task 1: Fix the touchdown validation bug

> A safe landing is supposed to require the ship to be over a pad, descending slowly, roughly level, *and* not moving sideways too fast. In the current build, a ship can slam down sideways — well beyond `MAX_SPEED_X` — on a pad at a safe vertical speed and angle, and it still counts as a perfect landing. Check the condition in `touchdown()` against all three constants it defines near the top of the file (`MAX_SPEED_X`, `MAX_SPEED_Y`, `MAX_ANGLE`), and see which one it never actually checks.

**✅ Done:** `touchdown()` never checked `MAX_SPEED_X`. Added `abs(self.vel.x) <= MAX_SPEED_X` to the success condition, plus a new crash reason – **"Crashed: drifting sideways too fast!"** – when horizontal speed is the cause.

### Task 2: Implement `ship_color(fuel_ratio)`

> Called once per frame in `draw`, as `color = ship_color(max(0.0, self.fuel) / FUEL_MAX) or (230, 230, 240)`. It receives the remaining fuel as a fraction from `0.0` (empty) to `1.0` (full) and should return an `(r, g, b)` hull color, or `None` to keep the default. Idea: shift the hull toward red as fuel runs low.

**✅ Done:** the hull blends linearly from white `(230, 230, 240)` at full fuel to red `(255, 30, 30)` when empty.

### Task 3: Implement `on_landing(score)`

> Called from `touchdown()` immediately after a successful landing's points are added to the score. It receives the number of points just earned from that landing. Its return value is ignored. Idea: a fireworks effect, or a distinct sound for a high-multiplier pad.

**✅ Done:** a fireworks/particle burst at the landing spot – 60 gold/white sparks on the x1 pad, 180 faster multicolour sparks on the x3 pad – plus a short beep (higher pitch on x3) that fails silently when no audio device is available.

### Task 4: Implement `bonus_life_threshold()`

> Called every frame in `update()`. It takes no arguments and should return an integer score value, or `None` to disable bonus lives entirely. Whenever the score crosses a multiple of that value for the first time, one life is awarded automatically — the bookkeeping (`self.bonus_awarded`) is already implemented, so you only need to choose the threshold. Idea: return `1500`.

**✅ Done:** returns `1500`; a **"BONUS LIFE!"** banner appears on screen for ~1.5 s whenever a life is awarded.

---

## Expected Behavior

- The ship wraps horizontally but never moves past the top of the screen; gravity and rotated thrust behave like real vectors
- Terrain always includes exactly two landing pads with different score multipliers
- A landing only counts as successful when the ship is over a pad, descending slowly, roughly level, and not drifting sideways too fast
- Fuel never goes negative, and thrust cuts out automatically once it runs out
- A crash costs a life; the game ends when lives reach zero

---

## Folder Structure

```
SE_LAB4_32_Lunar_Lander/
├── README.md              <- this file
└── Lab-4/
    ├── game.py            <- updated game (bug fix + 3 features, tagged # TASK n)
    ├── before.mp4         <- 10 s gameplay before changes (bug visible)
    ├── after.mp4          <- 10 s gameplay after changes (fix + features)
    ├── README.md          <- detailed change log and testing notes
    ├── changes.diff       <- diff vs. the original game.py
    ├── record_demo.py     <- auto-play script used to record the videos
    └── (chat history doc/pdf)
```

---

## Submission Checklist

- [x] A 10-second video of gameplay **before** the changes, showing the bug – [`Lab-4/before.mp4`](Lab-4/before.mp4) (a sideways landing at Vx = 60 > 25 counted as "Perfect landing!")
- [x] A 10-second video of gameplay **after** the changes, showing the fix and new features – [`Lab-4/after.mp4`](Lab-4/after.mp4)
- [x] Updated code – [`Lab-4/game.py`](Lab-4/game.py)
- [ ] The Chat/LLM used page link, with the complete chat history – exported as doc/pdf into `Lab-4/`
