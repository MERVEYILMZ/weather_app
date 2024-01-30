# pipelines.py
import pymongo
from scrapy.exceptions import DropItem
from InfoTechWeatherApp import settings

class MongoPipeline(object):

    collection_name = 'city_data'

    def __init__(self):
        connection = pymongo.MongoClient(
            settings.MONGODB_URI
        )
        self.db = connection[settings.MONGODB_DATABASE]
        self.collection = self.db[self.collection_name]
        
        self.collection.delete_many({})
        # 'country' and 'population' sorting
        self.collection.create_index([('country', pymongo.ASCENDING), ('population', pymongo.DESCENDING)])

    def process_item(self, item, spider):
        # Check for missing values
        if not all(item.values()):
            raise DropItem("Missing values from {}".format(item))
        
        # Convert population to integer for proper sorting
        try:
            item['population'] = int(item['population'].replace(',', ''))
        except ValueError:
            raise DropItem(f"Invalid population value for {item}")

        # Insert item into MongoDB
        self.collection.insert_one(dict(item))
        return item
