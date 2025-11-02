import scrapy

from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        for quote in response.css('div.card-body'):
            text = ' '.join(
                t.strip() for t in quote.css('p.card-text::text').getall()
            ).strip()
            data = {
                'author': quote.css('strong::text').get(),
                'text': text,
                'date': quote.css('small.text-muted::text').get(),
            }
            yield YatubeParsingItem(data)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
