# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import logging 
from scrapy import signals
from scrapy.exporters import CsvItemExporter

def sendToFtp():
    from ftplib import FTP
    session = FTP(HOST)
    session.login(USER,PW)

    file = open('data.csv','rb')                  # file to send
    session.storbinary('STOR data.csv', file)     # send the file
    file.close()                                  # close file and FTP

    logging.info('============== FILE SENT TO FTP ======================')
    session.retrlines('LIST')
    logging.info('======================================================')

    session.quit()

def csvColumnClean():
    import pandas as pd 
    data = pd.read_csv("data.csv") 
    data.rename(columns = { "product_type":"tax:product_type",
                            "product_cat":"tax:product_cat",
                            "up_sell": "upsell_ids",
                            "cross_sell": "crosssell_ids",
                            "poordi_korgus": "Attribute:pa_Poordi kõrgus",
                            "poordi_korgus_data": "Attribute_data:pa_Poordi kõrgus",
                            "kasti_sisemoodud": "Attribute:pa_pa_Kasti sisemõõdud",
                            "kasti_sisemoodud_data": "Attribute_data:pa_Kasti sisemõõdud",
                            "haagise_gabariidid": "Attribute:pa_Haagise gabariidid",
                            "haagise_gabariidid_data": "Attribute_data:pa_Haagise gabariidid",
                            "uldkorgus": "Attribute:pa_Üldkõrgus",
                            "uldkorgus_data": "Attribute_data:pa_Üldkõrgus",
                            "sillatuup": "Attribute:pa_Sillatüüp",
                            "sillatuup_data": "Attribute_data:pa_Sillatüüp",
                            "raam": "Attribute:pa_Raam",
                            "raam_data": "Attribute_data:pa_Raam",
                            "pohi": "Attribute:pa_Põhi",
                            "pohi_data": "Attribute_data:pa_Põhi",
                            "taismass": "Attribute:pa_Täismass",
                            "taismass_data": "Attribute_data:pa_Täismass",
                            "tuhimass": "Attribute:pa_Tühimass",
                            "tuhimass_data": "Attribute_data:pa_Tühimass",
                            "kandevoime": "Attribute:pa_Kandevõime",
                            "kandevoime_data": "Attribute_data:pa_Kandevõime",
                            "pistiku_tuup": "Attribute:pa_Pistiku tüüp",
                            "pistiku_tuup_data": "Attribute_data:pa_Pistiku tüüp",
                            "rehvid": "Attribute:pa_Rehvid",
                            "rehvid_data": "Attribute_data:pa_Rehvid",
                            "kallutatav": "Attribute:pa_Kallutatav",
                            "kallutatav_data": "Attribute_data:pa_Kallutatav",
                            "pidurid": "Attribute:pa_Pidurid",
                            "pidurid_data": "Attribute_data:pa_Pidurid",
                            "sobilik_paatidele": "Attribute:pa_Sobilik paatidele kuni",
                            "sobilik_paatidele_data": "Attribute_data:pa_Sobilik paatidele kuni",
                            "haagise_valismoodud": "Attribute:pa_Haagise välismõõdud",
                            "haagise_valismoodud_data": "Attribute_data:pa_Haagise välismõõdud",
                            "reguleeritav_silla": "Attribute:pa_Reguleeritav silla asukoht",
                            "reguleeritav_silla_data": "Attribute_data:pa_Reguleeritav silla asukoht",
                            "laadimiskorgus": "Attribute:pa_Laadimiskõrgus",
                            "laadimiskorgus_data": "Attribute_data:pa_Laadimiskõrgus",
                            "luuk": "Attribute:pa_Luuk",
                            "luuk_data": "Attribute_data:pa_Luuk",
                            "sisekorgus": "Attribute:pa_Sisekõrgus",
                            "sisekorgus_data": "Attribute_data:pa_Sisekõrgus",
                            "sisemoodud": "Attribute:pa_Sisemõõdud",
                            "sisemoodud_data": "Attribute_data:pa_Sisemõõdud",
                            "valismoodud": "Attribute:pa_Välismõõdud",
                            "valismoodud_data": "Attribute_data:pa_Välismõõdud",
                            "sisemoot": "Attribute:pa_Sisemõõt",
                            "sisemoot_data": "Attribute_data:pa_Sisemõõt",
                            "varv": "Attribute:pa_Värv",
                            "varv_data": "Attribute_data:pa_Värv",
                            "moota": "Attribute:pa_Mõõt A",
                            "moota_data": "Attribute_data:pa_Mõõt A",
                            "mootb": "Attribute:pa_Mõõt B",
                            "mootb_data": "Attribute_data:pa_Mõõt B",
                            "mootc": "Attribute:pa_Mõõt C",
                            "mootc_data": "Attribute_data:pa_Mõõt C",

                            }, inplace=True) 
    data.to_csv('data.csv', index = False)

class RespoPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('data.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        csvColumnClean() # Column rename
        sendToFtp() # send to FTP


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
