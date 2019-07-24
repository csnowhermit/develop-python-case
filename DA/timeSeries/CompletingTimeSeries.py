import os
import sys
import time
import datetime
import cx_Oracle as cxo

'''
    客流时间序列分析：补全缺失时段
'''

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

oracleHost = "10.10.56.106"
oraclePort = 1521
oracleUser = "gzm"
oraclePassword = "gzm"
oracleDatabaseName = "ORCL"
oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
conn = cxo.connect(oracleConn)
cursor = conn.cursor()
print("已获取数据库连接")


'''
    循环控制器
'''
def controller():
    startdate, enddate = getDateRange()
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')

    stationAndLines = getStationAndLine()
    now = startdate
    delta = datetime.timedelta(days=1)
    while now <= enddate:
        for staLine in stationAndLines:
            complete(now.strftime("%Y-%m-%d"), str(staLine).split(',')[0], str(staLine).split(',')[1])
        now += delta

'''
    获取站线信息：要确保某线某站已启用
'''
def getStationAndLine():
    sql = "select distinct station_name, line_name from passenger_flow order by line_name, station_name"
    rs = cursor.execute(sql)
    result = rs.fetchall()
    stationAndLines = []
    for r in result:
        stationAndLines.append(str(r[0]) + "," + str(r[1]))
    return stationAndLines

'''
    补数：应判断某天该站开放没，没开放的话略过
'''
def complete(now, station_name, line_name):
    all_interval = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                     '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    select_sql = "select OPER_DATE, LINE_NAME, STATION_NAME, FLOW_IN, FLOW_OUT, TIME_INTERVAL  from passenger_flow where to_char(oper_date, 'yyyy-mm-dd')='%s' and station_name='%s' and line_name='%s' order by time_interval asc" % (now, station_name, line_name)
    rs = cursor.execute(select_sql)
    result = rs.fetchall()
    time_interval = []
    for r in result:
        time_interval.append(str(r[5]))

    if time_interval is None or len(time_interval)==0:
        print("%s %s 站 %s 天 尚未开放，无需补数" % (line_name, station_name, now))
        return

    loss_interval = list(set(all_interval) - set(time_interval))    # 缺失的时段
    if loss_interval is None or len(loss_interval)==0:
        print("%s %s 站 %s 天 数据完整，无需补数" % (line_name, station_name, now))
    else:
        if loss_interval is not None and len(loss_interval)>0:
            loss_interval.sort()
            for loss in loss_interval:
                s_sql = "" """
                    insert into passenger_flow 
                    (OPER_DATE, LINE_NAME, STATION_NAME, FLOW_IN, FLOW_OUT, TIME_INTERVAL) 
                    values(to_date('%s', 'yyyy-mm-dd'), '%s', '%s', 0, 0, '%s')
                """ % (now, line_name, station_name, loss)

                cursor.execute(s_sql)
            cursor.execute("commit")
            print("已补全 %s 天 %s %s 站的数据，已补时段：%s" % (now, line_name, station_name, loss_interval))


'''
    获取日期范围
'''
def getDateRange():
    sql = "select to_char(min(oper_date), 'yyyy-mm-dd'), to_char(max(oper_date), 'yyyy-mm-dd') from passenger_flow"
    rs = cursor.execute(sql)
    result = rs.fetchall()
    return str(result[0][0]), str(result[0][1])


def main():
    start = time.time()
    getDateRange()
    controller()

    cursor.close()
    print("补数完成，耗时：%s" % (time.time() - start))

if __name__ == '__main__':
    main()
