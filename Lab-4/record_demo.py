"""Auto-play demo recorder: drives the game with scripted inputs, saves frames, stitches with ffmpeg.
usage: python record_demo.py <game.py> <out.mp4>"""
import os, sys, random, shutil, subprocess, importlib.util
os.environ["SDL_VIDEODRIVER"] = "dummy"; os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame
path, out = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("game", path); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
pygame.init(); screen = pygame.display.set_mode((g.WIDTH, g.HEIGHT))
frames = "frames_" + os.path.basename(out).split(".")[0]; shutil.rmtree(frames, ignore_errors=True); os.makedirs(frames)
class Keys:
    def __init__(self, up=False): self.up = up
    def __getitem__(self, k): return self.up if k == pygame.K_UP else False
random.seed(32)
game = g.Game(); n = 0
def label(text):
    f = pygame.font.Font(None, 24); s = f.render(text, True, (150, 200, 255)); screen.blit(s, (g.WIDTH - s.get_width() - 10, 10))
def run(seconds, autopilot_vy=None, caption=""):
    global n
    for _ in range(int(seconds * 60)):
        up = autopilot_vy is not None and game.vel.y > autopilot_vy
        game.update(1 / 60, Keys(up)); game.draw(screen); label(caption)
        pygame.image.save(screen, f"{frames}/{n:04d}.png"); n += 1
def setup(pad_idx, dx, vx, vy, height, fuel):
    x1, x2, y, m = game.pads[pad_idx]
    game.pos.update((x1 + x2) / 2 - dx, y - g.FOOT - height); game.vel.update(vx, vy); game.angle = 0.0; game.fuel = fuel
# 1) sideways slam: level, safe Vy, but Vx = 60 (> MAX_SPEED_X = 25)
t = 1.2; setup(0, 60 * t, 60, 30 - 18 * t, 30 * t - 9 * t * t + 0.5, g.FUEL_MAX)
run(3.0, caption="Test 1: sideways landing, Vx=60 > 25")
# 2) low-fuel careful descent onto the x3 pad (score preset to 1300 so this landing crosses 1500)
game.state = "fly"; game.new_round() if game.state != "fly" else None
game.new_round(); game.score = 1300; game.lives = 3
setup(1, 0, 0, 25, 70, 100)
run(4.8, autopilot_vy=25, caption="Test 2: low fuel + gentle x3 landing")
# 3) continue to next level -> bonus life check runs
if game.state == "landed": game.level += 1
game.new_round(); game.pos.y = 70; game.vel.update(0, 0)
run(10 - n / 60, caption="Test 3: score >= 1500 -> bonus life")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "60", "-i", f"{frames}/%04d.png",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", out], check=True)
print(out, n, "frames; final:", game.state, game.score, game.lives, game.message)
