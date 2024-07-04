#!/usr/bin/env python

import os

import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import polars as pl


class IndividualToClass:

    def binary_classify_metrics(self, df, save_path):
        pred_counts = df["Prediction"].value_counts()
        fig = px.bar(pred_counts, x="Prediction", y="count", text="count")
        fig.update_xaxes(tickangle=45)
        plotly.offline.plot(
            fig, filename=os.path.join(save_path, "figs", "pred_counts.html")
        )
        pred_counts.write_ndjson(os.path.join(save_path, "pred_counts.json"))

        # cls_counts = df.group_by("Class").agg(pl.col("Member").sum())
        # cls_counts = cls_counts.rename({"Member": "count"})
        # cls_counts = cls_counts.sort("count", descending=True)
        # fig = px.bar(cls_counts, x="Class", y="count", text="count")
        # fig.update_xaxes(tickangle=45)
        # plotly.offline.plot(
        #     fig, filename=os.path.join(save_path, "figs", "cls_counts.html")
        # )
        # cls_counts.write_ndjson(os.path.join(save_path, "cls_counts.json"))
        #
        # ind_counts = df.group_by("Individual").agg(pl.col("Member").sum())
        # ind_counts = ind_counts.rename({"Member": "count"})
        # ind_counts = ind_counts.sort("count", descending=True)
        # fig = px.bar(ind_counts, x="Individual", y="count", text="count")
        # fig.update_xaxes(tickangle=45)
        # plotly.offline.plot(
        #     fig, filename=os.path.join(save_path, "figs", "ind_counts.html")
        # )
        # ind_counts.write_ndjson(os.path.join(save_path, "ind_counts.json"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Responses file")

    args = parser.parse_args()
    df = pl.read_ndjson(args.file)
    save_path = os.path.dirname(args.file)
    itc_obj = IndividualToClass()
    itc_obj.binary_classify_metrics(df, save_path)
