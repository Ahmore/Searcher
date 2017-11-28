from scrapy.exceptions import DropItem
from engine.index import Index


class WikiPipeline(object):
    documents = {}

    def process_item(self, item, spider):
        if item["url"] in self.documents:
            raise DropItem("Duplicate item found: %s" % item["url"])
        else:
            self.documents[item["url"]] = item

    def close_spider(self, spider):
        print("------------------------------------------")
        print("I have %d items" % self.documents.__len__())
        print("------------------------------------------")

        index = Index(self.documents)
        index.init_dictionary()
        index.create_index()
        index.parse_matrix_with_idf()
        index.save_to_json()

        print("------------------------------------------")
        print("I have %d items in dict" % index.dictionary.__len__())
        print("------------------------------------------")

