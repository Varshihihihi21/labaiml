from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tictactoe')
def tictactoe():
    return render_template('tictactoe.html')

@app.route('/waterjug')
def waterjug():
    return render_template('waterjug.html')

@app.route('/puzzle')
def puzzle():
    return render_template('puzzle.html')

@app.route('/travellingsalesman')
def travellingsalesman():
    return render_template('travellingsalesman.html')

if __name__ == '__main__':
    app.run(debug=True)