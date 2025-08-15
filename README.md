# The Book Recommendation System

Helping readers find their next favourite book through AI-powered recommendations.

## Introduction

In a world overflowing with books, choosing what to read next can be overwhelming. Despite the abundance of options, reading habits are in decline: in Australia, nearly 30% of the population did not read or listen to a single book in the past year, while in the UK, up to 40% reported the same. At the same time, the global recommendation engine market — valued at USD 6.3 billion in 2024 — is expected to grow exponentially in the coming decade, driven by the demand for personalization.

This project addresses both challenges: helping readers rediscover the joy of reading while leveraging data science and machine learning to deliver tailored book recommendations. Our goal is to reduce decision fatigue, motivate new reading habits, and support commercial platforms in optimizing their catalogues and user engagement.

To achieve this, we built a comprehensive, up-to-date dataset by combining Goodreads’ data (last updated in 2020) with fresh information retrieved from Open Library and Google Books APIs. We expanded the dataset with multiple genres and languages, ensuring our recommender system can serve a diverse and global audience.

## Data

At the start of this project, no complete, up-to-date database for our purposes existed. While GoodReads offered a rich dataset, its latest update was from 2020. To ensure our recommendation system worked with current information, we enriched it with data from Open Library and Google Books APIs, covering publications up to July 2025.

We began by defining a list of genres to include in our system and the fields for the final dataset:

| **Genres**              | **Dataset Fields**         |
|-------------------------|----------------------------|
| Fiction                 | Title                      |
| Historical Fiction      | Original Title              |
| Mystery                 | Author(s)                   |
| Thriller                | Series                      |
| Romance                 | Pages                       |
| Fantasy                 | Cover                       |
| Romantasy               | Release Date                |
| Science Fiction         | Publisher                   |
| Horror                  | Original Language           |
| Young Adult             | ISBN                        |
| Non Fiction             | Genre                       |
| Memoir                  | Stars                       |
| Autobiography           | Ratings                     |
| History                 | Reviews                     |
| Biography               | Format                      |
| Humor                   | Physical Format             |
| Gay                     | Awards                      |
| LGBT                    | Setting                     |
| Queer                   | Places                      |
| Paranormal              | Number of Editions          |
| Historical Romance      |                            |
| Contemporary            |                            |
| Classic                 |                            |
| Comics                  |                            |
| Manga                   |                            |
| True Crime              |                            |
| Poetry                  |                            |
| Graphic Novels          |                            |
| Adventure               |                            |

Since the Google Books API proved limited, we later expanded the genre list and added books in multiple languages, including: Spanish, Portuguese, German, Italian, French, Chinese, Japanese, and Korean.

The raw dataset initially contained 21 columns and 74,789 rows. After extensive data cleaning and preprocessing, the final dataset contained 57,305 rows of high-quality, relevant records.

### Cleaning process included:

- **Missing values**: Replaced with NaN as a first step.  
- **Removed columns**: ISBN, BookId, Number of ratings, % of Likes, Settings, and Characters.  
- **Duplicates**: Checked for duplicate titles/authors while keeping different volumes in series.  
- **Series**: Missing values replaced with "Standalone Novel".  
- **Awards**: Converted into a boolean column.  
- **Format**: Missing values replaced with "Paperback".  
- **Description**: Removed rows without descriptions.  
- **Language codes**: Standardized to ISO format.  
- **Pages**: Removed null values and converted to integers.  
- **Publisher**: Removed null values.  
- **Publish Date & First Publish Date**: Standardized date format.  
- **Cover image**: Removed rows with missing values.  

## Advanced preprocessing and feature engineering

Before imputing missing ratings, we performed several transformations to optimize model performance:

- **Genre parsing**: Converted string genre lists into Python lists.  
- **Categorical encoding**: Applied LabelEncoder separately to series, language, bookFormat.  
- **Boolean conversion**: Converted awards and firstPublishDate to booleans.  
- **Author-based feature**: Created `author_rating` column.  
- **Genre one-hot encoding**: Used MultiLabelBinarizer to transform genres into binary columns.  

### Imputation of missing ratings using KNN

- **Features used**: series, language, bookFormat, firstPublishDate, awards, author_rating, plus one-hot genres.  
- **Training data**: Books with existing ratings.  
- **Prediction target**: Ratings of books with missing values.  
- **k parameter**: k = 2.  

This allowed us to preserve dataset size and diversity.

## Methodology

We implemented three different recommendation approaches:

### 1. QUICK PICK – Baseline filtering system

**Objective**: Provide fast and simple recommendations based on explicit preferences.  

**Approach**:  
- Genre filtering  
- Author exclusion  
- Language filtering  
- Minimum rating threshold  
- Sorting and deduplication  

**Pros**: Fast, transparent  
**Cons**: No deep personalization  

