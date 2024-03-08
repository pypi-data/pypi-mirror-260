import pandas as pd
from tqdm import tqdm
from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering
from sklearn.model_selection import RandomizedSearchCV
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix
from collections import Counter
import numpy as np
import scipy.stats as ss
from matplotlib.lines import Line2D
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import inspect

warnings.filterwarnings("ignore", lineno=142)


# Normalize from 0 to 1
def normalize_df(df):
    max_score = df.max().max()
    min_score = df.min().min()
    return (df - min_score) / (max_score - min_score)


class dracoon_cutoff:
    def __init__(self, data, conditions_df, network, pval_columns, cutoff_upper_bound, scoring_method):
        self.data = data
        self.conditions_df = conditions_df
        self.network = network
        self.pval_columns = pval_columns
        self.scoring_method = scoring_method
        self.cutoff_upper_bound = cutoff_upper_bound
        self.best_performer = None
        self.predicted_labels = None

        true_labels = self.conditions_df['condition']
        lb = preprocessing.LabelBinarizer()
        self.true_labels = lb.fit_transform(true_labels).flatten()
        self.scoring_dictionary = {'MCC': self.clustering_scorer_MCC, 'Jaccard': self.clustering_scorer_JCC}

    def run(self):
        if self.scoring_method is None:
            score = None
        else:
            score = self.scoring_dictionary[self.scoring_method]

        self.hc_randomsearch(cutoff_upper_bound=self.cutoff_upper_bound, scoring_function=self.scoring_method)
        self.predict_labels_best_performer()
        self.match_labels_calculate_jaccard()
        print("MCC:", self.matthews_cc(self.true_labels, self.predicted_labels))
        self.plot_heatmap()

    @staticmethod
    def jaccard_similarity(label, true_labels, predicted_labels):
        true_indices = np.where(true_labels == label)[0]
        predicted_indices = np.where(predicted_labels == label)[0]

        intersection = len(np.intersect1d(true_indices, predicted_indices))
        union = len(np.union1d(true_indices, predicted_indices))

        return intersection / union if union > 0 else 0

    @staticmethod
    def matthews_cc(true_labels, predicted_labels):
        TP = np.bitwise_and(true_labels, predicted_labels).sum()
        TN = np.bitwise_and(np.logical_not(true_labels), np.logical_not(predicted_labels)).sum()
        FP = np.bitwise_and(np.logical_not(true_labels), predicted_labels).sum()
        FN = np.bitwise_and(true_labels, np.logical_not(predicted_labels)).sum()

        mcc_numerator = (TP * TN) - (FP * FN)
        mcc_denominator = np.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))
        MCC = mcc_numerator / mcc_denominator
        return abs(MCC)

    def clustering_scorer_MCC(self, estimator, X, true_labels):
        predicted_labels = estimator.fit_predict(X)
        return self.matthews_cc(true_labels, predicted_labels)

    def clustering_scorer_JCC(self, estimator, X, true_labels):
        predicted_labels = estimator.fit_predict(X)

        cm = confusion_matrix(true_labels, predicted_labels)
        row_ind, col_ind = linear_sum_assignment(cm, maximize=True)
        predicted_labels_mapped = np.zeros_like(predicted_labels)

        for i in range(len(row_ind)):
            predicted_labels_mapped[predicted_labels == col_ind[i]] = row_ind[i]

        unique_labels = np.unique(np.concatenate([true_labels, predicted_labels_mapped]))
        label_weights = Counter(true_labels)

        weighted_jaccard_similarities = [
            self.jaccard_similarity(label, true_labels, predicted_labels_mapped) * (
                    label_weights[label] / len(true_labels))
            for label in unique_labels
        ]

        return sum(weighted_jaccard_similarities)

    def hc_randomsearch(self, cutoff_upper_bound=None, scoring_function=None):
        if cutoff_upper_bound is None:
            cutoff_upper_bound = 0.05
            print("No upper bound specified using 0.05")
        else:
            cutoff_upper_bound = self.cutoff_upper_bound

        if scoring_function is None:
            scoring_function = self.clustering_scorer_JCC
        else:
            scoring_function = self.scoring_dictionary[self.scoring_method]
        param_dist = {
            'n_clusters': range(2, 3),
            'metric': ['braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean',
                       'hamming', 'jaccard', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
                       'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'],
            'linkage': ['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'],
        }

        random_search = RandomizedSearchCV(
            AgglomerativeClustering(),
            param_distributions=param_dist,
            n_iter=50,
            scoring=scoring_function,
            cv=[(slice(None), slice(None))],  # Use a single "fold" since the clustering is unsupervised
            verbose=0,
            n_jobs=-1,
            random_state=0,
        )

        selected_rows = self.network[(self.network[self.pval_columns] < cutoff_upper_bound).any(axis=1)]
        min_values = selected_rows[self.pval_columns].values.ravel('K')
        min_values = [x for x in min_values if x < cutoff_upper_bound]
        min_values = sorted(min_values, reverse=True)
        print(f"Iterating through {len(min_values)} cutoffs")

        #run the first time before cutoffing
        nodes = pd.unique(selected_rows[['source', 'target']].values.ravel('K'))
        filtered_data = self.data[nodes]
        random_search.fit(filtered_data, self.true_labels)

        self.best_performer = {'score': random_search.best_score_, 
                               'params' : random_search.best_params_,
                               'subnet': selected_rows,
                               'cutoff': cutoff_upper_bound, 
                               'nodes' : nodes}

        for cutoff in tqdm(min_values):
            df = selected_rows[(selected_rows[self.pval_columns] < cutoff).any(axis=1)]
            # print(len(df))
            nodes = pd.unique(df[['source', 'target']].values.ravel('K'))
            
            if len(df) == 0:
                break

            filtered_data = self.data[nodes]
            random_search.fit(filtered_data, self.true_labels)

            if random_search.best_score_ >= self.best_performer['score'] and len(df) <= self.best_performer['subnet'].shape[0]:
                self.best_performer['score'] = random_search.best_score_
                self.best_performer['params'] = random_search.best_params_
                self.best_performer['subnet'] = df
                self.best_performer['cutoff'] = cutoff
                self.best_performer['nodes'] = nodes

        return self.best_performer

    def predict_labels_best_performer(self):
        best_hc = AgglomerativeClustering(**self.best_performer['params'])

        # Fit the model to the data and obtain the predicted cluster labels
        heatmap_df = self.data[self.best_performer['nodes']]
        self.predicted_labels = best_hc.fit_predict(heatmap_df)
        return self.predicted_labels

    def match_labels_calculate_jaccard(self):
        # Create the confusion matrix
        cm = confusion_matrix(self.true_labels, self.predicted_labels)

        # Find the optimal assignment using the Hungarian algorithm
        row_ind, col_ind = linear_sum_assignment(cm, maximize=True)

        # Map the predicted labels to the true labels
        predicted_labels_mapped = np.zeros_like(self.predicted_labels)
        for i in range(len(row_ind)):
            predicted_labels_mapped[self.predicted_labels == col_ind[i]] = row_ind[i]

        # Calculate the weighted Jaccard similarity
        unique_labels = np.unique(np.concatenate([self.true_labels, predicted_labels_mapped]))
        label_weights = Counter(self.true_labels)

        weighted_jaccard_similarities = [
            self.jaccard_similarity(label, self.true_labels, predicted_labels_mapped) * (
                        label_weights[label] / len(self.true_labels))
            for label in unique_labels
        ]

        weighted_jaccard_similarity = sum(weighted_jaccard_similarities)

        print("Weighted Jaccard Similarity:", weighted_jaccard_similarity)
        return weighted_jaccard_similarity

    def plot_heatmap(self):
        heatmap_df = ss.zscore(self.data[self.best_performer['nodes']], axis=1)

        row_conditions_df = pd.DataFrame({'predicted_labels': self.predicted_labels,
                                          'condition': self.conditions_df['condition']})
        unique_conditions = list(set(row_conditions_df['condition']))
        unique_predicted_labels = list(set(row_conditions_df['predicted_labels']))

        # Create a color map based on the row conditions, plates, and images
        color_map_predicted_labels = {label: color for label, color in zip(unique_predicted_labels,   sns.color_palette("tab10", len(unique_predicted_labels)))}
        row_colors_predicted_labels = row_conditions_df['predicted_labels'].map(color_map_predicted_labels)

        color_map_conditions = {condition: color for condition, color in zip(unique_conditions, sns.color_palette("husl", len(unique_conditions)))}
        row_colors_conditions = row_conditions_df['condition'].map(color_map_conditions)

        # Combine the color maps
        row_colors = pd.concat([row_colors_conditions, row_colors_predicted_labels], axis=1)

        # Plot the heatmap with the additional dataframe as color code for rows
        g = sns.clustermap(heatmap_df, row_colors=row_colors, figsize=(10, 8), row_cluster=True, cmap='coolwarm')

        # Create legends
        legend_elements_conditions = [
            Line2D([0], [0], marker='o', color='w', label=label_name, markerfacecolor=color, markersize=8) for
            label_name, color in color_map_conditions.items()]
        legend_elements_predicted_labels = [
            Line2D([0], [0], marker='o', color='w', label=f'Cluster {label_name}', markerfacecolor=color, markersize=8)
            for label_name, color in color_map_predicted_labels.items()]

        # Add legends to the plot
        legend_conditions = g.fig.legend(legend_elements_conditions, unique_conditions, title='Condition',
                                         bbox_to_anchor=(0.4, 0.1), loc='upper left', frameon=True)
        g.fig.add_artist(legend_conditions)
        legend_predicted_labels = g.fig.legend(legend_elements_predicted_labels,
                                               [f'Cluster {label_name}' for label_name in unique_predicted_labels],
                                               title='Predicted Clusters', bbox_to_anchor=(0.6, 0.1), loc='upper left',
                                               frameon=True)
        g.fig.add_artist(legend_predicted_labels)

        # Show the plot
        fig = plt.gcf()  # get the current figure
        fig.set_dpi(300)  # Set the DPI to 300
        plt.show()


