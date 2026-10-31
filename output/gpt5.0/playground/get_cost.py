import tiktoken, os, json

INPUT_COST=1.25/1_000_000
CACHED_INPUT_COST=0.8/1_000_000
OUTPUT_COST=10.00/1_000_000

def get_token(text: str, model: str = "gpt-5") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def instance_cost(traj: list[str]) -> float:
    cost = 0.0
    cached_input_tok = 0
    cur_input_tok = 0
    for turn in traj:
        if "content" not in turn.keys():
            continue
        if turn["role"] != "assistant":
            cur_input_tok += get_token(turn["content"])
        else:
            output_tok = get_token(turn["content"])
            cost += CACHED_INPUT_COST*cached_input_tok + INPUT_COST*cur_input_tok + OUTPUT_COST*output_tok
            cached_input_tok += cur_input_tok
            cur_input_tok = output_tok
    #print(cost)
    return cost
cost=0.0
count=0
base="/home/v-rongzhili/code/comparison/repo2run/playground"
for instance_id in os.listdir(base):
    repo = instance_id
    while repo[-1].isnumeric() or repo[-1].endswith("-"):
        repo = repo[:-1]
    repo = repo.replace("__", "/")
    #input(repo)
    if os.path.exists(f"{base}/{instance_id}/output/{repo}/track.json"):
        with open(f"{base}/{instance_id}/output/{repo}/track.json") as f:
            l=json.load(f)
    cost += instance_cost(l)
    count+=1
print(cost, count, cost/count)