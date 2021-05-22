class ArsTechnica:
    def is_url_ok(self, url):
        if "www.twitter.com" in url:
            return False
        if "arstechnica.com/author" in url:
            return False
        return url.startswith('http') or url.startswith('https')

    def update(self, main_url, page):
        page.find(id="header-nav-primary").decompose()
        page.find(id="article-footer-wrap").decompose()
        page.find(id="social-footer").decompose()
        elements = page.find_all("footer", {"class": "site-footer"})
        for element in elements:
            element.decompose()

        elements = page.find_all("div", {"class": "header-right"})
        for element in elements:
            element.decompose()

        logo = page.find(id="header-logo")
        logo['href'] = ""

        page.find(id="social-left").decompose()

        references = {}
        urls = []
        i = 0
        subpage = page.find_all("section", {"class":"article-guts"})[0]
        for a in subpage.find_all("a", href=True):
            url = a['href']
            a.string = f"{a.string} [{i}]"
            references[i] = url
            i += 1
            if self.is_url_ok(url):
                urls.append(url.split('?', maxsplit=1)[0])

        article = subpage.find_all("div", {"class": ["article-content", "post-page"]})[0]
        for number,url in references.items():
            tag = page.new_tag("p")
            tag["class"] = "column-wrapper"
            a_tag = page.new_tag("a")
            a_tag['href'] = url
            a_tag["style"] = "color: #000000;"
            a_tag.append(f"[{number}] {url}")
            tag.insert(0, a_tag)
            article.insert_after(tag)
            article = tag

        tag = page.new_tag("p")
        tag.append(main_url)
        page.find_all("header", {"class": "site-header"})[0].insert_before(tag)
        page.find("body")['style'] = "background-color: #F0F1F2"

        return page

