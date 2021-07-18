import flask
from flask import request, jsonify

app = flask.Flask(__name__) # Flask application object
app.config["DEBUG"] = True

# test data
questions = [
    {'question': 'Create: What changes would you make to solve this?',
     'target': 'Some birth defects, like heart problems, require urgent vet attention.',
     'line_num': 177},
    {'question': 'Understand: What is the meaning of the word \'polydactyly\'?',
     'target': 'polydactyly',
     'line_num': 178},
    {'question': 'Understand: What is the meaning of the word \'lever\'?',
     'target': 'lever.',
     'line_num': 59},
]

questions = {'question': 'Create: What changes would you make to solve this?',
     'target': 'Some birth defects, like heart problems, require urgent vet attention.',
     'sentence_number': 177}



@app.route('/', methods=['GET'])
def home():
    return "<h1>I'm alive!</p>"

@app.route('/api/test_sentences', methods=['GET'])
def api_all():
    return jsonify(questions)

#app.run(host='127.0.0.1', debug=True, ssl_context=('cert.pem', 'key.pem'))
app.run()
