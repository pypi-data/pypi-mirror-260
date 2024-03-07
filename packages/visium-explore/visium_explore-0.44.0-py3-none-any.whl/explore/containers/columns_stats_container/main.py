"""Container displaying stats for the columns of the selected DataFrame."""

import pathlib

import streamlit as st

from explore.io import read_df


def columns_stats_container(file_path: pathlib.Path) -> None:
    st.write("---")
    st.header("Columns statistics")
    df = read_df(file_path)
    stats_df = df.describe(include="all").transpose()

    stats_df["ratio_null"] = df.isnull().mean()

    # Add the type of the column
    stats_df["type"] = df.dtypes

    st.write(stats_df)
