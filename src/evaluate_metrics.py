import ast
import re
from functools import lru_cache
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from torch.nn import functional as F
from nltk.translate.bleu_score import sentence_bleu

tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")


def get_similarity(text1, text2, aggregate="cls"):
    # can be 'cls' or 'mean'

    # Tokenize input
    input_ids = [
        tokenizer.encode(t, add_special_tokens=True, return_tensors="pt")
        for t in [text1, text2]
    ]

    # Compute token embeddings

    with torch.no_grad():
        last_hidden_states = [model(i) for i in input_ids]

    last_hidden_states1 = last_hidden_states[0][0][0]
    last_hidden_states2 = last_hidden_states[1][0][0]

    if aggregate == "cls":
        # compute similarity between CLS tokens
        last_hidden_states1 = F.normalize(last_hidden_states1[0], p=2, dim=0)
        last_hidden_states2 = F.normalize(last_hidden_states2[0], p=2, dim=0)

    elif aggregate == "mean":
        # compute similarity between mean of all tokens
        last_hidden_states1 = F.normalize(last_hidden_states1.mean(0), p=2, dim=1)
        last_hidden_states2 = F.normalize(last_hidden_states2.mean(0), p=2, dim=1)

    similarity = F.cosine_similarity(last_hidden_states1, last_hidden_states2, dim=0)

    return similarity


def get_bleu_score(text1, text2):
    separators = "[\s,()\"']"
    text1 = re.split(separators, text1)
    text1 = [t for t in text1 if t]
    text2 = re.split(separators, text2)
    text2 = [t for t in text2 if t]

    return sentence_bleu([text1], text2, weights=(0.5, 0.5))


def get_PR_funcs(pseudocode_GT, pseudocode_pred):
    # Implements a precision and recall metric for functions
    functions_pred = parse_pseudocode(pseudocode_pred)
    functions_GT = parse_pseudocode(pseudocode_GT)

    return calculate_precision_recall(list(functions_GT.keys()), list(functions_pred))


def get_PR_args(pseudocode_GT, pseudocode_pred):
    # Implements a precision and recall metric for function arguments
    functions_pred = parse_pseudocode(pseudocode_pred)
    functions_GT = parse_pseudocode(pseudocode_GT)

    precision = []
    recall = []

    for func_name, args_pred in functions_pred.items():
        if func_name in functions_GT:
            args_gt = functions_GT[func_name]

            p, r = calculate_precision_recall(
                list(args_gt.keys()), list(args_pred.keys())
            )
            precision.append(p)
            recall.append(r)

    return np.nanmean(precision).item(), np.nanmean(recall).item()


def get_args_similarity(pseudocode_GT, pseudocode_pred):
    # Implements a precision and recall metric for function arguments
    functions_pred = parse_pseudocode(pseudocode_pred)
    functions_GT = parse_pseudocode(pseudocode_GT)

    similarities = []

    for func_name, args_pred in functions_pred.items():
        if func_name in functions_GT:
            args_gt = functions_GT[func_name]
            for arg_name, arg_value_pred in args_pred.items():
                if arg_name in args_gt:
                    arg_value_gt = args_gt[arg_name]

                    similarities.append(get_similarity(arg_value_pred, arg_value_gt))

    return np.mean(similarities).item()


def get_args_bleu(pseudocode_GT, pseudocode_pred):
    # Implements a precision and recall metric for function arguments
    functions_pred = parse_pseudocode(pseudocode_pred)
    functions_GT = parse_pseudocode(pseudocode_GT)

    bleu_scores = []

    for func_name, args_pred in functions_pred.items():
        if func_name in functions_GT:
            args_gt = functions_GT[func_name]
            args_gt_str = []
            for k, v in args_gt.items():
                args_gt_str.append(k)
                args_gt_str.append(v)
            args_gt_str = " ".join(args_gt_str)

            args_pred_str = []
            for k, v in args_pred.items():
                args_pred_str.append(k)
                args_pred_str.append(v)
            args_pred_str = " ".join(args_pred_str)

            bleu_scores.append(get_bleu_score(args_pred_str, args_gt_str))

    return np.mean(bleu_scores).item()


