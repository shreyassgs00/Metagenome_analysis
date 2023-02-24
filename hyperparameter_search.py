import random
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_curve, auc

def hyperparameter_search(X_train,Y_train,X_test,Y_test):
    trains_X = []
    trains_Y = []
    tests_X = []
    tests_Y = []
    for i in range(5):
        range_for_folds = [i*31, (i+1)*31]
        test_X = X_train[range_for_folds[0]:range_for_folds[1]]
        test_Y = Y_train[range_for_folds[0]:range_for_folds[1]]
        tests_X.append(test_X)
        tests_Y.append(test_Y)
        train_X = []
        train_Y = []
        for j in range(0, len(X_train)):
            if j < range_for_folds[0] or j >= range_for_folds[1]:
                train_X.append(X_train[j])
                train_Y.append(Y_train[j])
        trains_X.append(train_X)
        trains_Y.append(train_Y)

    fprs = []
    tprs = []
    s = []
    hyperparameters = []
    for i in range(50):
        fprs_temp = []
        tprs_temp = []
        s_temp = []
        hyper_temp = []
        n_estimators_rand = random.randint(70,200)
        min_samples_leaf_rand = random.randint(1,20)
        hyper_temp.append([n_estimators_rand, min_samples_leaf_rand])
        new_classifier = RandomForestClassifier(n_estimators = n_estimators_rand, min_samples_leaf = min_samples_leaf_rand)
        for j in range(5):
            train_X = trains_X[j]
            train_Y = trains_Y[j]
            test_X = tests_X[j]
            test_Y = tests_Y[j]
            new_classifier.fit(train_X, train_Y)
            predicted_Y = new_classifier.predict(test_X)
            fpr,tpr,thresholds = roc_curve(test_Y, predicted_Y)
            auc_score = auc(fpr,tpr)
            fprs_temp.append(fpr)
            tprs_temp.append(tpr)
            s_temp.append(auc_score)
        fprs.append(fprs_temp)
        tprs.append(tprs_temp)
        s.append(s_temp)
        hyperparameters.append(hyper_temp)

    mean_aucs = []
    for i in s:
        su = 0
        for j in i:
            su+=j
        mean_aucs.append(su/5)

    return mean_aucs