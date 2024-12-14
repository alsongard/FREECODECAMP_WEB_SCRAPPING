import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] # domain for which we will scrape
    start_urls = ["https://books.toscrape.com"]
    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            yield{
                "name": book.css('h3 a::text').get(),
                "price": book.css('p.price_color').get(),
                "url": book.css('h3 a').attrib["href"]
            }