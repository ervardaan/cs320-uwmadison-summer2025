import os, sys, json, csv, re, math, copy
import matplotlib.pyplot as plt
import graphviz
from collections import namedtuple
import subprocess
from pathlib import Path

try:
    sys.path.append(os.path.abspath("../.utils"))
    import hardcoding
finally:
    sys.path.pop()

BOLD = "\033[1m"
RESET = "\033[0m"
RED = "\033[31m"

Answer = namedtuple("Answer", ["question", "type", "value", "stream", "notes"])

code = {}

def read_code_cells(ipynb, default_notes={}):
    answers = []
    with open(ipynb) as f:
        nb = json.load(f)
        cells = nb["cells"]
        expected_exec_count = 1
        source_code = []
        for cell in cells:
            if "execution_count" in cell and cell["execution_count"]:
                exec_count = cell["execution_count"]
                if exec_count != expected_exec_count:
                    raise Exception(f"{BOLD}Error: Notebook cells may have been run out of order. Please restart the kernel, run all cells, and save the notebook before running the tester.{RESET}")
                expected_exec_count = exec_count + 1
            if cell["cell_type"] != "code":
                continue
            if not cell["source"]:
                continue
            m = re.match(r"#[qQ](\d+)(.*)", cell["source"][0].strip())
            if not m:
                source_code.extend(cell["source"])
                continue
            qnum = int(m.group(1))
            source_code.extend(cell["source"])
            code[qnum] = copy.deepcopy(source_code) # add all previous code to dict entry for this question
            notes = m.group(2).strip()
            config = parse_question_config(notes)
            if "run" in config:
                exec(config["run"])
            print(f"Reading Question {qnum}")
            if qnum in [a.question for a in answers]:
                raise Exception(f"Answer {qnum} repeated!")
            expected = max([0] + [a.question for a in answers]) + 1
            if qnum != expected:
                print(f"Warning: Expected question {expected} next but found {qnum}!")

            # plots are display_data, so try to find those before looking for regular cell outputs
            outputs = [o for o in cell["outputs"]
                       if o.get("output_type") == "display_data"]
            stdout = ""
            if len(outputs) == 0:
                outputs = [o for o in cell["outputs"]
                           if o.get("output_type") == "execute_result"]
            assert len(outputs) < 2
            if len(outputs) > 0:
                output_str = "".join(outputs[0]["data"]["text/plain"]).strip()
                if output_str.startswith("<Figure"):
                    output_str = "plt.Figure()"
                if output_str.startswith("<") and "Digraph" in output_str:
                    output_str = "graphviz.graphs.Digraph()"
                if output_str == "nan":
                    output_str = 'float("nan")'
            else:
                stream = [o for o in cell["outputs"]
                          if o.get("output_type") == "stream"]
                try:
                    stdout = stream[0]["text"][0].strip()
                except:
                    pass
                output_str = "None"
            try:
                output = eval(output_str)
                if isinstance(output, tuple):
                    type_name = "tuple"
                else:
                    type_name = type(output).__name__
            except NameError as e:
                type_name = "*"
            answers.append(Answer(qnum, type_name, output_str, stdout, notes))
    return answers

def dump_results(ipynb, csv_path, default_notes={}):
    with open(csv_path, "w") as f:
        wr = csv.writer(f)
        wr.writerow(Answer._fields)
        for answer in read_code_cells(ipynb, default_notes):
            wr.writerow(answer)
    print(f"Wrote results to {csv_path}.")

def compare_bool(expected, actual, config={}):
    return (expected == actual, None)

def compare_int(expected, actual, config={}):
    return (expected == actual, None)

def compare_type(expected, actual, config={}):
    return (expected == actual, None)

def compare_float(expected, actual, config={}):
    if math.isnan(expected) and math.isnan(actual):
        return (True, None)
    tolerance = float(config.get("tolerance", 0))
    return (math.isclose(expected, actual, abs_tol=tolerance), None)

def compare_str(expected, actual, config={}):
    if config.get("case") == "any":
        return (expected.upper() == actual.upper(), None)
    return (expected == actual, None)

def compare_list(expected, actual, config={}):
    if config.get("order") == "strict":
        return (expected == actual, None)
    else:
        return (sorted(expected) == sorted(actual), None)

