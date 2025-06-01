from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.learning import Vocabulary, Grammar, Quiz
from extensions import db
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

# Vocabulary Management
@admin_bp.route('/vocabulary')
@login_required
@admin_required
def vocabulary_list():
    words = Vocabulary.query.all()
    return render_template('admin/vocabulary/list.html', words=words)

@admin_bp.route('/vocabulary/add', methods=['GET', 'POST'])
@login_required
@admin_required
def vocabulary_add():
    if request.method == 'POST':
        try:
            word = Vocabulary(
                word=request.form['word'],
                meaning=request.form['meaning'],
                example=request.form['example']
            )
            db.session.add(word)
            db.session.commit()
            flash('Vocabulary word added successfully!', 'success')
            return redirect(url_for('admin.vocabulary_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding vocabulary word: {str(e)}', 'error')
    return render_template('admin/vocabulary/add.html')

@admin_bp.route('/vocabulary/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def vocabulary_edit(id):
    word = Vocabulary.query.get_or_404(id)
    if request.method == 'POST':
        try:
            word.word = request.form['word']
            word.meaning = request.form['meaning']
            word.example = request.form['example']
            db.session.commit()
            flash('Vocabulary word updated successfully!', 'success')
            return redirect(url_for('admin.vocabulary_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating vocabulary word: {str(e)}', 'error')
    return render_template('admin/vocabulary/edit.html', word=word)

# Grammar Management
@admin_bp.route('/grammar')
@login_required
@admin_required
def grammar_list():
    lessons = Grammar.query.all()
    return render_template('admin/grammar/list.html', lessons=lessons)

@admin_bp.route('/grammar/add', methods=['GET', 'POST'])
@login_required
@admin_required
def grammar_add():
    if request.method == 'POST':
        try:
            lesson = Grammar(
                title=request.form['title'],
                explanation=request.form['explanation'],
                example=request.form['example']
            )
            db.session.add(lesson)
            db.session.commit()
            flash('Grammar lesson added successfully!', 'success')
            return redirect(url_for('admin.grammar_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding grammar lesson: {str(e)}', 'error')
    return render_template('admin/grammar/add.html')

@admin_bp.route('/grammar/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def grammar_edit(id):
    lesson = Grammar.query.get_or_404(id)
    if request.method == 'POST':
        try:
            lesson.title = request.form['title']
            lesson.explanation = request.form['explanation']
            lesson.example = request.form['example']
            db.session.commit()
            flash('Grammar lesson updated successfully!', 'success')
            return redirect(url_for('admin.grammar_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating grammar lesson: {str(e)}', 'error')
    return render_template('admin/grammar/edit.html', lesson=lesson)

# Quiz Management
@admin_bp.route('/quiz')
@login_required
@admin_required
def quiz_list():
    questions = Quiz.query.all()
    return render_template('admin/quiz/list.html', questions=questions)

@admin_bp.route('/quiz/add', methods=['GET', 'POST'])
@login_required
@admin_required
def quiz_add():
    if request.method == 'POST':
        try:
            options = [
                request.form['option1'],
                request.form['option2'],
                request.form['option3'],
                request.form['option4']
            ]
            question = Quiz(
                question=request.form['question'],
                options=options,
                correct_option=int(request.form['correct_option'])
            )
            db.session.add(question)
            db.session.commit()
            flash('Quiz question added successfully!', 'success')
            return redirect(url_for('admin.quiz_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding quiz question: {str(e)}', 'error')
    return render_template('admin/quiz/add.html')

@admin_bp.route('/quiz/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def quiz_edit(id):
    question = Quiz.query.get_or_404(id)
    if request.method == 'POST':
        try:
            options = [
                request.form['option1'],
                request.form['option2'],
                request.form['option3'],
                request.form['option4']
            ]
            question.question = request.form['question']
            question.options = options
            question.correct_option = int(request.form['correct_option'])
            db.session.commit()
            flash('Quiz question updated successfully!', 'success')
            return redirect(url_for('admin.quiz_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating quiz question: {str(e)}', 'error')
    return render_template('admin/quiz/edit.html', question=question) 