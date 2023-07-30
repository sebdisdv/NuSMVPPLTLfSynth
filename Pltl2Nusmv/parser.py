import subprocess
import argparse

from pylogics.parsers import parse_pltl
from pylogics.syntax.pltl import Atomic, Since
from pylogics.syntax.base import And, Or, Implies
from random import sample, seed


NUSMV_EXEC_PATH = "NuSMV/build/bin/ltl2smv"

def get_tableaux_lines(input_file):
    tableaux = None
    try:
        tableaux = subprocess.run([NUSMV_EXEC_PATH,"1", input_file], capture_output=True, text=True, check=True)
    except subprocess.SubprocessError:
        return None
    return tableaux.stdout.split("\n")

class PLTL2NuSmv():

    _operand_classes = [Since, Or, And, Implies]

    def __init__(self,input_file:str, fname: str):
        self._f_file = input_file
        with open(input_file) as f:
            self.formula_str = f.readline()[:-1]
            
        self._formula = parse_pltl(self.formula_str)

        self._fname = f"Pltl2Nusmv/output/{fname}.smv"

        self._atomic_vars = self._extract_atomic_varaibles()
        self._controllable = self._get_random_controllable()

    def _extract_atomic_varaibles(self):
        """
        extract all atomic variables from the input formula
        """
        queue = [self._formula]
        names = set()
        while len(queue) != 0:
            curr_node = queue.pop(0)
            curr_node_type = type(curr_node)
            if curr_node_type == Atomic:
                names.add(curr_node.name)
            elif curr_node_type in self._operand_classes:
                for op in curr_node.operands:
                    queue.append(op)
            else:
                # Not, Historically, Once case
                queue.append(curr_node.argument)
        return names
    
    def _get_random_controllable(self):
        """
        return a random set of controllable variables extracted randomly from the set of atomic variables
        """
        return sample(list(self._atomic_vars), k= int(len(self._atomic_vars) // 2))

    def write_nusmv(self):
        tableaux = get_tableaux_lines(self._f_file)
        with open(self._fname, "w") as file:
            file.write("MODULE main\n")

            # Boolean variables
            file.write("VAR\n")
            for name in self._atomic_vars:
                file.write(f"\t{name} : boolean;\n")
            index_st = tableaux.index("VAR")

            for i in range(index_st+1, len(tableaux)):
                file.write(f"{tableaux[i]}\n")

            file.write("CONTROLLABLES\n")
            file.write("\t")
            for var in self._controllable:
                file.write(f"{var} ")
            file.write("\n")

    def __repr__(self):
        return f"{self.formula_str}\n{self._controllable}"

            
            
def main(settings):
    seed(settings.seed)
    fsmv = PLTL2NuSmv(input_file=settings.input, fname=settings.fname)
    fsmv.write_nusmv()

if __name__ == "__main__":

    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-i",
        "--input",
        default=None,
        required=True,
        type=str,
        help="The file containing the PLTL formula",
    )
    argsparser.add_argument(
        "-s",
        "--seed",
        default=23,
        required=False,
        type=int,
        help="The SEED for the random split of controllable variables",
    )
    argsparser.add_argument(
        "-fn",
        "--fname",
        default=None,
        required=True,
        type=str,
        help="The name for the output smv file"
    )
    main(argsparser.parse_args())