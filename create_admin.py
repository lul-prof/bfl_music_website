from app import create_app, db
from app.models.user import User

def create_admin_user(username, email, password):
    app = create_app()
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Error: A user with email {email} already exists!")
            return False
            
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            print(f"Error: Username {username} is already taken!")
            return False
        
        try:
            # Create new admin user
            admin = User(username=username, email=email, is_admin=True)
            admin.set_password(password)
            
            # Add to database
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user {username} created successfully!")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {str(e)}")
            return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python create_admin.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    success = create_admin_user(username, email, password)
    if not success:
        sys.exit(1)