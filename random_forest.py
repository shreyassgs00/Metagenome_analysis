import preprocessing1
import preprocessing2

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_curve, auc

def perform_random_forest_classification(X_train, Y_train, X_test, Y_test):
    classifier = RandomForestClassifier(n_estimators=100 ,min_samples_leaf = 1)   #Creating a random forest classifier
    classifier.fit(X_train, Y_train)

    predicted_target = classifier.predict(X_test)
    return predicted_target, metrics.accuracy_score(Y_test, predicted_target)

def get_auc_score(X_train, Y_train, X_test, Y_test, predicted_target):
    classifier = RandomForestClassifier(n_estimators=100 ,min_samples_leaf = 1) 
    predicted_values = cross_val_predict(classifier, X_train, Y_train, cv = 5)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(Y_train, predicted_values)
    false_positive_rate_independent, true_positive_rate_independent, thresholds_independent = roc_curve(Y_test, predicted_target)
    auc_score = auc(false_positive_rate, true_positive_rate)
    return auc_score, false_positive_rate_independent, true_positive_rate_independent, false_positive_rate, true_positive_rate

def perform_cross_fold_validation(X_train, Y_train, X_test, Y_test):
    classifier = RandomForestClassifier(n_estimators=100 ,min_samples_leaf = 1) 
    false_positive_rates = []
    true_positive_rates = []
    scores = []

    for i in range(5):
        range_for_folds = [i*31, (i+1)*31]
        test_X = X_train[range_for_folds[0]:range_for_folds[1]]
        test_Y = Y_train[range_for_folds[0]:range_for_folds[1]]
        train_X = []
        train_Y = []
        for j in range(0, len(X_train)):
            if j < range_for_folds[0] or j >= range_for_folds[1]:
                train_X.append(X_train[j])
                train_Y.append(Y_train[j])
        classifier.fit(train_X, train_Y)
        predicted_Y = classifier.predict(test_X)
        fpr, tpr, thresholds = roc_curve(test_Y, predicted_Y)
        auc_score = auc(fpr, tpr)
        false_positive_rates.append(fpr)
        true_positive_rates.append(tpr)
        scores.append(auc_score)

    return scores, false_positive_rates, true_positive_rates