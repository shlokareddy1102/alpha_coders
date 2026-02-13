from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

# The sentences to encode
jd = [
   "Looking for a Machine Learning engineer with Python experience"
]
students = [
    "Python, SQL, Machine Learning, NLP project",
    "Java, Spring Boot, Backend development, REST APIs",
    "React, JavaScript, Frontend development, UI design"
]
# 2. Calculate embeddings by calling model.encode()
student_embeddings = model.encode(students)
jd_embeddings=model.encode(jd)

# [3, 384]

# 3. Calculate the embedding similarities
similarities = model.similarity( jd_embeddings,student_embeddings)
for i, score in enumerate(similarities[0]):
    print(f"Student {i+1} similarity score: {score:.4f}")
