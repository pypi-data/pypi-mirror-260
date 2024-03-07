"""Container displaying stats for the columns of the selected DataFrame."""

import pathlib

import numpy as np
import pandas as pd
import streamlit as st

from explore.io import read_df


def columns_stats_container(file_path: pathlib.Path) -> None:
    st.write("---")
    st.header("Columns statistics")
    df = read_df(file_path)

    col1, col2 = st.columns([1, 1])

    with col1:
        stats_df_number = df.describe(include=np.number).transpose()
        display_column_stats(stats_df_number, df)

    with col2:
        stats_df_object = df.describe(include=object).transpose()
        display_column_stats(stats_df_object, df)


def display_column_stats(stats_df: pd.DataFrame, df: pd.DataFrame):
    stats_df["ratio_null"] = df.isnull().mean()
    stats_df["type"] = df.dtypes
    st.write("### Object columns")
    st.dataframe(
        stats_df,
        column_config={"ratio_null": st.column_config.ProgressColumn("Ratio null", min_value=0, max_value=1)},
    )
