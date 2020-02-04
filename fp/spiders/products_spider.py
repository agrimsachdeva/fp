import scrapy
import json
from scrapy.http import HtmlResponse

class ProductsSpider(scrapy.Spider):
    name = "products"

    start_urls = ['https://www.fashionphile.com/shop?pageSize=180&sort=date-desc&page=1']

    def parse(self, response):

        # follow links to product pages
        pattern = r'\bvar\s+bootstrappedShopResults\s*=\s*(\{.*?\})\s*;\s*\n'
        json_data = response.xpath('/html/body/div[3]/script[1]/text()').re_first(pattern, replace_entities=False)
        j = json.loads(json_data)

        products = j['products']

        prodHtml = HtmlResponse(url="HTML string", body=products, encoding='utf-8')

        for href in prodHtml.css('.caption > a::attr(href)'):
            yield response.follow(href, self.parse_product)

        # follow pagination links
        for href in response.css('a[rel="next"] ::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_product(self, response):
        
        productid = response.css('meta[itemprop=productID]').get() 
        brand = response.css('meta[itemprop=brand]').get() 
        name = response.css('meta[itemprop=name]').get() 

        price = response.css('.price *::text').getall() 
        price_string = (' ').join(price) 

        details = response.css('#tabDetails *::text').getall() 
        details_string = (' ').join(details) 

        condition = response.css('#tabCondition *::text').getall() 
        condition_string = (' ').join(condition) 

        cart = response.css('i.fa-shopping-bag + sup ::text').get()
        heart = response.css('i.fa-heart-o + sup ::text').get()

        yield {
            'productid': productid,
            'brand': brand,
            'name': name,
            'price': price_string,
            'details': details_string,
            'condition': condition_string,
            'cart': cart,
            'heart': heart
        }