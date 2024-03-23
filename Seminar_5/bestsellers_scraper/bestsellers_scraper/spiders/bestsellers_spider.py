import scrapy


class BestsellersSpider(scrapy.Spider):
    name = "bestsellers_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_best-selling_books"]

    def parse(self, response):
        for i in range(1,5):
            books = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[{i}]/tbody/tr')
            for book in books:
                name = book.xpath('.//td[1]//a/text()').get()
                author = book.xpath('.//td[2]//a/text()').get() \
                    if book.xpath('.//td[2]//a/text()').get() else book.xpath('.//td[2]/text()').get()\
                    if book.xpath('.//td[2]/text()').get() else 'N\A'
                orig_language = book.xpath('.//td[3]/text()').get()
                first_published = book.xpath('.//td[4]/text()').get()
                approx_sales = book.xpath('.//td[5]/text()').get()
                genre = book.xpath('.//td[6]//a/text()').get() \
                    if book.xpath('.//td[6]//a/text()').get() else book.xpath('.//td[6]/text()').get()\
                    if book.xpath('.//td[6]/text()').get() and book.xpath('.//td[6]/text()').get() != '\n' else 'N/A'
                if name:
                    yield {
                        'Book_name': name.strip(),
                        'Author': author.strip(),
                        'Original_language': orig_language.strip(),
                        'First_published': first_published.strip(),
                        'Approximate_sales': approx_sales,
                        'Genre': genre.strip()
                    }
