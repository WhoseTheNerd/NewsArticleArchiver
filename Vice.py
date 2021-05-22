class Vice:
    def fix_links(self, page):
        # Fix script links
        for script_src in page.find_all('script', src=True):
            src = script_src['src']
            if not src.startswith('http') or not src.startswith('https'):
                script_src['src'] = "https://www.vice.com" + src
                pass

        # Fix css and other stuff links
        for stylesheet in page.find_all('link', href=True):
            link = stylesheet['href']
            if link.startswith('/'):
                if "www.googletagmanager.com" in link:
                    print("Unexpected link, fixing")
                    stylesheet['href'] = "www.googletagmanager.com"
                stylesheet['href'] = "https://www.vice.com" + link

    def is_url_ok(self, url):
        return url.startswith('http') or url.startswith('https')

    def update(self, main_url, page):

        self.fix_links(page)

        article_components = page.find_all("div", {"class": "article__body-components"})[0]

        ads = article_components.find_all('span', attrs={"class": None})
        for ad in ads:
            # Apparently we can't decompose it, we'll have to hide it
            # Since decompose can't delete recursively, so we are stuck with this
            ad['style'] = "display: none"

        page.find_all('div', {"class": "navbar-wrapper"})[0]['style'] = "display: none"
        page.find_all('span', {"class": "article__socialize"})[0]['style'] = "display:none"
        page.find_all('div', {"class": "article__tagged"})[0]['style'] = "display:none"
        newsletters = page.find_all('div', {"class": "user-newsletter-signup"})
        for newsletter in newsletters:
            newsletter['style'] = "display:none"
            newsletter.decompose()
        page.find_all('div', {"class": "recirc-footer"})[0]['style'] = "display:none"

        footers = page.find_all('footer', {"class": "page-footer"})
        for footer in footers:
            footer['style'] = "display:none"

        page.find('body')['style'] = "background-color: #FFFFFF"

        references = {}
        urls = []
        i = 0
        subpage = page.find_all("main", {"class": "main-content"})[0]
        for a in subpage.find_all("a", href=True):
            url = a['href']
            if self.is_url_ok(url):
                urls.append(url.split('?', maxsplit=1)[0])
                a.string = f"{a.string} [{i}]"
                references[i] = url
                i += 1

        article = page.find_all("span", {"class": ["abc__textblock", "size--article"], "data-component": "TextBlock"})[-1]
        for number, url in references.items():
            tag = page.new_tag("p")
            tag["class"] = "abc__textblock"
            a_tag = page.new_tag("a")
            a_tag['href'] = url
            a_tag["style"] = "color: #000000;"
            a_tag.append(f"[{number}] {url}")
            tag.insert(0, a_tag)
            article.insert_after(tag)
            article = tag

        tag = page.new_tag("p")
        tag.append(main_url)
        page.find('div', id="__next").insert_before(tag)

        images = page.find_all('picture', {"class": "responsive-image"})
        for image in images:
            sources = image.find_all('source', srcset=True)
            link = sources[0]['srcset'].split('?', maxsplit=1)[0]
            for source in sources:
                source.decompose()
            img = image.find('img')
            img['src'] = link
            img['width'] = "100%"
            img['height'] = "100%"
            image['class'] = "responsive-image"

        return page

