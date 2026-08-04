import pandas as pd
import numpy as np
import time
import re
import ast
import math
from tqdm import tqdm
from pathlib import Path
from app.services import embedding_service, db_service
from app.config import settings
from app.schemas.db_schemas import DescriptorDoc, FragranceDoc

BASE_DIR = Path(__file__).resolve().parent
ACCORD_DECAY = settings.etl.accord_decay
NOTE_WEIGHT = settings.etl.note_weight
ACCORD_WEIGHT = settings.etl.accord_weight
TOP_NOTES_WEIGHT = settings.etl.top_notes_weight
MID_NOTES_WEIGHT = settings.etl.mid_notes_weight
BASE_NOTES_WEIGHT = settings.etl.base_notes_weight
EMBED_DIM = settings.openai.dimensions

df = pd.read_csv(f"{BASE_DIR}/data/fra_cleaned.csv", encoding="Windows-1252", sep=";")
df_sorted = df.sort_values(by="Rating Count", ascending=True)
df = df_sorted.reset_index(drop=True)
unclean_df = pd.read_csv(f"{BASE_DIR}/data/fra_perfumes.csv", encoding="utf-8", sep=",")


descriptor_map = {
    "wild lavender": "lavender",
    "citruses": "citrus",
    "woodsy notes": "wood",
    "sweet notes": "sweet",
    "green accord": "green",
    "cedar essence": "cedar",
    "cedarwood": "cedar",
    "california orange": "orange",
    "oriental notes": "oriental notes",
    "mastic or lentisque": "mastic",
    "mandarin": "mandarin orange",
    "calabrian mandarin": "italian mandarin",
    "sicilian mandarin": "italian mandarin",
    "lily-of-the-valley": "lily of the valley",
    "american apple": "apple",
    "citrus leaf": "citrus leaves",
    "citruses water": "citrus water",
    "citruses with sugar": "sweet citrus",
    "sicilian citruses": "sicilian citrus",
    "cornflower or sultan seeds": "cornflower/sweet sultan seeds",
    "arbutus (madrona, bearberry tree)": "arbutus (madrone/bearberry tree)",
    "agathosma betulina": "agathosma betulina (buchu)",
    "cubeb or tailed pepper": "tailed pepper (cubeb)",
    "christmas tree or flame tree": "flame tree",
    "melilot or sweet clover": "sweet clover (meliot)",
    "woodruff or galium odoratum": "sweet woodruff (galium odoratum)",
    "hamanasu or japanese rose": "japanese rose (hamanasu)",
    "portulaca or pigweed": "portulaca (pigweed)",
    "silk vine or milk broom": "periploca (milk broom/silk vine)",
    "pepperwood or hercules club": "hercules club (pepperwood)",
    "zanthoxylum clava-herculis": "hercules club (pepperwood)",
    "cypriol oil or nagarmotha": "cypriol oil (nagarmotha)",
    "chimonanthus or wintersweet": "chimonanthus (wintersweet)",
    "black hemlock or tsuga": "black hemlock (tsuga mertensiana)",
    "princess tree or paulownia": "princess tree (paulownia tomentosa)",
    "dark woodsy": "dark wood",
    "pepperwood™": "pepperwood",
    "white woods": "white wood",
    "oriental woodsy": "oriental woods",
    "woody": "wood",
    "coton candy": "cotton candy",
    "pine": "pine tree",
    "virginian cedar": "virginian cedar",
    "apple tree blossom": "apple blossom",
    "vanila": "vanilla",
}

brand_map = {
    "de-gabor": "De Gabor",
    "di-ser": "Di Ser",
    "m-int": "M.int",
    "e-coudray": "E.Coudray",
    "ne-emah-for-fragrance-oudh": "Ne'emah For Fragrance & Oudh",
    "fragrance-du-bois": "Fragrance Du Bois",
}

new_fragrances = []
new_descriptors = []
added_descriptor_names = set(db_service.STORED_DESCRIPTOR_NAMES)
added_fragrance_urls = set(db_service.STORED_FRAGRANCE_URLS)

