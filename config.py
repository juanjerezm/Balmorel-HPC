"""
Main author: Juan Jerez, jujmo@dtu.dk

Configuration file of the Balmorel-HPC script. Here the user can define
global settings that don't change across different projects in Balmorel.

Thus, it should only be modified during installation or development.
"""

from pathlib import Path

# path to the user's folder in the HPC
path_user = Path('/work3/jujmo/')

# maximum number of simultaneous submissions to HPC, to avoid spamming the HPC
max_runs = 10

# if testing_mode is set to 'True', demo_project directories and data are used.
# Default value for proper use is 'False'
testing_mode = False

# if option_submit is 'False', job submmission to the HPC is skipped
# (submitting jobs in local machine breaks the code)
# (can be mannually overriden if testing on the HPC)
# option_submit = False if testing_mode else True
option_submit = True
