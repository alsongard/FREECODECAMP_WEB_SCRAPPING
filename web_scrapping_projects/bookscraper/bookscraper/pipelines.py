# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



#  used for data processing
class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        ## show price in float
        price_keys = ["price_excl_tax", 'price_incl_tax', 'tax', 'price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)


        ## availability -> show number
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter["availability"] = int(availability_array[0])
            

        # convert reviews into interger
        reviews_string = adapter.get("num_reviews")
        adapter['num_reviews'] = int(reviews_string)


        # converst starts text into number
        star_text = adapter.get("stars")
        star_string_array =star_text.split(" ") 
        star_string_value = star_string_array[1].lower()
        if star_string_value == "zero":
            adapter["stars"] = 0
        elif star_string_value == "one":
            adapter["stars"] = 1
        elif  star_string_value == "two":
            adapter["stars"] = 2
        elif  star_string_value == "three":
            adapter["stars"] = 3
        elif  star_string_value == "four":
            adapter["stars"] = 4
        elif star_string_value == "five":
            adapter["stars"] = 5



        return item