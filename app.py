from flask import Flask, render_template, url_for
from charts import process_data

app = Flask(__name__)

data = None

@app.route('/process')
def process():
    global data
    data = process_data()
    return "done"

@app.route('/')
def redir():
    return render_template('/interim.html')

@app.route('/index')
def index():
    return render_template('/index.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html')


@app.route('/charts')
def charts():
    global data
    return render_template('/charts.html', data=data)


@app.route('/decisiontree')
def decision():
    global data
    return render_template('/decisiontree.html', data=data)


@app.route('/group')
def group():
    return render_template('/group.html')


if __name__ == '__main__':
    app.run()
