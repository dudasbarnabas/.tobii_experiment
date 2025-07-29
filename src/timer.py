import time
from psychopy import core, event

clock = core.Clock()
# clock.reset()

py = clock.getTime()
sys_time = time.time()

while True:
    py = clock.getTime()
    sys_time = time.time()
    print(f"{py:.3f}, {sys_time}")
    core.wait(1)