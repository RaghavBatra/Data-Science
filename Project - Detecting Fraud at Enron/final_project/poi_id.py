#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

# imports

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data

# pretty printing
import pprint

# plotting
import matplotlib.pyplot as plt

# numpy
import numpy as np

# pandas
import pandas as pd

# better plotting
import seaborn as sns

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary'] 
# You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Store to my_dataset for easy export below.
my_dataset = data_dict

df = pd.DataFrame.from_dict(data_dict, orient = "index")

n_poi = len(df[df['poi'] == True])
n_npoi = len(df[df['poi'] == False])
total = len(df)

print "Total # of people in the dataset:"
print total

print "Total # of POIs in the dataset:"
print n_poi

# replace the 'NaN' with actual NaN values
df = df.replace(['NaN'], np.nan)

#################################################################

print "################################################################\
"

### Task 2: Remove outliers

# subset df into only the 'poi' and 'salary' columns
# and remove any NaN values in this subset.
# 
# This is going to be very common in this script.
# If we removed all NaN values from the dataframe,
# then we would get an empty dataframe, since every
# row contains atleast one NaN value!
#
# This way by subsetting the data, and only
# removing the NaN from this subset, we get the most of 
# the most of the data.

# generic function to plot a boxplot
def boxplot(x, y):	
	sns.boxplot(data = df.dropna(subset = [x, y]), x = x, y = y)
	plt.xlabel(str(x))
	plt.ylabel(str(y))
	plt.show()

boxplot('poi', 'salary')
plt.savefig('testplot.png')

# Strange! The boxplots seems to have been 'squashed'
# into tiny boxplots because of the large outlier with a
# value of almost 2.6e7!

max_salary = df.sort_values(['salary'], ascending = False)
print max_salary[:1]
# Woah! This is the 'TOTAL' field! Seems to be a spreadsheet
# typo. Let's remove it!

# Removes 'TOTAL' field
df = max_salary[1:]

boxplot('poi', 'salary')
# This looks much better!

# It seems that POI earned more on average

##################################################################

print "################################################################\
"


# generic function to plot scatter plots
def scatter(x, y):
	sns.lmplot(data = df.dropna(subset = [x, y]), x = x, y = y, hue = 'poi', fit_reg = False)
	plt.xlabel(str(x))
	plt.ylabel(str(y))
	plt.show()


scatter('salary', 'bonus')

# Not very helpful in terms of trends or outliers but it seems
# that having salary < 300000 and bonus < 550000 almost 
# guarantees non-POI

# subsetting the data to investigate
df_s_b = df.dropna(subset = ['salary', 'bonus'])
df_i = df_s_b[(df_s_b["salary"] < 300000) & (df_s_b["bonus"] < 550000)]

total = len(df_i)
poi = len(df_i[df_i['poi'] == True])

print "\n%age of POIs with salary < 300000 and bonus < 550000"
print round(poi * 1.0 / total, 2)

print "\nNumber of people with salary < 300000 and bonus < 550000"
print total

# Ah! This seemed promising in terms of differentiating POIs, but # the fact that this label only applies to 23 people makes it only 
# mediocrely very promising

##################################################################

print "################################################################\
"

# Ah! Seemed like plotting bonus vs salary didn't show any trends,
# but what if we plotted salary vs bonus as a %age of the salary

# Creating this new feature
df_s_b = df.dropna(subset = ['salary', 'bonus'])
df['bonus/salary'] = df['bonus'] * 1.0/df['salary']

scatter('salary', 'bonus/salary')

print "Number of POI with a ratio > 15"
df_s_bs = df.dropna(subset = ['bonus/salary', 'poi'])
print len(df_s_bs[(df_s_bs['bonus/salary'] > 15) & (df_s_bs['poi'] == True)])

# Too few! This is also not a good metric
# But it makes sense to investigate the above values
print df_s_bs[(df_s_bs['bonus/salary'] > 15) & (df_s_bs['poi'] == True)]

##################################################################

print "################################################################\
"

df_p_lti = df.dropna(subset = ['poi', 'long_term_incentive'])

boxplot('poi', 'long_term_incentive')

# It seems that the long term incentive is higher, on average, for # POIs
# After doing some scratchwork, it seems there is nothing
# further to investigate. The 'outlier' is in the non-POI side.

