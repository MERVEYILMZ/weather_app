# settings.py
BOT_NAME = 'InfoTechWeatherApp'

SPIDER_MODULES = ['InfoTechWeatherApp.spiders']
NEWSPIDER_MODULE = 'InfoTechWeatherApp.spiders'

# MongoDB settings
MONGODB_URI = 'mongodb+srv://seanalone:Carry417641@cluster0.dvcnxfp.mongodb.net/'
MONGODB_DATABASE = 'weather_database'

ITEM_PIPELINES = {
    'InfoTechWeatherApp.pipelines.MongoPipeline': 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
