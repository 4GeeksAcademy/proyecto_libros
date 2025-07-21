import pandas as pd
from tqdm import tqdm
from langdetect import detect
from deep_translator import GoogleTranslator
from pypinyin import lazy_pinyin
from korean_romanizer.romanizer import Romanizer
import pykakasi

def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return "unknown"

def romanizar_jap(texto):
    kks = pykakasi.kakasi()
    resultado = kks.convert(texto)
    return "".join([item['hepburn'] for item in resultado])

def romanizar_kor(texto):
    r = Romanizer(texto)
    return r.romanize()

def chino_a_pinyin(texto):
    return " ".join(lazy_pinyin(texto))

def traducir(texto, src="auto", dest="en"):
    try:
        return GoogleTranslator(source=src, target=dest).translate(texto)
    except Exception as e:
        print(f"Error traduciendo: {e}")
        return texto

df = pd.read_csv("books_2020_to_2025.csv")

for idx, row in tqdm(df.iterrows()):
    title = str(row['Title'])
    author = str(row['Author(s)'])
    description = str(row['Description'])
    publisher = str(row['Publisher'])

    lang_title = detectar_idioma(title)
    if lang_title == "ja":
        df.at[idx, 'Title'] = romanizar_jap(title)
    elif lang_title == "ko":
        df.at[idx, 'Title'] = romanizar_kor(title)
    elif lang_title in ["zh-cn", "zh-tw"]:
        df.at[idx, 'Title'] = chino_a_pinyin(title)

    lang_author = detectar_idioma(author)
    if lang_author == "ja":
        df.at[idx, 'Author(s)'] = romanizar_jap(author)
    elif lang_author == "ko":
        df.at[idx, 'Author(s)'] = romanizar_kor(author)
    elif lang_author in ["zh-cn", "zh-tw"]:
        df.at[idx, 'Author(s)'] = chino_a_pinyin(author)

    df.at[idx, 'Description'] = traducir(description)
    df.at[idx, 'Publisher'] = traducir(publisher)

df.to_csv("books_2020_to_2025_translated.csv", index=False)

print("Traducción y romanización completadas.")
