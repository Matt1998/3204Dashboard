from flask import Flask, render_template
import charts

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():  # put application's code here
    return render_template('/index.html')


@app.route('/charts')
def charts():
    graphJSON = json.dumps(charts.precision_bar, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('/charts.html', graphJSON=graphJSON)


@app.route('/group')
def group():
    return render_template('/group.html')


if __name__ == '__main__':
    charts.process_data()
    app.run()
