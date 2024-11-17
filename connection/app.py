import sys
import os

# CS-INSIDE 루트를 Python 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from connection.models import db, User, Class, UserClasses
from connection.config import Config
from connection.initialize_db import initialize_database
from recommendation.similarity_calc import calculate_similarity
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)

# 초기화 SQLAlchemy
db.init_app(app)

@app.route('/')
def home():
    return "Flask app connected to PostgreSQL!"

# 학생 추가 API
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(user_name=data['user_name'], email=data.get('email'), password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!", "user_id": new_user.user_id}), 201

# 수업 추가 API
@app.route('/add_class', methods=['POST'])
def add_class():
    data = request.json
    new_class = Class(
        uuid=data['uuid'], name=data['name'], number=data['number'],
        subject=data['subject'], instructors=data.get('instructors'),
        avg_grades=data.get('avg_grades'), total_grades=data.get('total_grades'),
        avg_gpa=data.get('avg_gpa')
    )
    db.session.add(new_class)
    db.session.commit()
    return jsonify({"message": "Class added successfully!", "class_id": new_class.uuid}), 201

# 학생과 수업 연결 API
@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.json
    new_enrollment = UserClasses(user_id=data['user_id'], class_id=data['class_id'])
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify({"message": "User enrolled in class successfully!"}), 201

# 데이터 조회 API
@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"user_id": user.user_id, "user_name": user.user_name, "email": user.email} for user in users])

@app.route('/students_in_class/<string:class_name>', methods=['GET'])
def get_students_in_class(class_name):
    # Query to find students in the specified class
    students = (
        db.session.query(User.user_id, User.user_name, User.email)
        .join(UserClasses, User.user_id == UserClasses.user_id)
        .join(Class, UserClasses.class_id == Class.uuid)
        .filter(Class.name == class_name)
        .all()
    )

    # Convert query results to a list of dictionaries
    student_list = [{"user_id": s.user_id, "user_name": s.user_name, "email": s.email} for s in students]

    if not student_list:
        return jsonify({"message": f"No students found in class '{class_name}'"}), 404

    return jsonify({"class_name": class_name, "students": student_list}), 200

# 유사한 수업 추천 API
@app.route('/similar_courses/<string:course_name>', methods=['GET'])
def similar_courses(course_name):
    recommendations, error = calculate_similarity(course_name)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({
        "course_name": course_name,
        "recommendations": recommendations.to_dict(orient="records")
    }), 200

# 상위 추천 수업 API
@app.route('/top_recommendations', methods=['GET'])
def top_recommendations():
    # 데이터베이스에서 수업 정보 가져오기
    courses = Class.query.all()
    if not courses:
        return jsonify({"error": "No courses available."}), 404

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
    recommendations = top_courses[["name", "score"]].to_dict(orient="records")

    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    initialize_database(app)  # 데이터베이스 초기화
    app.run(debug=True)
