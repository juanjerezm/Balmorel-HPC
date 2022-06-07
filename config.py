"""
Main author: Juan Jerez, jujmo@dtu.dk

Configuration file of the Balmorel-HPC script. Here the user can define
global settings that don't change across different projects in Balmorel.
Thus, it should only be modified during installation or development.
"""

from pathlib import Path

# path to the user's folder in the HPC, where the project folder is located
path_user = Path('/work3/jujmo/')

# maximum number of simultaneous submissions to HPC, to avoid spamming the HPC
max_runs = 10

# if option_testing is set to 'True', script uses example data from demo_project.
# Default value for proper use is 'False'
option_testing = True

# if option_submit is set to 'False', job submmission to the HPC is skipped (submitting jobs in the local machine will break the code)
option_submit = False


if option_testing:
    base_path = Path.cwd()
    file_executable = 'andean'
else:
    base_path = path_user
    file_executable = 'model/Balmorel'