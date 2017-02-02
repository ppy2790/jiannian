#coding=utf-8

from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from jiannian.items import  ArticleItem




import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class JiannianSpider(CrawlSpider):

    name = 'jiannian'

    start_urls=[
        'http://www.jianshu.com/c/063d8408c9b4?order_by=added_at&page=1'

        #'http://www.jianshu.com/u/21cc2f606243'
    ]

    def parse(self, response):
        selector = Selector(response)

        infos = selector.xpath("//ul[@class='note-list']/li")

        item = ArticleItem()

        for info in infos:

            article = info.xpath('div/a/text()').extract()[0]
            url = 'http://www.jianshu.com'+str(info.xpath('div/a/@href').extract()[0])

            pub_day = info.xpath('div/div[1]/div/span/@data-shared-at').extract()[0]


            author = info.xpath('div/div[1]/div/a/text()').extract()[0]
            author_url = 'http://www.jianshu.com'+str(info.xpath('div/div[1]/div/a/@href').extract()[0])

            reads = info.xpath('div/div[2]/a[1]/text()').extract()

            rd = int(str(reads[1]).strip())


            comments = info.xpath('div/div[2]/a[2]/text()').extract()

            cmt = int(str(comments[1]).strip())


            likes = info.xpath('div/div[2]/span/text()').extract()[0]
            likes = int(str(likes))


            rewards = info.xpath('div/div[2]/span[2]/text()').extract()

            if rewards:

                rewards =int(str(rewards[0]))
            else:
                rewards = 0


            item['author']=author
            item['url'] = url
            item['article'] = article
            item['reads'] = rd
            item['comments'] = cmt
            item['likes'] = likes
            item['rewards'] = rewards
            item['author_url'] = author_url
            item['pub_day']=pub_day

            yield item


            for i in range(2,839):
                nexturl = 'http://www.jianshu.com/c/063d8408c9b4?order_by=added_at&page=%s'%i

                yield Request(nexturl,callback=self.parse)


    def parse_author(self,response):

        selector = Selector(response)

        infos = selector.xpath("//div[@class='meta-block']/p/text()").extract()

        focus_num= int(str(infos[0]))
        fan_num= int(str(infos[1]))
        article_num = int(str(infos[2]))
        word_num = int(str(infos[3]))
        like_num = int(str(infos[4]))



        ## 从动态中抓取作者的注册时间
        ## 'http://www.jianshu.com/users/21cc2f606243/timeline?max_id=91276055&page=2'
        ## 问题 如何分页
        ## 问题 selenium可以实现分页操作  Scrapy+selenium 怎么整合













