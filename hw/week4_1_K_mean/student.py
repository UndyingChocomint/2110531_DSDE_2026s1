#import your other libraries here
import pandas as pd 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np 
class Clustering:
    def __init__(self, file_path): # DO NOT modify this line
        #Add other parameters if needed
        self.file_path = file_path
       # self.df = None #parameter for loading csv
        self.df = pd.read_csv(self.file_path)

    def Q1(self): # DO NOT modify this line
        """
        Step1-4
            1. Load the CSV file.
            2. Choose edible mushrooms only.
            3. Only the variables below have been selected to describe the distinctive
               characteristics of edible mushrooms:
               'cap-color-rate','stalk-color-above-ring-rate'
            4. Provide a proper data preprocessing as follows:
                - Fill missing with mean
                - Standardize variables with Standard Scaler
        """
        # step1 using self.df 
        # step2 
        df_eat_mushroom = self.df[self.df["label"] == "e"]
        #
        columns_to_select = ['cap-color-rate','stalk-color-above-ring-rate']
        df_eat_mushroom =  df_eat_mushroom[columns_to_select]
       # print(df_eat_mushroom.shape)
        # remove pass and replace with you code

        # step3 fill missing, and standardize variable
        df_eat_mushroom = df_eat_mushroom.fillna(df_eat_mushroom.mean())
        Scalar = StandardScaler()
        df_eat_transform = Scalar.fit_transform(df_eat_mushroom)
       # self.df = df_eat_transform 
        return df_eat_transform.shape

    def Q2(self): # DO NOT modify this line

        df_eat_mushroom = self.df[self.df["label"] == "e"]
        #
        columns_to_select = ['cap-color-rate','stalk-color-above-ring-rate']
        df_eat_mushroom =  df_eat_mushroom[columns_to_select]
       # print(df_eat_mushroom.shape)
        # remove pass and replace with you code

        # step3 fill missing, and standardize variable
        df_eat_mushroom = df_eat_mushroom.fillna(df_eat_mushroom.mean())
        Scalar = StandardScaler()
        df_eat_transform = Scalar.fit_transform(df_eat_mushroom)
       # self.df = df_eat_transform 
        """
        Step5-6
            5. K-means clustering with 5 clusters (n_clusters=5, random_state=0, n_init='auto')
            6. Show the maximum centroid of 2 features ('cap-color-rate' and 'stalk-color-above-ring-rate') in 2 digits.
        """
        # remove pass and replace with you code
        K_model =KMeans(n_clusters=5, random_state=0, n_init='auto')
        K_model.fit(df_eat_transform)
        centroids = K_model.cluster_centers_
        max_centroid = centroids.max(axis=0)
        max_centroid_rounded = np.round(max_centroid, 2)
        return max_centroid_rounded

    def Q3(self): # DO NOT modify this line
        """
        Step7
            7. Convert the centroid value to the original scale, and show the minimum centroid of 2 features in 2 digits.

        """
        # remove pass and replace with you code
        
        df_eat_mushroom = self.df[self.df["label"] == "e"]
        #
        columns_to_select = ['cap-color-rate','stalk-color-above-ring-rate']
        df_eat_mushroom =  df_eat_mushroom[columns_to_select]
       # print(df_eat_mushroom.shape)
        # remove pass and replace with you code

        # step3 fill missing, and standardize variable
        df_eat_mushroom = df_eat_mushroom.fillna(df_eat_mushroom.mean())
        Scalar = StandardScaler()
        df_eat_transform = Scalar.fit_transform(df_eat_mushroom)
       # self.df = df_eat_transform 
        """
        Step5-6
            5. K-means clustering with 5 clusters (n_clusters=5, random_state=0, n_init='auto')
            6. Show the maximum centroid of 2 features ('cap-color-rate' and 'stalk-color-above-ring-rate') in 2 digits.
        """
        # remove pass and replace with you code
        K_model =KMeans(n_clusters=5, random_state=0, n_init='auto')
        K_model.fit(df_eat_transform)
        centroids = K_model.cluster_centers_

        min_centroid = centroids.min(axis=0)
        value = np.round(Scalar.inverse_transform(min_centroid.reshape(1, -1)), 2).flatten()

        return value 