import os
import subprocess
import pytest
import sys
import pandas as pd
from ..webuse import webuse
from ..use import use
from .._dataset import current

# from ..nn.finetune import finetune
# from ..fine_tuning.fthuggingface import fthuggingface, fthuggingface_old, askhuggingface
from ..fine_tuning.fthuggingface import fthuggingface, askhuggingface
from ..nn.pipeline import pipeline


# def df_maker(records):
#     y0 = pd.DataFrame.from_records(records)
#     y0["split"] = "train"
#     y1 = pd.DataFrame.from_records(records)
#     y1["split"] = "test"

#     return pd.concat([y0, y1], axis=0)


# @pytest.mark.skip
@pytest.mark.slow
def test_finetune_fill_mask():
    from .fixtures import eli5

    df = pd.DataFrame.from_records(eli5)
    # eli_df = df_maker(eli5)
    use(df)
    fthuggingface("text", "fill-mask")  # , num_examples=100)
    assert "text" in current.df.columns
    askhuggingface("This is my first Yelp review.")
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)
    # os.system(f"rm -rf {current.last_huggingface_ftmodel_dir}")


# @pytest.mark.skip
@pytest.mark.slow
def test_finetune_sentiment_analysis():
    from .fixtures import yelp_reviews

    # yelp_reviews_df = df_maker(yelp_reviews)
    # use(yelp_reviews_df)
    df = pd.DataFrame.from_records(yelp_reviews)
    use(df)
    fthuggingface("stars text", "sentiment-analysis")  # , num_examples=100)
    assert "stars" in current.df.columns
    askhuggingface("This is my first Yelp review.")
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)
    # os.system(f"rm -rf {current.last_huggingface_ftmodel_dir}")


# @pytest.mark.skip
@pytest.mark.slow
def test_finetune_text_classification():
    from .fixtures import yelp_reviews

    # yelp_reviews_df = df_maker(yelp_reviews)
    df = pd.DataFrame.from_records(yelp_reviews)
    use(df)
    fthuggingface("stars text")
    assert "stars" in current.df.columns
    askhuggingface("This is my first Yelp review.")
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)
    # os.system(f"rm -rf {current.last_huggingface_ftmodel_dir}")


# @pytest.mark.skip
# @pytest.mark.slow
# @pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
# def test_finetune2():
#     use(os.path.join(os.path.dirname(__file__), "yelp_mini.dta"))  # fixture
#     fthuggingface_old("label text", num_examples=100)
#     pipeline("text")
#     import numpy as np

#     assert np.corrcoef(current.df.label, current.df._finetuned)[0][1] > 0.50
