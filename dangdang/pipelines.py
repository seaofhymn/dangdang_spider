# -*- coding: utf-8 -*-
from pymysql import connect
from pymongo import MongoClient

class DangdangPipeline(object):
    def process_item(self, item, spider):
        con = connect(host ="localhost",port=3306, user='root', password='', database='dangdang', charset='utf8')
        cur = con.cursor()
        sql = """insert into dd (name,img,cat,price,book_detail,book_comments_num,book_comments_href,book_author,book_pub,book_pub_time,comments,home,home_link,book_more_info,all_more,book_content,book_abs_jud,book_jud) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");""" %(item['name'], item['img'], item['cat'], item['price'], item['book_detail'], item['book_comments_num'], item['book_comments_href'], item['book_author'], item['book_pub'], item['book_pub_time'], item['comments'], item['home'], item['home_link'], item['book_more_info'], item['all_more'], item['book_content'], item['book_abs_jud'], item['book_jud'])
        # sql = """insert into yunyinyue (na,likes,href) values("%s","%s","%s");""" %(item["name"],item["likes"],item["href"])
        cur.execute(sql)
        con.commit()
        # print(item)
        cur.close()
        con.close()
        return item

class DangdangMongoDBPipeline(object):
    def process_item(self,item,spider):
        conn = MongoClient('', 27017)
        db = conn.dangdang
        my_set = db.dang
        my_set.insert(item)
        conn.close()
        return item
