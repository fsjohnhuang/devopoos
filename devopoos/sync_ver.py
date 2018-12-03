import cx_Oracle

DB_URI = 'qms/TeSt_!35232@10.16.35.232:1608/mdqmsprd.midea.com'
ENCODING = 'UTF-8'
#alter table rpt_new_indicator_slice add(product_category_detail varchar2(4000) null)
#comment on column rpt_new_indicator_slice.product_category_detail is '产品分类明细'

sql = """

"""



conn = cx_Oracle.connect(DB_URI, encoding=ENCODING, nencoding=ENCODING)
cursor = conn.cursor()
cursor.execute(sql)

cursor.close()
conn.close()
