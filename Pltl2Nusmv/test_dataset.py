from utils.parser import PLTL2NuSmv

import os
import subprocess
import argparse
import os.path as path
import time
import datetime

NUSMV_EXEC_PATH = "NuSMV/build/bin/NuSMV"

command = lambda fsmv : f"-int -dynamic -source Pltl2Nusmv/nusmv_commands.txt {fsmv}"

def create_NuSMV_files(folder):
    outputs = []
    for i in os.listdir(folder):
        try:
            p = PLTL2NuSmv(f"{folder}/{i}", os.path.basename(i)[:-4], os.path.basename(folder))
            # print(p._controllable)
            # print(p._notcontrollable)
            try:
                outputs.append((p.formula_str, p.write_nusmv(), p._fname, len(p._controllable), len(p._notcontrollable), len(p._tableaux_vars)))
            except IndexError:
                # print(p._formula)
                print("INDEX ERROR")
                exit()
        except ValueError:
            pass
    return outputs
    
def execute_file(f):
    try:
        out = subprocess.run([NUSMV_EXEC_PATH,"-int", "-dynamic", "-source", "Pltl2Nusmv/nusmv_commands.txt", f], capture_output=True, text=True, check=True)
    except subprocess.SubprocessError:
        return None
    return out

def nano2ms(t):
    return t / (10**6)

import json

def prepare_dataset(f):
    j_file:str = f
    base_name = j_file.split("/")[-1]
    
    with open(j_file, "r") as js:
        j_file = json.load(js)
        
    if not os.path.isdir(f"Pltl2Nusmv/input/{base_name}"):
        os.mkdir(f"Pltl2Nusmv/input/{base_name}")
        if not os.path.isdir(f"Pltl2Nusmv/input/{base_name}/formulas"):
            os.mkdir(f"Pltl2Nusmv/input/{base_name}/formulas")
        if not os.path.isdir(f"Pltl2Nusmv/input/{base_name}/controllables"):
            os.mkdir(f"Pltl2Nusmv/input/{base_name}/controllables")
        
    
    for k, v in j_file.items():
        with open(f"Pltl2Nusmv/input/{base_name}/formulas/{k}.txt", "w") as wf:
            wf.write(f"{v['formula_past']}\n")
            with open(f"Pltl2Nusmv/input/{base_name}/controllables/{k}.txt", "w") as wf2:
                wf2.write(f"{','.join(v['controllable'])}\n")
    
    print(f"Wrote files to 'Pltl2Nusmv/input/{base_name}") 
    return os.path.join("Pltl2Nusmv", "input", base_name)

def main(settings):
    
    #s_time = time.time_ns()
    
    path_t = prepare_dataset(settings.input)
    
    outputs = create_NuSMV_files(f"{path_t}/formulas")
    
    #e_time = time.time_ns()
    
    log_file = f"Pltl2Nusmv/logs/{path.basename(path_t)}_{datetime.datetime.now()}.csv"
    
    with open(log_file, "w") as out:
        out.write("Specification, Controllables, NotControllables, PnfVars, Time, Results\n")
        #out.write(f"Time for creating Symbolic systems {nano2ms(e_time - s_time)} ns \n")
        for output in outputs:
            print("/"*30)
            print(output[1])
            s_time = time.time_ns()
            execution = execute_file(output[1])
            e_time = time.time_ns()
            if execution is not None:
                cout = execution.stdout.split("\n")[15:]
                print(output[0])
                print(cout[-3])
                out.write(f"{path.basename(output[2])[:-4]},{output[3]}, {output[4]}, {output[5]},{nano2ms(e_time - s_time)}, {cout[-3]}\n")
            else:
                print("ERROR")
    # os.remove(log_file)
    print(f"Log saved at {log_file}")

    


if __name__ == "__main__":
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-i",
        "--input",
        default=None,
        required=True,
        type=str,
        help="The json file containing the formulas",
    )
    
    main(settings=argsparser.parse_args())