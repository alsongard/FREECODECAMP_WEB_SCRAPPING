import scrapy
from bookscraper.items import BookItem
import random


"""
user_agent_list = [
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
   'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
   'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]
"""

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"] # domain for which we will scrape
    start_urls = ["https://books.toscrape.com"]



    def parse(self, response):
        books = response.css('article.product_pod')    

        for book in books:

            relative_url = book.css('h3 a::attr(href)').get()

            if "catalogue/" in relative_url:
                next_page_data = "https://books.toscrape.com"  + relative_url
            else:
                next_page_data = "https://books.toscrape.com/catalogue/" + relative_url
            # yield response.follow(next_page_data, callback=self.parse_book_page,headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]})
            yield response.follow(next_page_data, callback=self.parse_book_page) 
        
        #  the link for the next page
            next_page = response.css('li.next a::attr(href)').get()
        
            # for the last page
            if next_page is not None:
                if "catalogue/" in next_page:
                    next_page_url = "https://books.toscrape.com/" + next_page
                else:
                    next_page_url =  "https://books.toscrape.com/catalogue/" + next_page
                # yield response.follow(next_page_url, callback= self.parse,headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]})
                yield response.follow(next_page_url, callback= self.parse)
        

    def parse_book_page(self, response):
        table_rows = response.css('table tr')

        book_item = BookItem()
        

        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css("td ::text").get()
        book_item['product_type' ] = table_rows[1].css("td ::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_item['tax'] = table_rows[4].css("td ::text").get(),
        book_item['availability'] = table_rows[5].css("td ::text").get(),
        book_item['num_reviews']=  table_rows[6].css("td ::text").get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),
        
        yield book_item
        # {
        # book_item["url" ]: response.url,
        # book_item["title"]: response.css('div.product_main h1 ::text').get(),
        # book_item["category"]: response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        # book_item["price_excl_tax"]: table_rows[2].css('td ::text').get(),
        # book_item["price_incl_tax"] : table_rows[3].css('td ::text').get(),
        # book_item["tax"]: table_rows[4].css('td ::text').get(),
        # book_item["price"]:  response.css('p.price_color ::text').get(),
        # book_item["availability"] : table_rows[5].css('td ::text').get(),
        # book_item["number_reviews"] : table_rows[6].css('td ::text').get(),
        # book_item["stars"] : response.css('p.star-rating').attrib["class"],
        # book_item['description']: response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        # }
        

        # get name of book
        # response.css('li.active
        # response.css('div.product_main h1')

        # get type of book
        # response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()


        # get description of the book
        # response.xpath("//article[@class='product_page']/div[@class='sub-header']/preceding-sibling::p[1]").get()
        #  response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()

        # getting stars
        #  response.css('p.star-rating').attrib['class']


        # for book in books:
        #     yield{
        #         "name": book.css('h3 a::text').get(),
        #         "price": book.css('p.price_color').get(),
        #         "url": book.css('h3 a').attrib["href"]
        #     }

        # next_page = response.css('li.next a::attr(href)').get()

        # # for the last page
        # if next_page is not None:
        #     if "catalogue/" in next_page:
        #         next_page_url = "https://books.toscrape.com/" + next_page
        #         yield response.follow(next_page_url, callback= self.parse)
        #     else:
        #         next_page_url =  "https://books.toscrape.com/catalogue/" + next_page
        #         yield response.follow(next_page_url, callback= self.parse)
                