import re
import json

from html import unescape
from math import ceil
from bs4 import BeautifulSoup as bs
from proxy_client import *
from utils.utils import *
from utils.structures import *


class Parser:
    BASE_URL = "https://www.deichmann.com/de-de"

    def __init__(self, proxy_client: ProxyClient, per_page: int) -> None:
        self.proxy_client = proxy_client
        self.per_page = per_page

    @debug("get_brands", True)
    def get_brands(self) -> list[str]:
        if html := bs(self.proxy_client.retry("GET", f"{self.BASE_URL}/damen-marken").text, "html.parser"):
            return list(
                re.search(r"/c-(.*)", i.get("href")).group(1)
                for i in html.select(Selectors.BRAND_LINK.value)
            )
        
    @debug("get_n_products", True)
    def get_n_products(self, brand: str) -> int:
        return self.proxy_client.retry(
            "GET",
            f"{self.BASE_URL}/rest/v2/deichmann-de/products/search?query=:relevance:allCategoriesSEO:{brand}:distributionChannel:ONLINESHOP:inStockFlag:true:orCategoriesSEO:ws:&currentPage=1&pageSize=100&fields=FULL"
        ).json().get("pagination").get("totalResults")
    
    @debug("get_products", True)
    def get_products(self, brand: str, page: int) -> list[dict[str, any]]:
        return self.proxy_client.retry(
            "GET",
            f"{self.BASE_URL}/rest/v2/deichmann-de/products/search?query=:relevance:allCategoriesSEO:{brand}:distributionChannel:ONLINESHOP:inStockFlag:true:orCategoriesSEO:ws:&currentPage={page}&pageSize=100&fields=FULL"
        ).json().get("products")
    
    @debug("")
    def get_product_data(self, product: dict[str, any]) -> list[ProductData]:
        v = []
        price = float(product.get("allPrices")[0].get("value"))

        if 15 <= price <= 300:
            url = self.BASE_URL + product.get("url")
            combined_sku = url.split("/")[-1]

            if html := bs(
                self.proxy_client.retry("GET", url).text, 
                "html.parser"
            ):
                spu = product.get("baseProduct")
                name = product.get("name")
                brand = product.get("brandName")
                
                if description := product.get("description", ""):
                    description = remove_tags(unescape(description.strip().replace("\n", "")))
                
                materials = {}
                if materials_data := html.select_one(Selectors.MATERIAL.value):
                    materials_data = materials_data.find("dl", {"class": "stats"})
                    materials = dict((MATERIALS.get(k.text.strip().replace(":", "")), v.text.strip()) for k, v in zip(materials_data.find_all("dt"), materials_data.find_all("dd")))

                color_origin = unescape(html.select_one(Selectors.COLOR.value).text).strip()
                color = COLORS.get(color_origin.title(), "не определено")
                category = product.get("topLevelCategory").get("code")

                images = []
                if (main_image := product.get("images")[0].get("url")).endswith("P.jpg"): 
                    images.append(main_image)
                    ni = 0
                else: ni = 1

                image_url_template = re.sub(r"\d*\.jpg", "", main_image)
                for i in range(1, len(html.select(Selectors.PRODUCT_IMAGE.value + ">div>img")) + ni):
                    images.append(image_url_template + f"{i}.jpg")

                for n, i in enumerate(html.select(Selectors.SIZE_LIST.value + ">li[aria-disabled='false']")):
                    size_data = i.select_one("span").text.strip().split("  ")
                    if StockData.LAST_ITEM.value in size_data: in_stock = 1
                    elif StockData.OUT_OF_STOCK.value in size_data: in_stock = 0
                    else: in_stock = 2

                    if in_stock > 0:
                        size_name = format_size(size_data[0])
                        v.append(
                            ProductData(
                                url,
                                combined_sku + str(n),
                                spu,
                                name,
                                brand,
                                category,
                                price,
                                in_stock,
                                color,
                                color_origin,
                                size_name,
                                images,
                                description,
                                materials
                            )
                        )

        return v

    def get_n_pages(self, total: int) -> int:
        return ceil(total / self.per_page)
