from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models.learning import Vocabulary, Grammar, Quiz, UserProgress
from extensions import db

learning_bp = Blueprint('learning', __name__)

def get_or_create_progress():
    progress = UserProgress.query.filter_by(user_id=current_user.id).first()
    if not progress:
        progress = UserProgress(user_id=current_user.id)
        db.session.add(progress)
        db.session.commit()
    return progress

@learning_bp.route('/vocabulary')
@login_required
def vocabulary():
    try:
        words = Vocabulary.query.all()
        progress = get_or_create_progress()
        return render_template('learning/vocabulary.html', words=words, progress=progress)
    except Exception as e:
        flash(f'Error loading vocabulary: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))

@learning_bp.route('/vocabulary/learn/<int:word_id>')
@login_required
def learn_vocabulary(word_id):
    try:
        word = Vocabulary.query.get_or_404(word_id)
        progress = get_or_create_progress()
        
        if not progress.last_vocabulary_id or progress.last_vocabulary_id != word_id:
            progress.vocabulary_learned += 1
            progress.last_vocabulary_id = word_id
            db.session.commit()
            flash('Word marked as learned!', 'success')
        
        return redirect(url_for('learning.vocabulary'))
    except Exception as e:
        flash(f'Error marking word as learned: {str(e)}', 'error')
        return redirect(url_for('learning.vocabulary'))

@learning_bp.route('/grammar')
@login_required
def grammar():
    try:
        lessons = Grammar.query.all()
        progress = get_or_create_progress()
        return render_template('learning/grammar.html', lessons=lessons, progress=progress)
    except Exception as e:
        flash(f'Error loading grammar lessons: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))

@learning_bp.route('/grammar/<int:lesson_id>')
@login_required
def grammar_lesson(lesson_id):
    try:
        lesson = Grammar.query.get_or_404(lesson_id)
        progress = get_or_create_progress()
        
        if not progress.last_grammar_id or progress.last_grammar_id != lesson_id:
            progress.grammar_completed += 1
            progress.last_grammar_id = lesson_id
            db.session.commit()
            flash('Lesson marked as completed!', 'success')
        
        return render_template('learning/grammar_lesson.html', lesson=lesson, progress=progress)
    except Exception as e:
        flash(f'Error loading grammar lesson: {str(e)}', 'error')
        return redirect(url_for('learning.grammar'))

@learning_bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        try:
            answer = int(request.form.get('answer'))
            current_question = session.get('current_question')
            
            if current_question and answer == current_question['correct_option']:
                session['score'] = session.get('score', 0) + 1
            
            session['total_questions'] = session.get('total_questions', 0) + 1
            
            # Get a new random question
            question = Quiz.query.order_by(db.func.random()).first()
            if question:
                session['current_question'] = {
                    'id': question.id,
                    'text': question.question,
                    'option1': question.option1,
                    'option2': question.option2,
                    'option3': question.option3,
                    'option4': question.option4,
                    'correct_option': question.correct_option
                }
                return render_template('learning/quiz.html', current_question=session['current_question'])
            else:
                # No more questions, show results
                score = session.get('score', 0)
                total = session.get('total_questions', 0)
                
                # Update user progress
                progress = get_or_create_progress()
                progress.quiz_score = max(progress.quiz_score or 0, score)
                db.session.commit()
                
                session.clear()
                return render_template('learning/quiz.html', score=score, total_questions=total)
        except Exception as e:
            flash(f'Error processing quiz: {str(e)}', 'error')
            return redirect(url_for('main.dashboard'))
    
    # Initialize quiz session
    try:
        session['score'] = 0
        session['total_questions'] = 0
        
        # Get first question
        question = Quiz.query.order_by(db.func.random()).first()
        if question:
            session['current_question'] = {
                'id': question.id,
                'text': question.question,
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'option4': question.option4,
                'correct_option': question.correct_option
            }
            return render_template('learning/quiz.html', current_question=session['current_question'])
        else:
            flash('No questions available', 'error')
            return redirect(url_for('main.dashboard'))
    except Exception as e:
        flash(f'Error starting quiz: {str(e)}', 'error')
        return redirect(url_for('main.dashboard')) 