def compare_tuple(expected, actual, config={}):
    return (expected == actual, None)

def compare_set(expected, actual, config={}):
    if config.get("require") == "superset":
        return (len(expected - actual) == 0, None)
    else:
        return (expected == actual, None)

def compare_dict(expected, actual, config={}):
    tolerance = config.get("tolerance", None)

    if tolerance:
        if expected.keys() != actual.keys():
            return (False, None)

        for key in expected.keys():
            if not compare_float(expected[key], actual[key], {"tolerance": tolerance}):
                return (False, None)
                
        return (True, None)

    return (expected == actual, None)

def compare_figure(expected, actual, config={}):
    if type(expected) != type(actual):
        return (False, None)
    
    name = config.get("name", None)
    tolerance = config.get("tolerance", None)
    fig_type = config.get("type", None)
    title = config.get("title", False)
    axis = config.get("axis", False)
    legend = config.get("legend", False)
    text = config.get("text", False)
    sort = config.get("sort", False)

    assert os.path.isfile(f".pkl/{name}.pkl")
    assert os.path.isfile(f"{name}.pkl")
    
    result = subprocess.run(
        ['python3', 
         '../.utils/image_tester.py', 
         f".pkl/{name}.pkl", 
         f"{name}.pkl", 
         fig_type, 
         tolerance, 
         "-t" if title else "", 
         "-ax" if axis else "",
         "-l" if legend else "", 
         "-tx" if text else "",
         "-s" if sort else ""], 
        capture_output=True, 
        text=True)
    
    errors = [error for error in result.stderr.split("\n") if error]
    
    return (result.returncode == 1, errors)

def compare_nonetype(expected, actual, config={}):
    return (type(expected) == type(actual), None)

compare_fns = {
    "bool": compare_bool,
    "int": compare_int,
    "float": compare_float,
    "str": compare_str,
    "list": compare_list,
    "tuple": compare_tuple,
    "set": compare_set,
    "dict": compare_dict,
    "type": compare_type,
    "Figure": compare_figure,
    "Digraph": compare_figure,
    "NoneType": compare_nonetype,
}

def parse_question_config(c):
    if c.startswith("run="):
        return {"run": c[4:]}
    config = {}
    opts = c.split(" ")
    for opt in opts:
        parts = opt.split("=")
        if len(parts) != 2:
            continue
        config[parts[0]] = parts[1].strip()
    return config

def compare_question_stream(expected_stream, actual_stream):
    return expected_stream == actual_stream

