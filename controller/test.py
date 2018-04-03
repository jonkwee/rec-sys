from html_similarity import style_similarity, structural_similarity, similarity
import dataprocess.PageContentProcessor as PCP
import scipy.cluster.hierarchy as hcluster
import matplotlib.pyplot as plt
import scipy.spatial.distance as ssd
import numpy as np
import database.HtmlDatabase as HtmlDatabase
import dataprocess.HtmlSimilarityProcessor as HtmlSimilarityProcessor
# pcp.change_url("https://github.com/TeamHG-Memex/page-compare")
# content1 = pcp.extract_content()
# html2 = pcp.get_soup_content()
#
# print("style similarity:", style_similarity(html1, html2))
# print("structural similarity:", structural_similarity(html1, html2))
# print("total similarity:", similarity(html1, html2))

def byte_content(url):
    pcp = PCP.PageContentProcessor()
    pcp.change_url(url)
    pcp.change_soup()
    return pcp.get_soup_content()

list_of_urls = [
    "http://treyhunner.com/2016/04/how-to-loop-with-indexes-in-python/",
    "https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.nditer.html",
    "https://stackoverflow.com/questions/29022451/dendrogram-through-scipy-given-a-similarity-matrix?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa",
    "https://stackoverflow.com/questions/9775297/append-a-numpy-array-to-a-numpy-array",
    "http://www.numericalexpert.com/blog/sqlite_blob_time/",
    "https://docs.python.org/2/library/os.path.html",
    "https://github.com/matiskay/html-similarity",
    "https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html"
]

htmlDB = HtmlDatabase.HtmlDatabase()
htmlsim = HtmlSimilarityProcessor.HtmlSimilarityProcessor(htmlDB)
htmlsim.hierarchy_clustering()

# insert into database (test)
# conn = htmlDB.connect_to_db()
# htmlDB.open_db()
# for i in list_of_urls:
#     cont = byte_content(i)
#     htmlDB.insert_content(cont)

