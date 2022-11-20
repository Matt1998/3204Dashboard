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


k_value = None


def process_data():
    df = pandas.read_excel("static/assets/charts/Packetbeat_Cleaned.xlsx")

    # Convert IP address to long
    df['destination.ip'] = df['destination.ip'].apply(lambda x: int(ipaddress.IPv4Address(x)))
    df['source.ip'] = df['source.ip'].apply(lambda x: int(ipaddress.IPv4Address(x)))

    # Convert transport protocol to int
    df['network.transport'] = df['network.transport'].apply(lambda x: 1 if 'tcp' else 2)

    # Convert size to bytes
    for i in range(len(df)):
        # Remove commas in size
        df.loc[i, "source.bytes (kb)"] = df.loc[i, "source.bytes (kb)"].replace(",", "")

        if 'MB' in df.loc[i, "source.bytes (kb)"]:
            df.loc[i, "source.bytes (kb)"] = float(df.loc[i, "source.bytes (kb)"].replace("MB", "")) * 1024 * 1024
        elif 'KB' in df.loc[i, "source.bytes (kb)"]:
            df.loc[i, "source.bytes (kb)"] = float(df.loc[i, "source.bytes (kb)"].replace("KB", "")) * 1024
        else:
            df.loc[i, "source.bytes (kb)"] = float(df.loc[i, "source.bytes (kb)"].replace("B", ""))

    df.to_excel("static/assets/charts/Packetbeat_Final.xlsx", index=False)

    # Make sure the excel sheet is uploaded to this colab (change later for gdrive)
    X = pandas.read_excel("static/assets/charts/Packetbeat_Final.xlsx")
    # Store attack column into Y
    Y = X["attack"]
    # Remove attack column from data
    X.drop("attack", inplace=True, axis=1)
    feature_cols = list(X.columns)

    # Determine best value for k
    k_range = range(1, 27)
    scores = {}
    nscores = {}
    scores_mean = {}
    nscores_mean = {}
    score_max = []
    for k in tqdm(k_range):
        # Create a new KNN model
        cv_model = KNeighborsClassifier(n_neighbors=k)
        # Train model with 10 folds
        cv_scores = cross_val_score(cv_model, X, Y, cv=10)
        scores[k] = cv_scores
        scores_mean[k] = np.mean(cv_scores)
        # for every k, determine best n
        for n in range(2, 15):
            cv_nmodel = KNeighborsClassifier(n_neighbors=k)
            cv_nscores = cross_val_score(cv_nmodel, X, Y, cv=n)
            nscores[n] = cv_nscores
            nscores_mean[n] = np.mean(cv_nscores)
            score_max.append(nscores_mean[n])
            # store best n value
            bn = max(nscores_mean, key=nscores_mean.get)
            # print("For k value "+str(k)+" and n "+str(n)+", the accuracy is "+str(nscores_mean[n]))
    # Store best k value
    k = max(scores_mean, key=scores_mean.get)

    # Show most accurate k value
    k_value = "The most accurate k value is \"" + str(k) + "\" and best value of n is \"" + str(
        bn) + "\" with accuracy of: " + str(max(score_max))

    # Training the model with best k
    # random_state to ensure same split to replicate test results (optional),
    # statify to ensure 25-75 split between non-attack and attack data for testing
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.3, random_state=44,
                                                        stratify=Y)  # X is the input, Y is the expected res
    # Train the model
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_Train, Y_Train)

    score_list_knn = []
    accknn = knn.score(X_Test, Y_Test)
    print("Accuracy:", accknn)
    y_pred = knn.predict(X_Test)
    y_true = Y_Test
    cmknn = confusion_matrix(y_true, y_pred)
    tpknn = cmknn[1][1]
    fpknn = cmknn[0][1]
    preknn = tpknn / (tpknn + fpknn)
    score_list_knn.append(accknn)
    score_list_knn.append(preknn)
    print("Precision:", preknn)
    f, ax = plt.subplots(figsize=(5, 5))
    group_names = ['True Neg', 'False Pos', 'False Neg', 'True Pos']
    group_percentages = ["{0:.4%}".format(value) for value in
                         cmknn.flatten() / np.sum(cmknn)]
    labels = [f"{v1}\n{v2}" for v1, v2 in
              zip(group_names, group_percentages)]
    labels = np.asarray(labels).reshape(2, 2)
    sns.heatmap(cmknn, annot=labels, fmt='', cmap='Blues')
    plt.savefig('static/assets/img/Knn_heatmap.png',dpi=300, bbox_inches = "tight")
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    score_list_rf = []
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.3, random_state=44)
    rf = RandomForestClassifier(oob_score=True)
    rf.fit(X_Train, Y_Train)
    y_pred = rf.predict(X_Test)
    accrf = metrics.accuracy_score(Y_Test, y_pred)
    print("Accuracy:", accrf)
    y_true = Y_Test
    cmrf = confusion_matrix(y_true, y_pred)
    tprf = cmrf[1][1]
    fprf = cmrf[0][1]
    prerf = tprf / (tprf + fprf)
    score_list_rf.append(accrf)
    score_list_rf.append(prerf)
    print("Precision:", prerf)
    f, ax = plt.subplots(figsize=(5, 5))
    group_names = ['True Neg', 'False Pos', 'False Neg', 'True Pos']
    group_percentages = ["{0:.4%}".format(value) for value in
                         cmknn.flatten() / np.sum(cmknn)]
    labels = [f"{v1}\n{v2}" for v1, v2 in
              zip(group_names, group_percentages)]
    labels = np.asarray(labels).reshape(2, 2)
    sns.heatmap(cmrf, annot=labels, fmt='', cmap='Blues')
    plt.savefig('static/assets/img/RandomForest_heatmap.png',dpi=300, bbox_inches = "tight")
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    score_list_dt = []
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.3,
                                                        random_state=44)  # X is the input, Y is the expected res
    clf = DecisionTreeClassifier()
    clf = clf.fit(X_Train, Y_Train)
    y_pred = clf.predict(X_Test)
    y_true = Y_Test
    accdt = metrics.accuracy_score(Y_Test, y_pred)
    print("Accuracy:", accdt)
    cmdt = confusion_matrix(y_true, y_pred)
    tpdt = cmdt[1][1]
    fpdt = cmdt[0][1]
    predt = tpdt / (tpdt + fpdt)
    score_list_dt.append(accdt)
    score_list_dt.append(predt)
    print("Precision:", predt)
    f, ax = plt.subplots(figsize=(5, 5))
    group_names = ['True Neg', 'False Pos', 'False Neg', 'True Pos']
    group_percentages = ["{0:.4%}".format(value) for value in
                         cmknn.flatten() / np.sum(cmknn)]
    labels = [f"{v1}\n{v2}" for v1, v2 in
              zip(group_names, group_percentages)]
    labels = np.asarray(labels).reshape(2, 2)
    svm = sns.heatmap(cmdt, annot=labels, fmt='', cmap='Blues')
    plt.savefig('static/assets/img/DecisionTree_heatmap.png',dpi=300, bbox_inches = "tight")
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True, feature_names=feature_cols, class_names=['0', '1'])
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png('decision.png')
    Image(graph.create_png())

    plt.bar(["KNN", "Decision Tree", "Random Forest"], [score_list_knn[1], score_list_dt[1], score_list_rf[1]],
            width=0.4)
    plt.xlabel('\nPrecision')
    plt.yscale("log")
    plt.savefig('static/assets/img/precision_bar.png',dpi=300, bbox_inches = "tight")
    print("\n")
    plt.bar(["KNN", "Decision Tree", "Random Forest"], [score_list_knn[0], score_list_dt[0], score_list_rf[0]],
            width=0.4)
    plt.xlabel('\nAccuracy')
    plt.yscale("log")
    plt.savefig('static/assets/img/accuracy_bar.png',dpi=300, bbox_inches = "tight")