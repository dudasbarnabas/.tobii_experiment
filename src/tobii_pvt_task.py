# Import modules
import random_isi as ri
from psychopy import visual, core, event
import numpy as np
import pandas as pd
import random
import time

from psychopy import visual, monitors, core
from titta import Titta, helpers_tobii as helpers
from titta.TalkToProLab import TalkToProLab
import random


#%% Monitor/geometry
MY_MONITOR                  = 'testMonitor' # needs to exists in PsychoPy monitor center
FULLSCREEN                  = True
SCREEN_RES                  = [1920, 1080]
SCREEN_WIDTH                = 52.7 # cm
VIEWING_DIST                = 63 #  # distance from eye to center of screen (cm)

mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
mon.setWidth(SCREEN_WIDTH)          # Width of screen (cm)
mon.setDistance(VIEWING_DIST)       # Distance eye / monitor (cm)
mon.setSizePix(SCREEN_RES)

#%% ET settings
et_name = 'Tobii Pro Spectrum'

dummy_mode = False
project_name = None # None or a project name that is open in Pro Lab.
                    # If None, the currently opened project is used.

# Change any of the default settings?
settings = Titta.get_defaults(et_name)

# Ask for patricipant id
while True:
    try:
        settings.FILENAME = int(input("Participant id: "))
        break
    except Exception as e:
        print(e)

# Participant ID and Project name for Lab
pid = settings.FILENAME

#%% Connect to eye tracker and calibrate (you need to do this outside of lab)
tracker = Titta.Connect(settings)
if dummy_mode:
    tracker.set_dummy_mode()
tracker.init()

#%% Talk to Pro Lab
ttl = TalkToProLab(project_name=project_name,
                   dummy_mode=dummy_mode)
participant_info = ttl.add_participant(pid)


def show_vas(win, question="Mennyire érzi magát fáradtnak?", left_label="Egyáltalán nem", right_label="Nagyon", line_length=1.0):

    # Line and markers
    vas_y = -0.2
    line = visual.Line(win, start=(-line_length/2, vas_y), end=(line_length/2, vas_y), lineWidth=3, lineColor='white')
    marker = visual.Circle(win, radius=0.01, fillColor='red', lineColor='red', pos=(0, vas_y))

    # Labels
    text_question = visual.TextStim(win, text=question, pos=(0, 0.2), height=0.06, color='white')
    text_left = visual.TextStim(win, text=left_label, pos=(-line_length/2, vas_y - 0.1), height=0.05, color='white', alignText='center')
    text_right = visual.TextStim(win, text=right_label, pos=(line_length/2, vas_y - 0.1), height=0.05, color='white', alignText='center')

    # Mouse
    mouse = event.Mouse(visible=True, win=win)
    response_given = False
    vas_response = None

    while not response_given:
        # Draw components
        win.flip()
        text_question.draw()
        text_left.draw()
        text_right.draw()
        line.draw()

        # Draw marker if mouse is on line
        mouse_pos = mouse.getPos()
        if (line.pos[0] - line_length/2) <= mouse_pos[0] <= (line.pos[0] + line_length/2) and abs(mouse_pos[1] - vas_y) < 0.05:
            marker.pos = (mouse_pos[0], vas_y)
            marker.draw()


        # Check for click
        if mouse.getPressed()[0]:  # left click
            if (line.pos[0] - line_length/2) <= mouse_pos[0] <= (line.pos[0] + line_length/2) and abs(mouse_pos[1] - vas_y) < 0.05:
                vas_response = (mouse_pos[0] + line_length/2) / line_length  # normalized between 0 and 1
                response_given = True
                core.wait(0.2)  # debounce click
            win.flip()

    mouse.setVisible(False)
    return vas_response

try:
    # Window set-up (this color will be used for calibration)
    win = visual.Window(monitor = mon, fullscr = FULLSCREEN,
                        screen=1, size=SCREEN_RES, units = 'deg')
    
    # Calibrate (must be done independent of Lab)
    tracker.calibrate(win)
    win.flip()

    #%% Recording

    # Check that Lab is ready to start a recording
    state = ttl.get_state()
    assert state['state'] == 'ready', state['state']

    ## Start recording (Note: you have to click on the Record Tab first!)
    rec = ttl.start_recording("image_viewing",
                        participant_info['participant_id'],
                        screen_width=1920,
                        screen_height=1080)
    
except Exception as e:
    print(e)


# Define stimuli
fixation = visual.TextStim(win, text='+', height=0.1, color='white')
target = visual.Circle(win, radius=0.1, fillColor='blue', lineColor='blue')
feedback_text = visual.TextStim(win, text='', height=0.08, color='white')

# Trial settings
n_trials = 1
max_response_time = 1  # seconds
fixation_times = []
reaction_times = []

# Initialize dataframe
df = pd.DataFrame(columns=['block', 'fixation', 'reaction', 'lapsus','last5', 'vas', 'pres_time'])

# Instructions
instructions = visual.TextStim(win, text='Press SPACE when you see the blue circle.\n\nPress any key to start.', 
                               height=0.06, wrapWidth=1.5)

vas_score = show_vas(win, question="How mentally fatigued do you feel?", left_label="Not at all", right_label="Extremely")
df2 = pd.DataFrame({'vas':[vas_score]})
df = pd.concat([df, df2], ignore_index=True)
print(df.tail(1))

instructions.draw()
win.flip()
event.waitKeys()

# Main experiment loop
for trial in range(n_trials):
    fixation_times = ri.split_time_integer()

    for fix_time in fixation_times:
        # Fixation period
        fixation.draw()
        win.flip()
        core.wait(fix_time)
        
        # Show target and start response timer
        target.draw()
        win.flip()
        sys_time = time.time()
        resp_clock = core.Clock()
        resp_clock.reset()
        timestamp = ttl.get_time_stamp()
        ttl.send_stimulus_event(rec['recording_id'],
                                    str(timestamp),
                                    'onset')
        
        first_key = None

        # Collect response
        while resp_clock.getTime() < max_response_time:
            keys = event.getKeys(keyList=['space'], timeStamped=resp_clock)
            if keys and not first_key:
                timestamp = ttl.get_time_stamp()
                first_key = keys[0]
                win.flip() # Clear screen on press
                ttl.send_stimulus_event(rec['recording_id'],
                                    str(timestamp),
                                    'keypress')
        
        # Record results
        if first_key:
            rt = first_key[1]
            lapsus = False
            reaction_times.append(rt)
        else:
            rt = max_response_time  # Mark no-response trials
            lapsus = True
        
        five = sum(reaction_times[-5:])/len(reaction_times) if len(reaction_times) > 0 else 'none'

        # Add to dataframe
        df2 = pd.DataFrame({'block':[trial+1], 'fixation':[fix_time], 'reaction':[rt], 'lapsus':[lapsus], 'last5':[five], 'pres_time':[sys_time]})
        df = pd.concat([df, df2], ignore_index=True)
        print(df[-1:])

vas_score = show_vas(win, question="How mentally fatigued do you feel?", left_label="Not at all", right_label="Extremely")
df2 = pd.DataFrame({'vas':[vas_score]})
df = pd.concat([df, df2], ignore_index=True)
print(df.tail(1))

# Save data
df.to_csv("tester.csv", sep="\t", index=False)

## Stop recording
ttl.stop_recording()
win.close()

#%% Finalize the recording
# Finalize recording
ttl.finalize_recording(rec['recording_id'])
ttl.disconnect()