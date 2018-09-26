from flask import Flask
from flask import request
from flask import render_template
from src.extract_aspects import demo_aspect_extraction

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("form.html") # this should be the name of your templates file

@app.route('/get_aspects')
def get_aspects():
  reviews = request.args.get('reviews')
  aspects = demo_aspect_extraction(reviews)
  return aspects


if __name__ == '__main__':
    app.run()