import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

data = {'Objective': {0: 'OBJ 3.4',
                      1: 'OBJ 3.3',
                      2: 'OBJ 3.2',
                      3: 'OBJ 3.1',
                      4: 'OBJ 2.5',
                      5: 'OBJ 2.4',
                      6: 'OBJ 2.3',
                      7: 'OBJ 2.2',
                      8: 'OBJ 2.1',
                      9: 'OBJ 1.4',
                      10: 'OBJ 1.3',
                      11: 'OBJ 1.2',
                      12: 'OBJ 1.1'},

        'Aim': {0: 'AIM 3',
                1: 'AIM 3',
                2: 'AIM 3',
                3: 'AIM 3',
                4: 'AIM 2',
                5: 'AIM 2',
                6: 'AIM 2',
                7: 'AIM 2',
                8: 'AIM 2',
                9: 'AIM 1',
                10: 'AIM 1',
                11: 'AIM 1',
                12: 'AIM 1'},
 
        'Start': {# Aim 3
                  0: pd.Timestamp('2024-02-12 00:00:00'),
                  1: pd.Timestamp('2024-01-29 00:00:00'),
                  2: pd.Timestamp('2024-01-29 00:00:00'),
                  3: pd.Timestamp('2024-01-29 00:00:00'),
                  # Aim 2
                  4: pd.Timestamp('2023-12-18 00:00:00'),
                  5: pd.Timestamp('2023-12-27 00:00:00'),
                  6: pd.Timestamp('2023-12-18 00:00:00'),
                  7: pd.Timestamp('2023-12-06 00:00:00'),
                  8: pd.Timestamp('2023-12-04 00:00:00'),
                  #Aim 1
                  9: pd.Timestamp('2023-12-04 00:00:00'),
                  10: pd.Timestamp('2023-12-18 00:00:00'),
                  11: pd.Timestamp('2023-11-13 00:00:00'),
                  12: pd.Timestamp('2023-11-13 00:00:00')},
 
        'End': {# Aim 3
                0: pd.Timestamp('2024-03-01 00:00:00'),
                1: pd.Timestamp('2024-02-26 00:00:00'),
                2: pd.Timestamp('2024-02-19 00:00:00'),
                3: pd.Timestamp('2024-02-19 00:00:00'),
                # Aim 2
                4: pd.Timestamp('2024-01-29 00:00:00'),
                5: pd.Timestamp('2024-01-29 00:00:00'),
                6: pd.Timestamp('2024-01-29 00:00:00'),
                7: pd.Timestamp('2024-01-29 00:00:00'),
                8: pd.Timestamp('2023-12-24 00:00:00'),
                # Aim 1
                9: pd.Timestamp('2023-12-20 00:00:00'),
                10: pd.Timestamp('2024-01-12 00:00:00'),
                11: pd.Timestamp('2024-01-12 00:00:00'),
                12: pd.Timestamp('2024-03-01 00:00:00')},
 
        'Completion': {0: 1.0,
                       1: 1.0,
                       2: 1.0,
                       3: 1.0,
                       4: 1.0,
                       5: 1.0,
                       6: 1.0,
                       7: 1.0,
                       8: 1.0,
                       9: 1.0,
                       10: 1.0,
                       11: 1.0,
                       12: 1.0}}


##### DATA PREP ##### 
df = pd.DataFrame(data)

# project start date
proj_start = df.Start.min()

# number of days from project start to Objective start
df['start_num'] = (df.Start-proj_start).dt.days

# number of days from project start to end of Objectives
df['end_num'] = (df.End-proj_start).dt.days

# days between start and end of each Objective
df['days_start_to_end'] = df.end_num - df.start_num

# days between start and current progression of each Objective
df['current_num'] = (df.days_start_to_end * df.Completion)

# create a column with the color for each department
def color(row):
    c_dict = {'AIM 1':'#E64646', 'AIM 2':'#E69646', 'AIM 3':'#34D05C'}
    return c_dict[row['Aim']]

df['color'] = df.apply(color, axis=1)

##### PLOT #####
fig, (ax, ax1) = plt.subplots(2, figsize=(16,6), gridspec_kw={'height_ratios':[20, 1]})

# bars
ax.barh(df.Objective, df.current_num, left=df.start_num, color=df.color)
ax.barh(df.Objective, df.days_start_to_end, left=df.start_num, color=df.color, alpha=0.5)

for idx, row in df.iterrows():
    ax.text(row.end_num+0.1, idx, f"{int(row.Completion*100)}%", va='center', alpha=0.8)
    ax.text(row.start_num-0.1, idx, row.Objective, va='center', ha='right', alpha=0.8)


# grid lines
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed', alpha=0.2, which='both')

# ticks
xticks = np.arange(0, df.end_num.max()+1, 7)
xticks_labels = pd.date_range(proj_start, end=df.End.max()).strftime("%d/%m")
xticks_minor = np.arange(0, df.end_num.max()+1, 1)
ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)
ax.set_xticklabels(xticks_labels[::7])
ax.set_yticks([])

# ticks top
# create a new axis with the same y
ax_top = ax.twiny()

# align x axis
ax.set_xlim(0, df.end_num.max())
ax_top.set_xlim(0, df.end_num.max())

# top ticks (markings)
xticks_top_minor = np.arange(0, df.end_num.max()+1, 7)
ax_top.set_xticks(xticks_top_minor, minor=True)
# top ticks (label)
xticks_top_major = np.arange(3.5, df.end_num.max()+1, 7)
ax_top.set_xticks(xticks_top_major, minor=False)
# week labels
xticks_top_labels = [f"Week {i}"for i in np.arange(1, len(xticks_top_major)+1, 1)]
ax_top.set_xticklabels(xticks_top_labels, ha='center', minor=False)

# hide major tick (we only want the label)
ax_top.tick_params(which='major', color='w')
# increase minor ticks (to marks the weeks start and end)
ax_top.tick_params(which='minor', length=8, color='k')

# remove spines
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))
ax.spines['top'].set_visible(False)

ax_top.spines['right'].set_visible(False)
ax_top.spines['left'].set_visible(False)
ax_top.spines['top'].set_visible(False)

plt.suptitle('Observational Astronomy Micor-Project')

##### LEGENDS #####
legend_elements = [Patch(facecolor='#E64646', label='Aim 1'),
                   Patch(facecolor='#E69646', label='Aim 2'),
                   Patch(facecolor='#34D05C', label='Aim 3')]

ax1.legend(handles=legend_elements, loc='upper center', ncol=5, frameon=False)

# clean second axis
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.set_xticks([])
ax1.set_yticks([])

plt.show()