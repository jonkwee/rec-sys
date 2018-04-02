from html_similarity import style_similarity, structural_similarity, similarity
import scipy.spatial.distance as ssd
import numpy as np
import scipy.cluster.hierarchy as hcluster
import matplotlib.pyplot as plt


class HtmlSimilarityProcessor:
    """Responsibility: Create similarity matrix and create clustering"""
    def __init__(self, html_database):
        self.html_database = html_database

    def create_similarity_matrix(self):
        """Create similarity matrix using html similarity where each row is a site's similarity to each other site"""
        similarity_matrix = []
        all_content = self.html_database.select_all_content()
        starting_counter = 0
        length_of_all_content = all_content.size
        for i in range(starting_counter, length_of_all_content):
            inner_array = []
            for i2 in range(length_of_all_content):
                if i2 == starting_counter:
                    inner_array = np.append(inner_array, [0])
                elif i2 < starting_counter:
                    inner_array = np.append(inner_array, similarity_matrix[:,starting_counter][i2])
                else:
                    similarity_score = similarity(all_content[starting_counter].decode('utf-8'),
                                                  all_content[i2].decode('utf-8'))
                    inner_array = np.append(inner_array, similarity_score)
            if i == 0:
                similarity_matrix = np.array([inner_array])
            else:
                similarity_matrix = np.vstack((similarity_matrix, inner_array))
            starting_counter += 1
        return np.array(similarity_matrix)

    def hierarchy_clustering(self):
        similarity_matrix = self.create_similarity_matrix()
        distVec = ssd.squareform(similarity_matrix)
        linkage = hcluster.linkage(1 - distVec)
        dendro = hcluster.dendrogram(linkage)
        plt.show()