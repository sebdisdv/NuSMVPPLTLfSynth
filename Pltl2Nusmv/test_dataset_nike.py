from argparse import ArgumentParser
import json
import os
import time

NIKE_APP_PATH = "/home/sebdis/PPLTL/Nike/nike/build/apps/nike-app/nike-app"

def nano2ms(t):
    return t / (10**6)

def main(args):
    dataset = args["input"]
    output_file = args["output"]
    
    with open(dataset, "r") as file:
        data = json.load(file)
    
    res = []
    
    for k in data:
        formula = data[k]["formula_future"]
        controllable = data[k]["controllable"]
        uncontrollable = data[k]["uncontrollable"]
        with open("temp_part.txt", "w") as file:
            file.write(f".inputs: {' '.join(uncontrollable)}\n")
            file.write(f".outputs: {' '.join(controllable)}\n")
            
        print("/"*30)
        print(formula)
        print(f"uncontrollable: {uncontrollable}")
        print(f"controllable: {controllable}")
        start = time.time_ns()
        # print(os.popen(f'./nike-app -i "{formula}" --mode bdd --strategy 2 --part "temp_part.txt" ').readlines())
        # print(os.popen(f'./nike-app -i "{formula}" --mode bdd --strategy 2 --part "temp_part.txt" ').read().replace("\n", '').lower())
        realizable = os.popen(f'{NIKE_APP_PATH} -i "{formula}" --mode bdd --strategy 2 --part "temp_part.txt" ').read().replace("\n", '').lower()
        end = time.time_ns()
        print(realizable)
        res.append([k, len(data[k]["atoms"]), realizable, str(nano2ms(end - start)) + "\n"])
    
    
    
    
    with open(f"Pltl2Nusmv/results_nike/{output_file}.csv", "w") as file:
        file.write("formula, n_atoms, result, time\n")
        file.writelines([",".join([str(x) for x in r]) for r in res])
        
    print(f"File saved in 'Pltl2Nusmv/results_nike/{output_file}.csv'")

if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument(
        "-i",
        "--input",
        required=True,
        default=None,
        help="json dataset containing the formulas"
    )
    args.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        required=True,
        help="name of the output file"
    )
    args = args.parse_args()
    main(vars(args))