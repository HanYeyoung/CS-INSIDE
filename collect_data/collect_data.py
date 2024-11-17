import requests
import csv

# API token
API_TOKEN = '7a0e6bb1414c471a82a7046faaf4fd6b'

# Headers for the API
HEADERS = {
    'Authorization': f'Token token={API_TOKEN}'
}

# Madgrades API endpoint
BASE_URL = "https://api.madgrades.com/v1/courses"

# List of target course names or numbers
TARGET_COURSES = {
    "Introduction to Computer Engineering",
    "Introduction to Programming",
    "Introduction to Discrete Mathematics",
    "Machine Organization and Programming",
    "Programming I",
    "Programming II",
    "Programming III",
    "Introduction to Algorithms",
    "Introduction to Artificial Intelligence",
    "Introduction to Operating Systems",
    "Data Sci Programming I",
    "Introduction to Data Structures",
    "Digital System Fundamentals",
    "Database Management Systems: Design and Implementation",
    "Problem Solving Using Computers",
    "Introduction to Data Programming",
    "Data Sci Programming II",
    "Introduction to Cryptography",
    "Introduction to Programming Languages and Compilers",
    "Computer Graphics",
    "Introduction to Computer Networks",
    "Introduction to Combinatorics",
    "Introduction to Computer Architecture",
    "Software Engineering",
    "Machine Learning",
    "Theory and Applications of Pattern Recognition",
    "Linear Programming Methods",
    "Undergraduate Elective Topics in Computing",
    "Introduction to Human-Computer Interaction",
    "Introduction to Numerical Methods"
}

# Fetch courses from the API
def fetch_courses(subject="266", page=1):
    params = {'page': page, 'per_page': 100, 'subject': subject}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Save the filtered courses to a CSV file
def save_to_csv(filtered_courses, filename="filtered_courses.csv"):
    headers = ['uuid', 'name', 'number', 'subject', 'instructors', 'grades']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for course in filtered_courses:
            row = {
                'uuid': course.get('uuid'),
                'name': course.get('name'),
                'number': course.get('number'),
                'subject': course.get('subjects')[0]['name'] if course.get('subjects') else '',
                'instructors': ", ".join(course.get('instructors', [])),
                'grades': course.get('grades')
            }
            writer.writerow(row)

# Main execution function
def collect_specific_courses():
    all_filtered_courses = []
    page = 1
    while True:
        print(f"Fetching page {page} for subject '266'...")
        data = fetch_courses(page=page)
        if not data or 'results' not in data or not data['results']:
            break
        # Filter courses based on the target list
        filtered_courses = [
            course for course in data['results']
            if course['name'] in TARGET_COURSES
        ]
        all_filtered_courses.extend(filtered_courses)
        page += 1
    return all_filtered_courses

# Execute the script
if __name__ == "__main__":
    filtered_courses = collect_specific_courses()
    if filtered_courses:
        print(f"Found {len(filtered_courses)} courses matching the criteria.")
        save_to_csv(filtered_courses, filename="filtered_courses.csv")
        print("Filtered courses saved to 'filtered_courses.csv'.")
    else:
        print("No matching courses found.")
