import pymysql

def getip():
    try:
        conn = pymysql.connect(host='', user='root', passwd='', port=3306, db='nihao')
        sql = """select ip,stat from dyn where randid=9;"""
        cur = conn.cursor()
        cur.execute(sql)
        # conn.commit()
        ret = cur.fetchall()
        if ret:
            sta = ret[0][1]
            if sta:
                ip = ret[0][0] + ':808'
                print(ip)
                conn.close()
                # time.sleep(10)
                return ip
        else:
            print("请等待")
            return 0
    except Exception as e:
        print(e)
        return 0

def main():
    getip()

if __name__ == "__main__":
    main()