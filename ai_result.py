# -*- coding: utf-8 -*-
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

replace_smoking ={"Smoking":{"к":"1", "н":"0", " ":"0"}}
replace_IL1b = {'IL1b':{'T/T':1,"T/C":1, "C/C":0}}
replace_TNF = {'TNF':{'A/A':1,'G/G':0,'G/A':0}}
replace_APEX1 = {"APEX1": {"G/G":1, "T/T":0,"T/G":0}}
replace_XPD={"XPD": {"T/G":1,"G/G":1, "T/T":0}}
replace_EGFR={"EGFR": {"A/A" :1, "T/T":0,"A/T":0}}
replace_CHEK2={"CHEK2":{"N/P":1,"P/P":1, "N/N":0}}
replace_TGFb1={"TGFb1": {"G/G":1, "G/C":0,"C/C":0}}
replace_EPHX1={"EPHX1 ": {"T/T":1, "T/C":0,"C/C":0}}

class Forest_AI():
    def __init__(self, is_smoking = True, is_Il1b = True,is_TNF = True,is_APEX1 = True,is_XPD = True, 
    is_EGFR = True,is_CHEK2 = True,is_TGFb1 = True, is_EPHX1 = True):
        self.error_read = False
        try:
            self.df = pd.read_csv("data_rak.csv", delimiter=';').dropna()
        except: 
            self.error_read = True
            return
        self.df = self.df.replace(replace_smoking) 
        #Il1b +
        self.df = self.df.replace(replace_IL1b) if is_Il1b else self.df.drop(list(replace_IL1b.keys())[0], axis = 1)
        #TNF +
        self.df = self.df.replace(replace_TNF) if is_TNF else self.df.drop(list(replace_TNF.keys())[0], axis = 1)
        #APEX1 +
        self.df = self.df.replace(replace_APEX1) if is_APEX1 else self.df.drop((list(replace_APEX1.keys())[0]), axis = 1)
        #XPD +
        self.df = self.df.replace(replace_XPD) if is_XPD else self.df.drop((list(replace_XPD.keys())[0]), axis = 1)
        #EGFR +
        self.df = self.df.replace(replace_EGFR) if is_EGFR else self.df.drop((list(replace_EGFR.keys())[0]), axis = 1)
        #CHEK2 +
        self.df = self.df.replace(replace_CHEK2) if is_CHEK2 else self.df.drop((list(replace_CHEK2.keys())[0]), axis = 1)
        #TGFb1 +
        self.df = self.df.replace(replace_TGFb1) if is_TGFb1 else self.df.drop(list(replace_TGFb1.keys())[0], axis = 1)
        #EPHX1 +
        self.df = self.df.replace(replace_EPHX1) if is_EPHX1 else self.df.drop(list(replace_EPHX1.keys())[0], axis = 1)    

        
    def train(self, test_size = 0.3, random_split = 2958, depth_par = 5, random_state_par = 1751):
        if test_size > 1 or test_size<=0:
            return None

        y = self.df['Status'].values
        self.df = self.df.drop('Status', axis = 1)
        print(self.df)
        x = self.df.values
        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=test_size, random_state = random_split, stratify=y)
        self.rf = RandomForestClassifier(n_jobs=-1,max_depth=depth_par, random_state = random_state_par, bootstrap = 1, min_samples_split=2, n_estimators=11, min_samples_leaf = 3, max_features='log2')
        self.rf.fit(x_train, y_train)
        rf_pred = self.rf.predict(x_test)
        acc_rf = accuracy_score(y_test, rf_pred)
        return acc_rf

    def calc_Answer(self, answer):
        if type(answer) != type(pd.DataFrame()):
            answer = pd.DataFrame(answer)
        rf_pred = self.rf.predict(answer)
        print(rf_pred)
        return rf_pred








