from human_mouse import move_mouse, human_click
import time

def test_basic_move():
    print("[TEST 1] Basic move test starting...")
    move_mouse(500, 400)
    time.sleep(0.5)
    print("[TEST 1] Finished.\n")

def test_move_and_click():
    print("[TEST 2] Move and click test starting...")
    move_mouse(600, 450)
    human_click()
    time.sleep(0.5)
    print("[TEST 2] Finished.\n")

def test_multiple_moves():
    print("[TEST 3] Multiple moves test starting...")
    positions = [(550, 420), (620, 470), (580, 440)]
    for pos in positions:
        move_mouse(*pos)
        time.sleep(0.3)
    print("[TEST 3] Finished.\n")

if __name__ == '__main__':
    print("Starting OrganicMouse tests in 3 seconds...")
    time.sleep(3)

    test_basic_move()
    test_move_and_click()
    test_multiple_moves()

    print("All tests completed.")
