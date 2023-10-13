import json
import glob
from evaluate_metrics import (
    get_PR_funcs,
    get_PR_args,
    get_args_similarity,
    get_args_bleu,
    get_levenshtein_distance,
)

if __name__ == "__main__":
    evaluation_folder = "./src/to_evaluate/*.json"
    results = []

    for f in glob.glob(evaluation_folder):
        with open(f, "r") as f:
            data = json.load(f)
            id = data["id"]
            model_name = data["model_name"]
            ground_truth = data["ground_truth"]
            prediction_code = data["prediction_code"]
            prediction_functions = data["prediction_functions"]
            prediction = f"{prediction_functions}\n{prediction_code}"

            levenshtein_distance = get_levenshtein_distance(
                prediction_functions, ground_truth, prediction
            )
            scaled_levenshtein_distance = levenshtein_distance / len(
                ground_truth.split("\n")
            )

            precision_funcs, recall_funcs = get_PR_funcs(ground_truth, prediction)
            precision_args, recall_args = get_PR_args(ground_truth, prediction)

            args_similarity = get_args_similarity(ground_truth, prediction)

            args_bleu = get_args_bleu(ground_truth, prediction)

            results.append(
                {
                    "model": model_name,
                    "id": id,
                    "function_precision": precision_funcs,
                    "recall_funcs": recall_funcs,
                    "precision_args": precision_args,
                    "recall_args": recall_args,
                    "args_similarity": args_similarity,
                    "args_bleu": args_bleu,
                    "levenshtein_distance": levenshtein_distance,
                    "scaled_levenshtein_distance": scaled_levenshtein_distance,
                }
            )

    with open("./results.json", "w") as f:
        json.dump(results, f)
