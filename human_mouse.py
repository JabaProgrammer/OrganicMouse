import pyautogui
import random
import time
import math

TARGET_SIZE = 25
BASE_SHAKE = 0.6
OVERSHOOT_CHANCE = 0.22
DOUBLE_OVERSHOOT_CHANCE = 0.05
MAX_OVERSHOOT = 22
PATH_RANDOMNESS = 0.12

def fitts_time(distance, width=TARGET_SIZE):
    return 0.14 + 0.07 * math.log2(distance / width + 1)

def bell_profile(t):
    return 4 * t * (1 - t)

def generate_path(start, end, allow_overshoot=False):
    x0, y0 = start
    x1, y1 = end

    if allow_overshoot:
        x1 += random.uniform(-MAX_OVERSHOOT, MAX_OVERSHOOT)
        y1 += random.uniform(-MAX_OVERSHOOT, MAX_OVERSHOOT)

    def deviation():
        return random.uniform(-60, 60) * PATH_RANDOMNESS

    ctrl1 = (x0 + (x1-x0)*0.3 + deviation(), y0 + (y1-y0)*0.3 + deviation())
    ctrl2 = (x0 + (x1-x0)*0.6 + deviation(), y0 + (y1-y0)*0.6 + deviation())

    steps = random.randint(40, 60)
    path, intervals = [], []

    for i in range(steps + 1):
        t = i / steps
        x = (1 - t)**3*x0 + 3*(1 - t)**2*t*ctrl1[0] + 3*(1 - t)*t**2*ctrl2[0] + t**3*x1
        y = (1 - t)**3*y0 + 3*(1 - t)**2*t*ctrl1[1] + 3*(1 - t)*t**2*ctrl2[1] + t**3*y1
        shake = BASE_SHAKE * (1.0 - bell_profile(t))
        x += random.gauss(0, shake)
        y += random.gauss(0, shake)
        path.append((x, y))
        v = max(bell_profile(t), 0.05)
        intervals.append(1 / v)

    distance = math.hypot(x1 - x0, y1 - y0)
    total_time = fitts_time(distance)
    scale = total_time / sum(intervals)
    intervals = [dt * scale for dt in intervals]

    return path, intervals

def move_mouse(x, y):
    start_pos = pyautogui.position()
    overshoot = random.random() < OVERSHOOT_CHANCE

    path, intervals = generate_path(start_pos, (x, y), allow_overshoot=overshoot)
    for (px, py), dt in zip(path, intervals):
        pyautogui.moveTo(px, py, _pause=False)
        time.sleep(dt)

    if overshoot:
        time.sleep(random.uniform(0.05, 0.12))
        second_overshoot = random.random() < DOUBLE_OVERSHOOT_CHANCE
        path, intervals = generate_path(pyautogui.position(), (x, y), allow_overshoot=second_overshoot)
        for (px, py), dt in zip(path, intervals):
            pyautogui.moveTo(px, py, _pause=False)
            time.sleep(dt)

def human_click(button='left'):
    time.sleep(random.uniform(0.07, 0.15))
    pyautogui.click(button=button)
    time.sleep(random.uniform(0.08, 0.2))
