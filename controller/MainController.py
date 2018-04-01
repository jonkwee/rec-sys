import ChromeDataCollector
import NaturalLanguageProcessor
import datetime as dt
import KMeansProcessor as KNP
import dataobject.WordListObject

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import WebsiteListProcessor
import matplotlib.cm as cm

class MainController:

    def __init__(self):
        self.chrome_data_collector = ChromeDataCollector.ChromeDataConnector()
        self.nl_processor = NaturalLanguageProcessor.NLProcessor()
        self.word_list_object = dataobject.WordListObject.WordListObject()
        self.kn_processor = KNP.KNNProcessor()

    def main(self):
        # get last stored date from pickle object
        stored_date = self.kn_processor.word_list_object.get_stored_date()
        if stored_date is None:
            stored_date = dt.datetime.now() - dt.timedelta(days=50)

        # get all url from database between time interval
        list_url = self.chrome_data_collector.get_visited_url_interval(stored_date, dt.datetime.now())

        # from all urls in database, filter out blacklisted websites
        wlp = WebsiteListProcessor.WebsiteListProcessor(list_url)
        wlp.filter_web_list()

        # prepare to train tfidf model with list of url
        self.kn_processor.set_url_list(wlp.get_web_list())
        array = self.kn_processor.fit_transform()

        # calculate cosine similarity
        cosine_sim_array = cosine_similarity(array)
        distance_array = 1 - cosine_sim_array

        # start kmeans clustering
        centroids = []
        distortion = []
        for i in range(2,20,2):
            kmeans = KMeans(n_clusters=i, random_state=0).fit(distance_array)
            distortion.append(kmeans.inertia_)
            centroids.append(i)
            ##print(kmeans.cluster_centers_)

        plt.xlabel("Number of centroids")
        plt.ylabel("Distortion")
        plt.plot(centroids, distortion)
        plt.show()








mc = MainController()
mc.main()


# def silhouette():
#     # Generating the sample data from make_blobs
#     # This particular setting has one distinct cluster and 3 clusters placed close
#     # together.
#
#     range_n_clusters = [2, 4, 6, 8, 10]
#
#     for n_clusters in range_n_clusters:
#         # Create a subplot with 1 row and 2 columns
#         fig, (ax1, ax2) = plt.subplots(1, 2)
#         fig.set_size_inches(18, 7)
#
#         # The 1st subplot is the silhouette plot
#         # The silhouette coefficient can range from -1, 1 but in this example all
#         # lie within [-0.1, 1]
#         ax1.set_xlim([-0.1, 1])
#         # The (n_clusters+1)*10 is for inserting blank space between silhouette
#         # plots of individual clusters, to demarcate them clearly.
#         ax1.set_ylim([0, len(distance_array) + (n_clusters + 1) * 10])
#
#         # Initialize the clusterer with n_clusters value and a random generator
#         # seed of 10 for reproducibility.
#         clusterer = KMeans(n_clusters=n_clusters, random_state=0)
#         cluster_labels = clusterer.fit_predict(distance_array)
#
#         # The silhouette_score gives the average value for all the samples.
#         # This gives a perspective into the density and separation of the formed
#         # clusters
#         silhouette_avg = silhouette_score(distance_array, cluster_labels)
#         print("For n_clusters =", n_clusters,
#               "The average silhouette_score is :", silhouette_avg)
#
#         # Compute the silhouette scores for each sample
#         sample_silhouette_values = silhouette_samples(distance_array, cluster_labels)
#
#         y_lower = 10
#         for i in range(n_clusters):
#             # Aggregate the silhouette scores for samples belonging to
#             # cluster i, and sort them
#             ith_cluster_silhouette_values = \
#                 sample_silhouette_values[cluster_labels == i]
#
#             ith_cluster_silhouette_values.sort()
#
#             size_cluster_i = ith_cluster_silhouette_values.shape[0]
#             y_upper = y_lower + size_cluster_i
#
#             color = cm.spectral(float(i) / n_clusters)
#             ax1.fill_betweenx(np.arange(y_lower, y_upper),
#                               0, ith_cluster_silhouette_values,
#                               facecolor=color, edgecolor=color, alpha=0.7)
#
#             # Label the silhouette plots with their cluster numbers at the middle
#             ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
#
#             # Compute the new y_lower for next plot
#             y_lower = y_upper + 10  # 10 for the 0 samples
#
#         ax1.set_title("The silhouette plot for the various clusters.")
#         ax1.set_xlabel("The silhouette coefficient values")
#         ax1.set_ylabel("Cluster label")
#
#         # The vertical line for average silhouette score of all the values
#         ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
#
#         ax1.set_yticks([])  # Clear the yaxis labels / ticks
#         ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
#
#         # 2nd Plot showing the actual clusters formed
#         colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
#         ax2.scatter(distance_array[:, 0], distance_array[:, 1], marker='.', s=30, lw=0, alpha=0.7,
#                     c=colors, edgecolor='k')
#
#         # Labeling the clusters
#         centers = clusterer.cluster_centers_
#         # Draw white circles at cluster centers
#         ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
#                     c="white", alpha=1, s=200, edgecolor='k')
#
#         for i, c in enumerate(centers):
#             ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
#                         s=50, edgecolor='k')
#
#         ax2.set_title("The visualization of the clustered data.")
#         ax2.set_xlabel("Feature space for the 1st feature")
#         ax2.set_ylabel("Feature space for the 2nd feature")
#
#         plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
#                       "with n_clusters = %d" % n_clusters),
#                      fontsize=14, fontweight='bold')
#
#         plt.show()











