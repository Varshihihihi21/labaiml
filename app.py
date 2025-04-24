from flask import Flask, render_template, request, jsonify, redirect

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

@app.route('/waterjug_pygame')
def waterjug_pygame():
    import waterjug_game
    game = waterjug_game.Game()
    game.run()
    return redirect('/')

@app.route('/finds')
def finds():
    return render_template('finds.html')

@app.route('/finds_pygame')
def finds_pygame():
    import finds_game
    game = finds_game.Game()
    game.run()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)