# df = pd.read_excel(
#     "/Users/fernando/Documents/Research/DraCooN/evaluation/real_data/victor_spatialtranscriptomics/DKD_eGFR/Normalized-Abundances-With-Data.xlsx",
#     sheet_name="Sheet1", index_col=0, header=0)
# X = df.iloc[:, :-6]
# # y = df['patient_class'] # 1 = diabetic, 0 = normal
# y = df['group']  # 1 = ctrl_no_fibrosis, 0 = ctrl_fibrosis, 2 = diabetes_fibrosis
# y = pd.DataFrame(y)
# y.columns = ['condition']
# y = y[y.condition != 'Diabetic-Nephropathy']
# X = X.iloc[X.index.isin(y.index)]
# X_norm = normalize_df(X)
#
# print(X_norm.shape)
# print(y['condition'].value_counts())
# true_labels = y['condition']
#
# # print(true_labels)
# lb = preprocessing.LabelBinarizer()
# true_labels = lb.fit_transform(true_labels).flatten()
# print(true_labels.shape)
#
# data = pd.read_csv(
#     '/Users/fernando/Documents/Research/DraCooN/evaluation/real_data/victor_spatialtranscriptomics/DN/zscore_fittedbg_bonferroni_DKDEGFR_nonckd_vs_ckd_entropy.tsv',
#     sep='\t', index_col=0)
#
# test = dracoon_cutoff(data=X_norm, conditions_df=y, network=data, pval_columns=['padj_shift'],
#                       cutoff_upper_bound=0.01, scoring_method='MCC')
# test.run()
