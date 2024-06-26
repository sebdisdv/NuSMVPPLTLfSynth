
import json
import random
import os


from typing import List
from argparse import ArgumentParser



class PLTL:
    @staticmethod
    def atom(p: str) -> str:
        return p

    @staticmethod
    def neg(p: str) -> str:
        return f"! {p}"

    @staticmethod
    def yesterday(p: str) -> str:
        return f"(Y {p})"

    @staticmethod
    def existence(p: str) -> str:
        return f"(O {p})"

    @staticmethod
    def since(p1: str, p2: str) -> str:
        return f"({p1} S {p2})"

    @staticmethod
    def historically(p: str) -> str:
        return f"(H {p})"

    @staticmethod
    def land(p1: str, p2: str) -> str:
        return f"({p1} & {p2})"

    @staticmethod
    def lor(p1: str, p2: str) -> str:
        return f"({p1} | {p2})"

    @staticmethod
    def implies(p1: str, p2: str) -> str:
        return f"({p1} -> {p2})"

    @staticmethod
    def seq(p1: str, formula: str) -> str:
        return f"(O ({p1} & Y({formula})))"

    @staticmethod
    def persistence(p: str) -> str:
        return f"H (O ({p}))"

    # up to here

    @staticmethod
    def abscence(p: str) -> str:
        return f"!O({p})"

    @staticmethod
    def choice(p1: str, p2: str) -> str:
        return f"O({p1}) | O({p2})"

    @staticmethod
    def exclusive_choice(p1: str, p2: str) -> str:
        return f"(O({p1}) | O({p2})) &  !(O({p1}) | O({p2}))"

    @staticmethod
    def responded_existence(p1: str, p2: str) -> str:
        return f"O({p1}) -> O({p2})"

    @staticmethod
    def co_existence(p1: str, p2: str) -> str:
        return f"H(!({p1})) <-> H(!({p2}))"

    @staticmethod
    def response(p1: str, p2: str) -> str:
        return f"(!({p1}) S ({p2})) | H (! ({p1}))"

    @staticmethod
    def precedence(p1: str, p2: str) -> str:
        return f"H(({p2}) -> O({p1}))"

    @staticmethod
    def chain_response(p1: str, p2: str) -> str:
        return f"H(Y({p1}) -> ({p2})) & !({p1})"

    @staticmethod
    def chain_precedence(p1: str, p2: str) -> str:
        return f"H(({p2}) -> Y({p1}))"

    @staticmethod
    def chain_succession(p1: str, p2: str) -> str:
        return f"(H(Y({p1}) -> ({p2})) & !({p1})) & H(Y(!({p1})) -> !({p2}))"

    @staticmethod
    def not_co_existence(p1: str, p2: str) -> str:
        return f"O({p1}) -> !O({p2})"

    @staticmethod
    def not_succession(p1: str, p2: str) -> str:
        return f"H(({p2}) -> !O({p1}))"

    @staticmethod
    def not_chain_succession(p1: str, p2: str) -> str:
        return f"H(({p2}) -> !Y({p1}))"

    @staticmethod
    def get_op_dict() -> dict:
        return {
            "unary": [
                PLTL.yesterday,
                PLTL.existence,
                PLTL.historically,
                PLTL.atom,
                PLTL.neg,
                PLTL.persistence,
                PLTL.abscence,
            ],
            "binary": [
                PLTL.land,
                PLTL.lor,
                PLTL.implies,
                PLTL.seq,
                PLTL.since,
                PLTL.choice,
                PLTL.exclusive_choice,
                PLTL.co_existence,
                PLTL.response,
                PLTL.chain_response,
                PLTL.chain_precedence,
                PLTL.chain_succession,
                PLTL.not_co_existence,
                PLTL.not_chain_succession,
                PLTL.not_succession,
            ],
        }


