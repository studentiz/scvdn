# Identifying SARS-CoV-2 Infected Cells with scVDN

This tutorial is designed to assist researchers in building and learning the scVDN model used to identify SARS-CoV-2 infected cells. All the necessary data and source code for scVDN can be found in this GitHub repository, and you can even reproduce the figures from our paper using this documentation.

## Runtime Environment

We strongly recommend using Google Colab to replicate scVDN projects, as scVDN requires a minimum of 50GB of memory for training. To use Colab with scVDN, users should subscribe to the Colab Pro service.

## Single Cell Data

You can download the raw single-cell data from nasal swab samples collected by the Jose Ordovas-Montanes group from the following link:

- https://drive.google.com/file/d/1XAATUnY3QPluIKtxDRQjJQPB9Y8wxqX1/view?usp=sharing

## scVDN Model Training

To train the scVDN model, you can use our code, which includes the necessary dataset preparation and neural network framework structure. Please note that due to the neural network using random gradient descent to optimize scVDN, the performance of the model you train may not be consistent with the performance of our trained model. The following files areavailable:

- `scVDN_model_training.ipynb`: This notebook file should be run in Jupyter Lab or Google Colab.
- `scvdn_model_training.py`: This Python file includes all the code from the `scVDN_model_training.ipynb` notebook.

## Trained scVDN Model

You can download our pre-trained scVDN model, which was trained using ciliated cells and is the same model mentioned in our published paper, from the following link:

- https://drive.google.com/file/d/1XAATUnY3QPluIKtxDRQjJQPB9Y8wxqX1/view?usp=share_link

## Model Evaluation

You can access the code for model evaluation policies in the following files:

- `Models_Evaluation.ipynb`: This notebook file should be run in Jupyter Lab or Google Colab.
- `Models_Evaluation.py`: This Python file includes all the code from the `Models_Evaluation.ipynb` notebook.

## Reproducing and Visualizing Figures in Paper

You can reproduce the figures and visualizations from our paper using the following files:

- `Figures.ipynb`: This notebook file should be run in Jupyter Lab or Google Colab.
- `figures.ipynb`: This Python file includes all the code from the `Figures.ipynb` notebook.

We hope that this tutorial will be helpful in using scVDN to identify SARS-CoThank you for your feedback. Here's the revised version of your README.md file in Markdown format: