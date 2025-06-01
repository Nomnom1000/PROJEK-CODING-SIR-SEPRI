from flask import Flask
from dotenv import load_dotenv
import os
from extensions import db, login_manager
from models.user import User
from controllers.auth import auth_bp
from controllers.main import main_bp
from controllers.learning import learning_bp
from controllers.admin import admin_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    
    # Configure SQLite database with proper permissions
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'english_learning.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Set proper permissions for instance directory
    os.chmod(os.path.dirname(db_path), 0o777)
    
    # Configure database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'check_same_thread': False}
    }
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import models
    from models.user import User
    from models.learning import Vocabulary, Grammar, Quiz, UserProgress
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import and register blueprints
    from controllers.auth import auth_bp
    from controllers.main import main_bp
    from controllers.learning import learning_bp
    from controllers.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)