"""
    @description:   
    @author:        RoyalClown
    @date:          2017/5/15
"""
import re

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


def belling(url):
    html_analyse = HtmlAnalyse(url)
    bs_content = html_analyse.get_bs_contents()

    pdf_tags = bs_content.find_all(name="a", attrs={"href": re.compile(r".*?\.pdf$")})
    hrefs = []
    for pdf_tag in pdf_tags:
        href = pdf_tag.get("href")
        print(href)
        hrefs.append(href)
    return hrefs


def file_write(hrefs):
    with open("../ComponentDepartment/pdf_urls.txt", "w") as f:
        for href in hrefs:
            f.writelines(href + "\n")


if __name__ == "__main__":
    urls = ["http://www.belling.com.cn/article.htm1?id=4591", "http://www.belling.com.cn/article.htm1?id=4590",
            "http://www.belling.com.cn/article.htm1?id=4590", "http://www.belling.com.cn/article.htm1?id=4588",
            "http://www.belling.com.cn/article.htm1?id=4589", "http://www.belling.com.cn/article.htm1?id=4587",
            "http://www.belling.com.cn/article.htm1?id=4584", "http://www.belling.com.cn/article.htm1?id=4586",
            "http://www.belling.com.cn/article.htm1?id=4740", "http://www.belling.com.cn/article.htm1?id=4582",
            "http://www.belling.com.cn/article.htm1?id=4581", "http://www.belling.com.cn/article.htm1?id=4579",
            "http://www.belling.com.cn/article.htm1?id=4657", "http://www.belling.com.cn/article.htm1?id=4597",
            "http://www.belling.com.cn/article.htm1?id=4596", "http://www.belling.com.cn/article.htm1?id=4595",
            "http://www.belling.com.cn/article.htm1?id=4593", "http://www.belling.com.cn/article.htm1?id=4592",
            "http://www.belling.com.cn/article.htm1?id=4594", "http://www.belling.com.cn/article.htm1?id=4658",
            "http://www.belling.com.cn/article.htm1?id=4675", "http://www.belling.com.cn/article.htm1?id=4676",
            "http://www.belling.com.cn/article.htm1?id=4677", "http://www.belling.com.cn/article.htm1?id=4678",
            "http://www.belling.com.cn/article.htm1?id=4739", "http://www.belling.com.cn/article.htm1?id=4679",
            "http://www.belling.com.cn/article.htm1?id=4673", "http://www.belling.com.cn/article.htm1?id=4674",
            "http://www.belling.com.cn/article.htm1?id=4694", "http://www.belling.com.cn/article.htm1?id=4684",
            "http://www.belling.com.cn/article.htm1?id=4685", "http://www.belling.com.cn/article.htm1?id=4686",
            "http://www.belling.com.cn/article.htm1?id=4687", "http://www.belling.com.cn/article.htm1?id=4688",
            "http://www.belling.com.cn/article.htm1?id=4689", "http://www.belling.com.cn/article.htm1?id=4690",
            "http://www.belling.com.cn/article.htm1?id=4693", "http://www.belling.com.cn/article.htm1?id=4534",
            "http://www.belling.com.cn/article.htm1?id=4681", "http://www.belling.com.cn/article.htm1?id=4682",
            "http://www.belling.com.cn/article.htm1?id=4683", "http://www.belling.com.cn/article.htm1?id=4005",
            "http://www.belling.com.cn/article.htm1?id=4003", "http://www.belling.com.cn/article.htm1?id=4008",
            "http://www.belling.com.cn/article.htm1?id=4009"]

    for url in urls:
        hrefs = belling(url)
        print("\n")

