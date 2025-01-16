import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint
import os

HYLEAK_DIR = "HyLeak-data/"
output_domain_size_dict = {
    "smartgrid-1": (3, 12),
    "prob-termination-5": (6, 10),
    "prob-termination-7": (8, 10),
    "smartgrid-2": (9, 12),
    "prob-termination-9": (10, 10),
    "prob-termination-12": (13, 20),
    "reservoir-4": (16, 4),
    "window-20": (20, 20),
    "window-24": (24, 24),
    "smartgrid-3": (27, 12),
    "window-28": (28, 28),
    "window-32": (32, 32),
    "reservoir-6": (64, 8),
    "smartgrid-4": (81, 12),
    "smartgrid-5": (243, 12),
    "reservoir-8": (256, 16),
    "random-walk-3": (500, 24),
    "random-walk-5": (500, 31),
    "random-walk-7": (500, 33),
    "random-walk-14": (500, 40),
    "reservoir-10": (1024, 32),
    "reservoir-12": (4096, 64),
}

method_order = [
    "empirical",
    "ChaoFON",
    "ChaoFRN",
    "ChaoION",
    "ChaoIRN",
    "miller",
    "ChaoFOM",
    "ChaoFRM",
    "ChaoIOM",
    "ChaoIRM",
    "HyLeak",
]

def parse_hyleak_log(log_path, debug=False):
    with open(log_path) as f:
        lines = [l.strip() for l in f.readlines()]
    linegroups = []
    linegroup = None
    for l in lines:
        if l.startswith("n:") and linegroup:
            linegroups.append(linegroup)
            linegroup = [l]
        else:
            if linegroup is None:
                linegroup = []
            linegroup.append(l)
    linegroups.append(linegroup)
    hyleak_esti_data, hyleak_time_data = [], []
    for idx, linegroup in enumerate(linegroups, 1):
        if debug:
            print(f"group {idx}")
            for l in linegroup:
                print(l)
            print()

        Nx = int(
            int(linegroup[0].split(" ")[1])
            / output_domain_size_dict[subject][0]
        )
        estimates = [
            float(v)
            for v in linegroup[3].split(": ")[1].strip("[]").split(", ")
        ]
        times = [
            (float(v) * 10**-3)
            for v in linegroup[5].split(": ")[1].strip("[]").split(", ")
        ]
        for trial_idx in range(len(estimates)):
            hyleak_esti_data.append([Nx, trial_idx, estimates[trial_idx]])
            hyleak_time_data.append([Nx, trial_idx, times[trial_idx]])
    colname = "HyLeak"
    hyleak_esti_df = pd.DataFrame(
        hyleak_esti_data, columns=["Nx", "trial", colname]
    )
    hyleak_esti_df.set_index(["Nx", "trial"], inplace=True)
    hyleak_time_df = pd.DataFrame(
        hyleak_time_data, columns=["Nx", "trial", colname]
    )
    hyleak_time_df.set_index(["Nx", "trial"], inplace=True)
    return hyleak_esti_df, hyleak_time_df

for subject in output_domain_size_dict.keys():
    print(f"Processing {subject}", flush=True)
    log_path = os.path.join(HYLEAK_DIR, f"{subject}.log")
    hyleak_heu_esti_df, hyleak_heu_time_df = parse_hyleak_log(log_path)
    existing_data_path = (
        f"result/esti-{subject}-i-xy.csv"
    )
    existing_data_df = pd.read_csv(
        existing_data_path, header=0, index_col=(0, 1)
    )
    merge_df = pd.merge(
        existing_data_df, hyleak_heu_esti_df, left_index=True, right_index=True
    )
    output_path = (
        f"result/esti-merged-{subject}-i-xy.csv"
    )
    merge_df.to_csv(output_path)
    existing_data_path = (
        f"result/time-{subject}-i-xy.csv"
    )
    existing_data_df = pd.read_csv(
        existing_data_path, header=0, index_col=(0, 1)
    )
    merge_df = pd.merge(
        existing_data_df, hyleak_heu_time_df, left_index=True, right_index=True
    )
    output_path = (
        f"result/time-merged-{subject}-i-xy.csv"
    )
    merge_df.to_csv(output_path)