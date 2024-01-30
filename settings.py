
from config import MONGODB_URI, MONGODB_DATABASE, OPENWEATHER_KEY
BOT_NAME = 'InfoTechWeatherApp'

SPIDER_MODULES = ['InfoTechWeatherApp.spiders']
NEWSPIDER_MODULE = 'InfoTechWeatherApp.spiders'

# MongoDB settings
MONGODB_URI = MONGODB_URI
MONGODB_DATABASE = MONGODB_DATABASE

ITEM_PIPELINES = {
    'InfoTechWeatherApp.pipelines.MongoPipeline': 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

OPENWEATHER_KEY = OPENWEATHER_KEY
