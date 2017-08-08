#!/usr/bin/python


"""
    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)

labels, features = targetFeatureSplit(data)

# print labels, features

# import decision tree
from sklearn import tree

# decision tree classifier
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)

# accuracy score
print "Accuary on (overfit) data with no train-test split"
print clf.score(features, labels)

# train test split
from sklearn.model_selection import train_test_split

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size = 0.3, random_state = 42)

# decision tree classifier using train-test split
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)

# accuracy score
print "\nAccuary on data with train-test split"
print clf.score(features_test, labels_test)

### it's all yours from here forward!  