def parse_python_code(code):  # Code is a multi-line string.
    lines = code.split("\n")  # Split the code into lines
    funcs = []  # Store the function names here
    main_code = []
    func = []
    in_func = False
    for line in lines:  # Parse string line by line
        if re.match(r"def [\w_]+\(.*?\):", line):  # start of a function
            in_func = True
            if func:  # if func is not empty, add it to funcs
                funcs.append("\n".join(func))
                func = []
        elif in_func and not re.match(r"\s", line):  # end of a function
            in_func = False
            funcs.append("\n".join(func))
            func = []
        if in_func:
            func.append(line)
        else:
            main_code.append(line)
    if func:  # if func is not empty after looping, add it to funcs
        funcs.append("\n".join(func))

    return funcs, "\n".join(main_code)


def get_function_names(pseudofunctions):
    pseudo_functions = [ast.parse(x) for x in parse_python_code(pseudofunctions)[0]]

    function_names = [
        node.name
        for tree in pseudo_functions
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]
    return function_names


def parse_pseudocode(code):
    functions = re.findall(r"(\w+)\s*\(([^)]+)\)", code)

    function_dict = {}

    for function in functions:
        function_name = function[0]
        arguments = re.findall(r'(\w+)=["\']([^"\']+)["\']', function[1])
        argument_dict = {arg_name: arg_val for arg_name, arg_val in arguments}
        function_dict[function_name] = argument_dict

    return append_index_to_function_names(function_dict)


def append_index_to_function_names(func_dict):
    func_count = {}
    new_func_dict = {}

    for func_name, args in func_dict.items():
        if func_name not in func_count:
            func_count[func_name] = 0
        else:
            func_count[func_name] += 1

        new_func_name = func_name + str(func_count[func_name])
        new_func_dict[new_func_name] = args

    return new_func_dict


def calculate_precision_recall(gt, pred):
    TPs = [k for k in pred if k in gt]
    FPs = [k for k in pred if k not in gt]
    FNs = [k for k in gt if k not in pred]

    if len(TPs) + len(FPs) == 0:
        precision = np.nan  # Avoid division by zero
    else:
        precision = len(TPs) / (len(TPs) + len(FPs))

    if len(TPs) + len(FNs) == 0:
        recall = np.nan  # Avoid division by zero
    else:
        recall = len(TPs) / (len(TPs) + len(FNs))

    return precision, recall


def lev_dist(a, b):
    """
    This function will calculate the levenshtein distance between two input
    strings a and b

    params:
        a (String) : The first string you want to compare
        b (String) : The second string you want to compare

    returns:
        This function will return the distnace between string a and b.

    example:
        a = 'stamp'
        b = 'stomp'
        lev_dist(a,b)
        >> 1.0
    """

    @lru_cache(None)  # for memorization
    def min_dist(s1, s2):
        if s1 == len(a) or s2 == len(b):
            return len(a) - s1 + len(b) - s2

        # no change required
        if a[s1] == b[s2]:
            return min_dist(s1 + 1, s2 + 1)

        return 1 + min(
            min_dist(s1, s2 + 1),  # insert character
            min_dist(s1 + 1, s2),  # delete character
            min_dist(s1 + 1, s2 + 1),  # replace character
        )

    return min_dist(0, 0)


def check_fn_errors(func):
    try:
        tree = ast.parse(func)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.args.args:
                    return "NoParametersWarning"
    except SyntaxError as e:
        error_type = str(type(e))
        if "IndentationError" in error_type:
            return "IndentationError"
        elif "SyntaxError" in error_type:
            return "SyntaxError"

    return None


