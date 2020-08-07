import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category, db
import sys

QUESTIONS_PER_PAGE = 10

def paginate_data(request, data):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  formatted_questions  = [question.format() for question in data]
  current_question = formatted_questions[start:end]
  return current_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      categories = Category.query.order_by(Category.type).all()
      if categories is None:
        abort(404)
      return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories},
        'total_category': len(categories)
      })
    except:
      abort(404)

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
      questions = Question.query.order_by(Question.id).all()
      current_questions = paginate_data(request, questions)
      if (len(current_questions) == 0):
        abort(404)
      categories =  Category.query.all()
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_question': len(questions),
        'categories': {category.id: category.type for category in categories},
        'current_categories': None
      })
    except():
      abort(404)

  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404)
      question.delete()
      return jsonify({
        'success': True,
        'deleted': question_id,
      })
    except:
      abort(422)

  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', '')
    new_answer = body.get('answer', '')
    new_category = body.get('category', '')
    new_difficulty = body.get('difficulty', '')
    if ((new_question == '') or (new_answer == '')
        or (new_category == '') or (new_difficulty == '')):
        abort(422)

    try:
      question = Question(question=new_question, answer=new_answer,
                   category=new_category, difficulty=new_difficulty)
      question.insert()
      selection = Question.query.filter(Question.id == question.id).order_by(Question.id).all()
      current_questions = paginate_data(request,selection)
      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    data = request.get_json()
    search_term = data.get('searchTerm', '')      
    if search_term == '':
      abort(422)
    try:
      results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      if len(results) == 0:
        abort(404)
      paginate_q = paginate_data(request, results)
      return jsonify({
        'success':True,
        'questions': paginate_q,
        'total_questions': len(results),
      })
    except:
      abort(404)
  
  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def get_q_by_category(category_id):
    try:
      results = Question.query.filter(
        Question.category == category_id
      ).all()
      if len(results) == 0:
        abort(404)
      paginate_q = paginate_data(request, results)
      return jsonify({
        'success': True,
        'questions': paginate_q,
        'total_questions': len(results),
        'category': category_id
      })
    except:
      abort(404)

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    try:
      body = request.get_json()
      # print(body, file=sys.stderr)
      quiz_category = body.get('quiz_category','')
      previous_questions = body.get('previous_questions','')

      # if the user selects all type
      if quiz_category['type'] == 'click':
        available_questions = Question.query.filter(
            Question.id.notin_(previous_questions)).all()
      # select a specific type
      else:
        available_questions = Question.query.filter_by(
          category = quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()

      new_question = available_questions[random.randrange(
          0, len(available_questions))].format() if len(available_questions) > 0 else None

      return jsonify({
        'success': True,
        'question': new_question
        })
    except:
      abort(404)

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable entity'
    }), 422


  
  return app