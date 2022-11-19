from flask import Flask, render_template, url_for
from charts import process_data

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():  # put application's code here
    return render_template('/index.html')


@app.route('/charts')
def charts():
    return render_template('/charts.html')


@app.route('/group')
def group():
    return render_template('/group.html')


if __name__ == '__main__':
    process_data()
    app.run()
