from datetime import datetime
from extensions import db

class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.Text, nullable=False)
    example = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vocabulary {self.word}>'

class Grammar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    example = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Grammar {self.title}>'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Quiz {self.question[:50]}...>'

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vocabulary_learned = db.Column(db.Integer, default=0)
    grammar_completed = db.Column(db.Integer, default=0)
    quiz_score = db.Column(db.Integer, default=0)
    last_vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary.id'))
    last_grammar_id = db.Column(db.Integer, db.ForeignKey('grammar.id'))
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('progress', uselist=False))
    last_vocabulary = db.relationship('Vocabulary', foreign_keys=[last_vocabulary_id])
    last_grammar = db.relationship('Grammar', foreign_keys=[last_grammar_id])

    def __repr__(self):
        return f'<UserProgress {self.user_id}>' 