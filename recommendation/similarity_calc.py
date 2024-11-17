from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def calculate_similarity(course_name):
    # 지연 가져오기
    from connection.models import Class

    # 데이터베이스에서 수업 정보 가져오기
    courses = Class.query.all()
    if not courses:
        return None, "No courses available."

    # Convert to DataFrame
    data = [{"name": c.name, "avg_grades": c.avg_grades, "total_grades": c.total_grades, "avg_gpa": c.avg_gpa} for c in courses]
    df = pd.DataFrame(data)

    # Check if the course exists
    if course_name not in df["name"].values:
        return None, f"Course '{course_name}' not found."

    # Normalize features
    features = ["avg_grades", "total_grades", "avg_gpa"]
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[features])
    df_features = pd.DataFrame(df_scaled, columns=features)

    # Find the target course vector
    idx = df[df["name"] == course_name].index[0]
    target_vector = df_features.iloc[idx].values.reshape(1, -1)

    # Calculate cosine similarity
    similarities = cosine_similarity(target_vector, df_features)

    # Add similarity scores to DataFrame
    df["similarity"] = similarities[0]

    # Exclude the target course and return the top 5 similar courses
    recommendations = df[df["name"] != course_name].sort_values(by="similarity", ascending=False).head(5)
    return recommendations[["name", "similarity"]], None
