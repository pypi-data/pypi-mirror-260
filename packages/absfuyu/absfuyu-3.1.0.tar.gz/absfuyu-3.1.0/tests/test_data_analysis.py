"""
Test: Data Analysis

Version: 1.1.0
Date updated: 06/03/2024 (dd/mm/yyyy)
"""


# Library
###########################################################################
import random

import numpy as np
import pandas as pd
import pytest

from absfuyu.general.generator import Generator, Charset
from absfuyu.extensions.extra.data_analysis import (
    DataAnalystDataFrame, SplittedDF
)


# Test
###########################################################################
@pytest.fixture
def sample_df() -> DataAnalystDataFrame:
    # Number of columns generated
    num_of_cols: int = random.randint(5, 10)
    # List of column name
    col_name: list = Generator.generate_string(
        Charset.LOWERCASE, 
        unique=True,
        times=num_of_cols
    )
    # Create DataFrame
    df = pd.DataFrame(
        np.random.randn(random.randint(5, 100), num_of_cols), 
        columns=col_name
    )
    out = DataAnalystDataFrame(df)
    return out


@pytest.fixture
def sample_df_2() -> DataAnalystDataFrame:
    return DataAnalystDataFrame.sample_df()


# Drop cols
def test_drop_rightmost(sample_df: DataAnalystDataFrame):
    num_of_cols_drop = random.randint(1, 4)
    
    num_of_cols_current = sample_df.shape[1]
    sample_df.drop_rightmost(num_of_cols_drop)
    num_of_cols_modified = sample_df.shape[1]
    
    condition = (num_of_cols_current - num_of_cols_modified) == num_of_cols_drop
    assert condition


# Add blank column
def test_add_blank_column(sample_df: DataAnalystDataFrame):
    original_num_of_cols = sample_df.shape[1]
    sample_df.add_blank_column("new_col", 0)
    new_num_of_cols = sample_df.shape[1]

    condition = (
        (new_num_of_cols - original_num_of_cols) == 1
        and sum(sample_df["new_col"]) == 0
    )
    assert condition


# Add date column
def test_add_date_from_month(sample_df_2: DataAnalystDataFrame):
    sample_df_2.add_detail_date("date", mode="m")
    original_num_of_cols = sample_df_2.shape[1]
    sample_df_2.add_date_from_month("month", col_name="mod_date")
    new_num_of_cols = sample_df_2.shape[1]
    
    original_month = sample_df_2["month"][0]
    modified_month = sample_df_2["mod_date"][0].month

    # assert original_month == modified_month
    condition = (
        (new_num_of_cols - original_num_of_cols) == 1
        and original_month == modified_month
    )
    assert condition

def test_add_date_column(sample_df_2: DataAnalystDataFrame):
    # Get random mode
    mode_list = ["d", "w", "m", "y"]
    test_mode = list(map(lambda x: "".join(x), Generator.combinations_range(mode_list)))
    random_mode = random.choice(test_mode)
    num_of_new_cols = len(random_mode)
    
    # Convert
    original_num_of_cols = sample_df_2.shape[1]
    sample_df_2.add_detail_date("date", mode=random_mode)
    new_num_of_cols = sample_df_2.shape[1]
    assert (new_num_of_cols - original_num_of_cols) == num_of_new_cols


# Join and split
def test_split_df(sample_df_2: DataAnalystDataFrame):
    test = sample_df_2.split_na("missing_value")
    assert len(test) > 1

def test_split_df_2(sample_df_2: DataAnalystDataFrame):
    test = SplittedDF.divide_dataframe(sample_df_2, "number_range")
    assert len(test) > 1

def test_join_df(sample_df_2: DataAnalystDataFrame):
    test = sample_df_2.split_na("missing_value")
    out = test.concat()
    assert out.shape[0] == 100

def test_join_df_2(sample_df_2: DataAnalystDataFrame):
    """This test static method"""
    test = SplittedDF.divide_dataframe(sample_df_2, "number_range")
    out = SplittedDF.concat_df(test)
    assert out.shape[0] == 100