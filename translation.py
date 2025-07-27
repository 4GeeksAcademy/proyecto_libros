import pandas as pd
from tqdm import tqdm
from langdetect import detect
from deep_translator import GoogleTranslator
from pypinyin import lazy_pinyin
from korean_romanizer.romanizer import Romanizer
import pykakasi

# Detectar idioma de un texto
def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return "unknown"

# Romanización para japonés
def romanizar_jap(texto):
    kks = pykakasi.kakasi()
    resultado = kks.convert(texto)
    return "".join([item['hepburn'] for item in resultado])

# Romanización para coreano
def romanizar_kor(texto):
    r = Romanizer(texto)
    return r.romanize()

# Romanización para chino (pinyin)
def chino_a_pinyin(texto):
    return " ".join(lazy_pinyin(texto))

# Traducción con división para textos largos
def traducir(texto, src="auto", dest="en", max_length=4500):
    if not texto or texto.strip() == "":
        return texto
    
    try:
        return GoogleTranslator(source=src, target=dest).translate(texto)
    except Exception:
        # Si falla (texto muy largo), dividirlo
        print(f"✂️ Fragmentando texto largo para traducir...")
        partes = [texto[i:i+max_length] for i in range(0, len(texto), max_length)]
        traducido = ""
        for parte in partes:
            try:
                traducido += GoogleTranslator(source=src, target=dest).translate(parte) + " "
            except Exception as e:
                print(f"⚠️ Error traduciendo fragmento: {e}")
                traducido += parte + " "
        return traducido.strip()

# Cargar CSV
df = pd.read_csv("data/full_data/libros_completados.csv")

# Procesar cada fila con tqdm
for idx, row in tqdm(df.iterrows(), total=len(df)):
    title = str(row['title'])
    author = str(row['author'])
    description = str(row['description'])
    publisher = str(row['publisher'])

    # Romanizar título
    lang_title = detectar_idioma(title)
    if lang_title == "ja":
        df.at[idx, 'title'] = romanizar_jap(title)
    elif lang_title == "ko":
        df.at[idx, 'title'] = romanizar_kor(title)
    elif lang_title in ["zh-cn", "zh-tw"]:
        df.at[idx, 'title'] = chino_a_pinyin(title)

    # Romanizar autor
    lang_author = detectar_idioma(author)
    if lang_author == "ja":
        df.at[idx, 'author'] = romanizar_jap(author)
    elif lang_author == "ko":
        df.at[idx, 'author'] = romanizar_kor(author)
    elif lang_author in ["zh-cn", "zh-tw"]:
        df.at[idx, 'author'] = chino_a_pinyin(author)

    # Traducir descripción si no está en inglés
    if detectar_idioma(description) != "en":
        df.at[idx, 'description'] = traducir(description)

    # Traducir editorial si no está en inglés
    if detectar_idioma(publisher) != "en":
        df.at[idx, 'publisher'] = traducir(publisher)

# Guardar resultado
df.to_csv("data/full_data/libros_completados.csv", index=False)

print("✅ Traducción y romanización completadas.")