# Pre-build O(1) accords lookup instead of re-scanning unclean_df on every row
url_to_accords = {}
for _, _row in unclean_df.iterrows():
    _url = str(_row.get("url", "")).lower()
    if _url and pd.notna(_row.get("Main Accords")):
        try:
            url_to_accords[_url] = [
                x.lower() for x in ast.literal_eval(str(_row["Main Accords"]))
            ]
        except Exception:
            pass


# --- Helper functions ---
def safe_str(val, default=""):
    return str(val).lower().strip() if pd.notna(val) else default


def safe_float(val, default=0.0):
    try:
        return float(str(val).replace(",", ".")) if pd.notna(val) else default
    except Exception:
        return default


def safe_int(val, default=0):
    try:
        return int(val) if pd.notna(val) else default
    except Exception:
        return default


def clean_note(text: str) -> str:
    text = text.strip().lower()
    match = re.search(r"\((.*?)\)", text)
    return match.group(1).strip() if match else text


def safe_list(val):
    if pd.isna(val) or not isinstance(val, str):
        return []
    # split only on commas that are not inside parentheses
    parts = re.split(r",\s*(?![^()]*\))", val)
    return [clean_note(x) for x in parts if x.strip()]


def safe_accords(url):
    return url_to_accords.get(url, [])


def parse_descriptor(descriptor):
    extra_words = ["accord", "notes"]
    if descriptor in descriptor_map:
        return descriptor_map[descriptor]
    pattern = r"\b(?:" + "|".join(extra_words) + r")\b\.?$"
    cleaned = re.sub(pattern, "", descriptor, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"[\s,;]+$", "", cleaned)
    return cleaned


def calculate_accords_vector(accord_descriptors):
    if not accord_descriptors:
        return np.zeros(EMBED_DIM)
    vecs = np.array([d.np_vector for d in accord_descriptors])
    weights = ACCORD_DECAY ** np.arange(len(vecs))
    weights /= weights.sum()
    return np.sum(vecs * weights[:, np.newaxis], axis=0)


def calculate_popularity(index):
    percentile = index / len(df_sorted)
    quintile = math.floor(percentile * 5) + 1
    return min(quintile, 5)


def parse_brand(brand: str):
    clean_str = safe_str(brand)
    if clean_str in brand_map:
        return brand_map[clean_str]

    split_str = clean_str.split("-")
    words = []
    for i in range(len(split_str)):
        if split_str[i] == "":
            continue
        if split_str[i] == "di" or split_str[i] == "de" or split_str[i] == "et":
            words.append(split_str[i])
            continue

        if i > 0 and (split_str[i] == "la" or split_str[i] == "du"):
            words.append(split_str[i])
            continue

        if i > 0 and i < len(split_str) - 1 and split_str[i] == "d":
            words.append(split_str[i] + "'" + split_str[i + 1].capitalize())
            split_str[i + 1] = ""
            continue

        words.append(split_str[i].capitalize())
    return " ".join(words)


def parse_name(name: str):
    clean_str = safe_str(name)

    split_str = clean_str.split("-")
    words = []
    for i in range(len(split_str)):
        if split_str[i] == "":
            continue
        if split_str[i] == "di" or split_str[i] == "de" or split_str[i] == "et":
            words.append(split_str[i])
            continue

        if i > 0 and (split_str[i] == "la" or split_str[i] == "du"):
            words.append(split_str[i])
            continue

        if i > 0 and i < len(split_str) - 1 and split_str[i] == "d":
            words.append(split_str[i] + "'" + split_str[i + 1].capitalize())
            split_str[i + 1] = ""
            continue

        words.append(split_str[i].capitalize())
    return " ".join(words)


