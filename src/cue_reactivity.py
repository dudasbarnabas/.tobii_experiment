from psychopy import visual, core, event
import pandas as pd

sorrend = []

# Read stimuli list
df_sor = pd.read_excel('.\cue_reactivity\sorrend.xlsx')
empty_found = False
for column in df_sor.columns:
    for row in df_sor.index:
        if pd.isna(df_sor.at[row, column]):
            empty_found = True
            break  # Exit the inner loop
        sorrend.append(str(df_sor.at[row, column]))
    if empty_found:
        break  # Exit the outer loop

# Initialize window
win = visual.Window(size=(1920, 1080), units='height', color='black')

# Define stimuli
fixation = visual.TextStim(win, text='+', height=0.1, color='white')

for stimuli in sorrend:
    image = visual.ImageStim(
        win,
        image=f".\cue_reactivity\stimuli\{stimuli}.png",  # Path to your image file
        pos=(0, 0),         # Center position (default)
    )
    # Show fixation
    fixation.draw()
    win.flip()
    core.wait(1)
    # Show image
    image.draw()
    win.flip()
    event.waitKeys()

win.close()