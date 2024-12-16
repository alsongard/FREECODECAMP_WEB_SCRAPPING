# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy.item


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

def serializer_price(value):
    return f"£ {str(value)}"


#  price_excl_tax = scrapy.Field(serializer=serialize_price)
#  define a new class for book


def serialize_price(value):
    return f'£ {str(value)}'


class BookItem(scrapy.Item):
   url = scrapy.Field()
   title = scrapy.Field()
   upc = scrapy.Field()
   product_type = scrapy.Field()
   price_excl_tax = scrapy.Field()
   price_incl_tax = scrapy.Field()
   tax = scrapy.Field()
   availability = scrapy.Field()
   num_reviews = scrapy.Field()
   stars = scrapy.Field()
   category = scrapy.Field()
   description = scrapy.Field()
   price = scrapy.Field()


# class BookItem(scrapy.Item):
#     url = scrapy.Field()
#     title = scrapy.Field()
#     category = scrapy.Field()
#     price_excl_tax = scrapy.Field()
#     price_incl_tax = scrapy.Field()
#     tax = scrapy.Field()
#     price = scrapy.Field()
#     availability = scrapy.Field()
#     number_reviews = scrapy.Field()
#     stars = scrapy.Field()
#     description = scrapy.Field()




#    upc = scrapy.Field()