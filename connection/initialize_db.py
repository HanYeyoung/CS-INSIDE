from connection.models import db

def initialize_database(app):
    """Initialize the database."""
    with app.app_context():
        db.create_all()  # 데이터베이스 테이블 생성
        print("Database initialized!")