class PLTL_pattern:

    @staticmethod
    def existence(p: str) -> str:
        return f"(O {p})"

    @staticmethod
    def abscence(p: str) -> str:
        return f"!(O({p}))"

    @staticmethod
    def choice(p1: str, p2: str) -> str:
        return f"O({p1}) | O({p2})"

    @staticmethod
    def exclusive_choice(p1: str, p2: str) -> str:
        return f"(O({p1}) | O({p2})) &  !(O({p1}) & O({p2}))"

    @staticmethod
    def co_existence(p1: str, p2: str) -> str:
        return f"H(!({p1})) <-> H(!({p2}))"

    @staticmethod
    def responded_existence(p1: str, p2: str) -> str:
        return f"O({p1}) -> O({p2})"

    @staticmethod
    def response(p1: str, p2: str) -> str:
        return f"(!({p1}) S ({p2})) | H (!({p1}))"

    @staticmethod
    def precedence(p1: str, p2: str) -> str:
        return f"H(({p2}) -> O({p1}))"

    @staticmethod
    def chain_response(p1: str, p2: str) -> str:
        return f"H(Y({p1}) -> ({p2})) & !({p1})"

    @staticmethod
    def chain_precedence(p1: str, p2: str) -> str:
        return f"H(({p2}) -> Y({p1}))"

    @staticmethod
    def chain_succession(p1: str, p2: str) -> str:
        return f"(H(Y({p1}) -> ({p2})) & !({p1})) & H(Y(!({p1})) -> !({p2}))"

    @staticmethod
    def not_co_existence(p1: str, p2: str) -> str:
        return f"O({p1}) -> !(O({p2}))"

    @staticmethod
    def not_succession(p1: str, p2: str) -> str:
        return f"H(({p2}) -> !(O({p1})))"

    @staticmethod
    def not_chain_succession(p1: str, p2: str) -> str:
        return f"H(({p2}) -> !(Y({p1})))"

    @staticmethod
    def get_op_dict() -> dict:
        return {
            "unary": [PLTL_pattern.existence, PLTL_pattern.abscence],
            "binary": [
                PLTL_pattern.choice,
                # PLTL_pattern.exclusive_choice,
                PLTL_pattern.co_existence,
                PLTL_pattern.responded_existence,
                PLTL_pattern.response,
                PLTL_pattern.precedence,
                PLTL_pattern.chain_response,
                # PLTL_pattern.chain_precedence,
                PLTL_pattern.chain_succession,
                PLTL_pattern.not_co_existence,
                PLTL_pattern.not_succession,
                PLTL_pattern.not_chain_succession,
            ],
        }


class LTLf_pattern:

    @staticmethod
    def existence(p: str) -> str:
        return f"(F {p})"

    @staticmethod
    def abscence(p: str) -> str:
        return f"!(F({p}))"

    @staticmethod
    def choice(p1: str, p2: str) -> str:
        return f"F({p1}) | F({p2})"

    @staticmethod
    def exclusive_choice(p1: str, p2: str) -> str:
        return f"(F({p1}) | F({p2})) &  !(F({p1}) & F({p2}))"

    @staticmethod
    def co_existence(p1: str, p2: str) -> str:
        return f"F({p1}) <-> F({p2})"

    @staticmethod
    def responded_existence(p1: str, p2: str) -> str:
        return f"F({p1}) -> F({p2})"

    @staticmethod
    def response(p1: str, p2: str) -> str:
        return f"G(({p1}) -> F({p2}))"

    @staticmethod
    def precedence(p1: str, p2: str) -> str:
        return f"(!({p2}) U ({p1})) | G(!({p2}))"

    @staticmethod
    def chain_response(p1: str, p2: str) -> str:
        return f"G(({p1}) -> X({p2}))"

    @staticmethod
    def chain_precedence(p1: str, p2: str) -> str:
        return f"G(X({p2}) -> ({p1})) & !({p2})"

    @staticmethod
    def chain_succession(p1: str, p2: str) -> str:
        return f"G(({p1}) <-> X({p2}))"

    @staticmethod
    def not_co_existence(p1: str, p2: str) -> str:
        return f"F({p1}) -> !(F({p2}))"

    @staticmethod
    def not_succession(p1: str, p2: str) -> str:
        return f"G(({p1}) -> !(F({p2})))"

    @staticmethod
    def not_chain_succession(p1: str, p2: str) -> str:
        return f"G(({p1}) -> !(X({p2})))"

    @staticmethod
    def get_op_dict() -> dict:
        return {
            "unary": [LTLf_pattern.existence, LTLf_pattern.abscence],
            "binary": [
                LTLf_pattern.choice,
                # LTLf_pattern.exclusive_choice,
                LTLf_pattern.co_existence,
                LTLf_pattern.responded_existence,
                LTLf_pattern.response,
                LTLf_pattern.precedence,
                LTLf_pattern.chain_response,
                # LTLf_pattern.chain_precedence,
                LTLf_pattern.chain_succession,
                LTLf_pattern.not_co_existence,
                LTLf_pattern.not_succession,
                LTLf_pattern.not_chain_succession,
            ],
        }


