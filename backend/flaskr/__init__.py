import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


#-------------------------------------------------------------#
# CREATING APP
#-------------------------------------------------------------#

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)     # , resources={r"*/*": {"origins": "*"}}



  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Origins', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE')
    return response



# Endpoint for categories
#-------------------------------------------------------------#
  @app.route('/categories')
  def retrieve_categories():
      categories = Category.query.order_by(Category.id).all()
      category_list = {}
      if categories is not None:

          for category in categories:
            category_list[category.id] = category.type
          # formatted_categories = [category.format() for category in categories]

          return jsonify({
            'success': True,
            'categories': category_list
            })
      else:
          abort(404)


# Endpoint for questions
#-------------------------------------------------------------#
  @app.route('/questions')
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()
    if questions is not None:
        current_questions = paginate_questions(request, questions)

        categories = Category.query.all()
        category_list = {}
        for category in categories:
          category_list[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
              'success':True,
              'questions':current_questions,
              'categories': category_list,
              'total_questions':len(Question.query.all()),
              'current_category': None
            })
    else:
        abort(404)


# Delete question
#-------------------------------------------------------------#
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      try:
          question = Question.query.filter(Question.id == question_id).one_or_none()

          if question is None:
              abort(404)
          else:
              question.delete()
              question = Question.query.order_by(Question.id).all()
              current_questions = paginate_questions(request, question)

              return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
                })

      except:
          abort(422)


# Create question
#-------------------------------------------------------------#
  @app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()

      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_category = body.get('category', None)
      new_difficulty = body.get('difficulty', None)

      try:
          question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
          question.insert()

          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request, selection)

          return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
            })

      except:
          abort(405)



# Search for question
#-------------------------------------------------------------#
  @app.route('/questions/search',  methods=['POST'])
  def search_questions():

    body = request.get_json()
    search_term = body.get('searchTerm', '')
    search_term = search_term.strip()
    try:
        selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        questions = paginate_questions(request, selection)

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(questions)
            })
    except:
      abort(405)


# Endpoint for questions based on categories
#-------------------------------------------------------------#
  @app.route('/categories/<category_id>/questions')
  def questions_by_category(category_id):
    try:
        category = Category.query.get(category_id)

        if category is not None:
            questions = Question.query.order_by(Question.id).filter(Question.category==category_id).all()
            total_questions = len(questions)
            current_questions = paginate_questions(request, questions)

            return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': total_questions,
              'current_category': category.type
            })
        else:
            abort(404)
    except:
        abort(400)


# Play Quiz
#-------------------------------------------------------------#
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    try:
        questions = Question.query.filter_by(category=str(quiz_category['id'])).filter(Question.id.notin_(previous_questions)).all()
        if len(questions) > 0:
            question = random.choice(questions).format()
            result = {
              "success": True,
              "question": question
            }
        else:
            result = {
              "success": True,
              "question": None
            }
        return jsonify(result)

    except:
        abort(422)


#----------------------------------------------------------------------------#
#  For errors
#----------------------------------------------------------------------------#
  @app.errorhandler(400)    # NENAUDOJU
  def bad_request(error):
      return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404

  @app.errorhandler(405)
  def not_found(error):
      return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
        }), 405

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
      }), 422



  if __name__ == '__main__':
      app.run(port=5000)
  return app
