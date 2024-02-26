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
    def yesterday(p: str) -> str:
        return f"(Y {p})"

    @staticmethod
    def once(p: str) -> str:
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
    def get_op_dict() -> dict:
        return {
            "unary": [PLTL.yesterday, PLTL.once, PLTL.historically, PLTL.atom],
            "binary": [PLTL.land, PLTL.lor, PLTL.implies, PLTL.seq, PLTL.since],
        }


def get_atoms_list(n_atoms: int) -> List[str]:
    return [f"p{i}" for i in range(n_atoms)]


def create_formula(depth: int, n_atoms: int) -> str:
    atoms = get_atoms_list(n_atoms)
    unary, binary = PLTL.get_op_dict().values()
    methods_type = [round(x) + 1 for x in [random.random() for _ in range(depth)]]
    print(methods_type)
    methods = []
    for i in range(len(methods_type)):
        methods.append(random.choice(unary if methods_type[i] == 1 else binary))

    atoms_used = set()

    for i in range(depth):
        if i == 0:
            if methods_type[i] == 1:
                p = random.choice(atoms)
                formula = methods[i](p)
                atoms_used.add(p)
            else:
                p1, p2 = random.sample(atoms, 2)
                formula = methods[i](p1, p2)
                atoms_used.add(p1)
                atoms_used.add(p2)

        else:
            if methods_type[i] == 1:
                formula = methods[i](formula)
            else:
                p = random.choice(atoms)

                if random.random() < 0.5:
                    formula = methods[i](p, formula)
                else:
                    formula = methods[i](formula, p)

                atoms_used.add(p)

    return formula, len(atoms_used)


def check_sat(formula):
    return os.popen(f"black solve -f '{formula}'").read()[:-1] == "SAT"


def write_to_json(formulas, dir, filename):
    res = {}
    for i, (formula, atoms) in enumerate(formulas):
        res[f"f{i}"] = {"formula": formula, "n_atoms": atoms}

    with open(os.path.join(dir, f"{filename}.json"), "w") as ofile:
        ofile.write(json.dumps(res))
        print(f"File {filename}.json saved in {dir}")


def main(args):

    # sat formulas counter
    generated_formulas = []
    n_formulas = 0

    # set seed
    random.seed(args["seed"])

    while n_formulas < args["number"]:

        formula, n_atoms = create_formula(args["depth"], args["prop_atom"])

        if check_sat(formula):
            generated_formulas.append((formula, n_atoms))
            n_formulas += 1

    write_to_json(generated_formulas, args["directory"], args["filename"])


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument(
        "-s",
        "--seed",
        default=None,
        required=True,
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
        "-pa",
        "--prop_atom",
        default=None,
        required=True,
        type=int,
        help="The maximum number of prop atom of formulas",
    )
    args.add_argument(
        "-dir",
        "--directory",
        default=None,
        required=True,
        type=str,
        help="The directory in which to put the creted json file",
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