mapping = {
    PLTL_pattern.existence: LTLf_pattern.existence,
    PLTL_pattern.abscence: LTLf_pattern.abscence,
    PLTL_pattern.choice: LTLf_pattern.choice,
    # PLTL_pattern.exclusive_choice: LTLf_pattern.exclusive_choice,
    PLTL_pattern.co_existence: LTLf_pattern.co_existence,
    PLTL_pattern.responded_existence: LTLf_pattern.responded_existence,
    PLTL_pattern.response: LTLf_pattern.response,
    PLTL_pattern.precedence: LTLf_pattern.precedence,
    PLTL_pattern.chain_response: LTLf_pattern.chain_response,
    # PLTL_pattern.chain_precedence: LTLf_pattern.chain_precedence,
    PLTL_pattern.chain_succession: LTLf_pattern.chain_succession,
    PLTL_pattern.not_co_existence: LTLf_pattern.not_co_existence,
    PLTL_pattern.not_succession: LTLf_pattern.not_succession,
    PLTL_pattern.not_chain_succession: LTLf_pattern.not_chain_succession,
}


from pylogics.parsers import parse_pltl
from pylogics.syntax.pltl import Atomic, Since
from pylogics.syntax.base import (
    And,
    Or,
    Implies,
    Equivalence,
    TrueFormula,
    FalseFormula,
)


def extract_atomic_varaibles(formula):
    """
    extract all atomic variables from the input formula
    """
    operand_classes = [Since, Or, And, Implies, Equivalence]
    queue = [parse_pltl(formula)]
    names = set()
    while len(queue) != 0:
        curr_node = queue.pop()
        curr_node_type = type(curr_node)
        if curr_node_type == Atomic:
            names.add(curr_node.name)
        elif curr_node_type in operand_classes:
            for op in curr_node.operands:
                queue.append(op)
        elif curr_node_type == FalseFormula:  
            names.add("False")
        elif curr_node_type == TrueFormula:
            names.add("True")
        else:
            # Not, Historically, Once case
            queue.append(curr_node.argument)
    return names


def get_atoms_list(n_atoms: int) -> List[str]:
    return [f"p{i}" for i in range(n_atoms)]


def create_formula(depth: int) -> str:
    
    atoms = get_atoms_list(depth*2)

    unary_past, binary_past = PLTL_pattern.get_op_dict().values()
    # unary_future, binary_future = LTLf_pattern.get_op_dict().values()

    methods_type = [
        2 if x > 0.2 else 1 for x in [random.random() for _ in range(depth)]
    ]

    methods_past = []
    methods_future = []

    for i in range(len(methods_type)):
        if i == 0:    
            methods_type[i] = 2
       
        methods_past.append(
                random.choice(unary_past if methods_type[i] == 1 else binary_past)
            )
        methods_future.append(mapping[methods_past[i]])
            
        # print(methods_past[i], methods_future[i])

    # from pprint import pprint as print
    #
    # print(methods_type)
    # print(methods_past)
    # print(methods_future)
    # methods_type = [2 for _ in range(depth)]
    # methods_past = [PLTL_pattern.response for _ in range(depth)]
    # methods_future = [LTLf_pattern.response for _ in range(depth)]

    atoms_used = set()

    for i in range(depth):
        if i == 0:
            if methods_type[i] == 1:
                p = random.choice(atoms)
                formula_past = methods_past[i](p)
                formula_future = methods_future[i](p)
                atoms_used.add(p)
            else:
                p1, p2 = random.sample(atoms, 2)
                formula_past = methods_past[i](p1, p2)
                formula_future = methods_future[i](p1, p2)
                atoms_used.add(p1)
                atoms_used.add(p2)

        else:
            if methods_type[i] == 1:
                formula_past = methods_past[i](formula_past)
                formula_future = methods_future[i](formula_future)
            else:
                p = random.choice(atoms)

                if random.random() < 0.5:
                    formula_past = methods_past[i](p, formula_past)
                    formula_future = methods_future[i](p, formula_future)
                else:
                    formula_past = methods_past[i](formula_past, p)
                    formula_future = methods_future[i](formula_future, p)

                atoms_used.add(p)

    #return formula_past, f"F({formula_future})", atoms_used
    return formula_past, formula_future, atoms_used

