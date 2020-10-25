import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from respo.items import ProductItem
from respo.items import LisavarustusItem
from scrapy.selector import Selector


def handleData(value):
    if value is None or value == '':
        return "0|0|0"
    else:
        return "0|1|0"

def get_name(value):
    switcher = {
        'Pealesõiduteed': "Pealesõidutee",
        'Koormarihmad ja aasad': "Koormarihm / Aas",
        'Tiisli tugirattad ja nurgatoed': "Tiisli tugirattas / Nurgatugi",
        'Kattekaaned': "Kattekaan",
        'Tendid': "Tent",
        'Poordikõrgendused': "Poordikorgendus",
        'Vaierid': 'Vaier',
        'Tiislid': 'Tiisel',
    }
    return switcher.get(value, "Nan")

class BasicSpider(scrapy.Spider):
    name = 'respo'

    script = '''
    function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(5.5))
    assert(splash:runjs('document.querySelector(".swatch-attribute-options >.nav.nav-tabs> li:nth-child(2) > a").click()'))
    return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
    }
    end
    '''

    def start_requests(self):
        url = 'https://www.respo.ee/et/haagised'
        url2 = 'https://www.respo.ee/et/lisavarustus'
        url3 = 'https://www.respo.ee/et/varuosad'
        yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 5.5 })
        yield SplashRequest(url=url2, callback=self.parse_lisavarustus, endpoint='render.html', args={'wait': 5.5 })
        yield SplashRequest(url=url3, callback=self.parse_lisavarustus, endpoint='render.html', args={'wait': 5.5 })

    def parse(self, response):
        for page in response.xpath("//*[@class='owl-stage']/div"):
            product_page_url = (page.xpath(".//div/a/@href").extract_first())
            yield SplashRequest(url=product_page_url, callback=self.parse_listings, endpoint='render.html', args={'wait': 5.5 })

    def parse_lisavarustus(self, response):
        for page in response.xpath("//*[@class='row flex-row']/div"):
            page_url = page.xpath(".//*[@class='item-card prod-cat']/@href").extract_first()
            yield SplashRequest(url=page_url, callback=self.parse_lisavarustus_listing, endpoint='render.html', args={'wait': 5.5 })

    def parse_lisavarustus_listing(self, response):

        cat_name = response.xpath("//*[@class='breadcrumb']/*[contains(@class, 'active')]/text()").extract_first()
        cat_name = cat_name.strip()

        for lisavarustus in response.xpath("//*[@id='listtable']/tbody/tr[position()>1]"):
            #loader = ItemLoader(item=LisavarustusItem(), selector=lisavarustus, response=response)
            loader = ItemLoader(item=ProductItem(), selector=lisavarustus, response=response)

            # Product name logic
            name_exists = lisavarustus.xpath(".//*[@class='col_name']/text()")
            if name_exists:
                loader.add_xpath('post_title', ".//*[@class='col_name']/text()")
            else:
                loader.add_value('post_title', get_name(cat_name))
            
            if lisavarustus.xpath(".//*[@class='col_description']/text()"):
                loader.add_xpath('post_content', ".//*[@class='col_description']/text()")  
            else:
                loader.add_xpath('post_content', ".//*[@class='col_description']/p/text()")  
            
            loader.add_xpath('sku', ".//*[@class='col_sku']/text()")
            loader.add_value('post_status', 'publish')
            loader.add_xpath('stock', ".//*[@class='text-center']/span/text()")
            loader.add_xpath('stock_status', ".//*[@class='text-center']/span/text()")
            loader.add_value('backorders', 'yes')
            loader.add_xpath('regular_price', ".//*[@class='price']/text()")

            img = lisavarustus.xpath(".//*[@class='thumb_preview']/@href")
            if img is None:
                loader.add_xpath('images', ".//*[@class='photo image img-responsive']/@src")
            else:
                loader.add_xpath('images', ".//*[@class='thumb_preview']/@href")
                
            loader.add_value('product_type',  "simple")
            loader.add_xpath('product_cat', "//*[@class='breadcrumb']/li[position()>1]")

            # Lisavarustus
            check = lisavarustus.xpath("//*[@class='breadcrumb']/li[position()>1 and position()<last()]/a/text()").extract_first()
            check = check.strip()

            if check == 'Lisavarustus':
                if lisavarustus.xpath(".//*[@class='col_trailer_external_dimensions']/text()"):
                    loader.add_xpath('valismoodud', ".//*[@class='col_trailer_external_dimensions']/text()")
                    loader.add_value('valismoodud_data', handleData(lisavarustus.xpath(".//*[@class='col_trailer_external_dimensions']/text()")))
                    # loader.add_value('attribute_1', "Välismõõdud")
                    # loader.add_xpath('attribute_data_1', ".//*[@class='col_trailer_external_dimensions']/text()")

                if lisavarustus.xpath(".//*[@class='col_load_capacity']/text()"):
                    loader.add_xpath('kandevoime', ".//*[@class='col_load_capacity']/text()")
                    loader.add_value('kandevoime_data', handleData(lisavarustus.xpath(".//*[@class='col_load_capacity']/text()")))
                    # loader.add_value('attribute_2', "Kandevõime")
                    # loader.add_xpath('attribute_data_2', ".//*[@class='col_load_capacity']/text()")

                if lisavarustus.xpath(".//*[@class='col_internal_dimensions']/text()"):
                    loader.add_xpath('sisemoot', ".//*[@class='col_internal_dimensions']/text()")
                    loader.add_value('sisemoot_data', handleData(lisavarustus.xpath(".//*[@class='col_internal_dimensions']/text()")))
                    # loader.add_value('attribute_3', "Sisemõõt")
                    # loader.add_xpath('attribute_data_3', ".//*[@class='col_internal_dimensions']/text()")

                if lisavarustus.xpath(".//*[@class='col_internal_height']/text()"):
                    loader.add_xpath('sisekorgus', ".//*[@class='col_internal_height']/text()")
                    loader.add_value('sisekorgus_data', handleData(lisavarustus.xpath(".//*[@class='col_internal_height']/text()")))
                    # loader.add_value('attribute_4', "Sisekõrgus")
                    # loader.add_xpath('attribute_data_4', ".//*[@class='col_internal_height']/text()")

                if lisavarustus.xpath(".//*[@class='col_extra_1']/text()"):
                    loader.add_xpath('varv', ".//*[@class='col_extra_1']/text()")
                    loader.add_value('varv_data', handleData(lisavarustus.xpath(".//*[@class='col_extra_1']/text()")))
                    # loader.add_value('attribute_5', "Värv")
                    # loader.add_xpath('attribute_data_5', ".//*[@class='col_extra_1']/text()")

            # Varuosad
            if check == 'Varuosad':
                is_tiisel = lisavarustus.xpath("//*[@class='breadcrumb']/li[last()]/text()").extract_first()
                is_tiisel = is_tiisel.strip()

                if is_tiisel != 'Tiislid':
                    if lisavarustus.xpath(".//*[@class='col_internal_dimensions']/text()"):
                        loader.add_xpath('moota', ".//*[@class='col_trailer_external_dimensions']/text()")
                        loader.add_value('moota_data', handleData(lisavarustus.xpath(".//*[@class='col_trailer_external_dimensions']/text()")))
                        # loader.add_value('attribute_1', "Mõõt A")
                        # loader.add_xpath('attribute_data_1', ".//*[@class='col_trailer_external_dimensions']/text()")

                    if lisavarustus.xpath(".//*[@class='col_internal_height']/text()"):
                        loader.add_xpath('mootb', ".//*[@class='col_internal_height']/text()")
                        loader.add_value('mootb_data', handleData(lisavarustus.xpath(".//*[@class='col_internal_height']/text()")))
                        # loader.add_value('attribute_2', "Mõõt B")
                        # loader.add_xpath('attribute_data_2', ".//*[@class='col_internal_height']/text()")


                if lisavarustus.xpath(".//*[@class='col_internal_dimensions']/text()"):
                    loader.add_xpath('moota', ".//*[@class='col_internal_dimensions']/text()")
                    loader.add_value('moota_data', handleData(lisavarustus.xpath(".//*[@class='col_internal_dimensions']/text()")))
                    # loader.add_value('attribute_1', "Mõõt A")
                    # loader.add_xpath('attribute_data_1', ".//*[@class='col_internal_dimensions']/text()")

                if lisavarustus.xpath(".//*[@class='col_internal_height']/text()"):
                    loader.add_xpath('mootb', ".//*[@class='col_internal_height']/text()")
                    loader.add_value('mootb_data', handleData(lisavarustus.xpath(".//*[@class='col_internal_height']/text()")))
                    # loader.add_value('attribute_2', "Mõõt B")
                    # loader.add_xpath('attribute_data_2', ".//*[@class='col_internal_height']/text()")

                if lisavarustus.xpath(".//*[@class='col_trailer_external_dimensions']/text()"):
                    loader.add_xpath('mootc', ".//*[@class='col_trailer_external_dimensions']/text()")
                    loader.add_value('mootc_data', handleData(lisavarustus.xpath(".//*[@class='col_trailer_external_dimensions']/text()")))
                    # loader.add_value('attribute_3', "Mõõt C")
                    # loader.add_xpath('attribute_data_3', ".//*[@class='col_trailer_external_dimensions']/text()")


            yield loader.load_item()

        #Go to next page if exists
        next_page = response.selector.xpath("//*[@class='action  next']/@href").extract_first()
        if next_page is not None:
            yield SplashRequest(url=next_page, callback=self.parse_lisavarustus_listing, endpoint='render.html', args={'wait': 5.5 })


    def parse_listings(self, response):
        for product in response.xpath("//tbody/tr[position()>1]"):
            product_url = product.xpath(".//*[@class='col_name']/a/@href").extract_first()
            yield SplashRequest(url=product_url, callback=self.parse_product, endpoint='render.html', args={'wait': 10.5 })

        #Go to next page if exists
        next_page = response.selector.xpath("//*[@class='action  next']/@href").extract_first()
        if next_page is not None:
            yield SplashRequest(url=next_page, callback=self.parse_listings, endpoint='render.html', args={'wait': 5.5 })

    def parse_product(self, response):
        product = response.xpath("//*[@id='maincontent']")
    
        loader = ItemLoader(item=ProductItem(), selector=product, response=response)
        loader.add_xpath('post_title', "//*[@class='img-title']/h1/text()")

        # Description logic
        has_more_text= response.xpath("//*[@class='row description']/div[@class='col-md-9']/*[not(self::strong)]/text()")
        if has_more_text:
            loader.add_xpath('post_content', "//*[@class='row description']/div[@class='col-md-9']/*[not(self::strong)]/text()")
        else:
            loader.add_xpath('post_content', "//*[@class='row description']/div[@class='col-md-9']/text()")  


        loader.add_xpath('sku', "//*[@class='img-title']/p/text()")
        loader.add_value('post_status', 'publish')
        loader.add_xpath('stock', "//*[@class='qty_field']/text()")
        loader.add_xpath('stock_status', "//*[@class='qty_field']/text()")
        loader.add_value('backorders', 'yes')

        # Sales price logic
        on_sale = response.xpath("//*[@data-price-type='oldPrice']/span/text()")
        if on_sale:
            loader.add_xpath('regular_price', "//*[@data-price-type='oldPrice']/span/text()")
            loader.add_xpath('sale_price', "//*[@data-price-type='finalPrice']/span/text()")     
        else:
            loader.add_xpath('regular_price', "//*[@data-price-type='finalPrice']/span/text()")
            loader.add_value('sale_price', "")

        loader.add_xpath('images',  "//*[@class='thumb-list']/a/@href")
        loader.add_value('product_type',  "simple")
        loader.add_xpath('product_cat', "//*[@class='breadcrumb']/li[position()>1 and position()<last()]")
        
        loader.add_xpath('up_sell', "//*[@id='tabaccessories']//tr[contains(@data-bind, 'attr: ')]/td[3]/text()")
        loader.add_xpath('cross_sell', "//*[@id='tabspare']//tr[contains(@data-bind, 'attr: ')]/td[3]/text()")
        

        # Get Attributes

        # Poordi kõrgus:
        loader.add_xpath('poordi_korgus', "//*[contains(text(),'Poordi kõrgus:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('poordi_korgus_data', handleData(product.xpath("//*[contains(text(),'Poordi kõrgus:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Kasti sisemõõdud:
        loader.add_xpath('kasti_sisemoodud', "//*[contains(text(),'Kasti sisemõõdud:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('kasti_sisemoodud_data', handleData(product.xpath("//*[contains(text(),'Kasti sisemõõdud:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Haagise gabariidid:
        loader.add_xpath('haagise_gabariidid', "//*[contains(text(),'Haagise gabariidid:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('haagise_gabariidid_data', handleData(product.xpath("//*[contains(text(),'Haagise gabariidid:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Üldkõrgus:
        loader.add_xpath('uldkorgus', "//*[contains(text(),'Üldkõrgus:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('uldkorgus_data', handleData(product.xpath("//*[contains(text(),'Üldkõrgus:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Sillatüüp:
        loader.add_xpath('sillatuup', "//*[contains(text(),'Sillatüüp:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('sillatuup_data', handleData(product.xpath("//*[contains(text(),'Sillatüüp:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Raam:
        loader.add_xpath('raam', "//*[contains(text(),'Raam:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('raam_data', handleData(product.xpath("//*[contains(text(),'Raam:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Põhi:
        loader.add_xpath('pohi', "//*[contains(text(),'Põhi:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('pohi_data', handleData(product.xpath("//*[contains(text(),'Põhi:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Täismass:
        loader.add_xpath('taismass', "//*[contains(text(),'Täismass:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('taismass_data', handleData(product.xpath("//*[contains(text(),'Täismass:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Tühimass:
        loader.add_xpath('tuhimass', "//*[contains(text(),'Tühimass:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('tuhimass_data', handleData(product.xpath("//*[contains(text(),'Tühimass:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Kandevõime:
        loader.add_xpath('kandevoime', "//*[contains(text(),'Kandevõime:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('kandevoime_data', handleData(product.xpath("//*[contains(text(),'Kandevõime:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Pistiku tüüp:
        loader.add_xpath('pistiku_tuup', "//*[contains(text(),'Pistiku tüüp:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('pistiku_tuup_data', handleData(product.xpath("//*[contains(text(),'Pistiku tüüp:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Rehvid:
        loader.add_xpath('rehvid', "//*[contains(text(),'Rehvid:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('rehvid_data', handleData(product.xpath("//*[contains(text(),'Rehvid:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Kallutatav:
        loader.add_xpath('kallutatav', "//*[contains(text(),'Kallutatav:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('kallutatav_data', handleData(product.xpath("//*[contains(text(),'Kallutatav:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Pidurid:
        loader.add_xpath('pidurid', "//*[contains(text(),'Pidurid:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('pidurid_data', handleData(product.xpath("//*[contains(text(),'Pidurid:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Sobilik paatidele kuni:
        loader.add_xpath('sobilik_paatidele', "//*[contains(text(),'Sobilik paatidele kuni:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('sobilik_paatidele_data', handleData(product.xpath("//*[contains(text(),'Sobilik paatidele kuni:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Haagise välismõõdud:
        loader.add_xpath('haagise_valismoodud', "//*[contains(text(),'Haagise välismõõdud:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('haagise_valismoodud_data', handleData(product.xpath("//*[contains(text(),'Haagise välismõõdud:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Reguleeritav silla asukoht:
        loader.add_xpath('reguleeritav_silla', "//*[contains(text(),'Reguleeritav silla asukoht:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('reguleeritav_silla_data', handleData(product.xpath("//*[contains(text(),'Reguleeritav silla asukoht:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Laadimiskõrgus:
        loader.add_xpath('laadimiskorgus', "//*[contains(text(),'Laadimiskõrgus:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('laadimiskorgus_data', handleData(product.xpath("//*[contains(text(),'Laadimiskõrgus:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Luuk:
        loader.add_xpath('luuk', "//*[contains(text(),'Luuk:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('luuk_data', handleData(product.xpath("//*[contains(text(),'Luuk:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Sisekõrgus:
        loader.add_xpath('sisekorgus', "//*[contains(text(),'Sisekõrgus:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('sisekorgus_data', handleData(product.xpath("//*[contains(text(),'Sisekõrgus:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Sisemõõdud:
        loader.add_xpath('sisemoodud', "//*[contains(text(),'Sisemõõdud:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('sisemoodud_data', handleData(product.xpath("//*[contains(text(),'Sisemõõdud:') and not(contains(@class, 'hidden'))]/span/text()")))
        # Välismõõdud:
        loader.add_xpath('valismoodud', "//*[contains(text(),'Välismõõdud:') and not(contains(@class, 'hidden'))]/span/text()")
        loader.add_value('valismoodud_data', handleData(product.xpath("//*[contains(text(),'Välismõõdud:') and not(contains(@class, 'hidden'))]/span/text()")))

        yield loader.load_item()

        # Variation check if exists
        product_version = product.xpath("//*[@id='product-options-wrapper']/div/div/div[2]/ul/li[2]/a[contains(@class, 'text') and not (contains(@class, 'selected'))]/@href").extract_first()
        if  product_version:
            url = response.request._original_url
            yield SplashRequest(url=url, callback=self.parse_product, endpoint='execute', args={'wait': 10.5 , 'lua_source': self.script}, dont_filter=True)
