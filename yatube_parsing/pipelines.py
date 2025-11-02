# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from scrapy.exceptions import DropItem


# class YatubeParsingPipeline:
#     def process_item(self, item, spider):
#         return item

Base = declarative_base()


class MondayPost(Base):
    __tablename__ = 'monday_post'
    id = Column(Integer, primary_key=True)
    author = Column(String(200))
    date = Column(Date)
    text = Column(Text)


class MondayPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        date_str = item.get('date')
        post_date = dt.datetime.strptime(date_str, '%d.%m.%Y').date()
        if post_date.weekday() == 0:
            post = MondayPost(
                author=item.get('author'),
                date=post_date,
                text=item.get('text')
            )
            self.session.add(post)
            self.session.commit()
            return item
        raise DropItem('Этотъ постъ написанъ не въ понедѣльникъ')

    def close_spider(self, spider):
        self.session.close()
