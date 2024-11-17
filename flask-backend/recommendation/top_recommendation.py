from flask import Blueprint, jsonify
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# Blueprint 생성
top_recommendation_bp = Blueprint("top_recommendation", __name__)

def get_top_recommendations_from_db():
    # 지연 가져오기
    from connection.models import Class

    # 데이터베이스에서 수업 정보 가져오기
    courses = Class.query.all()
    if not courses:
        return None, "No courses available."

    # Convert to DataFrame
    data = [{"name": c.name, "avg_grades": c.avg_grades, "total_grades": c.total_grades, "avg_gpa": c.avg_gpa} for c in courses]
    df = pd.DataFrame(data)

    # 정규화 대상 특징
    features = ["avg_grades", "total_grades", "avg_gpa"]
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[features])
    df_features = pd.DataFrame(df_scaled, columns=features)

    # 가중치 설정
    weights = {"avg_grades": 0.3, "total_grades": 0.2, "avg_gpa": 0.5}

    # 종합 점수 계산
    df["score"] = (
        df_features["avg_grades"] * weights["avg_grades"] +
        df_features["total_grades"] * weights["total_grades"] +
        df_features["avg_gpa"] * weights["avg_gpa"]
    )

    # 상위 5개 추천
    top_courses = df.sort_values(by="score", ascending=False).head(5)
    return top_courses[["name", "score"]].to_dict(orient="records"), None


