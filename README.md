# Balmorel-HPC
Automates the generation and submission of Balmorel jobs to the HPC cluster.

## Intro
This script automates the execution of Balmorel runs in the HPC cluster. It generates bash-files (.sh) with the necessary commands, and submits the jobs to the cluster. It follows this overall overall approach:

- Loads the file *submit_template.sh*, which contains the required *BSUB* job submission commands.
- Loads a csv-file, provided by the user, with values for each of these commands.
- Fills the template with the values from the csv file.
- The contents of this filled template are written to a submission file (*submit.sh*) in its respective scenario folder in the HPC.
- The submission file is sent to the HPC through the command line, submitting the job to the queue.

## Prequerisites
- Python 3.6 or higher

## Installation
- Setting and environment in the HPC is not strictly necessary.
- Copy the contents of this repository in your HPC folder.
- Project and scenario folder names **must** coincide with data provided to the script.
- The script is built assuming the following directory structure:
    ```    
    home_user/
    ├─ Balmorel-HPC/
    │  ├─ files in this repo
    │  ├─ ...
    ├─ project_name/
    │  ├─ scenario_first/
    │  │  ├─ model/
    │  │  │  ├─ Balmorel.gams
    │  ├─ scenario_second/
    │  │  ├─ model/
    │  │  │  ├─ Balmorel.gams
    ```

## Execution
- On the HPC terminal, change directory to the folder containing this script and execute the following command:
    > ```python3 Balmorel-HPC.py project_name datafile.csv```
- When running the script for testing purposes, set *option_testing* in *config.py* to **True**. This way, files stored in folder *demo_project* are used. Then, execute the following command:
    > ```python3 Balmorel-HPC.py```


## Author
* **[Juan Jerez](mailto:jujmo@dtu.dk)** - *Initial work*


## License
This project is licensed under the GNU General Public License vers. 3 or later - see the [LICENSE.md](LICENSE.md) file for details.