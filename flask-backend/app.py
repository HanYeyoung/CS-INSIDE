import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests  # 날씨 API 호출을 위한 모듈
from datetime import datetime  # 현재 시간 제공

app = Flask(__name__)
CORS(app)

# 환경 변수에서 API 키 가져오기
GEMINI_API_KEY = "AIzaSyAdi-HBKUXqWJgmJkHKWs2yP7FSBrctTZM"
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다. 환경 변수에 API 키를 추가하세요.")

# Visual Crossing API 키 설정 (날씨 정보)
VISUAL_CROSSING_API_KEY = "T8QMW932J97JVZUFTVQG5KCXT"  # Visual Crossing API 키

# Madgrades API 토큰 설정
MADGRADES_API_TOKEN = "758621a952db42dba100fcb6b25580f3"  # Madgrades API 토큰

headers = {
    "Authorization": f"Token token={MADGRADES_API_TOKEN}"
}

# Gemini API 초기화
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Invalid request"}), 400

    question = data['question'].lower()
    print("Processing question:", question)  # 디버깅: 질문 출력

    try:
        # 특수 질문 처리 (날씨 및 시간)
        if "weather" in question or "날씨" in question:
            return get_weather_response()
        elif "time" in question or "시간" in question:
            return get_time_response()
        elif "day" in question or "날짜" in question or "요일" in question:
            return get_day_response()  

        # 모델 초기화
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 텍스트 생성
        response = model.generate_content(
            question,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                stop_sequences=['x'],
                temperature=1.0
            )
        )

        # Cheezyy의 캐릭터성 추가
        character_name = "Cheezyy"
        intro = f" "
        response_text = response.text.strip()
        cheezyy_response = f"{intro}{response_text} cheezzz 🐭!"

        # 응답 처리
        print("Response received:", cheezyy_response)  # 디버깅: 응답 출력
        return jsonify({"answer": cheezyy_response})

    except Exception as e:
        print("Error occurred:", str(e))  # 디버깅: 에러 출력
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def get_weather_response():
    """날씨 정보를 Visual Crossing API에서 가져와 반환합니다."""
    data = request.get_json()
    location = data.get('location', 'Madison, USA').strip()   # 기본 위치
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"
    params = {
        "unitGroup": "metric",
        "key": VISUAL_CROSSING_API_KEY,
        "contentType": "json",
    }

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
        print("Weather API Error:", str(e))
        return jsonify({"error": "An error occurred while fetching weather information."}), 500


def get_time_response():
    """현재 날짜와 시간을 반환합니다."""
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_message = f"The current date and time is {current_datetime} cheezzz 🐭!"
    return jsonify({"answer": time_message})

def get_day_response():
    """현재 요일과 날짜를 반환합니다."""
    current_date = datetime.now().strftime("%A, %Y-%m-%d")  
    day_message = f"Today is {current_date} cheezzz 🐭!"
    return jsonify({"answer": day_message})


if __name__ == '__main__':
    app.run(debug=True, port=5000)