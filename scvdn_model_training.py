# -*- coding: utf-8 -*-
"""scVDN model training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DU6xysXftsk2uhr8zwvBj_8Nuo4pArKI

# Mount Google Cloud Disk
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Install Dependency Package"""

!pip install scanpy gseapy umap-learn[plot] xgboost shap lime

"""# Import Dependency Package"""

# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import scanpy as sc
from scipy.stats import wasserstein_distance
import gc
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import scipy.stats
import gseapy as gp
import networkx as nx
from tqdm import tqdm
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, RandomForestRegressor
from sklearn import metrics
import shap
shap.initjs()
from sklearn.decomposition import PCA, NMF
from sklearn.metrics import mean_squared_error, mean_poisson_deviance
from scipy.stats import pearsonr, spearmanr, kendalltau
from sklearn import metrics
import pickle
import tensorflow as tf
import umap
import umap.plot
import lime
import lime.lime_tabular

def saveobj(obj, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)

def loadobj(filepath):
    pkl_file = open(filepath, 'rb')
    return pickle.load(pkl_file)

WORK_DIR = "/content/drive/MyDrive/SingleCellVirus/"

"""* Image clarity
* Change the font to 'Liberation Mono'
"""

# Commented out IPython magic to ensure Python compatibility.
# %config InlineBackend.figure_format = 'retina'
import matplotlib.pyplot as plt
plt.rc('font',family='Liberation Mono')

"""# scVDN

## Extract Ciliated Cells
"""

NasalSwab = sc.read_h5ad("/content/drive/MyDrive/SingleCellVirus/Datasets/20210217_NasalSwab_Broad_BCH_UMMC_to_CZI.h5ad")
CiliatedCells = NasalSwab[NasalSwab.obs.Annotation=="Ciliated Cells"]
# Delete NasalSwab and free memory
del NasalSwab
gc.collect()

"""## Establishing the training set"""

pos_obs = CiliatedCells.obs.query("SingleCell_SARSCoV2_RNA_Status=='pos' & Cohort_Disease_WHO_Score=='COVID19_WHO_1-5'")
neg_obs = CiliatedCells.obs.query("SingleCell_SARSCoV2_RNA_Status=='neg' & Cohort_Disease_WHO_Score=='COVID19_WHO_1-5'")

feature_names = CiliatedCells.var.index[CiliatedCells.var["mvp.variable"]]

pos_anndata = CiliatedCells[pos_obs.index][:, feature_names]
neg_anndata = CiliatedCells[neg_obs.index][:, feature_names]

pos_data = pos_anndata.X.A
neg_data = neg_anndata.X.A

# free memory
del pos_anndata, neg_anndata
gc.collect()

"""### Collect positive samples"""

sample_size = 4000

new_pos_data_part_pp = []
# new_pos_data_part_pp1 = np.zeros((4950, 3508))
# new_pos_data_part_pp2 = np.zeros((4950, 3508))
temp_count = pos_data.shape[0]
# temp_total_index = 0
for i in tqdm(range(temp_count)):
    for j in range(i+1, temp_count):
        new_pos_data_part_pp.append([pos_data[i], pos_data[j]])
        # new_pos_data_part_pp1[temp_total_index] = pos_data[i]
        # new_pos_data_part_pp2[temp_total_index] = pos_data[j]
        # temp_total_index += 1

new_pos_data_part_pp = np.array(new_pos_data_part_pp)
temp_index = np.random.choice(range(new_pos_data_part_pp.shape[0]), size=sample_size, replace=False)
new_pos_data_part_pp = new_pos_data_part_pp[temp_index]
new_pos_data_part_pp1 = new_pos_data_part_pp[:,0,:]
new_pos_data_part_pp2 = new_pos_data_part_pp[:,1,:]
del new_pos_data_part_pp
gc.collect()

new_pos_data_part_nn = []
# new_pos_data_part_nn1 = np.zeros((686206, 3508))
#new_pos_data_part_nn2 = np.zeros((686206, 3508))
temp_count = neg_data.shape[0]
temp_total_index = 0
for i in tqdm(range(temp_count)):
    for j in range(i+1, temp_count):
        new_pos_data_part_nn.append([neg_data[i], neg_data[j]])
        # new_pos_data_part_nn1[temp_total_index] = neg_data[i]
        # new_pos_data_part_nn2[temp_total_index] = neg_data[j]
        # temp_total_index += 1

new_pos_data_part_nn = np.array(new_pos_data_part_nn)
temp_index = np.random.choice(range(new_pos_data_part_nn.shape[0]), size=sample_size, replace=False)
new_pos_data_part_nn = new_pos_data_part_nn[temp_index]
new_pos_data_part_nn1 = new_pos_data_part_nn[:,0,:]
new_pos_data_part_nn2 = new_pos_data_part_nn[:,1,:]
del new_pos_data_part_nn
gc.collect()

"""### Collect negative samples"""

sample_size = 8000

