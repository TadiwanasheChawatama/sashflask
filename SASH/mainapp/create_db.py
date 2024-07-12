# create_db.py
from bacuup.modelserr import app, db  # Replace 'app' with the name of your Flask app module

with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")