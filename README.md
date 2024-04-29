# Realizability check for pure Past Linear Temporal Logic on finite traces


## Setup Environment

### Python libraries

The python libraries necessary to run the main script can be installed in a virtual environment with the following command

`pip install -r requirements.txt`

### Other tools for comparison

The following three tools needs to be installed on your machine along with their dependancies

- [Synthetico](https://github.com/Shufang-Zhu/synthetico)
- [SyftMax](https://github.com/Shufang-Zhu/SyftMax)
- [Nike](https://github.com/marcofavorito/nike)

### Build NuSMV

For building NuSMV run the following commands 
```
cd NuSMV
mkdir build && cd build
cmake ..
make
```

### Create .env file

Once every tool is properly installed you need to create an .env file with the following five variables
``` 
NUSMV_EXEC_PATH = "<path_to>/NuSMV/build/bin/NuSMV"
NIKE_APP_PATH = "<path_to>/Nike/nike/build/apps/nike-app/nike-app"
SYFTMAX_EXEC_PATH = "<path_to>/SyftMax/build/bin/Syftmax"
SYNTHETICO_EXEC_PATH = "<path_to>/synthetico/build/synth"
LTL2SMV_EXEC_PATH = "<path_to>/NuSMV/build/bin/ltl2smv"
```

### Run the experiments

`python3 Pltl2Nusmv/test_dataset.py [-h] -i INPUT [-k] [-m] [-s]`
```
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT The path to the json file containing the formulas
  -k, --nike            enable nike
  -m, --syftmax         enable syftmax
  -s, --synthetico      enable synthetico
```