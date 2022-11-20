from flask import Flask, render_template, url_for
from charts import process_data

app = Flask(__name__)

data = None

@app.before_first_request
def before_first_request():
    global data
    data = process_data()


@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html')


@app.route('/charts')
def charts():
    global data
    return render_template('/charts.html', data=data)


@app.route('/group')
def group():
    return render_template('/group.html')


if __name__ == '__main__':
    app.run()