##################################################################

print "################################################################\
"

boxplot('poi', 'total_stock_value')

# It seems that the total stock value is higher, on average, with some "outliers" for POIs
# Let us explore this

df_p_tsv = df.dropna(subset = ['poi', 'total_stock_value']) 
df_i = df_p_tsv[df_p_tsv['total_stock_value'] > 2.5e7]

total = len(df_i)
poi = len(df_i[df_i['poi'] == True])

print "\n%age of POIs with total stock value > 2.5e7"
print round(poi * 1.0 / total, 2)
print "\nNumber of people with total stock value > 2.5e7"
print total

# Ah! This is good in identification of POIs (100%)!
# But only 3 data values lead to not much credibility!

##################################################################

print "################################################################\
"

boxplot('poi', 'from_messages')

# From messages seem to be higher, on average, with more "outliers" for non-POIs
# let us explore this

df_p_fm = df.dropna(subset = ['poi', 'from_messages'])
df_i = df_p_fm[df_p_fm['from_messages'] > 500]

total = len(df_i)
poi = len(df_i[df_i['poi'] == True])

print "\n%age of POIs with 'from' messages > 500"
print round(poi * 1.0 / total, 2)
print "\nNumber of people with 'from' messages > 500"
print total

# Too few again! Not great!
# Still, what's with this 'outlier' in the non-POI side at
# ~14000

max_from_messages = df_p_fm.sort_values(['from_messages'], ascending = False)

print max_from_messages[:1]

# This is a good feature. The person 'VINCENT KAMINSKI'
# seemed to have to an active opponent against the scam at Enron.
# That maybe explains the high 'from_messages': maybe she 
# suspected something was up, and sent a lot of messages
# Her bonus/salary seems low to support the fact she was
# not a POI in the Enron scam

##################################################################

print "################################################################\
"

scatter('from_messages', 'to_messages')

# 'From' messages are higher, on average, for non-POIs with more "outliers" for non-POIs
# Let us explore this

df_f_t = df.dropna(subset = ['from_messages', 'to_messages'])
df_i = df_f_t[(df_f_t['from_messages']) > 10000 & (df_f_t['to_messages'] > 10000)]

total = len(df_i)
poi = len(df_i[df_i['poi'] == True])

print "\n%age of POIs with 'from' and 'to' messages > 10000"
print poi
print "\nNumber of people with 'from' and 'to' messages > 10000"
print total
				
# 86 people! That's much better and the % of POI (14%) is not too high to make it a discriminatory feature

##################################################################

print "################################################################\
"

scatter('poi', 'deferred_income')

df_p_di = df.dropna(subset = ['poi', 'deferred_income'])
df_i = df_p_di[df_p_di['deferred_income'] > -150000]

total = len(df_i)
poi = len(df_i[df_i['poi'] == True])

print "\n%age of POIs with deferred income > -1500000"
print poi
print "\nNumber of people with deferred income > -150000"
print total

# Again, too few people to make it a discriminatory feature

##################################################################

print "################################################################\
"

### Task 3: Create new feature(s)

# Create the features that are 'good'

df['salary_bonus'] = (df["salary"] < 300000) & (df["bonus"] < 550000)

df['high_from_to'] = (df['from_messages'] > 10000) & (df['to_messages'] > 10000)

# salary & long term incentive seem to be more for POIs
# These may help as well.

features_list = ['salary_bonus', 'high_from_to', 'salary', 'long_term_incentive']

# use SKLearn Imputer() to fill the numerical columns
# that have NaN values
from sklearn.preprocessing import Imputer

# We don't care about string values here, so let's remove
# them from our dataset for convenience and simplicity.

# Non string (numerical) values
df_non_string = df.select_dtypes(exclude = ['object'])

# String values
df_string = df.select_dtypes(include = ['object'])

imp = Imputer()
imp = imp.fit_transform(df_non_string)
imp = pd.DataFrame(imp, columns = list(df_non_string.columns.values))


### Store to my_dataset for easy export below.
my_dataset = pd.DataFrame.to_dict(imp, orient = 'index')

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)

labels, features = targetFeatureSplit(data)

#################################################################