new_neg_data_part_ng = []
# new_neg_data_part_ng1 = np.zeros((117200, 3508))
# new_neg_data_part_ng2 = np.zeros((117200, 3508))
temp_count1 = neg_data.shape[0]
temp_count2 = pos_data.shape[0]
# temp_total_index = 0
for i in tqdm(range(temp_count1)):
    for j in range(temp_count2):
        new_neg_data_part_ng.append([neg_data[i], pos_data[j]])
        # new_neg_data_part_ng1[temp_total_index] = neg_data[i]
        # new_pos_data_part_nn2[temp_total_index] = pos_data[j]
        # temp_total_index += 1

new_neg_data_part_ng = np.array(new_neg_data_part_ng)
temp_index = np.random.choice(range(new_neg_data_part_ng.shape[0]), size=sample_size, replace=False)
new_neg_data_part_ng = new_neg_data_part_ng[temp_index]
new_neg_data_part_right = new_neg_data_part_ng[:,0,:]
new_neg_data_part_left = new_neg_data_part_ng[:,1,:]
del new_neg_data_part_ng
gc.collect()

del pos_data, neg_data
gc.collect()

"""### Merge positive and negative samples"""

new_pos_data_part_right = np.vstack((new_pos_data_part_pp1, new_pos_data_part_nn1))
new_pos_data_part_left = np.vstack((new_pos_data_part_pp2, new_pos_data_part_nn2))
del new_pos_data_part_pp1, new_pos_data_part_nn1, new_pos_data_part_pp2, new_pos_data_part_nn2
gc.collect()

data_part_right = np.vstack((new_pos_data_part_right, new_neg_data_part_right))
data_part_left = np.vstack((new_pos_data_part_left, new_neg_data_part_left))
del new_pos_data_part_right, new_neg_data_part_right, new_pos_data_part_left, new_neg_data_part_left
gc.collect()

"""### Generate Label"""

sample_size = 8000*2
label = np.hstack((np.ones(int(sample_size/2)), np.zeros(int(sample_size/2))))

"""### Randomly rearrange data"""

data_index = np.random.choice(range(sample_size), size=sample_size, replace=False)
data_part_right = data_part_right[data_index]
data_part_left = data_part_left[data_index]
label = label[data_index]

"""### Save training data"""

filepath = os.path.join(WORK_DIR, "data_part_right.pkl")
saveobj(data_part_right, filepath)
filepath = os.path.join(WORK_DIR, "data_part_left.pkl")
saveobj(data_part_left, filepath)
filepath = os.path.join(WORK_DIR, "label.pkl")
saveobj(label, filepath)

"""## Load training data"""

filepath = os.path.join(WORK_DIR, "data_part_right.pkl")
data_part_right = loadobj(filepath)
filepath = os.path.join(WORK_DIR, "data_part_left.pkl")
data_part_left = loadobj(filepath)
filepath = os.path.join(WORK_DIR, "label.pkl")
label = loadobj(filepath)

"""## Establish scVDN model structure"""

# Define the input shape
feature_shape = data_part_right.shape[1]
input_shape = feature_shape

def feature_model(input_shape):

    input_layer = tf.keras.layers.Input(shape=(input_shape,), name="input_layer")
    
    x_layer = tf.keras.layers.Dropout(0.5)(input_layer)

    x_layer = tf.keras.layers.Dense(784, 
                                    activation='linear',
                                    kernel_initializer='lecun_normal'
                                    )(x_layer)
    x_layer = tf.keras.layers.LayerNormalization(axis=-1)(x_layer)

    x_layer = tf.keras.layers.Dense(256, 
                                    activation='relu',
                                    kernel_initializer='lecun_normal'
                                    )(x_layer)

    x_layer = tf.keras.layers.Dense(32, activation='relu', kernel_initializer='lecun_normal')(x_layer)

    return tf.keras.models.Model(inputs=input_layer, outputs=x_layer)



# Create the twin models
feature_extraction = feature_model(input_shape)

# Define the input data
left_input = tf.keras.Input(shape=input_shape)
right_input = tf.keras.Input(shape=input_shape)

# Get the output from each model
left_output = feature_extraction(left_input)
right_output = feature_extraction(right_input)

def cosine_distance(vectors):
    vector1, vector2 = vectors
    dot_product = tf.reduce_sum(tf.multiply(vector1, vector2), axis=1, keepdims=True)
    norm_product = tf.norm(vector1, axis=1, keepdims=True) * tf.norm(vector2, axis=1, keepdims=True)
    return dot_product / norm_product

# Calculate the distance between the outputs
distance = tf.keras.layers.Lambda(cosine_distance)([left_output, right_output])

# Define the final model
siamese_model = tf.keras.models.Model(inputs=[left_input, right_input], outputs=distance)

# Compile the model
siamese_model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.000001, clipvalue=0.99), metrics=['accuracy'])

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
siamese_model.fit([data_part_right, data_part_left], label, epochs=1000, batch_size=128, validation_split=0.2, shuffle=True, callbacks=[callback])

"""## Save the trained scVDN model"""

filepath = os.path.join(WORK_DIR, "siamese_model_t.pkl")
saveobj(siamese_model, filepath)