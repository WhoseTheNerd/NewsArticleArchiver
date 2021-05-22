class EFF:
    def is_url_ok(self, url):
        return url.startswith('http') or url.startswith('https')

    def update(self, main_url, page):
        page.find(id="header").decompose()

        # Wow, so much effort to remove signup forms on the side, lol
        for x in page.find(id='main-content').find_all('div', {"class": "main-column"}):
            elements = x.find_all('div', {"class": ["panel-pane", "pane-page-content"]})
            if len(elements) > 0:
                for element in elements:
                    subelements = element.find_all('div', {"class": ["onecol", "column", "content-wrapper"]})
                    if len(subelements) > 0:
                        for subelement in subelements:
                            subsubelements = subelement.find_all('div', {"class": ["column", "side-content"]})
                            if len(subsubelements) > 0:
                                for subsubelement in subsubelements:
                                    thrice_nested_elements = subsubelement.find_all('div', {"class": ["panel-pane", "pane-sidebar-content"]})
                                    if len(thrice_nested_elements) > 0:
                                        for thrice_nested_element in thrice_nested_elements:
                                            signup_forms = thrice_nested_element.find_all('div', {"class": "pane-effector-signup"})
                                            share_blog_forms = thrice_nested_element.find_all('div', {"class": ["pane-eff-share-blog", "desktop"]})
                                            field_issue_forms = thrice_nested_element.find_all('div', {"class": "pane-node-field-issue"})
                                            if len(signup_forms) > 0 and len(share_blog_forms) > 0 and len(field_issue_forms) > 0:
                                                signup_forms[0].decompose()
                                                share_blog_forms[0].decompose()
                                                field_issue_forms[0].decompose()

        for img in page.find_all('img', src=True):
            link = img['src']
            if not link.startswith('https') and not link.startswith('http') and not link.startswith('#'):
                img['src'] = "https://www.eff.org" + link

        h2_elements = page.find_all('h2', {"class": "pane-title"})
        for h2_element in h2_elements:
            if h2_element.get_text() == "Related Updates":
                h2_element.parent.decompose()
            else:
                h2_element.decompose()

        forms = page.find_all('form', {"class": "newsletter-form", "accept-charset": "UTF-8", "action": "https://supporters.eff.org/subscribe", "method": "post"})
        forms[0].parent.decompose()

        try:
            craps = page.find_all('a', {"href": "/issues/competition"})
            craps[0].parent.parent.parent.decompose()
        except:
            pass

        craps = page.find_all('div', {"class": "share-links"})
        for crap in craps:
            crap.decompose()

        page.find(id="footer").decompose()
        page.find(id="footer-bottom").decompose()

        references = {}
        urls = []
        i = 0
        subpage = page.find_all("article", {"class": ["node", "node--blog", "node--promoted", "node--full", "node--blog--full"], "role": "article"})[0]
        for a in subpage.find_all("a", href=True):
            url = a['href']
            a.string = f"{a.string} [{i}]"
            references[i] = url
            i += 1
            if self.is_url_ok(url):
                urls.append(url.split('?', maxsplit=1)[0])

        #article = subpage.find_all("div", {"class": ["article-content", "post-page"]})[0]
        article = subpage
        for number, url in references.items():
            tag = page.new_tag("p")
            tag["style"] = "padding: 0;margin: 0"
            a_tag = page.new_tag("a")
            a_tag['href'] = url
            a_tag["style"] = "color: #000000;"
            a_tag.append(f"[{number}] {url}")
            tag.insert(0, a_tag)
            article.insert_after(tag)
            article = tag

        tag = page.new_tag("p")
        tag.append(main_url)
        tag['style'] = "padding-top: 15px; padding-bottom: 0px; margin: 0px"
        page.find(id="site_banner").insert_after(tag)

        return page