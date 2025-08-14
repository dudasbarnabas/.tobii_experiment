# while True:
#     try:
#         asd = int(input('hello:'))
#         print(asd)
#         break
#     except Exception as e:
#         print(e)


from psychopy.hardware import keyboard
from psychopy import visual, core


win = visual.Window([800, 600], fullscr=False)
kb = keyboard.Keyboard()
kb.clock.reset()

visual.TextStim(win, text="Press SPACE (ESC to quit)").draw()
win.flip()

while True:
    keys = kb.getKeys(keyList=['space','escape'], clear=False, waitRelease=False)
    if keys:
        k = keys[0]
        print(k)
        # k.name -> 'space'
        # k.rt   -> seconds since kb.clock.reset()
        # k.duration -> press duration (if waitRelease=True)
        break 