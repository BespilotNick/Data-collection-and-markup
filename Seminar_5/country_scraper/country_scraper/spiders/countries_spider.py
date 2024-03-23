import scrapy


# class CountriesSpiderSpider(scrapy.Spider):
#     name = "countries_spider"
#     allowed_domains = ["en.wikipedia.org"]
#     start_urls = ["https://en.wikipedia.org/wiki/List_of_sovereign_states"]

#     def parse(self, response):
#         for country in response.css('table.wikitable.sortable tbody tr'):
#             name = country.css('td:nth-child(1) b a::text').get()
#             if name:
#                 yield {'Country': name}


class CountriesSpiderSpider(scrapy.Spider):
    name = "countries_spider"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_sovereign_states"]

    def parse(self, response):
        for country in response.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr'):
            name = country.xpath('.//td[1]//a/text()').get()
            membership = country.xpath('.//td[2][1]/text()').get()
            sovereignity_dispute = country.xpath('.//td[3][1]/text()').get()
            status = country.xpath('.//td[4]/text()').get()
            link = country.xpath('.//b/a/@href').get()
            if name:
                # yield {

                #     'Country': name.strip() if name else 'N/A',
                #     'Membership_UN': membership.strip() if membership.strip() else 'N/A',
                #     'Sovereignity_dispute': sovereignity_dispute.strip() if sovereignity_dispute.strip() else 'N/A',
                #     'Country_status_info': status.strip() if status.strip() else 'N/A'
                # }
                yield response.follow(url = link if link else '/wiki/Zambia', 
                                    callback = self.parse_country, 
                                    meta = {                                 
                                        'Country': name,
                                        'Membership_UN': membership,
                                        'Sovereignity_dispute': sovereignity_dispute,
                                        'Country_status_info': status
                                    })
    

    def parse_country(self, response):
        rows = response.xpath('//table[contains(@class,"infobox ib-country vcard")][1]/tbody')
        for row in rows:
            capital = row.xpath('.//td[contains(@class, "infobox-data")]/a/text()').get()
            name = response.request.meta['Country']
            Membership_UN = response.meta['Membership_UN']
            Sovereignity_dispute = response.meta['Sovereignity_dispute']
            Country_status_info = response.meta['Country_status_info']
            yield {
                'Country': name,
                'Capital': capital,
                'Membership_UN': Membership_UN.strip(),
                'Sovereignity_dispute': Sovereignity_dispute.strip(),
                'Country_status_info': Country_status_info.strip()
            }
