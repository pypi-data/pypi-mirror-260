from easy_eval import HarnessEvaluator, HarnessTaskManager
from easy_eval.config import EvaluatorConfig

tasks = HarnessTaskManager.load_tasks(["babi"])
print(tasks)
config = EvaluatorConfig(limit=1, log_samples=True)

eval = HarnessEvaluator(model_backend="huggingface", model_name_or_path="gpt2")
results = eval.evaluate(tasks=tasks, show_results_terminal=True, config=config)

print(results)
