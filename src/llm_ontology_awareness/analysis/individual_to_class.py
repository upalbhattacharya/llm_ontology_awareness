#!/usr/bin/env python

import json
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import polars as pl


class IndividualToClass:

    def binary_classify_metrics(self, args):
        stat_dict = defaultdict(float)
        pred_df = pl.read_ndjson(args.pred_file)
        save_path = os.path.dirname(args.pred_file)
        true_df = pl.read_ndjson(os.path.join(args.data_dir, "data.json"))
        target_counts = pl.read_ndjson(
            os.path.join(args.data_dir, "target_counts.json")
        )
        cls_counts = pl.read_ndjson(os.path.join(args.data_dir, "cls_counts.json"))

        pred_counts = pred_df["Prediction"].value_counts()
        fig = px.bar(pred_counts, x="Prediction", y="count", text="count")
        fig.update_xaxes(tickangle=45)
        plotly.offline.plot(
            fig, filename=os.path.join(save_path, "figs", "pred_counts.html")
        )
        pred_counts.write_ndjson(os.path.join(save_path, "pred_counts.json"))

        cls_pred_counts = pred_df.group_by("Class").agg(pl.col("Prediction").sum())
        cls_pred_counts = cls_pred_counts.rename({"Prediction": "count"})
        cls_pred_counts = cls_pred_counts.sort("count", descending=True)
        fig = px.bar(cls_pred_counts, x="Class", y="count", text="count")
        fig.update_xaxes(tickangle=45)
        plotly.offline.plot(
            fig, filename=os.path.join(save_path, "figs", "cls_pred_counts.html")
        )
        cls_pred_counts.write_ndjson(os.path.join(save_path, "cls_pred_counts.json"))

        cls_joined = cls_counts.join(cls_pred_counts, on="Class", how="inner")

        rank_corr = cls_joined.select(
            pl.corr("count", "count_right", method="spearman")
        ).item()
        stat_dict["rank_corr"] = rank_corr

        with open(os.path.join(save_path, "pred_stats.json"), "w") as f:
            json.dump(stat_dict, f, indent=4)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--pred_file", help="Responses file")
    parser.add_argument("-d", "--data_dir", help="Directory containing gold data")

    args = parser.parse_args()
    itc_obj = IndividualToClass()
    itc_obj.binary_classify_metrics(args)
