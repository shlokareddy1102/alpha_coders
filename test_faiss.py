from faiss_engine import register_student, match_jd, remove_student

# Add students
register_student(101, "Python, SQL, Machine Learning, NLP project")
register_student(102, "Java, Spring Boot, Backend development")
register_student(103, "React, JavaScript, Frontend UI design")

# Test matching
jd = "Looking for Machine Learning engineer with Python experience"

results = match_jd(jd)

print("\nRanking:")
for r in results:
    print(r)

# Optional: Remove a student
# remove_student(102)
