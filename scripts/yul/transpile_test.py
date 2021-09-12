import pytest
import os
import json
import difflib

from yul.main import generate_cairo

warp_root = os.path.abspath(os.path.join(__file__, "../../.."))
test_dir = os.path.join(warp_root, "tests", "yul")
tests = [
    os.path.join(test_dir, item)
    for item in os.listdir(test_dir)
    if item.endswith(".sol")
]
cairo_suffix = ".cairo"
main_contract = "WARP"


@pytest.mark.parametrize(("solidity_file"), tests)
def test_transpilation(solidity_file):
    gen_cairo_code = generate_cairo(solidity_file, main_contract).splitlines()

    cairo_file_path = solidity_file[:-4] + cairo_suffix
    with open(cairo_file_path, "r") as cairo_file:
        cairo_code = cairo_file.read().splitlines()
        cairo_file.close()

    temp_file_path = f"{cairo_file_path}.temp"
    with open(temp_file_path, "w") as temp_file:
        print(*gen_cairo_code, file=temp_file, sep="\n")
        gen_cairo_code = clean(gen_cairo_code)
        cairo_code = clean(cairo_code)
        compare_codes(gen_cairo_code, cairo_code)
        os.remove(temp_file_path)


def compare_codes(lines1, lines2):
    d = difflib.Differ()
    diff = d.compare(lines1, lines2)

    message = ""
    result = False
    for item in diff:
        result |= item.startswith("+") or item.startswith("-")
        message += item + "\n"

    assert not result, message


def clean(lines):
    res = []
    for line in lines:
        l = line.strip()
        if len(l) > 0:
            res.append(l)

    return res
