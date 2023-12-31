# Produces a DataFrame containing a full translation of the Hebrew Bible
# https://www.tanach.us/Pages/About.html
# import pyperclip
import json
import xmltodict
import pandas as pd
import re

books = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Samuel_1",
    "Samuel_2",
    "Kings_1",
    "Kings_2",
    "Isaiah",
    "Jeremiah",
    "Ezekiel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Psalms",
    "Proverbs",
    "Job",
    "Song_of_Songs",
    "Ruth",
    "Lamentations",
    "Ecclesiastes",
    "Esther",
    "Daniel",
    "Ezra",
    "Nehemiah",
    "Chronicles_1",
    "Chronicles_2",
]

# Remove books that use poetic cantillation marks
books.remove("Job")
books.remove("Proverbs")
books.remove("Psalms")

records = []

# book = "Genesis"

for book in books:
    print(book)
    with open(f"Tanach.xml/books/{book}.xml", "r", encoding="utf-8") as f:
        data_dict = xmltodict.parse(f.read())

    chapters = data_dict["Tanach"]["tanach"]["book"]["c"]

    for i, chapter_item in enumerate(chapters):
        chapter_number = i + 1
        # print(chapter_number)
        try:
            verse_list = chapter_item["v"]
        except:
            Exception(chapter_item)
        for j, verse_item in enumerate(verse_list):
            verse_number = j + 1
            assert type(verse_item["w"]) == list

            filtered_list = []

            for item in verse_item["w"]:
                if isinstance(item, dict) and "#text" in item:
                    filtered_list.append(item["#text"])
                else:
                    filtered_list.append(item)
            verse_text = " ".join(filtered_list)

            records.append(
                {
                    "book_name": book,
                    "chapter": chapter_number,
                    "verse": verse_number,
                    "he2": verse_text,
                }
            )

he2 = pd.DataFrame.from_records(records)
# try:
#     " ".join(verse_item["w"])
# except:
#     print(verse_text)
#     pyperclip.copy(verse_text)
# he.to_pickle("tanakh.pkl")
############################################
# https://www.biblesupersearch.com/bible-downloads/ (json format)
with open("net.json", "r", encoding="utf-8") as f:
    netbible_text = f.read()

records = json.loads(netbible_text)["verses"]
en = pd.DataFrame.from_records(records)


def book_name_map(x):
    _map = {
        "1 Chronicles": "Chronicles_1",
        "2 Chronicles": "Chronicles_2",
        "1 Kings": "Kings_1",
        "2 Kings": "Kings_2",
        "1 Samuel": "Samuel_1",
        "2 Samuel": "Samuel_2",
        "Song of Solomon": "Song_of_Songs",
    }
    if x in _map:
        return _map[x]
    else:
        return x


en["book_name"] = en["book_name"].apply(book_name_map)
en = en.rename(columns={"text": "en"})
en = en.drop("book", axis=1)
############################################
# Hebrew with vowels only i.e., no cantillation
with open("wlc.json", "r", encoding="utf-8") as f:
    netbible_text = f.read()
records = json.loads(netbible_text)["verses"]
he1 = pd.DataFrame.from_records(records)
he1["book_name"] = he1["book_name"].apply(book_name_map)
he1 = he1.rename(columns={"text": "he1"})
he1 = he1.drop("book", axis=1)
############################################
# merges
merged0 = en.merge(
    he2,
    on=["book_name", "chapter", "verse"],
    # indicator=True,
    how="inner",
    validate="one_to_one",  # The standard vlookup style merge
)
merged0["system"] = "translate English to Biblical Hebrew with Cantillation"

merged1 = he1.merge(
    he2,
    on=["book_name", "chapter", "verse"],
    # indicator=True,
    how="inner",
    validate="one_to_one",  # The standard vlookup style merge
)
# Remove paseq #
merged1["he1"] = merged1["he1"].apply(lambda x: x.replace(" ׀", ""))
# Interpret ׃ as a period #
merged1["he1"] = merged1["he1"].apply(lambda x: x.replace("׃", "."))
# Remove maqqaf #
merged1["he1"] = merged1["he1"].apply(lambda x: x.replace("־", " "))


def extract_qeri(text):
    # Remove the options with 'כ'
    text = re.sub(r"\[[^\]]* כ\]", "", text)

    # Replace the 'ק' options by removing the parentheses, 'ק', and preceding space
    text = re.sub(r"\(\s*([^\)]*)\sק\)", r"\1", text)

    text = text.replace("  ", " ")
    return text


merged1["he1"] = merged1["he1"].apply(extract_qeri)


# Remove פ at end of string #
merged1["he1"] = merged1["he1"].apply(
    lambda text: re.sub(f'{re.escape(" פ")}$', "", text)
)

# Remove פ at end of string #
merged1["he1"] = merged1["he1"].apply(
    lambda text: re.sub(f'{re.escape("  ס")}$', "", text)
)


# import pandas as pd

# Sample dataframe with two text columns
# df = pd.DataFrame(
#     {
#         "group": ["A", "A", "B", "B"],
#         "text1": ["Hello", "World", "Goodbye", "Earth"],
#         "text2": ["How", "Are", "You", "Today"],
#     }
# )

# Group by 'group' column and merge the text rows for each text column
# merged1 = (
#     merged1.groupby("chapter").agg({"he1": " ".join, "he2": " ".join}).reset_index()
# )

# merged1['he1_count'] = merged1['he1'].str.split().str.len()
# merged1['he2_count'] = merged1['he2'].str.split().str.len()

# Create a range index from 0 to the length of the DataFrame - 1
index_range = pd.RangeIndex(start=0, stop=len(merged1))

# Assign group numbers by dividing the index by 20 and taking the floor
merged1["group"] = index_range // 20

merged1 = merged1.groupby("group").agg({"he1": " ".join, "he2": " ".join}).reset_index()
merged1["he1_count"] = merged1["he1"].str.split().str.len()
merged1["he2_count"] = merged1["he2"].str.split().str.len()

merged1[
    "system"
] = "add cantillation marks to Hebrew text that is already marked with vowels"


# print(merged_df)

# text = "[אֲכָלָנוּ כ] (אֲכָלַנִי ק) [הֲמָמָנוּ כ] (הֲמָמַנִי ק) נְבוּכַדְרֶאצַּר מֶלֶךְ בָּבֶל [הִצִּיגָנוּ כ] (הִצִּיגַנִי ק) כְּלִי רִיק [בְּלָעָנוּ כ] (בְּלָעַנִי ק) כַּתַּנִּין מִלָּא כְרֵשֹׂו מֵעֲדָנָי [הֱדִיחָנוּ כ] (הֱדִיחָנִי. ק)"


# print(text)


# use(merged1)
# keep('if book_name=="Esther" and chapter==8 and verse==9')
# tmp123 = current.df.iloc[0].he1

# merged = merged.rename(columns={"_merge": "_merge0"})
# merged = merged.merge(
#     he,
#     on=["book_name", "chapter", "verse"],
#     indicator=True,
#     how="outer",
#     validate="one_to_one",  # The standard vlookup style merge
# )

# books_to_drop = [
# ]

# def sample(n):
#     print(current.df.iloc[n].en)
#     pyperclip.copy(current.df.iloc[n].he)
