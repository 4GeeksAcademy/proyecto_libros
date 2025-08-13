# utils/languages.py
LANG_VARIANTS_TO_ISO = {
    # EN
    'english': 'en', 'english, middle (1100-1500)': 'en', 'en': 'en',
    # FR
    'french': 'fr', 'french, middle (ca.1400-1600)': 'fr', 'fr': 'fr',
    # DE
    'german': 'de', 'de': 'de',
    # FA (Persian/Farsi)
    'persian': 'fa', 'farsi': 'fa', 'fa': 'fa', 'iranian (other)': 'fa',
    # AR
    'arabic': 'ar', 'ar': 'ar',
    # ES
    'spanish': 'es', 'es': 'es',
    # MULTIPLE
    'multiple languages': 'mul',
    # PT / PT-BR
    'portuguese': 'pt', 'pt-br': 'pt', 'pt': 'pt',
    # IT
    'italian': 'it', 'it': 'it',
    # RO
    'romanian': 'ro', 'ro': 'ro',
    # TR
    'turkish': 'tr', 'tr': 'tr',
    # PL
    'polish': 'pl', 'pl': 'pl',
    # BG
    'bulgarian': 'bg', 'bg': 'bg',
    # TA
    'tamil': 'ta', 'ta': 'ta',
    # JA
    'japanese': 'ja', 'ja': 'ja',
    # NO
    'norwegian': 'no', 'bokmål, norwegian; norwegian bokmål': 'no',
    'norwegian nynorsk; nynorsk, norwegian': 'no', 'no': 'no',
    # UR
    'urdu': 'ur',
    # NL
    'dutch': 'nl', 'dutch, middle (ca.1050-1350)': 'nl', 'nl': 'nl',
    # FI
    'finnish': 'fi', 'fi': 'fi',
    # MR
    'marathi': 'mr',
    # ZH
    'chinese': 'zh', 'zh-cn': 'zh',
    # SV
    'swedish': 'sv', 'sv': 'sv',
    # IS
    'icelandic': 'is',
    # ML
    'malayalam': 'ml',
    # HR
    'croatian': 'hr',
    # ET
    'estonian': 'et',
    # EL / GRC
    'greek, modern (1453-)': 'el', 'greek, ancient (to 1453)': 'grc',
    # RU
    'russian': 'ru', 'ru': 'ru',
    # KU
    'kurdish': 'ku',
    # DA
    'danish': 'da', 'da': 'da',
    # HI
    'hindi': 'hi',
    # TL
    'filipino; pilipino': 'tl', 'tagalog': 'tl', 'tl': 'tl',
    # SR
    'serbian': 'sr', 'sr': 'sr',
    # BN
    'bengali': 'bn',
    # MS
    'malay': 'ms', 'ms': 'ms',
    # CA
    'catalan; valencian': 'ca', 'ca': 'ca',
    # CS
    'czech': 'cs', 'cs': 'cs',
    # VI
    'vietnamese': 'vi', 'vi': 'vi',
    # HY
    'armenian': 'hy',
    # KA
    'georgian': 'ka',
    # KN
    'kannada': 'kn',
    # KO
    'korean': 'ko', 'ko': 'ko',
    # NE
    'nepali': 'ne',
    # SK
    'slovak': 'sk',
    # TE
    'telugu': 'te',
    # HU
    'hungarian': 'hu', 'hu': 'hu',
    # AZ
    'azerbaijani': 'az',
    # LT
    'lithuanian': 'lt', 'lt': 'lt',
    # UK
    'ukrainian': 'uk',
    # FO
    'faroese': 'fo',
    # EU
    'basque': 'eu',
    # ID
    'indonesian': 'id', 'id': 'id',
    # MK
    'macedonian': 'mk',
    # MT
    'maltese': 'mt',
    # GU
    'gujarati': 'gu', 'gu': 'gu',
    # AM
    'amharic': 'am',
    # SQ
    'albanian': 'sq', 'sq': 'sq',
    # AS
    'assamese': 'as',
    # PA
    'panjabi; punjabi': 'pa',
    # LV
    'latvian': 'lv',
    # BS
    'bosnian': 'bs',
    # TH
    'thai': 'th', 'th': 'th',
    # AF
    'afrikaans': 'af',
    # MN
    'mongolian': 'mn',
    # GL
    'galician': 'gl', 'gl': 'gl',
    # SL
    'slovenian': 'sl', 'sl': 'sl',
    # Otros/familias
    'aromanian; arumanian; macedo-romanian': 'rup',
    'may languages': 'myn', 'australian languages': 'aus',
    'duala': 'dua', 'aleut': 'ale',
    # Undetermined
    'un': 'und', 'undetermined': 'und'
}

ISO_TO_LANG = {
    'en':'English','fr':'French','de':'German','fa':'Persian','ar':'Arabic','es':'Spanish',
    'mul':'Multiple languages','pt':'Portuguese','it':'Italian','ro':'Romanian','tr':'Turkish',
    'pl':'Polish','bg':'Bulgarian','ta':'Tamil','ja':'Japanese','no':'Norwegian','ur':'Urdu',
    'nl':'Dutch','fi':'Finnish','mr':'Marathi','zh':'Chinese','sv':'Swedish','is':'Icelandic',
    'ml':'Malayalam','hr':'Croatian','et':'Estonian','el':'Greek','grc':'Ancient Greek',
    'ru':'Russian','ku':'Kurdish','da':'Danish','hi':'Hindi','tl':'Tagalog / Filipino',
    'sr':'Serbian','bn':'Bengali','ms':'Malay','ca':'Catalan / Valencian','cs':'Czech',
    'vi':'Vietnamese','hy':'Armenian','ka':'Georgian','kn':'Kannada','ko':'Korean','ne':'Nepali',
    'sk':'Slovak','te':'Telugu','hu':'Hungarian','az':'Azerbaijani','lt':'Lithuanian',
    'uk':'Ukrainian','fo':'Faroese','eu':'Basque','id':'Indonesian','mk':'Macedonian',
    'mt':'Maltese','gu':'Gujarati','am':'Amharic','sq':'Albanian','as':'Assamese','pa':'Punjabi',
    'lv':'Latvian','bs':'Bosnian','th':'Thai','af':'Afrikaans','mn':'Mongolian','gl':'Galician',
    'sl':'Slovenian','rup':'Aromanian (Macedo-Romanian)','myn':'Mayan languages',
    'aus':'Australian languages','dua':'Duala','ale':'Aleut','und':'Undetermined'
}

def lang_to_iso(value: str) -> str:
    s = value.strip().lower() if isinstance(value, str) else ''
    if not s:
        return 'und'
    if s in LANG_VARIANTS_TO_ISO:
        return LANG_VARIANTS_TO_ISO[s]
    if '-' in s:  # ej. pt-br, en-us, zh-cn
        base = s.split('-')[0]
        if base in ISO_TO_LANG:
            return base
    if s in ISO_TO_LANG:
        return s
    return 'und'

def iso_to_display(code: str) -> str:
    return ISO_TO_LANG.get(code, code.upper())
