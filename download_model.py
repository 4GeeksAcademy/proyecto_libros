from sentence_transformers import SentenceTransformer

# Descarga el modelo una vez
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Lo guarda en una carpeta local dentro del repo
model.save("./models/all-MiniLM-L6-v2")
