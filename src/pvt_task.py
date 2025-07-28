import random_isi as ri
from psychopy import visual, core, event
import numpy as np
import pandas as pd
import random

def show_vas(win, question="How tired are you?", left_label="Not at all", right_label="Extremely", line_length=1.0):

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


# Initialize window
# win = visual.Window(size=(1920, 1080), units='height', color='black')
win = visual.Window(fullscr=False, color='black')

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
df = pd.DataFrame(columns=['block', 'fixation', 'reaction', 'lapsus','last5','vas'])

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
        resp_clock = core.Clock()
        resp_clock.reset()
        
        first_key = None

        # Collect response
        while resp_clock.getTime() < max_response_time:
            keys = event.getKeys(keyList=['space'], timeStamped=resp_clock)
            if keys and not first_key:
                first_key = keys[0]
        
        # Record results
        if first_key:
            rt = first_key[1]
            feedback = f'Correct! RT: {rt*1000:.0f} ms'
            lapsus = False
            reaction_times.append(rt)
        else:
            rt = max_response_time  # Mark no-response trials
            lapsus = True
            feedback = 'Too slow!'
        
        five = sum(reaction_times[-5:])/len(reaction_times) if len(reaction_times) > 0 else 'none'

        # Add to dataframe
        df2 = pd.DataFrame({'block':[trial+1], 'fixation':[fix_time], 'reaction':[rt], 'lapsus':[lapsus], 'last5':[five]})
        df = pd.concat([df, df2], ignore_index=True)
        print(df[-1:])

        if trial == 0:
            # Show feedback
            feedback_text.text = feedback
            feedback_text.draw()
            win.flip()
            core.wait(0.8)

vas_score = show_vas(win, question="How mentally fatigued do you feel?", left_label="Not at all", right_label="Extremely")
df2 = pd.DataFrame({'vas':[vas_score]})
df = pd.concat([df, df2], ignore_index=True)
print(df.tail(1))

# Save data
df.to_csv("tester.csv", sep="\t", index=False)

# Cleanup
win.close()