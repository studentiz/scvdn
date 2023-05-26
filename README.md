# Single-cell virus detection network (scVDN)
* Identifying SARS-CoV-2 infected cells with scVDN

## Runtime Environment
* We strongly recommend users to use Google Colab to replicate scVDN projects. Specifically, scVDN requires at least 50GB of memory for training, and users should subscribe to the Colab Pro service.

## Original single cell data
* You can download the raw single-cell data from the nasal swab samples collected by the Jose Ordovas-Montanes group via the following link.
* https://drive.google.com/file/d/1XAATUnY3QPluIKtxDRQjJQPB9Y8wxqX1/view?usp=sharing

## The scVDN model training
* You can train the scVDN model based on our code. The following code includes the dataset preparation and neural network framework structure required for training the scVDN model. Note: Due to the neural network using random gradient descent to optimize scVDN, the performance of the scVDN model you trained may not be consistent with the performance of the scVDN model we trained.
* <u>"scVDN_model_training.ipynb"</u> needs to be run in jupyter lab or Google Colab.
* <u>"scvdn_model_training.py"</u> includes all codes of <u>"scVDN_model_training.ipynb"</u>.

## The scVDN model trained by the author
* You can download our pre-trained scVDN model, which was trained using ciliated cells. This model is the same scVDN model mentioned in our published paper.
* https://drive.google.com/file/d/1XAATUnY3QPluIKtxDRQjJQPB9Y8wxqX1/view?usp=share_link


## Trained scVDN model link
* You can directly download our trained scVDN model at the following link. This model is consistent with the scVDN model in the paper, which uses ciliated cells for training.
* https://drive.google.com/file/d/1Kl_-m4KyVeD1JYTuP03kmuyKI_C4nmaO/view?usp=sharing

## Models evolution
* You can access the code for model evaluation policies in any of the following files. 
* <u>"Models_Evaluation.ipynb"</u> needs to be run in jupyter lab or Google Colab.
* <u>"Models_ Evaluation.py"</u> includes all codes of <u>"Models_Evaluation.ipynb"</u>.

## Reproducing and visualizing figures in paper
* You can reproduce the figures and visualizations from our paper using this section of code.
* <u>"Figures.ipynb"</u> needs to be run in jupyter lab or Google Colab.
* <u>"figures.ipynb"</u> includes all codes of <u>"Figures.ipynb"</u>.