### 2. SMART MATCH – KNN-based collaborative/content hybrid filtering

**Objective**: Recommendations based on genre similarity.  

**Approach**:  
- Genre encoding with MultiLabelBinarizer  
- Cosine similarity  
- NearestNeighbors model  

**Pros**: Flexible, captures implicit relationships  
**Cons**: Relies on accurate genre tagging  

### 3. DEEP DIVE – NLP-powered semantic search using FAISS

**Objective**: Recommendations based on full semantic meaning of descriptions and genres.  

**Approach**:  
- SentenceTransformer embeddings  
- FAISS index with cosine similarity  
- Free-text queries + filters  

**Strengths**: Captures complex intent, scalable  
**Limitations**: Requires robust descriptions, more computation  

## Project Structure

PROYECTO 
```
├── .streamlit
│   └── config.toml
├── .vscode
│   └── settings.json
├── data
│   ├── final_data
│   │   ├── df_web.csv
│   │   ├── embeddings.npy
│   │   └── faiss_index.idx
├── EDA
│   ├── eda1.ipynb
│   ├── eda2.ipynb
│   └── busqueda.ipynb
```

- In **streamlit**, the main color has been defined.  
- In **data**, we have saved all the endings with which we have already executed the project, including the final df and the embedding and faiss index from the FAISS section.  
- In the **EDA** folder, you will find the search files in which we have merged data from Google Books and Open Library with our main Data Frame.  
  - In `eda1`, we have done an intensive clean-up and created graphs with results.  
  - In `eda2`, we have realized the model.  

```
├── full_data
│   ├── datos
│   │   ├── data_2020_2025.py
│   │   └── data_2020.ipynb
│   └── full_data.ipynb
```

- In **full_data**, we have combined the main df (which only had data up to 2020) with another df that includes data from 2020 to 2025.

```
├── images
├── Models
│   ├── __pycache__
│   ├── all-MiniLM-L6-v2
│   │   ├── __init__.py
│   │   ├── cribado.py
│   │   ├── faiss_module.py
│   │   └── knn_module.py
├── notebooks
│   ├── basic_model.ipynb
│   ├── faiss_ok.ipynb
│   └── KNN.ipynb
├── pages
│   ├── 1_Quick_Pick.py
│   ├── 2_Smart_Match.py
│   └── 3_Deep_Dive.py
```

- **images** contains all the images displayed in the interface.  
- **Models** contains the three main files for each model we created:  
  - `cribado.py` → used in `pages/1_Quick_Pick.py`  
  - `knn_module.py` → used in `pages/2_Smart_Match.py`  
  - `faiss_module.py` → used in `pages/3_Deep_Dive.py`  
- The **all-MiniLM-L6-v2** folder stores a local copy of the embeddings model downloaded with SentenceTransformer.  
- **notebooks** are the raw experimental files from the beginning, later converted into `.py` files for `/Models`.  

```
├── utils
│   ├── __pycache__
│   ├── __init__.py
│   ├── cards.py
│   ├── home_style.py
│   ├── inner_pages.py
│   ├── language.py
│   ├── sorting.py
│   ├── time_out.py
│   └── translation.py
```

- **utils** contains shared files across multiple pages:  
  - `home_style.py` → CSS styles for the home page.  
  - `inner_pages.py` → CSS styles for internal pages.  
  - `cards.py` → formatting for book results (shared by all three pages).  
  - `language.py` → mapping between language names and ISO codes.  
  - `sorting.py` → prioritizes sorting (letters, numbers, symbols, empty).  
  - `time_out.py` → infinite keep-alive loop to prevent inactivity shutdown.  
  - `translation.py` → romanizes Japanese, Korean, and Chinese text to Latin characters.  

```
├── download_model.py
├── Home.py
├── README.md
├── requirements.txt
└── runtime.txt
```

- `download_model.py` → downloads and saves the embeddings model locally.  
- `Home.py` → main entry point for the app.  
- `requirements.txt` → lists all necessary dependencies.  
- `runtime.txt` → stores the Python version used after a conflict resolution.

## Conclusions

This project taught us about imperfect data, iterative problem-solving, and adapting to hurdles.  
We learned that APIs like Google Books/Open Library have limitations, ISBNs were unreliable, and balancing simplicity with sophistication in models is tricky.

## Future Work

- Retry translating/normalizing dataset to English with a more automated pipeline.  
- Source better datasets.  
- Combine recommendation models into a hybrid.  
- Incorporate user feedback to fine-tune.  
- Optimize performance with cached embeddings.  
- Implement true multilingual support.

## Contact:

- *Elena*: https://www.linkedin.com/in/elenasanchez25/
- *Noemí*: https://www.linkedin.com/in/noem%C3%AD-g%C3%B3mez-bouzada/
- *Sami*:  https://www.linkedin.com/in/samillyamarante/
