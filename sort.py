# -*- coding:utf-8 -*-

# 找名字 名字列表 nameList
# 找日期 日系列表 dateList
# 找时间点 时间列表 timeList
# 排序 最大时间 maxTime，minTime
# 最终结果 字典result{'name':{date:{'minTime':minTime,'maxTime':maxTime, timeLength:maxTime-minTime}}}

import xlrd, os, time, sys, xlwt
import traceback
from collections import OrderedDict
from xlutils.copy import copy


def test(file):
    try:
        dataAll = []
        nameList = []
        dateList = []
        result = {}
        data = xlrd.open_workbook(file)
        table = data.sheet_by_name(u'Sheet1')  # 通过名称获取
        nrows = table.nrows

        # 将数据整理到对应列表中
        for i in range(nrows):
            if i > 0:
                dataAll.append(table.row_values(i))
                nameList.append(dataAll[i-1][1])
                dateList.append(xlrd.xldate.xldate_as_datetime(dataAll[i - 1][4], 0))

        nameSet = set(nameList)
        dateSet = set(dateList)

        for name in nameSet:
            result[name] = {}
            resultDateTemp = {}
            for date in dateSet:
                resultDateTemp[date] = {}
                resultTimeTemp = {}
                timeTempList = []
                for dataList in dataAll:
                    temp = xlrd.xldate.xldate_as_datetime(dataList[4], 0)
                    if dataList[1] == name and temp == date and dataList[5]:
                        # dataAll.remove(dataList)
                        if dataList[5] != 'NULL':
                            timeTempList.append(xlrd.xldate.xldate_as_datetime(dataList[5], 0))


                if timeTempList:
                    # 找出最大最小值
                    maxTime = max(timeTempList)
                    minTime = min(timeTempList)
                    timeLength = maxTime - minTime
                    resultTimeTemp['maxTime'] = maxTime
                    resultTimeTemp['minTime'] = minTime
                    resultTimeTemp['timeLength'] = timeLength
                    resultDateTemp[date] = resultTimeTemp

            result[name] = resultDateTemp
            pass

        style = xlwt.easyxf(num_format_str='Y/m/d')
        style1 = xlwt.easyxf(num_format_str='H:M:S')

        ww = xlwt.Workbook()
        ww.add_sheet('Sheet1')
        ww.save('out.xls')
        rexcel = xlrd.open_workbook('out.xls')
        rows = rexcel.sheets()[0].nrows
        excel = copy(rexcel)
        table = excel.get_sheet(0)
        row = rows
        table.write(row, 0, u'姓名')
        table.write(row, 1, u'日期')
        table.write(row, 2, u'上班时间')
        table.write(row, 3, u'下班时间')
        table.write(row, 4, u'时长')
        excel.save('out.xls')

        ww_temp = []
        for key, value in result.items():
            print key , "===="
            v = sorted(value.keys())
            for item in v:
                print item,
                temp = []
                for key2, value2 in value[item].items():
                    print key2, ":", value2,
                    temp.append(value2)
                if len(temp):
                    w_temp = [key, item, temp[0], temp[2], temp[1]]
                    ww_temp.append(w_temp)
            print

        rexcel = xlrd.open_workbook('out.xls')
        excel = copy(rexcel)
        table = excel.get_sheet(0)
        rows = rexcel.sheets()[0].nrows
        row = rows
        for w_temp in ww_temp:
            table.write(row, 0, w_temp[0])
            table.write(row, 1, str(w_temp[1]).split()[0], style)
            table.write(row, 2, str(w_temp[2]).split()[1], style1)
            table.write(row, 3, str(w_temp[3]).split()[1], style1)
            table.write(row, 4, str(w_temp[4]))
            row = row+1


        excel.save('out.xls')


    except :
        print traceback.format_exc()


if __name__ == '__main__':
    start = time.time()
    test(u'互联网产品部考勤--8、9.xlsx')

    # test(u'互联网产品部考勤--8、9 - 副本.xlsx')
    end = time.time()
    print end-start


