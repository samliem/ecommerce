# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin
import random

class TopedSpider(Spider):
    name = 'toped'
    allowed_domains = ['tokopedia.com']
    start_urls = [
        'https://www.tokopedia.com/p/buku/arsitektur-desain?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/buku-hukum?ob=9&page=1',
        # 'https://www.tokopedia.com/p/buku/buku-import?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/buku-masakan?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/buku-persiapan-ujian?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/buku-remaja-dan-anak?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/ekonomi-bisnis?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/hobi?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/kamus?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/kedokteran?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/keluarga?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/kesehatan-gaya-hidup?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/kewanitaan?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/komik?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/komputer-internet?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/majalah?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/novel-sastra?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/pendidikan?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/pengembangan-diri-karir?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/pertanian?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/religi-spiritual?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/sosial-politik?ob=5&page=1',
        # 'https://www.tokopedia.com/p/buku/teknik-sains?ob=5&page=1'
    ]

    # counter = 0

    def parse(self, response):
        next_click_time = (5, 5.5, 6, 6.5, 7)
        open_url_start_time = (12, 12.5, 13, 13.5)
        self.driver = webdriver.Chrome(r"D:\scrapy\selenium\chromedriver.exe")
        
        # for url in self.start_urls:
            # reset counter for each link
            # self.counter = 0

        self.driver.get(response.url)
        elapse_open_url_start = random.choice(open_url_start_time)
        sleep(elapse_open_url_start)
        sel = Selector(text=self.driver.page_source)
        prod_links = sel.xpath('//*[contains(@class,"css-bk6tzz")]/a[not(@label-atm)]/@href').extract()
        for prod_link in prod_links:
            open_product_page = (4, 4.5, 5, 5.5, 6)
            sleep(random.choice(open_product_page))
            yield Request(prod_link, callback=self.parse_books)
            
            # continue_crawl = True
            # while continue_crawl:
            #     try:
        next_page = self.driver.find_element_by_xpath('//i[contains(@class,"css-98hn3t")]')
        next_sleep = random.choice(next_click_time)
        sleep(next_sleep)
        next_page.click()
        sel = Selector(text=self.driver.page_source)
        prod_links = sel.xpath('//*[contains(@class,"css-bk6tzz")]/a[not(@label-atm)]/@href').extract()

        for prod_link in prod_links:
                        # if self.counter == 100:
                        #     continue_crawl = False
                        #     break

            open_product_page = (4, 4.5, 5, 5.5, 6)
            sleep(random.choice(open_product_page))
            yield Request(prod_link, callback=self.parse_books)

                # except NoSuchElementException:
                #     self.logger.info('No more pages to load.')
                #     break
        
        # sleep(30)
        # self.driver.quit()
            
    def parse_books(self, response):
        terjual = response.xpath('(//span[@data-testid="lblPDPDetailProductSuccessRate"]/text())[3]').extract_first()
        if terjual: 
            terjual = int(terjual)
            root_cat = response.xpath('//li[@class="css-mbdxj3"]/a/text()').extract()[1]
            in_cat = response.xpath('//li[@class="css-mbdxj3"]/a/text()').extract()[-2]
            
            merchant_type = response.xpath('//p[@data-testid="imgPDPDetailShopBadge"]/@type').extract_first()
            if merchant_type :
                if merchant_type == 'OS': merchant_type = 'Official Store'
                if merchant_type == 'PM': merchant_type = 'Power Merchant'

            prod_name = response.xpath('//h1[@data-testid="lblPDPDetailProductName"]/text()').extract_first()
            rating = float(response.xpath('//span[@data-testid="lblPDPDetailProductRatingNumber"]/text()').extract_first())
            ulasan = int(response.xpath('//span[@data-testid="lblPDPDetailProductRatingCounter"]/text()[2]').extract_first())
            dilihat = int(response.xpath('//span[@data-testid="lblPDPDetailProductSeenCounter"]/b/text()').extract_first())
            merchant_name = response.xpath('//a[@data-merchant-test="llbPDPFooterShopName"]/text()').extract_first()
            merchant_city = response.xpath('//span[@data-testid="lblPDPFooterLastOnline"]/text()').extract_first()
            price = response.xpath('//h3[@data-testid="lblPDPDetailProductPrice"]/text()').extract_first()
            price = int(price.split("Rp",1)[1].replace(".",""))
            weight = response.xpath('//p[@data-testid="PDPDetailWeightValue"]/text()').extract_first()
            weight = int(weight.replace("gr","").replace("Kg",""))

            voucher_type = response.xpath('//p[@data-testid="MerchantVoucherType"]/text()').extract()
            #dialokasikan 2 voucher saja
            if voucher_type:
                voucher_val = response.xpath('//h2[@data-testid="MerchantVoucherValue"]/text()').extract() 
                voucher_type1 = voucher_type[0]
                voucher_val1 = voucher_val[0]
                if len(voucher_type) > 1 :
                    voucher_type2 = voucher_type[1]
                    voucher_val2 = voucher_val[1]
            else:
                voucher_type1 = voucher_type2 = voucher_val1 = voucher_val2 = ""
            
            yield {
                'root_cat': root_cat,
                'in_cat': in_cat,
                'merchnat_name': merchant_name,
                'merchant_type': merchant_type,
                'merchant_city': merchant_city,
                'prod_name': prod_name,
                'rating': rating,
                'ulasan': ulasan,
                'terjual': terjual,
                'dilihat': dilihat,
                'price': price,
                'weight': weight,
                'voucher_type1': voucher_type1,
                'voucher_val1': voucher_val1,
                'voucher_type2': voucher_type2,
                'voucher_val2': voucher_val2
            }
