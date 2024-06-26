from pandas import read_csv
import pandas
from utils.parser import PLTL2NuSmv
from shutil import rmtree
from dotenv import load_dotenv

import os
import os.path as path
import subprocess
import argparse
import time
import datetime
import json







def create_NuSMV_files(folder):
    outputs = []
    for i in os.listdir(folder):
        try:

            p = PLTL2NuSmv(
                f"{folder}/{i}", os.path.basename(i)[:-4], folder.split("/")[-2]
            )
            # print(p._controllable)
            # print(p._notcontrollable)
            try:
                outputs.append(
                    (
                        p.formula_str,
                        p.write_nusmv_new(),
                        p._fname,
                        len(p._controllable),
                        len(p._notcontrollable),
                        len(p._tableaux_vars),
                    )
                )
            except IndexError:
                # print(p._formula)
                print("INDEX ERROR")
                exit()
        except ValueError:
            pass
    return outputs


def execute_file(nusmv_file):
    try:
        out = subprocess.run(
            [
                os.environ["NUSMV_EXEC_PATH"],
                "-int",
                "-dynamic",
                "-source",
                "Pltl2Nusmv/nusmv_commands.txt",
                nusmv_file,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.SubprocessError:
        return None
    return out


def nano2ms(t):
    return t / (10**6)


def prepare_dataset(f):
    j_file: str = f
    base_name = j_file.split("/")[-1]

    with open(j_file, "r") as js:
        j_file = json.load(js)

    if not path.isdir(path.join("Pltl2Nusmv", "input")):
        os.mkdir(path.join("Pltl2Nusmv", "input"))
    
    if os.path.isdir(f"Pltl2Nusmv/input/{base_name}"):
        rmtree(f"Pltl2Nusmv/input/{base_name}")

    os.mkdir(f"Pltl2Nusmv/input/{base_name}")
    if not os.path.isdir(f"Pltl2Nusmv/input/{base_name}/formulas"):
        os.mkdir(f"Pltl2Nusmv/input/{base_name}/formulas")
    if not os.path.isdir(f"Pltl2Nusmv/input/{base_name}/controllables"):
        os.mkdir(f"Pltl2Nusmv/input/{base_name}/controllables")
    if not os.path.isdir(f"Pltl2Nusmv/input/{base_name}/uncontrollables"):
        os.mkdir(f"Pltl2Nusmv/input/{base_name}/uncontrollables")

    for k, v in j_file.items():
        with open(f"Pltl2Nusmv/input/{base_name}/formulas/{k}.txt", "w") as wf:
            wf.write(f"{v['formula_past']}\n")
            with open(
                f"Pltl2Nusmv/input/{base_name}/controllables/{k}.txt", "w"
            ) as wf2:
                wf2.write(f"{','.join(v['controllable'])}\n")
            with open(
                f"Pltl2Nusmv/input/{base_name}/uncontrollables/{k}.txt", "w"
            ) as wf2:
                wf2.write(f"{','.join(v['uncontrollable'])}\n")

    print(f"Wrote files to 'Pltl2Nusmv/input/{base_name}")
    
    
    
    
    return os.path.join("Pltl2Nusmv", "input", base_name)


def main(settings):

    path_t = prepare_dataset(settings["input"])

    outputs = create_NuSMV_files(f"{path_t}/formulas")

    log_file = f"Pltl2Nusmv/logs/{path.basename(path_t)}_{datetime.datetime.now()}.csv"
    res = {}
    with open(log_file, "w") as out:
        out.write("formula,n_atoms,result,time\n")

        for _, output in enumerate(outputs):
            # print("/" * 30)
            # print(output[1])
            s_time = time.time_ns()
            execution = execute_file(output[1])
            e_time = time.time_ns()
            if execution is not None:
                cout = execution.stdout.split("\n")[15:]
                # print(output[0])
                # print(cout[-3])
                res[path.basename(output[2])[:-4]] = [
                    cout[-3],
                    nano2ms(e_time - s_time),
                ]
                out.write(
                    f"{path.basename(output[2])[:-4]},{output[3] + output[4]},{cout[-3]},{nano2ms(e_time - s_time)}\n"
                )
            else:
                res[path.basename(output[2])[:-4]] = ["Error", nano2ms(e_time - s_time)]
                # print("ERROR")
            # print(f"{i}/1000")

    # os.remove(log_file)
    print(f"Log saved at {log_file}")
    return res


def main_SyftMax(args):

    dataset = args["input"]
    output_file = path.basename(dataset).split(".")[0]

    with open(dataset, "r") as file:
        data = json.load(file)

    res = []

    for k in data:
        formula: str = data[k]["formula_future"]
        formula = formula.replace("X", "X[!]")
        controllable = data[k]["controllable"]
        uncontrollable = data[k]["uncontrollable"]
        with open("temp_part.txt", "w") as file:
            file.write(f".inputs: {' '.join(uncontrollable)}\n")
            file.write(f".outputs: {' '.join(controllable)}\n")
        with open("temp_formula.txt", "w") as file:
            file.write(formula + "\n")

        # print("/" * 30)
        # print(k)
        # print(formula)
        # print(f"uncontrollable: {uncontrollable}")
        # print(f"controllable: {controllable}")
        start = time.time_ns()
        realizable = os.popen(
            f'{os.environ["SYFTMAX_EXEC_PATH"]} -f "temp_formula.txt"  -p "temp_part.txt" '
        ).readlines()

        realizable = realizable[1].split()[-1].lower()
        end = time.time_ns()


        res.append(
            [k, len(data[k]["atoms"]), realizable, str(nano2ms(end - start)) + "\n"]
        )

    with open(f"Pltl2Nusmv/results_SyftMax/{output_file}.csv", "w") as file:
        file.write("formula,n_atoms,result,time\n")
        file.writelines([",".join([str(x) for x in r]) for r in res])

    print(f"File saved in 'Pltl2Nusmv/results_SyftMax/{output_file}.csv'")

    return {formula: [realizable, float(t)] for formula, _, realizable, t in res}


def main_Synthetico(args):
    dataset = args["input"]
    output_file = path.basename(dataset).split(".")[0]

    with open(dataset, "r") as file:
        data = json.load(file)

    res = []
    for k in data:
        formula: str = f'F({data[k]["formula_past"]})'
        # controllable = data[k]["controllable"]
        uncontrollable = data[k]["uncontrollable"]
        # print("/" * 30)
        # print(k)
        # print(formula)
        # print(f"uncontrollable: {uncontrollable}")
        # print(f"controllable: {controllable}")
        start = time.time_ns()

        try:
            # sub_res = subprocess.run(args=[SYNTHETICO_EXEC_PATH, 'bdd', f"'{formula}'", " ".join(uncontrollable)], capture_output=True, timeout=20, check=True, text=True, shell=True)
            sub_res = subprocess.run(
                f'{os.environ["SYNTHETICO_EXEC_PATH"]} bdd "{formula}" {" ".join(uncontrollable)}',
                capture_output=True,
                timeout=1,
                check=True,
                text=True,
                shell=True,
            )
            realizable = sub_res.stdout.replace("\n", "").lower()
        except subprocess.TimeoutExpired:
            realizable = "timeout"

        end = time.time_ns()
        res.append(
            [k, len(data[k]["atoms"]), realizable, str(nano2ms(end - start)) + "\n"]
        )

    with open(f"Pltl2Nusmv/results_synthetico/{output_file}.csv", "w") as file:
        file.write("formula,n_atoms,result,time\n")
        file.writelines([",".join([str(x) for x in r]) for r in res])

    print(f"File saved in 'Pltl2Nusmv/results_synthetico/{output_file}.csv'")

    return {formula: [realizable, float(t)] for formula, _, realizable, t in res}


def main_nike(args):

    dataset = args["input"]
    output_file = path.basename(dataset).split(".")[0]

    with open(dataset, "r") as file:
        data = json.load(file)

    res = []

    for k in data:
        formula: str = data[k]["formula_future"]
        formula = formula.replace("X", "X[!]")  
        controllable = data[k]["controllable"]
        uncontrollable = data[k]["uncontrollable"]
        with open("temp_part.txt", "w") as file:
            file.write(f".inputs: {' '.join(uncontrollable)}\n")
            file.write(f".outputs: {' '.join(controllable)}\n")

        # print("/" * 30)
        # print(k)
        # print(formula)
        # print(f"uncontrollable: {uncontrollable}")
        # print(f"controllable: {controllable}")
        start = time.time_ns()
        realizable = (
            os.popen(
                f'{os.environ["NIKE_APP_PATH"]} -i "{formula}" --no-empty --mode bdd --strategy 2 --part "temp_part.txt" '
            )
            .read()
            .replace("\n", "")
            .lower()
        )
        end = time.time_ns()
        # print(realizable)
        res.append(
            [k, len(data[k]["atoms"]), realizable, str(nano2ms(end - start)) + "\n"]
        )

    with open(f"Pltl2Nusmv/results_nike/{output_file}.csv", "w") as file:
        file.write("formula,n_atoms,result,time\n")
        file.writelines([",".join([str(x) for x in r]) for r in res])

    print(f"File saved in 'Pltl2Nusmv/results_nike/{output_file}.csv'")

    return {formula: [realizable, float(t)] for formula, _, realizable, t in res}




def check_res_dir():
    
    if not path.isdir(path.join("Pltl2Nusmv", "logs")):
        os.mkdir(path.join("Pltl2Nusmv", "logs"))
    else:
        print("Log folder for nusmv exists")
    
    
    if not path.isdir(path.join("Pltl2Nusmv", "results_nike")):
        os.mkdir(path.join("Pltl2Nusmv", "results_nike"))
    else:
        print("Log folder for nike exists")
        
    if not path.isdir(path.join("Pltl2Nusmv", "results_synthetico")):
        os.mkdir(path.join("Pltl2Nusmv", "results_synthetico"))
    else:
        print("Log folder for synthetico exists")
        
    if not path.isdir(path.join("Pltl2Nusmv", "results_SyftMax")):
        os.mkdir(path.join("Pltl2Nusmv", "results_SyftMax"))
    else:
        print("Log folder for Syftmax exists")
    

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

    argsparser.add_argument(
        "-k",
        "--nike",
        action='store_true',
        help="enable nike",
    )
    argsparser.add_argument(
        "-m",
        "--syftmax",
        action='store_true',
        help="enable syftmax",
    )
    argsparser.add_argument(
        "-s",
        "--synthetico",
        action='store_true',
        help="enable synthetico",
    )
    
    
    settings = vars(argsparser.parse_args())
    
    load_dotenv()
    check_res_dir()
    res_nusmv = main(settings)
    res_nike = main_nike(settings) if settings["nike"] else None
    res_syftmax = main_SyftMax(settings) if settings["syftmax"] else None
    res_synthetico = main_Synthetico(settings) if settings["synthetico"] else None
    
    print(
        "formula".ljust(10),
        "nusmv".ljust(20),
        "synthetico".ljust(20) if res_synthetico is not None else "",
        "syftmax".ljust(20) if res_syftmax is not None else "",
        "nike".ljust(20) if res_nike is not None else "",
    )
    print("\n")

    for k in sorted(list(res_nusmv.keys())):
        print(
            k.ljust(10),
            res_nusmv[k][0].ljust(20),
            res_synthetico[k][0].ljust(20) if res_synthetico is not None else "",
            res_syftmax[k][0].ljust(20) if res_syftmax is not None else "",
            res_nike[k][0].ljust(20) if res_nike is not None else "",
        )
