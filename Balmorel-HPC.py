"""
Main author: Juan Jerez, jujmo@dtu.dk

---------- GENERAL DESCRIPTION ----------

This script automates the execution of Balmorel runs in the HPC cluster.
It generates bash-files (.sh) with the necessary commands, and submits
the jobs to the cluster. It follows this overall overall approach:

- Loads "submit_template.sh" with required job submission commands.
- Loads a csv-file with values for these commands, and fills the template.
- The filled template is written in respective scenario folders in HPC.
- Those files are sent to the HPC, submitting jobs to the queue.

---------- ASSUMPTIONS ----------

- This script assumes the following structure of your directories:
    home_user/
    │  ├─ files in this repo
    │  ├─ ...
    ├─ project_name/
    │  ├─ scenario_first/
    │  │  ├─ model/
    │  │  │  ├─ Balmorel.gams
    │  ├─ scenario_second/
    │  │  ├─ model/
    │  │  │  ├─ Balmorel.gams

- Project and scenario folder names MUST coincide with data provided to the script.

- Python 3.6+ is installed, due to the cwd argument in sub.process run.

---------- USAGE ----------

- To run this program, change your working directory to the folder
  containing this script and execute the following command:

    python3 Balmorel-HPC.py project_name /path/to/datafile.csv

---------- LEGAL STUFF ----------

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import argparse
import csv
import subprocess
import sys
from pathlib import Path
from string import Template

import config as cfg


def HPCSubmit(project_name, datafile):
    # Checks Python version
    if sys.version_info < (3, 6):
        print("-----------------------------------------------------")
        sys.exit("ERROR: PYTHON 3.6+ IS REQUIRED. SCRIPT HAS STOPPED")

    # Loads bash-file template
    submission_template = Path('submit_template.sh')
    with submission_template.open(mode='r') as file:
        template_text = Template(file.read())

    # Stores argument values of each run (scenario) into a dict
    # Compiles non-empty rows in the list 'runs'
    if Path(datafile).is_file():
        with open(datafile, mode='r') as file:
            reader = csv.DictReader(file)
            runs = [row for row in reader if any(row.values())]
    else:
        sys.exit("ERROR: Input csv-file not found, make sure its full path is included. SCRIPT HAS STOPPED")

    # Stops the code if: incomplete rows in csv-file, or more runs than allowed
    if len([run for run in runs if not all(run.values())]):
        sys.exit("ERROR: INCOMPLETE ROWS IN DATAFILE. SCRIPT HAS STOPPED")
    elif len(runs) > cfg.max_runs:
        sys.exit(
            f"ERROR: EXCEEDED MAX RUNS, SEE CONFIG.PY SETTINGS. SCRIPT HAS STOPPED")

    # from here on, it prepares and submits each job
    for run in runs:
        # Sets path to the directory and executable file of each scenario
        path_executable = set_path_executable(project_name, run['scenario'])
        path_scenario = path_executable.parent

        # Fills argument values into the bash-file template
        submission_content = template_text.substitute(
            run, project_name=project_name, path_executable=path_executable.as_posix())

        if path_scenario.is_dir():
            # Writes the template once filled into the scenario folder
            submission_file = Path(path_scenario, 'submit.sh')
            with submission_file.open(mode='w+') as file:
                file.write(submission_content)
            print("-----------------------------------------------------")          
            print(f"Submission file for scenario '{run['scenario']}' created")

            # Submits the job to the HPC
            job_submit(path_scenario, run['scenario'], submission_file)
        else:
            print(f"Scenario '{run['scenario']}' skipped, directory not found")
    print("\n ----------------- END OF EXECUTION ----------------- \n")

# Returns the path to the executable file
def set_path_executable(project_name, scenario_name):
    if cfg.option_testing:
        base = Path.cwd()
        program = 'andean'
    else:
        base = cfg.path_user
        program = 'model/Balmorel'
    return Path(base, project_name, scenario_name, program)

# Submits the job through the terminal (PuTTY on Windows)
def job_submit(path_scenario, scenario_name, submission_file):
    if cfg.option_submit:
        with submission_file.open(mode='r') as file:
            subprocess.run(['bsub'], stdin=file, cwd=path_scenario)
        print(f"Scenario '{scenario_name}' successfully submitted")
    else:
        print(
            f"Scenario '{scenario_name}' not submitted due to config.py settings")


if __name__ == "__main__":
    if cfg.option_testing:
        print("-----------------------------------------------------")
        print("ATTENTION: RUNNING SCRIPT IN TESTING MODE, CONTINUE? ")
        print("-----------------------------------------------------")
        user_input = input("Press Y/N and then Enter: ")
        if user_input == 'Y' or user_input == 'y':
            HPCSubmit('demo_project', 'demo_project/demo_data.csv')
    else:
        parser = argparse.ArgumentParser(
            description="Automates the generation and submission of Balmorel runs")
        parser.add_argument(
            'project', type=str, help="Project name, common to all Balmorel scenarios")
        parser.add_argument(
            'datafile', type=str, help="Full path to CSV file with BSUB command arguments")
        args = parser.parse_args()
        HPCSubmit(args.project, args.datafile)
