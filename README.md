# mpc-add-border

Add a 1/8th inch border to a Magic the Gathering proxy for printing.

## Requirements

Python 3

<br>

## Installing dependancies

### Create a python virtual environment in your desired directory

Ref: https://docs.python.org/3/library/venv.html#creating-virtual-environments

```
python3 -m venv .venv
```

### Enter the virtual environment

This part is OS dependant. To see the full list of commands to enter the virtual environment based on your operating system, see https://docs.python.org/3/library/venv.html#how-venvs-work. For most users, it will be one of these:

Linux/MacOS
```
source .venv/bin/activate
```

Windows (cmd)
```
.venv\Scripts\activate.bat
```

Windows (Powershell)
```
.venv\Scripts\Activate.ps1
```

### Install the dependancies listed in `requirements.txt` with `pip`

```
pip install -r requirements.txt
```
<br>

## Run the script

If you made a folder called `input` in the same directory you cloned this repo and add all your proxy images to it:

```
python3 mpc-add-border.py input
```

All the edited images will be saved to a folder named `output` in the working directory.

<br>

## Script Options

```
usage: mpc-add-border.py [-h] [-o OUTPUT] [-r] [-s SCALE] inputPath

Adds a black 1/8 inch bleed edge around a MTG proxy and converts to jpg

positional arguments:
  inputPath             The path to the input directory containing Magic card images.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The output directory. Defaults to <currentPath>/output
  -r, --recursive       Include all image files in subdirectories of <inputPath>
  -s SCALE, --scale SCALE
                        Scale of final image. Percentage as a decimal. 1=same scale as original. Default=1.0
```
