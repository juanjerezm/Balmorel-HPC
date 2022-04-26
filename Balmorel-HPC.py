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
    home_folder/
    ├─ Balmorel-HPC/
    │  ├─ files in this repo
    │  ├─ ...
    ├─ project_name/
    │  ├─ scenario_first/
    │  │  ├─ model/
    │  │  │  ├─ Balmorel.gams
    │  │  ├─ ...
    │  ├─ scenario_second/
    │  │  ├─ model/
    │  │  │  ├─ Balmorel.gams
    │  │  ├─ ...
    │  ├─ ...
    ├─ ...

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
from datetime import datetime
from pathlib import Path
from string import Template

import config as cfg

timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')


def HPCSubmit(project_name, datafile):
    # Checks Python version
    if sys.version_info < (3, 6):
        print("-----------------------------------------------------")
        sys.exit("ERROR: PYTHON 3.6+ IS REQUIRED. SCRIPT HAS STOPPED")

    # Reads and stores job parameters for each scenario (run) into a dict
    if Path(datafile).is_file():
        with open(datafile, mode='r') as file:
            # Detects the csv file's delimiter
            delimiter = csv.Sniffer().sniff(file.read()).delimiter
            file.seek(0)
            reader = csv.DictReader(file, delimiter=delimiter)
            # Compilation of non-empty csv rows, each is row a dict like {job_parameter:value, ...}
            runs = [row for row in reader if any(row.values())]
    else:
        sys.exit(
            "ERROR: Input csv-file not found, make sure its full path is included. SCRIPT HAS STOPPED")

    # Stops the code if there're incomplete rows from csv-file
    if len([run for run in runs if not all(run.values())]):
        sys.exit("ERROR: INCOMPLETE ROWS IN DATAFILE. SCRIPT HAS STOPPED")
    # Stops the script if number of scenarios is larger than the simultaneous runs allowed in the HPC
    elif len(runs) > cfg.max_runs:
        sys.exit(
            f"ERROR: EXCEEDED MAX ALLOWED HPC RUNS, SEE CONFIG.PY SETTINGS. SCRIPT HAS STOPPED")

    # Loads jobscript template (bash file)
    with Path('submit_template.sh').open(mode='r') as file:
        jobscript_template = Template(file.read())

    # from here on, the script creates each job, and submits it
    for run in runs:
        # Sets path of each scenario folder, along with its executable and jobscript files
        path_scenario, path_executable, path_jobscript = set_filepaths(
            project_name, run['scenario'])

        print("-----------------------------------------------------")
        if path_scenario.is_dir():
            # Populates the jobscript template with parameters, and writes it into the scenario folder
            job_creation(project_name, jobscript_template, run,
                         path_executable, path_jobscript)
            # Submits the jobscript to the HPC
            job_submision(run['scenario'], path_scenario, path_jobscript)
        else:
            print(f"Scenario '{run['scenario']}' skipped, directory not found")
    print("\n ----------------- END OF EXECUTION ----------------- \n")


def set_filepaths(project_name, scenario_name):
    # Returns the path to the scenario folder, as well as the executable and jobscript files
    path_executable = Path(cfg.base_path, project_name,
                           scenario_name, cfg.file_executable)
    path_scenario = path_executable.parent
    # path_scenario = Path(cfg.base_path, project_name, scenario_name)
    # path_executable = Path(path_scenario, cfg.file_executable)
    path_jobscript = Path(path_scenario, f"jobscript_{timestamp}.sh")
    return path_scenario, path_executable, path_jobscript


def job_creation(project_name, template_text, scenario, path_executable, path_jobscript):
    # Fills argument values into the bash-file template
    jobscript_content = template_text.substitute(
        scenario, project_name=project_name, path_executable=path_executable.as_posix(), output=path_executable.name)
    with path_jobscript.open(mode='w+') as file:
        file.write(jobscript_content)
    print(f"Submission file for scenario '{scenario['scenario']}' created")
    return


def job_submision(scenario_name, path_scenario, path_jobscript):
    # Submits the job through the terminal (PuTTY on Windows)
    if cfg.option_submit:
        with path_jobscript.open(mode='r') as file:
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
