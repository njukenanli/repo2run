import os, shutil

base="/home/v-rongzhili/code/comparison/repo2run/output"

def rec(folder):
    for subfolder in os.listdir(folder):
        if os.path.isdir(f"{folder}/{subfolder}") and subfolder=="repo":
            print(f"{folder}/{subfolder}")
            shutil.rmtree(f"{folder}/{subfolder}")
        elif os.path.isdir(f"{folder}/{subfolder}"):
            rec(f"{folder}/{subfolder}")

rec(base)