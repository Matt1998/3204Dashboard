from flask import Flask, render_template, url_for
from charts import process_data

app = Flask(__name__)

k_value = ""

@app.before_first_request
def before_first_request():
    k_value = process_data()


@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html')


@app.route('/charts')
def charts():
    return render_template('/charts.html', k_value=k_value)


@app.route('/group')
def group():
    return render_template('/group.html')


if __name__ == '__main__':
    app.run()
