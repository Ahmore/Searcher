import time
from scrapy.exceptions import DropItem
from engine.jsonstorage import JSONStorage


class WikiPipeline(object):
    documents = {}

    def __init__(self):
        self.start_time = 0

    def process_item(self, item, spider):
        if item["url"] in self.documents:
            raise DropItem("Duplicate item found: %s" % item["url"])
        else:
            self.documents[item["url"]] = item

    def open_spider(self, spider):
        print("[Web crawling]")
        self.start_time = time.time()

    def close_spider(self, spider):
        print("--- %s seconds ---" % (time.time() - self.start_time))

        print("")

        print("[Saving to file]")
        st = time.time()
        storage = JSONStorage("documents/wikidocuments%d.json" % self.start_time)
        storage.save({
            "documents": self.documents
        })
        print("--- %s seconds ---" % (time.time() - st))

        print("")

        print("[Done]")
        print("--- %s seconds ---" % (time.time() - self.start_time))
