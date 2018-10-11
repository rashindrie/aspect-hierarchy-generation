import sys
sys.path.append('../')
from flask import Flask
from flask import request
from flask import render_template
from flask import send_file, make_response
from src.extract_aspects import demo_aspect_extraction
from src.run_dendogram_generator import get_hierarchy

app = Flask(__name__)
# app.config['OUTPUT'] = OUTPUT

@app.route('/')
def my_form():
    return render_template("form.html") # this should be the name of your templates file

@app.route('/get_aspects')
def get_aspects():
  reviews = request.args.get('reviews')

  aspects = demo_aspect_extraction(reviews.encode('ascii','replace'))
  # hierarchy = get_hierarchy()

  return ('ok')

@app.route('/get_tree')
def get_tree():
    return render_template("d3.html") # this should be the name of your templates file


if __name__ == '__main__':
    app.run()