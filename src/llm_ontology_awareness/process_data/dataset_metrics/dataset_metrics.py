#!/usr/bin/env python

import os

import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns


class IndividualToClass:

    def binary_classify_metrics(self, df, save_path):
        counts = df["Member"].value_counts()
        plt.figure(figsize=(5, 8))
        sns.set_style("whitegrid")
        ax = sns.barplot(counts, x="Member", y="count")
        ax.bar_label(ax.containers[0], fontsize=10)
        ax.figure.savefig(os.path.join(save_path, "class_counts.png"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Dataset file")

    args = parser.parse_args()
    df = pl.read_ndjson(args.file)
    save_path = os.path.dirname(args.file)
    itc_obj = IndividualToClass()
    itc_obj.binary_classify_metrics(df, save_path)
