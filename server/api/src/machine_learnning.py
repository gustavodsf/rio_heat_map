#!/usr/bin/env python
import sys
import json
import urllib.request
import psycopg2
#from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_regression
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn import preprocessing
from sklearn import svm
import cgi, cgitb

cgitb.enable()  # debug

data = cgi.FieldStorage()

class MachineLearnning:

  def run(self, arrData):
    #test
    #text = np.genfromtxt('modified_result.csv', delimiter="\t", dtype=None, skip_header=1)
    #r = urllib.request.urlopen("http://localhost:8080/violence/get/3000")
    #arrData = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    #print(text)
    #arrData = []
    '''
    for t in text:
      arrData.append(str(t).split(","))
    arrData = np.array(arrData)
    '''
    #regr = RandomForestClassifier(max_depth=2, random_state=0)
    clf = svm.SVC()
    le = preprocessing.LabelEncoder()
    #print(arrData[0])
    #indices = np.where(arrData["type"] == '2')[0] #crime type = 2
    #print(indices)
    '''
    result = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0,'None':0}
    for k in arrData:
      result[k["type"]]+=1
    print(result)
    '''

    data = []
    labels = []
    for a in arrData:
      data.append([a["neighborhood"],a["day_of_week"]])
      labels.append(a["shift"])


    qtyTrain = int(len(labels)*0.8)
    data = np.array(data)

    attr1 = data[:,0]
    le.fit(attr1)
    attr1Train = le.transform(attr1[:qtyTrain]) 
    attr1Test = le.transform(attr1[qtyTrain:])

    attr2 = data[:,1]
    le.fit(attr2)
    attr2Train = le.transform(attr2[:qtyTrain])
    attr2Test = le.transform(attr2[qtyTrain:])

    testData = []
    trainData = []

    for i in range(len(attr1Train)):
      trainData.append([attr1Train[i], attr2Train[i]])
    for x in range(len(attr1Test)):
      testData.append([attr1Test[x], attr2Test[x]])

    labels = np.array(labels)
    trainLabels = labels[:qtyTrain]

    #print(trainData)
    #print(testData)

    #regr.fit(trainData, trainLabels)
    clf.fit(trainData, trainLabels)

    testLabels = labels[qtyTrain:]
    #le.fit(testLabels)
    #testLabels = le.transform(testLabels)
    #X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
    #print(regr.feature_importances_)
    #predicted = regr.predict(testData)
    #print(testLabels)
    #print(predicted)
    #print(accuracy_score(testLabels, predicted))

    predicted = clf.predict(testData)
    #print(testLabels)
    #print(predicted)
    return(accuracy_score(testLabels, predicted))