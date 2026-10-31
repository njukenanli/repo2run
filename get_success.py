import os, json

with open("/home/v-rongzhili/code/comparison/repo2run/dataset.jsonl") as f:
    ds = [json.loads(i) for i in f]

mapping = {i["instance_id"]: i["repo"] for i in ds}

def success(log: str) -> bool:
    passed = 0
    failed = 0
    report = log.splitlines()[-1].replace("=","").split(" in ")[0].split(", ")
    for i in report:
        parts = i.strip().split()
        if len(parts) >2 :
            continue
        num, status = parts
        try:
            int(num)
        except:
            continue
        if "pass" in status.lower():
            print(num, status)
            passed += int(num)
        else:
            failed += int(num)
    return passed > failed

base = "/home/v-rongzhili/code/comparison/repo2run/output/DeepSeek-V4-Pro/playground"
suc = 0
for instance_id in os.listdir(base):
    repo = mapping[instance_id]
    if os.path.exists(f"{base}/{instance_id}/output/{repo}/test.txt"):
        with open(f"{base}/{instance_id}/output/{repo}/test.txt") as f:
            test = f.read()
    if success(test):
        suc+=1

print(suc)