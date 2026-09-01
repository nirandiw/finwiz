import re
GOLD_PRECISION = 5 

CONSTANTS = {"m1": -1.0}
OPS = {
    "add":      lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide":   lambda a, b: a / b,
    "exp":      lambda a, b: a ** b,
    "greater":  lambda a, b: "yes" if a > b else "no",
}

STEP = re.compile(r"([a-z_]+)\(([^()]*)\)")


class DSLError(ValueError):
    """Program could not be parsed or executed."""


def _operand(token: str, results: list) -> float:
    token = token.strip()

    if token.startswith("#"):
        index = int(token[1:])
        if index >= len(results):
            raise DSLError(f"forward reference {token}")
        return results[index]

    if token.startswith("const_"):
        name = token[len("const_"):]
        return CONSTANTS.get(name, None) if name in CONSTANTS else float(name)

    if token.endswith("%"):
        return float(token[:-1].replace(",", "")) / 100.0

    return float(token.replace(",", "").replace("$", ""))


def execute(program: str) -> float | str:
    steps = STEP.findall(program)
    if not steps:
        return _operand(program, [])        # bare literal: "206588"

    results = []
    for op, raw_args in steps:
        if op not in OPS:
            raise DSLError(f"unknown operator {op!r}")
        args = [_operand(a, results) for a in raw_args.split(",")]
        results.append(OPS[op](*args))

    return results[-1]



def calculator(dsl_answer: str) -> float | str:
    """Return the value response for display."""
    answer = execute(dsl_answer)
    return answer if isinstance(answer, str) else round(answer, GOLD_PRECISION)