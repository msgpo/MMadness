# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 16:26:16 2015

@author: jmf
"""


"""

Train an SVM to decide which team wins a game, given the observed stats for 
team1 and team2

Train multiple SVMs to predict an "observed" variable from a team's prob dist
for each statistic (computed from the season)
"""

#import sklearn
import numpy as np
import sklearn
from sklearn import svm
from os.path import isfile
import cPickle

def readPickles():
    with open("../data/allGames.pickle",'rb') as f:
        seasons = cPickle.load(f)
    with open("../data/allTeams.pickle",'rb') as f:
        teams = cPickle.load(f)
    return teams, seasons
    
#def SRSfactor(srs,npvec):
#    if srs < 0:
#        neg = True
#    else:
#        neg = False
#    s = np.sqrt()
    
def toData(teams,seasons):
    data=[]
    z   =[]
    labels = []
    for year,season in seasons.iteritems():
        for game in season:
            try:
                #print str(game.year)+" WTeam: " + str(game.winTeam) + "LTeam: "+ str(game.loseTeam)
                wTeam = teams[year][game.winTeam]
                wStat = game.getWStats(teams)
                wSRS  = wTeam.srs
#                print "game winner stats:" + str(wStat)
#                print "winning team srs: " + str(wSRS)
                lTeam = teams[year][game.loseTeam]
                lStat = game.getLStats(teams)
                lSRS  = lTeam.srs
#                print "losing team stats: "+str(lStat)
#                print "losing team srs: " + str(lSRS)
                if np.random.random() < 0.5: #scramble winning/losing team
                    l = [1]
                    r = []
                    r = np.append(r,wSRS)
                    r = np.append(r,wStat[0])
                    r = np.append(r,wStat[1])
                    r = np.append(r,lSRS)
                    r = np.append(r,lStat[0])
                    r = np.append(r,lStat[1])
                    r = np.array(r).flatten()
                    r = np.reshape(r,(1,r.shape[0]))
                    #print "both stats:" + str(r)                    
                else:
                    l = [0]  
                    r = []
                    r = np.append(r,lSRS)
                    r = np.append(r,lStat[0])
                    r = np.append(r,lStat[1])
                    r = np.append(r,wSRS)
                    r = np.append(r,wStat[0])
                    r = np.append(r,wStat[1])
                    r = np.array(r).flatten()
                    r = np.reshape(r,(1,r.shape[0]))
                    #print "both stats: " +str(r)
                if data == []:
                    data = np.array(r)
                    labels = np.array(l)
                else:
                    data = np.append(data,r,axis=0)  
                    labels = np.append(labels,l,axis=0)

            except KeyError as e:
                #print "No game or team: " + str(e) 
                pass
    return data, labels
    
clf = sklearn.svm.SVC()    
if not isfile("../data/alldata.pickle") & isfile("../data/alllabels.pickle"): 
    print "Parsing data from txts"       
    teams, seasons = readPickles()
    data,labels = toData(teams, seasons)
    with open("../data/alldata.pickle",'wb') as f:
        cp = cPickle.Pickler(f)
        cp.dump(data)
    with open("../data/alllabels.pickle",'wb') as f:
        cp = cPickle.Pickler(f)
        cp.dump(labels)
else:
    print "Reading data from pickles"
    with open("../data/alldata.pickle",'rb') as f:
        data = cPickle.load(f)
    with open("../data/alllabels.pickle",'rb') as f:
        labels = cPickle.load(f)
    print data[0]
    print np.sum(labels)*1./len(labels)
means = np.mean(data,axis=0)
stDev = np.std(data,axis=0)
data = np.divide(np.subtract(data,means),stDev)
l = data.shape[0]
tl = int(4*l/5)
train = data[:tl]
test = data[tl:]
trainlab = labels[:tl]
testlab = labels[tl:]
clf.fit(train,trainlab)
pred = clf.predict(test)
count = 0
correct = 0
wrong = 0
for x in pred:
    if x == testlab[count]:
        correct +=1
    else:
        wrong += 1
    count+=1
print correct, wrong, str(correct*1./(correct+wrong))    
