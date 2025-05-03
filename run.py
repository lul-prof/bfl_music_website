from app import create_app, db
from werkzeug.security import generate_password_hash
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create the admin user


        db.create_all()
    app.run(debug=True)