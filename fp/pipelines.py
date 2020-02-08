# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.mail import MailSender
import time
import datetime
import pprint

class FpPipeline(object):
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):

        subject = 'Fashionphile Scraper:' + datetime.date.today().strftime("%m/%d/%y")
        intro = "Summary stats from Scrapy spider and total products scraped: \n\n"
        body = spider.crawler.stats.get_stats()
        body = pprint.pformat(body)
        body = intro + body

        mailer = MailSender()
        mailer.send(to=["agsach@iu.edu, jjzhang@indiana.edu"], subject="Fashionphile Scrapy Stats", body="Some body")