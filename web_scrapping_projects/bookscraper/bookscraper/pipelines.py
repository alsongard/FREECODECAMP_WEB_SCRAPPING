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
    

import mysql.connector

class SavetoMySQLPipeLine:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="alson",
            password="black_hole",
            database="books"
        )

        # creating cursor object
        self.cursor = self.database.cursor()

        sql = """
            CREATE TABLE IF NOT EXIST books(
                id INT NOT NULL auto_increment PRIMARY KEY,
                url VARCHAR(255),
                title text,
                upc VARCHAR(255),
                product_type VARCHAR(255),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                price DECIMAL,
                availability INTEGER,
                num_reviews INTEGER,
                stars INTEGER,
                category VARCHAR(255),
                description text,
            )ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
            """
        self.cursor.execute(sql)

    def process_item(self, item, spider):

        # insert data statements
        self.cursor.execute("""
            INSERT INTO books(
                url,
                title,
                upc,
                product_type ,
                price_excl_tax,
                price_incl_tax,
                tax,
                price ,
                availability,
                num_reviews,
                stars,
                category,
                description,
                )
            values(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s                                            
            )
        """, (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"][0])
        )
        )
        self.database.commit()
        return item
    

    def close_spider(self,spider):
        # close cursor & connection
        self.cursor.close()
        self.database.close()