def compare(expected_csv, actual_csv):
    result = {"score": 0, "errors": [], "hardcoding": []}
    passing = 0

    with open(expected_csv) as f:
        expected_rows = {int(row["question"]): dict(row) for row in csv.DictReader(f)}
    with open(actual_csv) as f:
        actual_rows = {int(row["question"]): dict(row) for row in csv.DictReader(f)}

    for qnum in sorted(expected_rows.keys()):
        if not qnum in actual_rows:
            continue
        expected = expected_rows[qnum]
        actual = actual_rows[qnum]
        if actual["type"] not in (expected["type"], "*"):
            err = f'Question {qnum}:\n{"-"*15}\nExpected type to be {expected["type"]}, but found {actual["type"]}'
            result["errors"].append(err)
            continue
        if not expected["type"] in compare_fns:
            raise Exception(f'Tester cannot handle type {expected["type"]} on question {qnum}')
        compare_fn = compare_fns[expected["type"]]
        config = parse_question_config(expected["notes"])
        if "run" in config:
            exec(config["run"])
        if expected.get("stream") != "":
            expected_stream = expected["stream"]
            actual_stream = actual["stream"]
            if not compare_question_stream(expected_stream, actual_stream):
                err = f'Question {qnum}: expected output to be "{expected_stream}", but found "{actual_stream}".'
                result["errors"].append(err)
                continue

        # ========================= Check for Hardcoding =========================
        if qnum != 18: # skip hardcoding check for q18
            hc = hardcoding.check_hardcoding(code[qnum], expected["value"], expected["type"], qnum)
            if hc:
                err = [
                    f"{BOLD}Question {qnum}:{RESET}",
                ]
                err.extend(hc)
                result["hardcoding"].append("\n".join(err))
                continue
        # ========================= Check for Hardcoding =========================

        # ========================= MP7 ONLY =========================
        if qnum == 19:
            print(f'\n{BOLD}Your model scored {float(actual["value"]):0.5f} ({float(expected["value"])} and above earns full credit on Q19){RESET}')
            points = 3.0*(float(actual["value"])/float(expected["value"]))
            passing += min(points, 3)
            continue
        if "just_dict" in config:
            keys = [val for key, val in config.items() if "key" in key]
            missing_keys = set()
            actual_dict = eval(actual["value"])
            for key in keys:
                if key in actual_dict:
                    passing = passing + 0.25
                else:
                    missing_keys.add(key)

            if missing_keys:
                err = [
                    f"{BOLD}Question {qnum}:{RESET}",
                    f"  EXPECTED KEYS: {keys}",
                    f"  ACTUAL KEYS: {', '.join(actual_dict.keys())}",
                ]
                result["errors"].append("\n".join(err))
        # ========================= MP7 ONLY =========================

        else:
            if qnum == 2: # skip graph grading for Q2 --> only check output type
                if type(eval(expected["value"])) != type(eval(actual["value"])):
                    compare_result = (False, None)
                else:
                    compare_result = (True, None)
            else:
                compare_result = compare_fn(eval(expected["value"]), eval(actual["value"]), config)
            if compare_result[0]:
                # ========================= MP7 ONLY =========================
                if qnum == 17: 
                    passing += 2.0
                # ========================= MP7 ONLY =========================
                else: 
                    passing += 1.0
            else:
                err = [
                    f"{BOLD}Question {qnum}:{RESET}",
                ]
                if not compare_result[1]:
                    err.extend([
                        f"EXPECTED: {expected['value']}",
                        f"ACTUAL: {actual['value']}",
                    ])
                elif compare_result[1]:
                    formatted_errors = "\n".join(compare_result[1])
                    err.append(f"ERRORS: {formatted_errors}")
                result["errors"].append("\n".join(err))

    result["missing"] = sorted(set(expected_rows.keys()) - set(actual_rows.keys()))
    score = round(100 * passing / 22)
    result["score"] = score
    result["summary"] = f"Result: {passing} of 22 points, for a score of {score}%."
    return result

def main():
    if len(sys.argv) != 1:
        print("Usage: python3 tester.py")
        return

    # dump results from this notebook to a summary .csv file
    ipynb = str(Path(__file__).parent.name) + ".ipynb"
    actual_path = ipynb.replace(".ipynb", ".csv").replace(".json", ".csv")
    
    try:
        dump_results(ipynb, actual_path)
    except Exception as e:
        print(e)
        return

    # ========================= Notebook Tests =========================
    expected_path = ipynb.replace(".ipynb", "-key.csv")
    result_notebook = compare(expected_path, actual_path)

    # ========================= Show Results ========================= 
    result = result_notebook

    # save results
    result_path = os.path.join(os.path.dirname(ipynb), "test.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    if len(result["errors"]) or len(result["missing"]) or len(result["hardcoding"]):
        print("\n" + "="*85 + "\n")

    # show user-friendly summary of test.json
    if len(result["errors"]) or len(result["missing"]):
        print(f"{BOLD}** There were a total of {len(result['errors'])} error(s) and {len(result['missing'])} missing answer(s) **{RESET}\n")
        
    # print notebook errors
    if len(result["errors"]) or len(result["missing"]):
        print(f"\n{BOLD}Notebook:{RESET}") 
        print("-"*20 + "\n")
        if len(result["errors"]):
            for err in result["errors"]:
                print(err)
                print() 
        if len(result["missing"]):
            print(f'{len(result["missing"])} answers not found, for question(s):',
                  ", ".join([str(m) for m in result["missing"]]))
            print()
            
    if len(result["hardcoding"]):
        print(f"{RED}{BOLD}Hardcoded answers detected. Please avoid directly writing answers in your code.\nIf you believe this is a mistake, feel free to attend office hours for clarification.{RESET}\n")
        for err in result["hardcoding"]:
                print(err)
                print() 
            
    print("\n" + "="*85)
    print(f"{BOLD}{result['summary']}{RESET}")
    print("="*85)


if __name__ == '__main__':
     main()