def create_formula_2(depth: int, rep = 2) -> str:
    
    atoms = lambda x : f"p{x}"

    unary_past, binary_past = PLTL_pattern.get_op_dict().values()
    # unary_future, binary_future = LTLf_pattern.get_op_dict().values()

    methods_type = [
        2 if x > 0.2 else 1 for x in [random.random() for _ in range(depth * rep)]
    ]

    methods_past = []
    methods_future = []

    for i in range(len(methods_type)):
        if i == 0:    
            methods_type[i] = 2
       
        methods_past.append(
                random.choice(unary_past if methods_type[i] == 1 else binary_past)
            )
        methods_future.append(mapping[methods_past[i]])
            
        # print(methods_past[i], methods_future[i])

    # from pprint import pprint as print
    #
    # print(methods_type)
    # print(methods_past)
    # print(methods_future)
    # methods_type = [2 for _ in range(depth)]
    # methods_past = [PLTL_pattern.response for _ in range(depth)]
    # methods_future = [LTLf_pattern.response for _ in range(depth)]

    atoms_used = set()
    c = -1
    atom_count = 0
    fs = [[None,None] for _ in range(rep)]
    for i in range(depth * rep):
        
        
        if i // rep == 0:
            c+=1
            if methods_type[i] == 1:
                p = atoms(atom_count)
                atom_count += 1
                fs[c][0] = methods_past[i](p)
                fs[c][1] = methods_future[i](p)
                atoms_used.add(p)
            else:
                p1, p2 = atoms(atom_count), atoms(atom_count+1)
                atom_count +=2
                fs[c][0] = methods_past[i](p1, p2)
                fs[c][1] = methods_future[i](p1, p2)
                atoms_used.add(p1)
                atoms_used.add(p2)

        else:
            if methods_type[i] == 1:
                fs[c][0] = methods_past[i](fs[c][0])
                fs[c][1] = methods_future[i](fs[c][1])
            else:
                p = atoms(atom_count)
                atom_count += 1

                if random.random() < 0.5:
                    fs[c][0] = methods_past[i](p, fs[c][0])
                    fs[c][1] = methods_future[i](p, fs[c][1])
                else:
                    fs[c][0] = methods_past[i](fs[c][0], p)
                    fs[c][1] = methods_future[i](fs[c][1], p)

                atoms_used.add(p)
                
    f_past = fs[0][0]
    f_future = fs[0][1]
    
    for i in range(1,rep):
        f_past = f"{f_past} | {fs[i][0]}" if random.random() > 0.5 else f"{f_past} & {fs[i][0]}"
        f_future = f"{f_future} | {fs[i][1]}" if random.random() > 0.5 else f"{f_future} & {fs[i][1]}"       
    #return formula_past, f"F({formula_future})", atoms_used
    return f_past, f_future, atoms_used

def check_sat(formula):
    with open("temp_formula.txt", "w") as f:
        f.write(formula)
        # f.write("\n")
    return os.popen(f"black solve --finite temp_formula.txt").read()[:-1] == "SAT"

def check_validity(formula):
    with open("temp_formula.txt", "w") as f:
        f.write(formula)
        # f.write("\n")
    return os.popen(f"black solve  --finite  temp_formula.txt").read()[:-1] == "UNSAT"

