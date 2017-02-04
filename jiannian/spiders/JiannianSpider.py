#coding=utf-8

from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from jiannian.items import  ArticleItem

import json




import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class JiannianSpider(CrawlSpider):

    name = 'jiannian'

    start_urls=[
        #'http://www.jianshu.com/c/063d8408c9b4?order_by=added_at&page=1' ## 简年 万人万字 8587篇
        #'http://www.jianshu.com/c/a8aa904095e4?order_by=added_at&page=1' ##妙笔福 33篇
        #'http://www.jianshu.com/c/ba695c8d02b8?order_by=added_at&page=1' ##慧眼福 34篇
        #'http://www.jianshu.com/c/71e0ef2c9cee?order_by=added_at&page=1' ##泉思福 50篇
        #'http://www.jianshu.com/p/72d082bf0ffb'  #测试文章url ,测试json用
        #'http://www.jianshu.com/p/320d06ef30bb'
    ]

    ## 解析json 数据,获得收录专题的title
    def parse_json(self,response):

        item = response.meta['item']
        author_url = item['author_url']

        data = json.loads(response.body)
        collect =  data['collections']
        cols=''
        if len(collect) >0 :
            for cc in collect:
                cols +=  cc['title']+';'


        item['inclu'] = cols

        yield item

        #yield Request(author_url, self.parse_author, meta={'item': item})



    def parse(self, response):
        selector = Selector(response)

        infos = selector.xpath("//ul[@class='note-list']/li")

        for info in infos:

            item = ArticleItem()

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

            yield Request(url,self.parse_article,meta={'item':item})


            for i in range(2,956):
            #for i in range(2, 7):
                nexturl = 'http://www.jianshu.com/c/063d8408c9b4?order_by=added_at&page=%s'%i
                #nexturl = 'http://www.jianshu.com/c/a8aa904095e4?order_by=added_at&page=%s' % i
                #nexturl = 'http://www.jianshu.com/c/ba695c8d02b8?order_by=added_at&page=%s' % i
                #nexturl = 'http://www.jianshu.com/c/71e0ef2c9cee?order_by=added_at&page=%s' % i

                yield Request(nexturl,callback=self.parse)


    ##到文章页面,获取这篇文章有多少字, 被哪些专题收录了
    ## 专题收录是json数据, 先要构造 json 目标url
    def parse_article(self,response):

        selector = Selector(response)

        wordage = selector.xpath("//span[@class='wordage']/text()").extract()[0]

        wordage = int(filter(str.isdigit,str(wordage)))

        item = response.meta['item']
        author_url = item['author_url']
        item['wordage'] = wordage

        #-------json url---------
        infos = selector.xpath("//meta/@content").extract()
        id = ''

        for info in infos:
            if (str(info).find('jianshu://notes/')) ==0 :
                id = filter(str.isdigit,str(info))
                break;

        collection_url ='http://www.jianshu.com/notes/%s/included_collections.json'%id

        #--------------------------

        yield Request(collection_url,callback=self.parse_json,meta={'item': item})


    ###到作者主页,主要是获取该作者一共写了多少篇文章
    ### ?? 这是一个冗余数据, 抓取时判断重复url
    ###    最后在这里 yied 重复url!
    ### 此方法去掉,另写一个Spider
    def parse_author(self,response):

        selector = Selector(response)

        infos = selector.xpath("//div[@class='meta-block']/p/text()").extract()

        item = response.meta['item']


        focus_num= int(str(infos[0]))
        fan_num= int(str(infos[1]))
        article_num = int(str(infos[2]))
        word_num = int(str(infos[3]))
        like_num = int(str(infos[4]))

        item['focus_num']= focus_num
        item['fan_num'] = fan_num
        item['article_num'] = article_num
        item['word_num'] = word_num
        item['like_num'] = like_num

        yield item


        ## 从动态中抓取作者的注册时间
        ## 'http://www.jianshu.com/users/21cc2f606243/timeline?max_id=91276055&page=2'
        ## 问题 如何分页
        ##
        ## 问题 selenium可以实现分页操作  Scrapy+selenium 怎么整合

        ## 问题: 如何在一篇文章中抓取被哪些专题收录
        ## A: 发现, 收录信息采用的异步加载 url如:http://www.jianshu.com/notes/8740848/included_collections?page=1
        ##    但是访问这个url得不到数据  ---> OK

        ## 问题: 抓取了冗余数据,Srapy如何操作数据库多个表(主从表)
        ## A: 感觉不行,还是要自己写一个爬取写入数据库多个表的














