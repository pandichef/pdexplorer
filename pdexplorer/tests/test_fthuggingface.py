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
# @pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
@pytest.mark.slow
def test_finetune_text_generation():
    from .fixtures import eli5

    df = pd.DataFrame.from_records(eli5)
    # eli_df = df_maker(eli5)
    use(df)
    fthuggingface("text", "text-generation")  # , num_examples=100)
    assert "text" in current.df.columns
    askhuggingface("This is my first Yelp review.", "text-generation")
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)
    # os.system(f"rm -rf {current.last_huggingface_ftmodel_dir}")


# @pytest.mark.skip
@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_finetune_fill_mask():
    from .fixtures import eli5

    df = pd.DataFrame.from_records(eli5)
    # eli_df = df_maker(eli5)
    use(df)
    fthuggingface("text", "fill-mask")  # , num_examples=100)
    assert "text" in current.df.columns
    askhuggingface("This is my first <mask> review.", "fill-mask")
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)
    # os.system(f"rm -rf {current.last_huggingface_ftmodel_dir}")


# @pytest.mark.skip
@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_finetune_sentiment_analysis():
    from .fixtures import yelp_reviews

    # yelp_reviews_df = df_maker(yelp_reviews)
    # use(yelp_reviews_df)
    df = pd.DataFrame.from_records(yelp_reviews)
    use(df)
    fthuggingface("stars text", "sentiment-analysis")  # , num_examples=100)
    assert "stars" in current.df.columns
    askhuggingface("This is my first Yelp review.", "sentiment-analysis")
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)
    # os.system(f"rm -rf {current.last_huggingface_ftmodel_dir}")


# @pytest.mark.skip
@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_finetune_text_classification():
    from .fixtures import yelp_reviews

    # yelp_reviews_df = df_maker(yelp_reviews)
    df = pd.DataFrame.from_records(yelp_reviews)
    use(df)
    fthuggingface("stars text", "text-classification")
    assert "stars" in current.df.columns
    askhuggingface("This is my first Yelp review.", "text-classification")
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)


# @pytest.mark.skip
@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_finetune_translation():
    from .fixtures import books

    # yelp_reviews_df = df_maker(yelp_reviews)
    df = pd.DataFrame.from_records(books)
    use(df)
    fthuggingface("fr en", "translation")
    # assert "stars" in current.df.columns
    text = "Legumes share resources with nitrogen-fixing bacteria."
    french_text = askhuggingface(text, "translation")[0]["translation_text"]
    assert (
        french_text
        == "Legumes partagent les ressources avec les bactéries fixatrices de azote."
    )
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)


# @pytest.mark.skip
@pytest.mark.slow
@pytest.mark.skipif(sys.platform != "win32", reason="only run locally")
def test_finetune_translation_hebrew():
    from .fixtures import niv

    # yelp_reviews_df = df_maker(yelp_reviews)
    df = pd.DataFrame.from_records(niv)
    use(df)
    fthuggingface("he en", "translation")
    # assert "stars" in current.df.columns
    text = "And there was evening, and there was morning—the third day."
    hebrew_text = askhuggingface(
        text, "translation", source_lang="en", target_lang="he"
    )[0]["translation_text"]
    # Note: t5-small can't handle Hebrew apparently
    assert hebrew_text == "Und es gab Abend, und es gab Morgen – der dritte Tag."
    subprocess.run(f"rm -rf {current.last_huggingface_ftmodel_dir}", shell=True)
