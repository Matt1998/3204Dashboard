from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('/index.html')


@app.route('/charts')
def charts():
    return render_template('/charts.html')


@app.route('/group')
def group():
    return render_template('/group.html')


if __name__ == '__main__':
    app.run()
