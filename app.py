from flask import Flask, render_template, url_for
from charts import process_data

app = Flask(__name__)

k_value = ""
knn_accuracy = ""
knn_precision = ""

@app.before_first_request
def before_first_request():
    global k_value, knn_accuracy, knn_precision
    k_value, knn_accuracy, knn_precision = process_data()


@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html')


@app.route('/charts')
def charts():
    global k_value, knn_accuracy, knn_precision
    return render_template('/charts.html', k_value=k_value, knn_accuracy=knn_accuracy, knn_precision=knn_precision)


@app.route('/group')
def group():
    return render_template('/group.html')


if __name__ == '__main__':
    app.run()
