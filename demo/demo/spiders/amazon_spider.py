import scrapy

from ..items import ProductionItem

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ['amazon.cn']
    host = "http://www.amazon.cn"
    view_search_items = "/s/field-keywords={search_name}"
    view_search_items_page = "/s/field-keywords={search_name}&page={page_index}"

    def start_requests(self):
        search_items = [
            "nike",
            "apple",
        ]
        for item in search_items:
            item_search_url = self.host + self.view_search_items.format(search_name=item)
            yield scrapy.Request(
                url=item_search_url,
                callback=self.parse_item_page,
                meta={
                    "search_name": item
                }
            )

    def parse_item_page(self, response):
        search_name = response.request.meta["search_name"]
        page_min = int(response.css(
            "div#centerBelowMinus "
            "div#bottomBar "
            "div#pagn "
            "span.pagnCur::text").extract_first())
        page_max = int(response.css(
            "div#centerBelowMinus "
            "div#bottomBar "
            "div#pagn "
            "span.pagnDisabled::text").extract_first())
        for page_index in range(page_min, page_max + 1):
            item_search_page_url = self.host + \
                                   self.view_search_items_page.format(
                                       search_name=search_name,
                                       page_index=str(page_index)
                                   )
            yield scrapy.Request(
                url=item_search_page_url,
                callback=self.parse_item_list,
                meta={
                    "search_name": search_name
                }
            )

    def parse_item_list(self, response):
        search_name = response.request.meta["search_name"]
        items_url_list = response.css(
            "div#atfResults "
            "ul#s-results-list-atf "
            "li.s-result-item "
            "a.a-link-normal::attr(href)"
        ).extract()
        for url in items_url_list:
            # self.log("item {url}".format(url=url))
            if not url.startswith("/s?"):
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_item_detail,
                    meta={
                        "search_name": search_name
                    }
                )

    def parse_item_detail(self, response):
        search_name = response.request.meta["search_name"]
        product_title = response.css("span#productTitle::text").extract_first()
        product_price = response.css("span#priceblock_ourprice::text").extract_first()
        product_availability = response.css("div#availability span::text").extract_first()
        product_image = response.css("div#main-image-container "
                                     "li.item span.a-list-item "
                                     "span.a-declarative "
                                     "div#imgTagWrapperId "
                                     "img::attr(data-old-hires)").extract_first()
        production = ProductionItem()
        production["keywords"] = search_name
        production["name"] = product_title.strip() if product_title else "no name"
        production["image_url"] = product_image
        production["price"] = product_price
        production["status"] = product_availability.strip() if product_availability else "no status"
        return production
        # self.log("name {name}; price {price}; status {status}; image {image}".format(
        #     name=product_title.strip() if product_title else "no name",
        #     price=product_price,
        #     status=product_availability.strip() if product_availability else "no status",
        #     image=product_image
        # ))
