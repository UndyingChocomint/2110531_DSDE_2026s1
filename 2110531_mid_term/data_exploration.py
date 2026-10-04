import pandas as pd

file_path_train = "./train.csv"
df_train = pd.read_csv(file_path_train, header=0)
file_path_picture ="./train"

# print(distribution of train model)
print(df_train['class_id'].value_counts(normalize= True).sort_index())


# how many picture taken

print(df_train['image_id'].value_counts())
print(df_train['image_id'].nunique())

#print(df_train['class_id'].unique())

# find the average cars per picture 

  # objects per image (all classes)
per_image = df_train.groupby("image_id").size()
print(per_image.describe())          # count, mean, std, min, max, quartiles
print("avg:", per_image.mean(), "sd:", per_image.std())

  # cars (class 0) per image — reindex so images with 0 cars count as 0
all_imgs = df_train["image_id"].unique()
cars_per_image = (
      df_train[df_train["class_id"] == 0]
      .groupby("image_id").size()
      .reindex(all_imgs, fill_value=0)
  )
print("cars avg:", cars_per_image.mean(), "sd:", cars_per_image.std())

  # avg + sd for EVERY class in one table
report = (
      df_train.groupby(["image_id", "class_id"]).size()
        .unstack("class_id", fill_value=0)   # one column per class, zeros filled
        .agg(["mean", "std"])                # avg & sd per class across images
  )
print(report.T)   # rows = class_id, cols = mean, std
