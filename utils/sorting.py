import unicodedata
import pandas as pd

def _lns_rank(s: str):
    """
    Devuelve (grupo, clave_normalizada) donde:
    grupo: 0=letra, 1=número, 2=símbolo, 3=vacío.
    """
    s = "" if s is None else str(s).strip()
    if not s:
        return (3, "")
    ch = s[0]
    group = 0 if ch.isalpha() else (1 if ch.isdigit() else 2)
    s_norm = unicodedata.normalize("NFKD", s)
    s_norm = "".join(c for c in s_norm if not unicodedata.combining(c))
    return (group, s_norm.casefold())

def sort_lns_iterable(iterable):
    """Ordena por letras → números → símbolos."""
    return sorted(iterable, key=_lns_rank)

def sort_df_by_title_lns(df: pd.DataFrame) -> pd.DataFrame:
    """Ordena un DataFrame por título con prioridad letras→números→símbolos."""
    tmp = df.copy()
    keys = tmp["title"].apply(_lns_rank)
    tmp["__grp"] = keys.apply(lambda t: t[0])
    tmp["__norm"] = keys.apply(lambda t: t[1])
    tmp = tmp.sort_values(by=["__grp", "__norm", "title"], ascending=[True, True, True])
    return tmp.drop(columns=["__grp", "__norm"])
