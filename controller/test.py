from html_similarity import style_similarity, structural_similarity, similarity
import PageContentProcessor as PCP


pcp = PCP.PageContentProcessor()
pcp.change_url("https://github.com/matiskay/html-similarity")
content = pcp.extract_content()
html1 = pcp.get_soup_content()
print(pcp.get_list_of_words())

# pcp.change_url("https://github.com/TeamHG-Memex/page-compare")
# content1 = pcp.extract_content()
# html2 = pcp.get_soup_content()
#
# print("style similarity:", style_similarity(html1, html2))
# print("structural similarity:", structural_similarity(html1, html2))
# print("total similarity:", similarity(html1, html2))