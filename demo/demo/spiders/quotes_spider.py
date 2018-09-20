import scrapy
import json

from ..items import WorkImageItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['ggac.net']
    host = "http://www.ggac.net/"
    api_work_list = "api/work"
    api_work_attachment = "api/work/attachment"
    view_work_detail = "work/detail/{work_id}"

    def start_requests(self):
        work_detail = self.host + self.api_work_list
        yield scrapy.FormRequest(
            method="POST",
            url=work_detail,
            formdata={
                "promote_conditions": "1",
                "work_conditions":"all",
                "right_condition": "publish",
                "current_page": "1",
                "page_size": "40",
                "csrfmiddlewaretoken": "FX4PvchJ7XYWSH9BwcLg7MPgdw25shwEYngFKN42B4TP3gAwRGpqELVYNYyHCaZB",
            },
            cookies={
                "csrftoken": "FX4PvchJ7XYWSH9BwcLg7MPgdw25shwEYngFKN42B4TP3gAwRGpqELVYNYyHCaZB"
            },
            callback=self.parse_work)

    def parse_work(self, response):
        response_work_list = json.loads(response.body)
        work_data = response_work_list.get("data", {})
        work_list = work_data.get("works", [])
        for work in work_list:
            yield scrapy.FormRequest(
                method="POST",
                url=self.host + self.api_work_attachment,
                formdata={
                    "wid": str(work["id"]),
                    "csrfmiddlewaretoken": "FX4PvchJ7XYWSH9BwcLg7MPgdw25shwEYngFKN42B4TP3gAwRGpqELVYNYyHCaZB",
                },
                cookies={
                    "csrftoken": "FX4PvchJ7XYWSH9BwcLg7MPgdw25shwEYngFKN42B4TP3gAwRGpqELVYNYyHCaZB"
                },
                callback=self.parse_work_attachment,
                meta={"work_id": work["id"]}
            )

    def parse_work_attachment(self, response):
        work_id = response.request.meta["work_id"]
        response_work_list = json.loads(response.body)
        work_data = response_work_list.get("data", {})
        work_image_list = work_data.get("work_images", [])
        image_urls = [image["url"] for image in work_image_list]
        item = WorkImageItem()
        item["title"] = work_id
        item["image_urls"] = image_urls
        return item
