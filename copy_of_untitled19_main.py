# -*- coding: utf-8 -*-
"""Copy of Untitled19 Main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HhHSCSNbu8jwjQRk7lNqdAHUigtgBk0t

Importing all files and Pretrained RESNET 50 for fine tuning
"""

from tqdm import tqdm 
import tensorflow as tf 
from keras.applications.resnet50 import ResNet50
from keras.layers import Flatten, Input
from keras.models import Model
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
from google.cloud import storage 
from io import BytesIO
import time
import cv2
start = time.time()
 
import pandas as pd

import zipfile

import os

# from google.colab import drive
# drive.mount('/content/drive')
# # !gdown https://drive.google.com/file/d/1h1z2fwar1a0W1r3rrRF8eDu3ZMjZT0Y7/view?usp=sharing

from keras.preprocessing import image
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input
import numpy as np
import cv2

import pandas as pd  
df = pd.DataFrame() 
p= [str(x) for x in range(512)]
df=pd.DataFrame(columns= p)
model = VGG19(weights='imagenet', include_top=False)
model.summary()
folder_containing image= "/content/gdrive/My Drive/Kaggle/1/" #change path accordingly
for i in range(1,1021,1):
    img_path =  folder_containing_image + str(i)+".tif"
    print(img_path)
    try:
        img = image.load_img(img_path, target_size=(32, 32)) 
    except:
        print("Not found")
        continue
    
    img = image.load_img(img_path, target_size=(32, 32))

    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    vgg19_feature = model.predict(img_data)

    df.loc[len(df.index)+1] =vgg19_feature[0][0][0]

update_df= df

import pandas as pd
from sklearn import preprocessing

x = update_df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
update_df = pd.DataFrame(x_scaled)

data= update_df
print(data.shape)
data=data.sample(frac=0.1,random_state=1)
print(data.shape)
columns=data.columns.tolist()

columns=[c for c in columns if c not in ["Class"]]

X=data[columns]

import numpy as np
from numpy.linalg import norm


class Kmeans:
  

    def __init__(self, n_clusters, max_iter=100, random_state=123):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state

    def initializ_centroids(self, X):
        np.random.RandomState(self.random_state)
        random_idx = np.random.permutation(X.shape[0])
        centroids = X[random_idx[:self.n_clusters]]
        return centroids

    def compute_centroids(self, X, labels):
        centroids = np.zeros((self.n_clusters, X.shape[1]))
        for k in range(self.n_clusters):
            centroids[k, :] = np.mean(X[labels == k, :], axis=0)
        return centroids

    def compute_distance(self, X, centroids):
        distance = np.zeros((X.shape[0], self.n_clusters))
        for k in range(self.n_clusters):
            row_norm = norm(X - centroids[k, :], axis=1)
            distance[:, k] = np.square(row_norm)
        return distance

    def find_closest_cluster(self, distance):
        return np.argmin(distance, axis=1)

    def compute_sse(self, X, labels, centroids):
        distance = np.zeros(X.shape[0])
        for k in range(self.n_clusters):
            distance[labels == k] = norm(X[labels == k] - centroids[k], axis=1)
        return np.sum(np.square(distance))
    
    def fit(self, X):
        self.centroids = self.initializ_centroids(X)
        for i in range(self.max_iter):
            old_centroids = self.centroids
            distance = self.compute_distance(X, old_centroids)
            self.labels = self.find_closest_cluster(distance)
            self.centroids = self.compute_centroids(X, self.labels)
            if np.all(old_centroids == self.centroids):
                break
        self.error = self.compute_sse(X, self.labels, self.centroids)
    
    def predict(self, X):
        distance = self.compute_distance(X, centroids)
        return self.find_closest_cluster(distance)
    
    def ret_old_centre(self,X):
      return old_centroids

import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd
import seaborn as sns
from sklearn.datasets.samples_generator import (make_blobs,
                                                make_circles,
                                                make_moons)
#from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_samples, silhouette_score
X_std = StandardScaler().fit_transform(update_df)

import math
 
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))
 
def length(v):
  return math.sqrt(dotproduct(v, v))
 
def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

list_centroids=[]
list_csize= []
K= 8
for i in range(2,K+1,1):
  km= Kmeans(i,100,123)
  km.fit(X_std)
  centroids = km.centroids
  df_predicted= km.predict(X_std)
  arr = np.array(df_predicted)
  list1= []
  list2= []
  list3= []
  for j in range(0,i,1):
    count = np.count_nonzero(arr == j)
    list1.append(count)
 
  for j in range(0,len(df),1):
    
    list2.append(list1[df_predicted[j]])
    list3.append(centroids[df_predicted[j]])
  
  list_centroids.append(list3)
  list_csize.append(list2)

avgsimscore=[]
for i in range(0,len(df),1):
  upper=0
  lower=0
  for j in range(0,K-1,1):
    for l in range(j+1,K-1,1):
      lower= lower+ list_csize[j][i]+ list_csize[l][i]
      try:
        k= angle(list_centroids[j][i], list_centroids[l][i])
      except:
        continue
      
      if (k <= (3.14/2)):
        upper= upper+ (list_csize[j][i]+ list_csize[l][i])*(abs(math.cos(k)))
      else:
        upper= upper+ (list_csize[j][i]+ list_csize[l][i])*(abs(math.cos(3.14- k)))
  print(i)

  
  
  avgsimscore.append(upper/lower)
  print (avgsimscore[i])

curve_points=[]
initial= 0
arr = np.array(avgsimscore)
for i  in range(0,100,1):
  count = sum((j >= initial) and (j<(initial+0.01))  for j in arr)
  curve_points.append(count)
  initial= initial+0.01

x_axis=[]
initial=0
for i in range(0,100,1):
  x_axis.append(initial)
  initial= initial+0.01

plt.plot(x_axis, curve_points)