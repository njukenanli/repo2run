import os, json
import subprocess
import argparse

os.makedirs("logs", exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str)
args = parser.parse_args()
model=args.model

os.makedirs(f"output/{model}/playground/", exist_ok=True)
os.makedirs(f"output/{model}/logs/", exist_ok=True)

with open("dataset.jsonl") as f:
    l = [json.loads(i) for i in f]

for i in reversed(l):
    if i["language"].lower() != "python":
        continue
    instance_id = i["instance_id"]
    print(instance_id, flush=True)
    repo = i["repo"]
    commit = i["base_commit"]
    cmd = f"""python build_agent/main.py --full_name "{repo}" --sha "{commit}" --root_path output/{model}/playground/{instance_id} --llm {model} > output/{model}/logs/{instance_id}.txt 2>&1"""
    # execute cmd and wait it to complete.
    subprocess.run(cmd, shell=True)
    