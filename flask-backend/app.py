import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from connection.models import db, User, Class, UserClasses
from connection.config import Config
from connection.initialize_db import initialize_database
from recommendation.similarity_calc import calculate_similarity
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import google.generativeai as genai
import requests
from datetime import datetime
import re




app = Flask(__name__)
CORS(app)

# Flask 앱 설정
app.config.from_object(Config)

# SQLAlchemy 초기화
db.init_app(app)

# 환경 변수에서 API 키 가져오기
GEMINI_API_KEY = "AIzaSyAdi-HBKUXqWJgmJkHKWs2yP7FSBrctTZM"
VISUAL_CROSSING_API_KEY = "T8QMW932J97JVZUFTVQG5KCXT"
MADGRADES_API_TOKEN = "758621a952db42dba100fcb6b25580f3"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. 환경 변수에 API 키를 추가하세요.")

# Gemini API 초기화
genai.configure(api_key=GEMINI_API_KEY)

headers = {
    "Authorization": f"Token token={MADGRADES_API_TOKEN}"
}

@app.route('/')
def home():
    return "Flask app connected to PostgreSQL and integrated with AI & Weather APIs!"

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
    students = (
        db.session.query(User.user_id, User.user_name, User.email)
        .join(UserClasses, User.user_id == UserClasses.user_id)
        .join(Class, UserClasses.class_id == Class.uuid)
        .filter(Class.name == class_name)
        .all()
    )
    student_list = [{"user_id": s.user_id, "user_name": s.user_name, "email": s.email} for s in students]
    if not student_list:
        return jsonify({"message": f"No students found in class '{class_name}'"}), 404
    return jsonify({"class_name": class_name, "students": student_list}), 200

# # 유사한 수업 추천 API
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
    courses = Class.query.all()
    if not courses:
        return jsonify({"error": "No courses available."}), 404
    data = [{"name": c.name, "avg_grades": c.avg_grades, "total_grades": c.total_grades, "avg_gpa": c.avg_gpa} for c in courses]
    df = pd.DataFrame(data)
    features = ["avg_grades", "total_grades", "avg_gpa"]
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[features])
    df_features = pd.DataFrame(df_scaled, columns=features)
    weights = {"avg_grades": 0.3, "total_grades": 0.2, "avg_gpa": 0.5}
    df["score"] = (
        df_features["avg_grades"] * weights["avg_grades"] +
        df_features["total_grades"] * weights["total_grades"] +
        df_features["avg_gpa"] * weights["avg_gpa"]
    )
    top_courses = df.sort_values(by="score", ascending=False).head(5)
    recommendations = top_courses[["name", "score"]].to_dict(orient="records")
    return jsonify({"recommendations": recommendations})


@app.route('/generate', methods=['POST'])
def generate_response():
    """
    자유로운 대화를 포함한 질문에 대한 응답 처리.
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Invalid request"}), 400

    question = data['question'].lower().strip()
    print(f"DEBUG: Received question: {question}")

    try:
        # 키워드 기반 특별 처리
        if "weather" in question or "날씨" in question:
            return get_weather_response()
        elif "time" in question or "시간" in question:
            return get_time_response()
        elif "day" in question or "날짜" in question or "요일" in question:
            return get_day_response()

        # Gemini API를 통한 자유 대화
        print("DEBUG: Sending to Gemini API")
        response = gemini_generate_response(question)
        print(f"DEBUG: Gemini response: {response}")

        return jsonify({"answer": response}), 200

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def gemini_generate_response(question):
    """
    Gemini API를 호출하여 자유로운 대화를 처리.
    """
    try:
        # Gemini 모델 호출
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            question,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,  # 단일 응답
                stop_sequences=['x'],  # 응답 종료 조건
                temperature=1.0  # 응답의 창의성 조정
            )
        )

        # 응답 내용 추출
        return response.text.strip() + " cheezzz 🐭!"

    except Exception as e:
        print(f"ERROR: Gemini API failed: {str(e)}")
        return "Sorry, I couldn't generate a response right now. Please try again later."


def get_weather_response():
    data = request.get_json()
    location = data.get('location', 'Madison, USA').strip()
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"
    params = {"unitGroup": "metric", "key": VISUAL_CROSSING_API_KEY, "contentType": "json"}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            current_conditions = weather_data.get("currentConditions", {})
            temperature = current_conditions.get("temp")
            description = current_conditions.get("conditions")
            weather_message = (
                f"The current weather in {location} is {description} with a temperature of {temperature}°C cheezzz 🐭!"
            )
            return jsonify({"answer": weather_message})
        else:
            return jsonify({"error": "Failed to fetch weather information."}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def get_time_response():
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_message = f"The current date and time is {current_datetime} cheezzz 🐭!"
    return jsonify({"answer": time_message})

def get_day_response():
    current_date = datetime.now().strftime("%A, %Y-%m-%d")
    day_message = f"Today is {current_date} cheezzz 🐭!"
    return jsonify({"answer": day_message})



def similar_courses(course_name):
    """
    특정 수업 이름에 대해 유사한 수업을 추천.
    """
    print("trying")
    try:
        recommendations, error = calculate_similarity(course_name)
        if error:
            return jsonify({"error": f"No similar courses found for '{course_name}'."}), 404

        return jsonify({
            "course_name": course_name,
            "recommendations": recommendations.to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500






# 수업 이름 추출 도우미 함수
def extract_course_name_for_similarity(question):
    """
    질문에서 유사한 수업 이름 추출.
    """
    # 질문 전처리
    question = ' '.join(question.split())  # 중복 공백 제거
    question = question.strip()  # 양쪽 공백 제거

    # 디버깅 로그
    print(f"DEBUG: Received question: {question}")

    # 정규 표현식을 통해 "courses like", "similar to", "비슷한 수업" 뒤에 있는 텍스트를 추출
    patterns = [
        r"courses like\s+(.+)",       # "courses like Math 101"
        r"similar to\s+(.+)",         # "similar to Math 101"
        r"비슷한 수업\s+(.+)",         # "비슷한 수업 Math 101"
        r"(.+)\s+와 비슷한 수업",     # "Math 101 와 비슷한 수업"
        r"(.+)\s+과 비슷한 수업",     # "Math 101 과 비슷한 수업"
        r"(.+)\s+와 비슷한 수업을 추천해줘", # "Math 101 와 비슷한 수업을 추천해줘"
        r"(.+)\s+과 비슷한 수업을 추천해줘"  # "Math 101 과 비슷한 수업을 추천해줘"
    ]

    for pattern in patterns:
        match = re.search(pattern, question)
        if match:
            # 정규식 그룹에서 첫 번째 매칭 결과를 반환
            course_name = match.group(1)
            # 특수 문자 및 불필요한 단어 제거
            course_name = re.sub(r"을 추천해줘|를 추천해줘|을 추천|를 추천", "", course_name).strip()
            print(f"DEBUG: Extracted course name: {course_name}")
            return course_name

    # 매칭 실패 시 None 반환
    print("DEBUG: No course name matched.")
    return None

if __name__ == '__main__':
    initialize_database(app)
    app.run(debug=True, port=5000)
