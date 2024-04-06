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
        return f"!O({p})"

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
            "unary": [PLTL_pattern.existence, PLTL_pattern.abscence],
            "binary": [
                PLTL_pattern.choice,
                PLTL_pattern.exclusive_choice,
                PLTL_pattern.co_existence,
                PLTL_pattern.responded_existence,
                PLTL_pattern.response,
                PLTL_pattern.precedence,
                PLTL_pattern.chain_response,
                PLTL_pattern.chain_precedence,
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
        return f"!F({p})"

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
        return f"F({p1}) -> !F({p2})"

    @staticmethod
    def not_succession(p1: str, p2: str) -> str:
        return f"G(({p1}) -> !F({p2}))"

    @staticmethod
    def not_chain_succession(p1: str, p2: str) -> str:
        return f"G(({p1}) -> !X({p2}))"

    @staticmethod
    def get_op_dict() -> dict:
        return {
            "unary": [LTLf_pattern.existence, LTLf_pattern.abscence],
            "binary": [
                LTLf_pattern.choice,
                LTLf_pattern.exclusive_choice,
                LTLf_pattern.co_existence,
                LTLf_pattern.responded_existence,
                LTLf_pattern.response,
                LTLf_pattern.precedence,
                LTLf_pattern.chain_response,
                LTLf_pattern.chain_precedence,
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
    PLTL_pattern.exclusive_choice: LTLf_pattern.exclusive_choice,
    PLTL_pattern.co_existence: LTLf_pattern.co_existence,
    PLTL_pattern.responded_existence: LTLf_pattern.responded_existence,
    PLTL_pattern.response: LTLf_pattern.response,
    PLTL_pattern.precedence: LTLf_pattern.precedence,
    PLTL_pattern.chain_response: LTLf_pattern.chain_response,
    PLTL_pattern.chain_precedence: LTLf_pattern.chain_precedence,
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
        elif curr_node_type == FalseFormula:  # TODO check this part
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
        methods_past.append(
            random.choice(unary_past if methods_type[i] == 1 else binary_past)
        )
        methods_future.append(mapping[methods_past[i]])
        print(methods_past[i], methods_future[i])

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

    return formula_past, f"F({formula_future})", atoms_used
    # return formula_past, formula_future, atoms_used


def check_sat(formula):
    return os.popen(f"black solve -f '{formula}'").read()[:-1] == "SAT"


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
   

def main(args):

    # sat formulas counter
    generated_formulas = []
    n_formulas = 0

    # set seed
    random.seed(args["seed"])
    
    const = set(["True", "False"])

    while n_formulas < args["number"]:

        formula_past, formula_future, n_atoms = create_formula(
            args["depth"]
        )
    
        if check_sat(formula_past) and check_sat(formula_future):        
            if not bool(const & extract_atomic_varaibles(formula_past)):
                generated_formulas.append((formula_past, formula_future, n_atoms))
                n_formulas += 1

    write_to_json(generated_formulas, args["filename"])


if __name__ == "__main__":
        
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

    main(vars(args.parse_args()))
