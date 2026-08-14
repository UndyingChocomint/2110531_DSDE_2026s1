import pandas as pd
from sklearn.model_selection import train_test_split

"""
    ASSIGNMENT 2 (STUDENT VERSION):
    Using pandas to explore Titanic data from Kaggle (titanic_to_student.csv) and answer the questions.
    (Note that the following functions already take the Titanic dataset as a DataFrame, so you don’t need to use read_csv.)

"""


def Q1(df):
    """
        Problem 1:
            How many rows are there in the "titanic_to_student.csv"?
    """
    # TODO: Code here
    return df.shape[0]


def Q2(df):
    '''
        Problem 2:
            2.1 Drop variables with missing > 50%
            2.2 Check all columns except 'Age' and 'Fare' for flat values, drop the columns where flat value > 70%
            From 2.1 and 2.2, how many columns do we have left?
            Note: 
            -Ensure missing values are considered in your calculation. If you use normalize in .value_counts(), please include dropna=False.
    '''
    # TODO: Code here
    # drop variables with missing > 50% 
    cols_to_drop = [col for col in df.columns if df[col].isnull().mean() > 0.5]
    df = df.drop(columns=cols_to_drop)
    
    cols_to_check = [col for col in df.columns if col not in ['Age', 'Fare']]
    flat_ratio = df[cols_to_check].apply(lambda x: x.value_counts(dropna=False).max() / len(x))    
    cols_to_drop_flat = flat_ratio[flat_ratio >= 0.7].index
    df = df.drop(columns=cols_to_drop_flat)
    return df.shape[1]


def Q3(df):
    '''
       Problem 3:
            Remove all rows with missing targets (the variable "Survived")
            How many rows do we have left?
    '''
    # TODO: Code here
    df=  df['Survived'].dropna()
    return df.shape[0]



def Q4(df):
    Q1 = df['Fare'].quantile(0.25)
    Q3 = df['Fare'].quantile(0.75)
    IQR = Q3 - Q1
    lowerbound = Q1 - 1.5 * IQR
    higherbound = Q3 + 1.5 * IQR
    df['Fare'] = df['Fare'].clip(lower=lowerbound, upper=higherbound)
    return round(df['Fare'].mean(), 2)

def Q5(df):
    '''
       Problem 5:
            Impute missing value
            For number type column, impute missing values with mean
            What is the average (mean) of “Age” after imputing the missing values (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    for i in df.index : 
        if df.loc[i,'Age'] == None: 
            df.loc[i,'Age'] = df['Age'].mean
    return round(df['Age'].mean(),2)


def Q6(df):
    '''
        Problem 6:
            Convert categorical to numeric values
            For the variable “Embarked”, perform the dummy coding.
            What is the average (mean) of “Embarked_Q” after performing dummy coding (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    # print(df['Embarked'].value_counts())
    # lamda use syntex value then if, but 
    
    dummies = pd.get_dummies(df['Embarked'], prefix='Embarked').astype(int)
    df = pd.concat([df, dummies], axis=1) 
    return round(df['Embarked_Q'].mean(),2)


def Q7(df):
    '''
        Problem 7:
            Split train/test split with stratification using 70%:30% and random seed with 123
            Show a proportion between survived (1) and died (0) in all data sets (total data, train, test)
            What is the proportion of survivors (survived = 1) in the training data (round 2 decimal points)?
            Hint: Use function round(_, 2), and train_test_split() from sklearn.model_selection, 
            Don't forget to impute missing values with mean.
    '''
    
    # TODO: Code here
    train,test = df.train_test_split(0.7, random_state = 123,)
    
    return None