# --- Main embedding loop ---
print("Started Embedding")
start_time = time.time()

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing fragrances"):
    url = safe_str(row.get("url"))
    if url in added_fragrance_urls:
        print(f"{parse_name(row.get("Perfume"))} already in db")
        continue
    fragrance = {}
    fragrance["name"] = parse_name(row.get("Perfume"))
    fragrance["fragrantica_url"] = url
    fragrance["rating"] = safe_float(row.get("Rating Value"))
    fragrance["rating_count"] = safe_int(row.get("Rating Count"))
    year = safe_int(row.get("Year"))
    if year == 0:
        fragrance["year"] = None
    else:
        fragrance["year"] = year
    fragrance["brand"] = parse_brand(row.get("Brand"))
    fragrance["gender"] = safe_str(row.get("Gender"))
    fragrance["country"] = safe_str(row.get("Country"))
    fragrance["popularity"] = calculate_popularity(idx)
    fragrance["top_notes"] = [
        parse_descriptor(note) for note in safe_list(row.get("Top"))
    ]
    fragrance["mid_notes"] = [
        parse_descriptor(note) for note in safe_list(row.get("Middle"))
    ]
    fragrance["base_notes"] = [
        parse_descriptor(note) for note in safe_list(row.get("Base"))
    ]
    fragrance["accords"] = [
        parse_descriptor(accord)
        for accord in safe_accords(fragrance["fragrantica_url"])
    ]

    t_end = len(fragrance["top_notes"])
    m_end = t_end + len(fragrance["mid_notes"])
    b_end = m_end + len(fragrance["base_notes"])

    all_descriptors = embedding_service.embed_descriptors(
        fragrance["top_notes"]
        + fragrance["mid_notes"]
        + fragrance["base_notes"]
        + fragrance["accords"]
    )

    top_notes_vector = embedding_service.avg_vectors(
        [d.np_vector for d in all_descriptors[:t_end]]
    )
    mid_notes_vector = embedding_service.avg_vectors(
        [d.np_vector for d in all_descriptors[t_end:m_end]]
    )
    base_notes_vector = embedding_service.avg_vectors(
        [d.np_vector for d in all_descriptors[m_end:b_end]]
    )
    accords_vector = calculate_accords_vector(all_descriptors[b_end:])

    notes_vector = (
        top_notes_vector * TOP_NOTES_WEIGHT
        + mid_notes_vector * MID_NOTES_WEIGHT
        + base_notes_vector * BASE_NOTES_WEIGHT
    )

    fragrance_vector = notes_vector * NOTE_WEIGHT + accords_vector * ACCORD_WEIGHT

    fragrance["fragrance_vector"] = embedding_service.l2_normalize(
        fragrance_vector
    ).tolist()

    fragrance["top_notes_vector"] = embedding_service.l2_normalize(
        top_notes_vector
    ).tolist()

    fragrance["mid_notes_vector"] = embedding_service.l2_normalize(
        mid_notes_vector
    ).tolist()

    fragrance["base_notes_vector"] = embedding_service.l2_normalize(
        base_notes_vector
    ).tolist()

    fragrance["accords_vector"] = embedding_service.l2_normalize(
        accords_vector
    ).tolist()

    seen_in_fragrance: set[str] = set()
    new_from_fragrance = []
    for d in all_descriptors:
        if d.name not in added_descriptor_names and d.name not in seen_in_fragrance:
            new_from_fragrance.append(DescriptorDoc(name=d.name, vector=d.list_vector))
            seen_in_fragrance.add(d.name)

    if new_from_fragrance:
        new_descriptors.extend(new_from_fragrance)
        added_descriptor_names.update(d.name for d in new_from_fragrance)

    new_fragrances.append(FragranceDoc(**fragrance))
    added_fragrance_urls.add(fragrance["fragrantica_url"])
end_time = time.time()

print(f"✅ Processed {len(df)} fragrances in {end_time - start_time:.2f} seconds")

print("Uploading to mongo")
if len(new_descriptors) > 0:
    db_service.upload_descriptors(new_descriptors)
    print("Descriptors uploaded")
else:
    print("No new descriptors")

if len(new_fragrances) > 0:
    db_service.upload_fragrances(new_fragrances)
    print("Fragrances uploaded")
else:
    print("No new fragrances")