def print_error(func):
    error_dict = {
        "IndentationError": "IndentationError: There are indentation errors in one or more of your function definitions. functions should have at least one indented line that has code and not comments in it. This can simply be a return or pass statement.",
        "SyntaxError": "SyntaxError: There are syntax errors in one or more of your function definitions.",
        "NoParametersWarning": "NoParametersWarning: One or more of your functions does not have any parameters. Functions typically have parameters to better describe the experiment.",
    }
    error = check_fn_errors(func)

    if error:
        return (
            "your code has the following error or warning: \n\n"
            + error_dict[error]
            + "\n\nplease resolve this error where applicable and try again."
        )
    else:
        return None


def error_check(code):
    funcs, main_code = parse_python_code(code)
    if len(funcs) <= 2:
        return "There do not appear to be any functions in your code. please define functions and try again."
    for func in funcs:
        error = check_fn_errors(func)
        if error:
            return check_fn_errors(func), print_error(func)

    return None


def test_check_fn_errors():
    # Test 1: Syntax error
    func = "def my_func(a=2):\n    print('Hello, world!')"
    errors = check_fn_errors(func)
    assert errors == None

    # Test 2: Indentation error
    func = "def my_func():\nprint('Hello, world!')"
    errors = check_fn_errors(func)
    assert errors == "IndentationError"

    # Test 3: No parameters warning
    func = "def my_func():\n    pass"
    errors = check_fn_errors(func)
    assert errors == "NoParametersWarning"


def check_code_errors(pseudofns, code):
    # check that the code only uses the pseudofunctions provided
    new_funcs, main_code = parse_python_code(code)
    parsed_functions = [ast.parse(func) for func in pseudofns]
    function_names = [
        node.name
        for tree in parsed_functions
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]
    if len(new_funcs) != 0:
        return "NewFunctionError"
    if len(main_code) == 0:
        return "NoMainCodeError"
    code_tree = ast.parse(main_code)
    for node in ast.walk(code_tree):
        if isinstance(node, ast.Call):
            if node.func.id not in function_names:
                return "UndefinedFunctionError"
    return None


def get_levenshtein_distance(pseudofunctions, pseudocode_GT, pseudocode_pred):
    # Step 1: Get the names of the pseudo-functions
    ALPHABET_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"  # Can make this longer if need be
    PENALTY_WEIGHT = 1
    pseudo_functions = [ast.parse(x) for x in parse_python_code(pseudofunctions)[0]]
    function_names = [
        node.name
        for tree in pseudo_functions
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]
    # Step 1.1: Append a function "undefined_function"
    UNDEFINED_FUNCTION_NAME = "undefined_function"
    function_names.append(UNDEFINED_FUNCTION_NAME)
    # Step 1.2: Define the mapping dictionary from function names to characters
    MAP_DICT = {
        function_names[i]: ALPHABET_STRING[i] for i in range(len(function_names))
    }

    def map_code(
        function_names, pseudocode, map_dict=MAP_DICT, und_f=UNDEFINED_FUNCTION_NAME
    ):
        penalty = 0  # Number of undefined functions used
        tree = ast.parse(pseudocode)
        functions_used = (
            []
        )  # List to be returned (No arguments).  # TODO: Handle if statements
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):  # Function call
                if node.func.id not in function_names:  # Check if defined function
                    print("Undefined function " + str(node.func.id) + " in code")
                    penalty += 1
                    functions_used.append(und_f)
                else:
                    functions_used.append(node.func.id)
        program_string = "".join(
            [map_dict[f] for f in functions_used]
        )  # Convert into a string
        return program_string, penalty

    prediction_string, prediction_penalty = map_code(function_names, pseudocode_pred)
    ground_truth_string, penalty_gt = map_code(function_names, pseudocode_GT)

    levenshtein_distance_metric_score = (
        lev_dist(prediction_string, ground_truth_string)
        + prediction_penalty * PENALTY_WEIGHT
    )

    return levenshtein_distance_metric_score
