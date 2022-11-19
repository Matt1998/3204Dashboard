from flask import Flask, render_template

from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas
from tqdm import tqdm
import ipaddress
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from six import StringIO
from IPython.display import Image
import pydotplus
import plotly
import plotly.express as pex

app = Flask(__name__)

precision_bar = None


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
    app.run()
