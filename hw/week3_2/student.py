
import pandas as pd
# hint
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import numpy as np
# sklearn_import for transform 
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

import math
import warnings # DO NOT modify this line
from sklearn.exceptions import ConvergenceWarning # DO NOT modify this line
warnings.filterwarnings("ignore", category=ConvergenceWarning) # DO NOT modify this line


class BankLogistic:
    def __init__(self, data_path): # DO NOT modify this line
        self.data_path = data_path
        self.df = pd.read_csv(data_path, sep=',')
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def Q1(self): # DO NOT modify this line
        """
        Problem 1:
            Load ‘bank-st.csv’ data from the “Attachment”
            How many rows of data are there in total?

        """

        # TODO: Paste your code here
        return self.df.shape[0]

    def Q2(self): # DO NOT modify this line
        """
        Problem 2:
            return the tuple of numeric variables and categorical variables are presented in the dataset.
        """
        nums = 0 
        cats = 0 
        for col in self.df: 
            # check cats
            if self.df[col].dtype == 'object' : 
                cats += 1 
            else : 
                nums +=1 
                
        # TODO: Paste your code here
        
        return nums, cats
    
    def Q3(self): # DO NOT modify this line
        """
        Problem 3:
            return the tuple of the Class 0 (no) followed by Class 1 (yes) in 3 digits.
        """
        
        # TODO: Paste your code here
     #   print(self.df.isna().sum())
        # no missing data 
     #   print(self.df['y'])
        
       # self.df['y'].apply(lambda x: 1 if 'yes'  else 0)
        percent = self.df['y'].value_counts(normalize=True).values.tolist() 
        class0 = round(percent[0],3)
        class1 = round(percent[1],3)
        
        return class0, class1
      
    

    def Q4(self): # DO NOT modify this line
        """
        Problem 4:
            Remove duplicate records from the data. What are the shape of the dataset afterward?
        """
        # TODO: Paste your code here
        self_df = self.df.drop_duplicates()
        return self_df.shape
        

    def Q5(self): # DO NOT modify this line
        """
        Problem 5:
            5. Replace unknown value with null
            6. Remove features with more than 99% flat values. 
                Hint: There is only one feature should be drop
            7. Split Data
            -	Split the dataset into training and testing sets with a 70:30 ratio.
            -	random_state=0
            -	stratify option
            return the tuple of shapes of X_train and X_test.

        """
        # TODO: Paste your code here
        # step 5 replace unknow with null 
        #print(self.df.isna().sum())
        self.df = self.df.drop_duplicates()
        self.df = self.df.replace('unknown', np.nan)
        # step 6 using normalize to find the feature that should be drop 
        #percent = self.df['y'].value_counts(normalize=True).values.tolist() 
        cols_to_drop = []

        for col in self.df.columns:
            if self.df[col].value_counts(normalize=True).max() > 0.99:
                cols_to_drop.append(col)
       # print(cols_to_drop)
        self.df = self.df.drop(columns=cols_to_drop)

        # split data 
        y = self.df.pop('y')
        x = self.df 
        x_train, x_test, y_train,y_test = train_test_split(x,y,test_size=0.3, random_state=0, stratify=y)

        return x_train.shape, x_test.shape 

       
    def Q6(self): 
        """
        Problem 6: 
            8. Impute missing
                -	For numeric variables: Impute missing values using the mean.
                -	For categorical variables: Impute missing values using the mode.
                Hint: Use statistics calculated from the training dataset to avoid data leakage.
            9. Categorical Encoder:
                Map the nominal data for the education variable using the following order:
                education_order = {
                    'illiterate': 1,
                    'basic.4y': 2,
                    'basic.6y': 3,
                    'basic.9y': 4,
                    'high.school': 5,
                    'professional.course': 6,
                    'university.degree': 7} 
                Hint: Use One hot encoder or pd.dummy to encode nominal category
            return the shape of X_train.

        """
        # TODO: Paste your code here
                # TODO: Paste your code here
        # step 5 replace unknow with null 
        #print(self.df.isna().sum())
        self.df = self.df.drop_duplicates()
        self.df = self.df.replace('unknown', np.nan)
        # step 6 using normalize to find the feature that should be drop 
        #percent = self.df['y'].value_counts(normalize=True).values.tolist() 
        cols_to_drop = []

        for col in self.df.columns:
            if self.df[col].value_counts(normalize=True).max() > 0.99:
                cols_to_drop.append(col)
       # print(cols_to_drop)
        self.df = self.df.drop(columns=cols_to_drop)

        # split data 
        y = self.df.pop('y')
        x = self.df 
        x_train, x_test, y_train,y_test = train_test_split(x,y,test_size=0.3, random_state=0, stratify=y)
        
        for col in x_train.columns:
            if x_train[col].dtype == 'object':
                mode_val = x_train[col].mode()[0]
                x_train[col] = x_train[col].fillna(mode_val)
                x_test[col] = x_test[col].fillna(mode_val)   # reuse train's mode — no leakage
            else:
                mean_val = x_train[col].mean()
                x_train[col] = x_train[col].fillna(mean_val)
                x_test[col] = x_test[col].fillna(mean_val)   # reuse train's mean — no leakage
        education_order = {
                    'illiterate': 1,
                    'basic.4y': 2,
                    'basic.6y': 3,
                    'basic.9y': 4,
                    'high.school': 5,
                    'professional.course': 6,
                    'university.degree': 7
        } 
        x_train['education'] = x_train['education'].map(education_order)
       # x_test['education'] = x_test['education'].map(education_order)
        x_train_transform = pd.get_dummies(x_train ).astype(int)

        self.X_test = x_test
        self.X_train = x_train_transform 
        self.y_test = y_test
        self.y_train = y_train

        return x_train_transform.shape 
    
    def Q7(self):
        ''' Problem7: Use Logistic Regression as the model with 
            random_state=2025, 
            class_weight='balanced' and 
            max_iter=500. 
            Train the model using all the remaining available variables. 
            What is the macro F1 score of the model on the test data? in 3 digits
        '''
        """
        Problem 6: 
            8. Impute missing
                -	For numeric variables: Impute missing values using the mean.
                -	For categorical variables: Impute missing values using the mode.
                Hint: Use statistics calculated from the training dataset to avoid data leakage.
            9. Categorical Encoder:
                Map the nominal data for the education variable using the following order:
                education_order = {
                    'illiterate': 1,
                    'basic.4y': 2,
                    'basic.6y': 3,
                    'basic.9y': 4,
                    'high.school': 5,
                    'professional.course': 6,
                    'university.degree': 7} 
                Hint: Use One hot encoder or pd.dummy to encode nominal category
            return the shape of X_train.

        """
        # TODO: Paste your code here
                # TODO: Paste your code here
        # step 5 replace unknow with null 
        #print(self.df.isna().sum())
        self.df = self.df.drop_duplicates()
        self.df = self.df.replace('unknown', np.nan)
        # step 6 using normalize to find the feature that should be drop 
        #percent = self.df['y'].value_counts(normalize=True).values.tolist() 
        cols_to_drop = []

        for col in self.df.columns:
            if self.df[col].value_counts(normalize=True).max() > 0.99:
                cols_to_drop.append(col)
       # print(cols_to_drop)
        self.df = self.df.drop(columns=cols_to_drop)

        # split data 
        y = self.df.pop('y')
        x = self.df 
        x_train, x_test, y_train,y_test = train_test_split(x,y,test_size=0.3, random_state=0, stratify=y)
        
        for col in x_train.columns:
            if x_train[col].dtype == 'object':
                mode_val = x_train[col].mode()[0]
                x_train[col] = x_train[col].fillna(mode_val)
                x_test[col] = x_test[col].fillna(mode_val)   # reuse train's mode — no leakage
            else:
                mean_val = x_train[col].mean()
                x_train[col] = x_train[col].fillna(mean_val)
                x_test[col] = x_test[col].fillna(mean_val)   # reuse train's mean — no leakage
        education_order = {
                    'illiterate': 1,
                    'basic.4y': 2,
                    'basic.6y': 3,
                    'basic.9y': 4,
                    'high.school': 5,
                    'professional.course': 6,
                    'university.degree': 7
        } 
        x_train['education'] = x_train['education'].map(education_order)
        x_test['education'] = x_test['education'].map(education_order)
        x_train_transform = pd.get_dummies(x_train ).astype(int)
        x_train_transform = pd.get_dummies(x_train).astype(int)
        x_test_transform = pd.get_dummies(x_test).astype(int)
        x_test_transform = x_test_transform.reindex(columns=x_train_transform.columns, fill_value=0)

        self.X_train = x_train_transform
        self.X_test = x_test_transform
        self.y_test = y_test
        self.y_train = y_train

        # Q7 
        LR = LogisticRegression(
            random_state=2025, 
            class_weight='balanced',
            max_iter=500,

        )
        # TODO: Paste your code here
        LR.fit(self.X_test, self.y_test)
        predict = LR.predict(self.X_test)
        report = classification_report(self.y_test, predict, digits=3,output_dict=True)
        macro_f1_from_report = report['macro avg']['f1-score']
        
        truncated = math.trunc(macro_f1_from_report * 100) / 100

        return truncated
        


   