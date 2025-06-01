import os
import sys
import stat
from datetime import datetime, timezone

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app, db
from models.user import User
from models.learning import Vocabulary, Grammar, Quiz, UserProgress

def ensure_directory_permissions(directory):
    """Ensure directory exists and has proper permissions."""
    if not os.path.exists(directory):
        os.makedirs(directory, mode=0o777)
    else:
        os.chmod(directory, 0o777)

def ensure_file_permissions(file_path):
    """Ensure file has proper permissions."""
    if os.path.exists(file_path):
        os.chmod(file_path, 0o666)

def update_database():
    app = create_app()
    
    # Ensure instance directory exists with proper permissions
    instance_path = app.instance_path
    ensure_directory_permissions(instance_path)
    
    with app.app_context():
        # Delete existing database file if it exists
        db_path = os.path.join(instance_path, 'english_learning.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Deleted existing database file.")

        # Create all tables
        db.create_all()
        print("Created new database tables.")

        # Ensure database file has write permissions
        ensure_file_permissions(db_path)

        try:
            # Add admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("Added admin user.")

            # Add sample vocabulary
            vocabulary = [
                Vocabulary(
                    word='perseverance',
                    meaning='Persistence in doing something despite difficulty or delay in achieving success',
                    example='His perseverance in studying paid off when he passed the exam.'
                ),
                Vocabulary(
                    word='eloquent',
                    meaning='Fluent or persuasive in speaking or writing',
                    example='She gave an eloquent speech at the graduation ceremony.'
                )
            ]
            db.session.add_all(vocabulary)
            print("Added sample vocabulary.")

            # Add sample grammar lessons
            grammar = [
                Grammar(
                    title='Present Perfect Tense',
                    explanation='The present perfect tense is used to describe actions that happened at an unspecified time before now or actions that started in the past and continue to the present.',
                    example='I have visited Paris three times.'
                ),
                Grammar(
                    title='Conditional Sentences',
                    explanation='Conditional sentences are used to express that the action in the main clause can only take place if a certain condition is fulfilled.',
                    example='If it rains, I will stay at home.'
                )
            ]
            db.session.add_all(grammar)
            print("Added sample grammar lessons.")

            # Add sample quiz questions
            quiz = [
                Quiz(
                    question='Which sentence uses the present perfect tense correctly?',
                    option1='I am going to the store yesterday.',
                    option2='I have been to the store.',
                    option3='I went to the store.',
                    option4='I will go to the store.',
                    correct_option=2
                ),
                Quiz(
                    question='What is the correct form of the verb in this sentence: "She _____ to Paris three times."',
                    option1='go',
                    option2='goes',
                    option3='has gone',
                    option4='went',
                    correct_option=3
                )
            ]
            db.session.add_all(quiz)
            print("Added sample quiz questions.")

            # Create initial progress for admin user
            admin_progress = UserProgress(
                user_id=1,
                vocabulary_learned=0,
                grammar_completed=0,
                quiz_score=0,
                last_activity=datetime.now(timezone.utc)
            )
            db.session.add(admin_progress)
            print("Created admin user progress.")

            # Commit all changes
            db.session.commit()
            print("Successfully updated database!")

            # Ensure database file has proper permissions after all operations
            ensure_file_permissions(db_path)
            print("Set database file permissions.")

        except Exception as e:
            db.session.rollback()
            print(f"Error updating database: {str(e)}")
            raise

if __name__ == '__main__':
    update_database() 