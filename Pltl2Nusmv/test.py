from parser import PLTL2NuSmv

import os
import subprocess
import argparse

NUSMV_EXEC_PATH = "NuSMV/build/bin/NuSMV"

command = lambda fsmv : f"-int -dynamic -source Pltl2Nusmv/nusmv_commands.txt {fsmv}"

def create_NuSMV_files(folder):
    for _,_,inputs in os.walk(folder):
        outputs = []
        for i in inputs:
            try:
                p = PLTL2NuSmv(f"{folder}/{i}", os.path.basename(i)[:-4])
                outputs.append((p.formula_str, p.write_nusmv()))
            except ValueError:
                pass
        return outputs
    
def execute_file(f):
    try:
        out = subprocess.run([NUSMV_EXEC_PATH,"-int", "-dynamic", "-source", "Pltl2Nusmv/nusmv_commands.txt", f], capture_output=True, text=True, check=True)
    except subprocess.SubprocessError:
        return None
    return out

def main(settings):
    outputs = create_NuSMV_files(settings.input)
    for output in outputs:
        execution = execute_file(output[1])
        if execution is not None:
            print(output[0], "\n","\n".join(execution.stdout.split("\n")[15:]))
            print("/"*30, "\n")
        
if __name__ == "__main__":
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-i",
        "--input",
        default=None,
        required=True,
        type=str,
        help="The folder containig the formulas",
    )
    
    main(settings=argsparser.parse_args())