import scrapy
from MTSBW.items import MtsbwItem
from random import randint

from PIL import Image

import threading

import json

import getpass

class spiderss(scrapy.Spider):
    name = 'MTSBW'
    UserAgent = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    ]

    def start_requests(self):
        url = 'https://passport.banggo.com/CASServer/login'
        yield scrapy.Request(callback=self.GetCaptcha, url=url, headers={'user-agent': self.UserAgent[0]}, meta={'cookiejar': 1})

    def GetCaptcha(self, response):
        data = {
            'username': input('请输入用户名：'),
            'password': getpass.getpass('请输入密码：'),
            'vcode': '',
            'rememberUsername': 'on',
            '_eventId': 'submit',
            'loginType': '0',
            'lastIp': '117.172.9.98',
            'lt': '',
            'returnurl': ''
        }
        data['lt'] = response.xpath('//input[@name="lt"]/@value').extract()[0]
        # print(data)
        vcode_l = response.xpath(
            '//img[@class="change_img"]/@src').extract()[0]
        yield scrapy.Request(callback=self.showCAPTCHA,
        url=vcode_l,
        headers={'user-agent': self.UserAgent[0]},
        meta={'cookiejar': response.meta['cookiejar'], 'data': data})

    def showCAPTCHA(self, response):
        with open('CAPTCHA.JPG', 'wb') as f:
            f.write(response.body)

        class showimg(threading.Thread):
            def __init__(self, file):
                threading.Thread.__init__(self)
                self.file = file

            def run(self):
                im = Image.open(self.file)
                im.show()
        a = showimg('CAPTCHA.JPG')
        a.start()
        response.meta['data']['vcode'] = input('请输入显示的验证码：')
        a.join()
        print(response.meta['data'])
        yield scrapy.FormRequest(
            url='https://passport.banggo.com/CASServer/login?service=http%3A%2F%2Fbgact.banggo.com%2Flogin.shtml%3Fr_url%3Dhttp%25253A%25252F%25252Fuser.banggo.com%25252Fmember%25252Findex', 
            method='POST',
            headers={
                'User-Agent': self.UserAgent[0],
                'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                #'Content-Length': '168',
                'cookie':'loginType=0; JSESSIONID=5E005B9CBAE219D268F09DD4C3468735;  PHPSESSID=ST323645AedPnNwU5ZIAHUAHgEuMpassportbanggocom01;Hm_lvt_0600094e16cec594db18b43c878d459f=1552309952; Hm_lpvt_0600094e16cec594db18b43c878d459f=1552309952; bgi_unique_id=15523099522877318; cas_sessionId=5E005B9CBAE219D268F09DD4C3468735',
                'Content-Type':'application/x-www-form-urlencoded',
                'Host': 'passport.banggo.com',
                'Origin': 'https://passport.banggo.com',
                'Referer': 'https://passport.banggo.com/CASServer/login?service=http://bgact.banggo.com/login.shtml%3Fr_url=http%253A%252F%252Fuser.banggo.com%252Fmember%252Findex',
                'Upgrade-Insecure-Requests': '1'
                }, 
            callback=self.GetPage, 
            formdata=response.meta['data'], 
            meta={'cookiejar': response.meta['cookiejar']},

            )
    def GetPage(self,response):
        urls=[
            'https://search.banggo.com/search/a_3_a_a_a_a_a_a_a_a_a_a.shtml',
            'https://search.banggo.com/search/a_4%7C13_a_a_a_a_a_a_a_a_a_a_97-203s.shtml?avn=1',
            'https://search.banggo.com/search/a_473.shtml?avn=1',
            'https://search.banggo.com/search/a_490_a_a_a_a_a_a_a_a_a_a.shtml?avn=1',
            'https://search.banggo.com/search/a_738_a_a_a_a_a_a_a_a_a_a.shtml?avn=1',
            'https://search.banggo.com/search/a_28%7C189%7C190%7C192%7C194%7C196_a_a_a_a_a_a_a_a_a_a.shtml'
        ]

        for url in urls:
            yield scrapy.Request(url=url,
            callback=self.GetPage1,
            headers={'user-agent': self.UserAgent[randint(0, 3)]},
            meta={'cookiejar':response.meta['cookiejar']})    

    def GetPage1(self, response):
        # print(response.text)
        with open('1.html','w',encoding='utf8') as f:
            f.write(response.text)
        link = response.xpath('//a[@class="mbshop_listPdImg"]/@href').extract()
        for i in link:
            id=i.split('/')[-1].split('.')[0]
            yield scrapy.Request(
                url='https://bgact.banggo.com/Goods/getProductBaseInfo?goods_sn='+id,
                callback=self.GetBaseInfo,
                headers={'user-agent': self.UserAgent[randint(0, 3)]},
                meta={'cookiejar': response.meta['cookiejar'],'id':id})
        if response.xpath('//a[contains(text(),"下一页")]/@href').extract()==[]:
            pass
        else:
            yield scrapy.Request(url='https://search.banggo.com'+response.xpath('//a[contains(text(),"下一页")]/@href').extract()[0],
            callback=self.GetPage1,
            headers={'user-agent': self.UserAgent[randint(0, 3)]},
            meta={'cookiejar':response.meta['cookiejar']})
         
            
    

    def GetBaseInfo(self,response):
        item=MtsbwItem()
        a=json.loads(response.text[1:-1])
        item['brand_name']=a['data']['productInfo']['brandName']
        item['disc_price']=a['data']['productInfo']['minSalesPrice']
        item['sell_count']=a['data']['productInfo']['saleCount']
        item['price']=a['data']['productInfo']['marketPrice']
        yield scrapy.Request(url='https://bgact.banggo.com/Goods/GetProductDescription?goods_sn='+response.meta['id'],
            callback=self.GetData,
            headers={'user-agent': self.UserAgent[randint(0, 3)]}, 
            meta={'cookiejar': response.meta['cookiejar'],'item':item})



    def GetData(self, response):
        a=json.loads(response.text[1:-1])
        response.meta['item']['season']=a['data']['goodsAttrs']['85']['attrValue'][0]
        response.meta['item']['gender']=a['data']['goodsAttrs']['97']['attrValue'][0]
        response.meta['item']['kind']=a['data']['categories']['categoryName']
        response.meta['item']['serial_id']=a['data']['productSysCode']
        response.meta['item']['name']=a['data']['productName']
        response.meta['item']['goods_url']='https://www.banggo.com/goods/'+response.meta['item']['serial_id']+'.shtml'

        # print(response.meta['item'])
        # print('-'*20)
        yield response.meta['item']