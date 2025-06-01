import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models.user import User

def check_admin():
    app = create_app()
    with app.app_context():
        try:
            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print("\nAdmin user found:")
                print(f"Username: {admin.username}")
                print(f"Email: {admin.email}")
                print(f"Is Admin: {admin.is_admin}")
                
                # Verify password
                if admin.check_password('admin123'):
                    print("Password verification: SUCCESS")
                else:
                    print("Password verification: FAILED")
                    print("Resetting admin password...")
                    admin.set_password('admin123')
                    db.session.commit()
                    print("Password has been reset to: admin123")
            else:
                print("\nAdmin user not found!")
                print("Creating admin user...")
                
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                
                print("\nAdmin user created successfully!")
                print("Username: admin")
                print("Password: admin123")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    check_admin() 