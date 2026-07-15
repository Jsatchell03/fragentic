import pandas as pd
import numpy as np
import time
import re
import ast
from tqdm import tqdm
from app.services.openai_service import get_embedding, get_many_embeddings
from app.services.db_service import upload_one, dump, get_all, check_match
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(f"{BASE_DIR}/data/fra_cleaned.csv", encoding="Windows-1252", sep=";")
df_sorted = df.sort_values(by="Rating Count", ascending=False)
df = df_sorted

unclean_df = pd.read_csv(f"{BASE_DIR}/data/fra_perfumes.csv", encoding="utf-8", sep=",")

EMBED_DIM = len(get_embedding("test"))

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


w_top, w_mid, w_base = 0.25, 0.30, 0.45
w_notes, w_accords = 0.4, 0.6

# Existing sets
all_brands = set([brand["name"] for brand in get_all("brands")])
all_countries = set([country["name"] for country in get_all("countries")])
all_notes = set([note["name"] for note in get_all("notes")])
all_accords = set([accord["name"] for accord in get_all("accords")])


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
    try:
        row = unclean_df.loc[unclean_df["url"].str.lower() == url, "Main Accords"]
        if not row.empty:
            return [x.lower() for x in ast.literal_eval(str(row.iloc[0]))]
    except Exception:
        pass
    return []


def parse_descriptor(descriptor):
    extra_words = ["accord", "notes"]
    if descriptor in descriptor_map:
        return descriptor_map[descriptor]
    pattern = r"\b(?:" + "|".join(extra_words) + r")\b\.?$"
    cleaned = re.sub(pattern, "", descriptor, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"[\s,;]+$", "", cleaned)
    return cleaned


def accord_vector(accords):
    if not accords:
        return np.zeros(EMBED_DIM)
    weights = np.linspace(len(accords), 1, num=len(accords))
    weights /= weights.sum()
    vecs = np.array(get_many_embeddings(accords))
    return np.sum(vecs * weights[:, np.newaxis], axis=0)


def average_embeddings(vectors, weight=1.0):
    vectors = np.asarray(vectors)
    if vectors.size == 0:
        return np.zeros(EMBED_DIM)
    return weight * np.mean(vectors, axis=0)


# --- Main embedding loop ---
print("Started Embedding")
start_time = time.time()

for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing fragrances"):
    url = safe_str(row.get("url"))

    fragrance = {}
    fragrance["name"] = safe_str(row.get("Perfume"))
    fragrance["url"] = url
    fragrance["rating"] = safe_float(row.get("Rating Value"))
    fragrance["rating_count"] = safe_int(row.get("Rating Count"))
    fragrance["year"] = safe_int(row.get("Year"))
    fragrance["brand"] = safe_str(row.get("Brand"))
    fragrance["gender"] = safe_str(row.get("Gender"))
    fragrance["country"] = safe_str(row.get("Country"))

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
        parse_descriptor(accord) for accord in safe_accords(fragrance["url"])
    ]

    top_vec = average_embeddings(get_many_embeddings(fragrance["top_notes"]), w_top)
    mid_vec = average_embeddings(get_many_embeddings(fragrance["mid_notes"]), w_mid)
    base_vec = average_embeddings(get_many_embeddings(fragrance["base_notes"]), w_base)

    notes_vector = (top_vec + mid_vec + base_vec) * w_notes
    accords_vector = accord_vector(fragrance["accords"]) * w_accords

    fragrance["fragrance_vector"] = (notes_vector + accords_vector).tolist()
    upload_one("fragrances", fragrance)

    # Update sets
    all_countries.add(fragrance["country"])
    all_brands.add(fragrance["brand"])
    all_notes.update(fragrance["top_notes"])
    all_notes.update(fragrance["mid_notes"])
    all_notes.update(fragrance["base_notes"])
    all_accords.update(fragrance["accords"])

print("Updating collections")
dump("countries", [{"name": country} for country in list(all_countries)])
dump("brands", [{"name": brand} for brand in list(all_brands)])
dump("notes", [{"name": note} for note in list(all_notes)])
dump("accords", [{"name": accord} for accord in list(all_accords)])

end_time = time.time()
print(f"✅ Processed {len(df)} fragrances in {end_time - start_time:.2f} seconds")
