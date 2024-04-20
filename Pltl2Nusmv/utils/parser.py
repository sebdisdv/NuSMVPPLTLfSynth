import subprocess
import argparse
import os.path as path
import os

from pylogics.parsers import parse_pltl
from pylogics.syntax.pltl import Atomic, Since
from pylogics.syntax.base import And, Or, Implies, Equivalence, TrueFormula, FalseFormula
from random import sample, seed
from typing import List

from re import search

LTL2SMV_EXEC_PATH = "NuSMV/build/bin/ltl2smv"

def get_tableaux_lines(input_file):
    tableaux = None
    try:
        tableaux = subprocess.run([LTL2SMV_EXEC_PATH,"1", input_file], capture_output=True, text=True, check=True)
    except subprocess.SubprocessError:
        return None
    return tableaux.stdout.split("\n")

class PLTL2NuSmv():

    _operand_classes = [Since, Or, And, Implies, Equivalence]

    def __init__(self,input_file:str, fname: str, problem_name:str = None):
        self._f_file = input_file
        self._tableaux_vars = []

       
        
        with open(input_file) as f:
            self.formula_str = f.readline()[:-1]
        with open(input_file.replace("formulas","controllables")) as f:
            self._controllable = f.readline()[:-1].split(",")
        with open(input_file.replace("formulas", "uncontrollables")) as f:
            self._notcontrollable = f.readline()[:-1].split(",")
        
        pattern_vars = r"\s*([a-zA-z0-9]*)\s*:\s*boolean.*;"
        pattern_trans = r"\s*([a-zA-z0-9]*)\s*(.)*\s*next(.*)"
        pattern_define = r"\s*([a-zA-z0-9]*)\s*:=\s*(.*);"
        
        self._atomic_vars = self._controllable + self._notcontrollable        
        # print(input_file)
        # print(self._controllable)
        # exit()
        # print(self._controllable)
        # print(self.formula_str)
        
        # self._formula = parse_pltl(self.formula_str)
        
        # print(self._formula)
        
        if not path.isdir(f"Pltl2Nusmv/output/{problem_name}"):
            os.mkdir(f"Pltl2Nusmv/output/{problem_name}")
        
        self._fname = f"Pltl2Nusmv/output/{problem_name}/{fname}.smv"
        # self._fname = f"Pltl2Nusmv/output/{fname}.smv"
         
        self._tableaux = get_tableaux_lines(self._f_file)
        
        if self._tableaux == None:
            print("VALUERROR")
            raise ValueError("Something went wrong for the subproccess handling the creation of the tablueaux")
        
        # index_st = self._tableaux.index("VAR")
        
        # index_define = self._tableaux.index("DEFINE")
        
        self.define_lines = []
        self.vars_lines = []
        self.trans_lines = []
        
        for line in self._tableaux:
            pat = search(pattern_vars, line)
            if pat is not None:
                self.vars_lines.append(pat[0])
                if "goal" not in pat.group(0):
                    self._tableaux_vars.append(pat.group(0).split()[0])
            pat = search(pattern_define, line)
            if pat is not None:
                self.define_lines.append(pat[0])
                
            pat = search(pattern_trans, line)
            if pat is not None:
                self.trans_lines.append(pat[0])
                
            
        
        #for i in range(index_st+1, index_define):
        #    var = self._tableaux[i].split()[0]
        #    self._tableaux_vars.append(var)

        # self._atomic_vars = self._extract_atomic_variables()
        # self._controllable = controllables if controllables is not None else self._get_random_controllable()
        # self._notcontrollable = self._get_notcontrollable()
        # self._toplevel = self._get_top_level() 

    
    def _extract_atomic_variables(self):
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
            # elif curr_node_type == FalseFormula: #TODO check this part
            #     names.add("False")
            # elif curr_node_type == TrueFormula:
            #     names.add("True")
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
            if "top_level_formula_name :=" in self._tableaux[i]:
                return self._tableaux[i].split()[0]

    def write_nusmv_new(self):
        with open(self._fname, "w") as file:
            file.write("MODULE main\n")
            
            file.write("VAR\n")
            for l in self.vars_lines:
                file.write(f"{l}\n")
            for v in self._atomic_vars:
                file.write(f"\t{v} : boolean;\n")
            
            file.write("DEFINE\n")
            for l in self.define_lines:
                file.write(f"{l}\n")
            
            for l in self._tableaux_vars:
                file.write("INIT\n")
                file.write(f"\t{l} = FALSE\n")
            file.write("INIT\n")
            file.write(f"\t__goal__ = FALSE\n")
            
            for l in self.trans_lines:
                file.write("TRANS\n")
                file.write(f"{l}\n")
            
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
            file.write(f"{self._tableaux_vars[-1]},")
            file.write(f"__goal__;\n")
                        
            file.write("REALIZABLE  ")
            file.write("__goal__;\n")
            
            
        
        return self._fname
            

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

        return self._fname
            

    def __repr__(self):
        return f"{self.formula_str}\n{self._controllable}\n{self._notcontrollable}"

            
            
def main(settings):
    seed(settings.seed)
    fsmv = PLTL2NuSmv(input_file=settings.input, fname=settings.fname)
    print(fsmv._controllable)
    print(fsmv._notcontrollable)
    print(fsmv.write_nusmv_new())

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