def test():
    unary, binary = PLTL_pattern.get_op_dict().values()
    f_past, f_future, method = [],[],[]
    for x in unary:
        f_past.append(f"F(({x('a')}) & wX(False))")
        f_future.append(f"{mapping[x]('a')}")
        method.append(x)
        
    for x in binary:
        f_past.append(f"F(({x('a','b')}) & wX(False))")
        f_future.append(f"{mapping[x]('a', 'b')}")
        method.append(x)
    
    for i in range(len(f_past)):
        print("/"*30, "\n")
        print("Property := ", str(method[i]).split()[1].split(".")[1])
        print(f"PAST = {f_past[i]}")
        print(f"FUTURE = {f_future[i]}")
        print(f"{f_past[i]} <-> ({f_future[i]})")
        
        print(f"past_sat = {check_sat(f_past[i])}")
        print(f"future_sat = {check_sat(f_future[i])}")
        print(check_validity(f"!(({f_past[i]}) <-> ({f_future[i]}))"))
        print("\n")

def write_to_json(formulas, filename):
    res = {}
    for i, (formula_past, formula_future, atoms) in enumerate(formulas):
        atoms = list(atoms)
        random.shuffle(atoms)
        contr, uncontr = atoms[: int(len(atoms) / 2)], atoms[int(len(atoms) / 2):]
        res[f"f{i}"] = {
            "formula_past": formula_past,
            "formula_future": formula_future,
            "atoms": atoms,
            "controllable" : contr,
            "uncontrollable" : uncontr
        }

    with open(os.path.join(os.getcwd(), "Pltl2Nusmv", "json_datasets", f"{filename}.json"), "w") as ofile:
        ofile.write(json.dumps(res))
        print(f"File {filename}.json saved in {os.path.join(os.getcwd(), 'Pltl2Nusmv', 'json_datasets')}")
   


def all_check(formula_past, formula_future):
    return check_sat(formula_past) and check_sat(formula_future) and check_validity(f"!( (F(({formula_past}) & wX(False))) <-> ({formula_future}) )")


CONST = set(["True", "False"])

def get_formula(depth):
    formula_past, formula_future, n_atoms = create_formula(
            depth
    )
    if all_check(formula_past, formula_future):        
        if not bool(CONST & extract_atomic_varaibles(formula_past)):
            return (formula_past, formula_future, n_atoms)
            # print(f"{n_formulas + 1} / {args['number']}")
            # n_formulas += 1
    return None

def main(args):

    
    
    # sat formulas counter
    generated_formulas = []
    n_formulas = 0

    # set seed
    random.seed(args["seed"])
    
    # const = set(["True", "False"])

    while n_formulas < args["number"]:
        
        
        
        #with concurrent.futures.ProcessPoolExecutor() as executor:
        #    procs = [executor.submit(get_formula, args['depth']) for _ in range(6)]
        #    
        #    res = [p.result() for p in procs]
        #    
        #for r in res:
        #    if r is not None:
        #        generated_formulas.append(r)
        #        n_formulas += 1
        #        print(f"{n_formulas + 1} / {args['number']}")
        
        
        if args["repeat"] == 1:
            formula_past, formula_future, n_atoms = create_formula(
                args["depth"]
            )
        else:
            formula_past, formula_future, n_atoms = create_formula_2(
                args["depth"], args["repeat"]
            )
        
        if all_check(formula_past, formula_future):        
            if not bool(CONST & extract_atomic_varaibles(formula_past)):
                generated_formulas.append((formula_past, formula_future, n_atoms))
                
                print(f"{n_formulas + 1} / {args['number']}")
                n_formulas += 1

    write_to_json(generated_formulas, args["filename"])


if __name__ == "__main__":
    
    # test()
    # exit()
  

    args = ArgumentParser()
    args.add_argument(
        "-s",
        "--seed",
        default=23,
        required=False,
        type=int,
        help="The SEED for the random number generator",
    )
    args.add_argument(
        "-n",
        "--number",
        default=None,
        required=True,
        type=int,
        help="The Number of formula to generate",
    )
    args.add_argument(
        "-d",
        "--depth",
        default=None,
        required=True,
        type=int,
        help="The temporal depth of the generated formulas",
    )
    
    args.add_argument(
        "-f",
        "--filename",
        default=None,
        required=True,
        type=str,
        help="Name of the output json file",
    )

    args.add_argument(
        "-r",
        "--repeat",
        default=1,
        required=False,
        type=int,
        help="raise this value to increase number of atoms"
    )
    
    main(vars(args.parse_args()))