print "################################################################\
"

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html


# Trying GaussianNB, DecisionTree, RandomForest & SVM and
# printing accuracy scores on the same features and labels

# For precision, recall and F1 metrics
from sklearn import metrics

# Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(features, labels)
print "Gaussian Naive Bayes"
print clf.score(features, labels)

print "\n"

# Decision Trees
from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf.fit(features, labels)
print "Decision Tree"
print clf.score(features, labels)


print "\n"

# Random Forests
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
clf.fit(features, labels)
print "Random Forest"
print clf.score(features, labels)

print "\n"
print "\n"

# SVM
# from sklearn.svm import SVC
# clf = SVC(kernel = 'linear')
# clf.fit(features, labels)
# print "SVM"
# print clf.score(features, labels)

#################################################################

print "################################################################\
"

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

# Used train-test split before; changed to cross-validation  #(better)
# from sklearn.cross_validation import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, 
# random_state=42)


clf = GaussianNB()
print "Gaussian Naive Bayes"

# using the given tester's classification function to perform 1000
# fold cross validation

test_classifier(clf, pd.DataFrame.to_dict(imp, orient = 'index'), features_list)

clf = tree.DecisionTreeClassifier()
print "Decision Tree"
test_classifier(clf, pd.DataFrame.to_dict(imp, orient = 'index'), features_list)

clf = RandomForestClassifier()
print "Random forest"
test_classifier(clf, pd.DataFrame.to_dict(imp, orient = 'index'), features_list)

# SVM took too long and didn't get any positive points
# in any of its runs

# clf = SVC(kernel = 'linear')
# clf.fit(features_train, labels_train)
# print "SVM"
# print clf.score(features_test, labels_test)
# pred = clf.predict(features_test)
# print "Precision"
# print metrics.precision_score(labels_test, pred)
# print "Recall"
# print metrics.recall_score(labels_test, pred)
# print "F1 score"
# print metrics.f1_score(labels_test, pred)

# Going ahead with decision trees; while the accuracy isn't
# the best; it's only slightly lower, but precision, recall
# and F1 metrics are much better than other algorithms

# Let's tweak this to a better performance

#################################################################

print "################################################################\
"

# Perform a GridSearchCV of certain parameters
from sklearn.model_selection import GridSearchCV
parameters = {'criterion':('gini', 'entropy'), 'max_features': [None, 1, 2, 3], 'min_impurity_split': [1e-7, 1e-3, 1e1]}

dt = tree.DecisionTreeClassifier()

clf = GridSearchCV(dt, parameters)
clf.fit(features_train, labels_train)

# print "The best parameters:"
# print clf.best_params_

# Using those parameters

#################################################################

print "################################################################\
"

print "Classifier with all the created features"

clf = tree.DecisionTreeClassifier(max_features = None, min_impurity_split = 1e-7, criterion = 'gini')
test_classifier(clf, pd.DataFrame.to_dict(imp, orient = 'index'), features_list)

print "Classifier with more than created features"

features_list = ['salary_bonus', 'high_from_to', 'long_term_incentive', 'salary', 'total_stock_value']

clf = tree.DecisionTreeClassifier(max_features = None, min_impurity_split = 1e-7, criterion = 'gini')
test_classifier(clf, pd.DataFrame.to_dict(imp, orient = 'index'), features_list)

print "Classifier with more than created features"

features_list = ['salary_bonus', 'high_from_to', 'long_term_incentive', 'salary', 'deferred_income']

clf = tree.DecisionTreeClassifier(max_features = None, min_impurity_split = 1e-7, criterion = 'gini')
test_classifier(clf, pd.DataFrame.to_dict(imp, orient = 'index'), features_list)


print "Classifier with more than created features"

features_list = ['salary_bonus', 'high_from_to', 'long_term_incentive', 'salary', 'total_stock_value']

clf = tree.DecisionTreeClassifier(max_features = None, min_impurity_split = 1e-7, criterion = 'gini')
test_classifier(clf, pd.DataFrame.to_dict(imp, orient = 'index'), features_list)


features_list = ['salary_bonus', 'high_from_to', 'salary', 'long_term_incentive']

#################################################################

print "################################################################\
"


# Not too good, but much better than expected!

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)