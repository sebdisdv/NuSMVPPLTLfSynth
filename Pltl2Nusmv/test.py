from parser import PLTL2NuSmv

import os
import subprocess


NUSMV_EXEC_PATH = "NuSMV/build/bin/NuSMV"

command = lambda fsmv : f"-int -dynamic -source Pltl2Nusmv/nusmv_commands.txt {fsmv}"

def create_NuSMV_files():
    for _,_,inputs in os.walk("Pltl2Nusmv/input_test"):
        outputs = []
        for i in inputs:
            try:
                p = PLTL2NuSmv(f"Pltl2Nusmv/input_test/{i}", os.path.basename(i)[:-4])
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

def main():
    outputs = create_NuSMV_files()
    for output in outputs:
        execution = execute_file(output[1])
        if execution is not None:
            print(output[0], "\n","\n".join(execution.stdout.split("\n")[15:]))
            print("/"*30, "\n")
        
if __name__ == "__main__":
    main()