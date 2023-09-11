import subprocess
import argparse
import os.path as path

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
        self._tableaux_vars = []

        with open(input_file) as f:
            self.formula_str = f.readline()[:-1]
            
        self._formula = parse_pltl(self.formula_str)

        self._fname = f"Pltl2Nusmv/output/{fname}.smv"

        self._tableaux = get_tableaux_lines(self._f_file)
        if self._tableaux == None:
            raise ValueError("Something went wrong for the subproccess handling the creation of the tablueaux")
        index_st = self._tableaux.index("VAR")
        index_define = self._tableaux.index("DEFINE")
        for i in range(index_st+1, index_define):
            var = self._tableaux[i].split()[0]
            self._tableaux_vars.append(var)

        self._atomic_vars = self._extract_atomic_varaibles()
        self._controllable = self._get_random_controllable()
        self._notcontrollable = self._get_notcontrollable()
        self._toplevel = self._get_top_level() 

    def _extract_atomic_varaibles(self):
        """
        extract all atomic variables from the input formula
        """
        queue = [self._formula]
        names = set()
        while len(queue) != 0:
            curr_node = queue.pop()
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

    def _get_notcontrollable(self):
        """
        return a random set of controllable variables extracted randomly from the set of atomic variables
        """
        return [ x for x in self._atomic_vars if x not in self._controllable]

    def _get_top_level(self):
        def_index = self._tableaux.index("DEFINE")
        for i in range(def_index, len(self._tableaux)):
            if "top_level_formula_name" in self._tableaux[i]:
                return self._tableaux[i].split()[0]

    def write_nusmv(self):
        with open(self._fname, "w") as file:
            file.write("MODULE main\n")

            # Boolean variables
            file.write("VAR\n")
            for name in self._atomic_vars:
                file.write(f"\t{name} : boolean;\n")
            
            index_st = self._tableaux.index("VAR")
            # index_init_top_level_formula = self._tableaux.index("INIT")
            for i in range(index_st+1, len(self._tableaux)):
                file.write(f"{self._tableaux[i]}\n")

            file.write("CONTROLLABLES   ")
            for i in range(len(self._controllable) - 1):
                file.write(f"{self._controllable[i]},")
            file.write(f"{self._controllable[-1]};")
            file.write("\n")

            file.write("NOTCONTROLLABLES    ")
            for i in range(len(self._notcontrollable) - 1):
                file.write(f"{self._notcontrollable[i]},")
            file.write(f"{self._notcontrollable[-1]};\n")

            file.write("PNFVARS     ")
            for i in range(len(self._tableaux_vars) - 1):
                file.write(f"{self._tableaux_vars[i]},")
            file.write(f"{self._tableaux_vars[-1]};\n")

            file.write("REALIZABLE  ")
            file.write(f"{self._toplevel};\n")

            

    def __repr__(self):
        return f"{self.formula_str}\n{self._controllable}\n{self._notcontrollable}"

            
            
def main(settings):
    seed(settings.seed)
    fsmv = PLTL2NuSmv(input_file=settings.input, fname=settings.fname)
    # print(fsmv._controllable)
    # print(fsmv._notcontrollable)
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
    main(settings=argsparser.parse_args())