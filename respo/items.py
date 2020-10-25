# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def return_stock(value):
    if value == '--':
        return 'onbackorder'
    else:
        return 'instock'

def return_stock_status(value):
    if value == '--':
        return '0'
    else:
        if '+' in value:
            return value.replace('+', '')
        else:
            return value.replace('tk', '')

def clean_eur(value):
    return value.replace('€', '')

class LisavarustusItem(scrapy.Item):
     post_title = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = Join()
    )

class ProductItem(scrapy.Item):     
    post_title = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = Join()
    )

    post_content = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = Join()
    )

    sku = scrapy.Field() 

    post_status = scrapy.Field() 

    stock = scrapy.Field(
        input_processor = MapCompose(return_stock),
        output_processor = TakeFirst()
    )

    stock_status = scrapy.Field(
        input_processor = MapCompose(return_stock_status),
        output_processor = TakeFirst()
    )

    backorders = scrapy.Field() 

    regular_price = scrapy.Field(
        input_processor = MapCompose(clean_eur),
        output_processor = TakeFirst()
    )
    
    sale_price = scrapy.Field(
        input_processor = MapCompose(clean_eur),
        output_processor = TakeFirst()
    )

    images = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = Join('|')
    )

    up_sell = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = Join('|')
    )

    cross_sell = scrapy.Field(
        input_processor = MapCompose(),
        output_processor = Join('|')
    )

    product_type = scrapy.Field()

    product_cat = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = Join('>')
    )

    poordi_korgus = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    poordi_korgus_data= scrapy.Field()

    kasti_sisemoodud= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    kasti_sisemoodud_data= scrapy.Field()

    haagise_gabariidid= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    haagise_gabariidid_data= scrapy.Field()
    
    uldkorgus= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    uldkorgus_data= scrapy.Field()
    
    sillatuup= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    sillatuup_data= scrapy.Field()
    
    raam= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    raam_data= scrapy.Field()
    
    pohi= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    pohi_data= scrapy.Field()
    
    taismass= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    taismass_data= scrapy.Field()
    
    tuhimass= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    tuhimass_data= scrapy.Field()
    
    kandevoime= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    kandevoime_data= scrapy.Field()
    
    pistiku_tuup= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    pistiku_tuup_data= scrapy.Field()
    
    rehvid= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    rehvid_data= scrapy.Field()
    
    kallutatav= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    kallutatav_data= scrapy.Field()
    
    pidurid= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    pidurid_data= scrapy.Field()

    sobilik_paatidele= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    sobilik_paatidele_data= scrapy.Field()
    
    haagise_valismoodud= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    haagise_valismoodud_data= scrapy.Field()
    
    reguleeritav_silla= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    reguleeritav_silla_data= scrapy.Field()
    
    laadimiskorgus= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    laadimiskorgus_data= scrapy.Field()
    
    luuk= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    luuk_data= scrapy.Field()
    
    sisekorgus= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    sisekorgus_data= scrapy.Field()
    
    sisemoodud= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    sisemoodud_data= scrapy.Field()
    
    valismoodud= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    valismoodud_data= scrapy.Field()
    
    # Lisavarustus ja Varuosad
    sisemoot= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    sisemoot_data= scrapy.Field()

    varv= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    varv_data= scrapy.Field()

    moota= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    moota_data= scrapy.Field()    

    mootb= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    mootb_data= scrapy.Field()    

    mootc= scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    mootc_data= scrapy.Field()            
  