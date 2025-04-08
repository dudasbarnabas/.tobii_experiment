from psychopy import visual, core, event
import numpy as np
import pandas as pd
import random

# Initialize window
win = visual.Window(size=(1920, 1080), units='height', color='black')

# Define stimuli
fixation = visual.TextStim(win, text='+', height=0.1, color='white')
target = visual.Circle(win, radius=0.1, fillColor='blue', lineColor='blue')
feedback_text = visual.TextStim(win, text='', height=0.08, color='white')

# Trial settings
n_trials = 1
max_response_time = 2.0  # seconds
fixation_times = [0.9, 1.2, 1.5, 1.7, 2.1]
reaction_times = []

# Initialize dataframe
df = pd.DataFrame(columns=['block', 'fixation', 'reaction', 'lapsus','last5'])

# Instructions
instructions = visual.TextStim(win, text='Press SPACE when you see the blue circle.\n\nPress any key to start.', 
                               height=0.06, wrapWidth=1.5)
instructions.draw()
win.flip()
event.waitKeys()

# Main experiment loop
for trial in range(n_trials):
    # Shuffle fixation times
    random.shuffle(fixation_times)

    for fix_time in fixation_times:
        # Fixation period
        fixation.draw()
        win.flip()
        core.wait(fix_time)
        
        # Show target and start response timer
        target.draw()
        win.flip()
        resp_clock = core.Clock()
        
        # Collect response
        keys = event.waitKeys(maxWait=max_response_time, keyList=['space'], timeStamped=resp_clock)
        
        # Record results
        if keys:
            rt = keys[0][1]
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

# Save data
df.to_csv("tester.csv", sep="\t", index=False)

# Cleanup
win.close()