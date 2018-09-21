# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

from elasticsearch import Elasticsearch
from .settings import ES_HOST, ES_PORT

class MyImagesPipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        self.es_host = ES_HOST
        self.es_port = ES_PORT

        super(MyImagesPipeline, self).__init__(
            store_uri,
            download_func,
            settings,
        )


    def open_spider(self, spider):
        self.es_client = Elasticsearch(
            hosts=[{
                "host": self.es_host,
                "port": self.es_port,
            }]
        )
        if not self.es_client.indices.exists(index="products_list_spider"):
            self.es_client.indices.create(index="products_list_spider")
        super(MyImagesPipeline, self).open_spider(spider)

    def close_spider(self, spider):
        del self.es_client

    def get_media_requests(self, item, info):
        # for image_url in item['image']:
        image_url = item['image_url']
        if image_url:
            yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        if item["image_url"]:
            image_path = results[0][1]["path"]
            if not image_path:
                raise DropItem("Item contains no images")
            self.es_client.index(
                index="products_list_spider",
                doc_type=item["keywords"],
                body={
                    "name": item["name"],
                    "image_url": item["image_url"],
                    "price": item["price"],
                    "status": item["status"],
                    "path": image_path
                }
            )
        return item
