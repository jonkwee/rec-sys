from html_similarity import style_similarity, structural_similarity, similarity
import dataprocess.PageContentProcessor as PCP

# pcp.change_url("https://github.com/TeamHG-Memex/page-compare")
# content1 = pcp.extract_content()
# html2 = pcp.get_soup_content()
#
# print("style similarity:", style_similarity(html1, html2))
# print("structural similarity:", structural_similarity(html1, html2))
# print("total similarity:", similarity(html1, html2))

def byte_content():
    pcp = PCP.PageContentProcessor()
    pcp.change_url("https://docs.python.org/2/library/os.path.html")
    pcp.change_soup()
    return pcp.get_soup_content()



# htmlDB = HtmlDatabase()
# conn = htmlDB.connect_to_db()
# htmlDB.open_db()
# cont = controller.test.byte_content()
# htmlDB.insert_content(cont)
# l_c = htmlDB.select_all_content()
