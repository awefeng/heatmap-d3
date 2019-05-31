import xlrd
import json
import datetime
import math
# 文件转换为json
def getDataFromCsv(path):
    dataSet = {'data': []}
    workbook = xlrd.open_workbook(path)
    table = workbook.sheets()[0]
    nrows = table.nrows
    for row_num in range(1, nrows):
        row_values = table.row_values(row_num)
        # 转换为时间
        delta = datetime.timedelta(row_values[0])
        today = datetime.datetime.strptime('1899-12-30','%Y-%m-%d')+delta
        date = datetime.datetime.strftime(today,'%Y-%m-%d')
        dateArr = date.split('-')
        # 如果当前已有该年份
        if dateArr[0] in dataSet:
            if dateArr[1] in dataSet[dateArr[0]]:
                dataSet[dateArr[0]][dateArr[1]]['min_temper']['value'].append(int(row_values[1]))
                dataSet[dateArr[0]][dateArr[1]]['max_temper']['value'].append(int(row_values[2]))
            else:
                dataSet[dateArr[0]][dateArr[1]] = {'year': dateArr[0], 'month': dateArr[1], 'max_temper': {'max': '', 'min': '', 'average': '', 'value': []}, 'min_temper': {'max': '', 'min': '', 'average': '', 'value': []}}
        # 如果当前没有该年份
        else:
            dataSet[dateArr[0]] = {}
            dataSet[dateArr[0]][dateArr[1]] = {'year': dateArr[0], 'month': dateArr[1], 'max_temper': {'max': '', 'min': '', 'average': '', 'value': [int(row_values[2])]},'min_temper': {'max': '', 'min': '', 'average': '', 'value': [int(row_values[2])]}}
        
    return dataSet

#求取每个月最大最小值平均数
def calcTempler(dateSet):
    for year in dateSet:
        for month in dateSet[year]:
            #填充每个月的最大温度的最大值 最大温度的最小值 最大温度的平均值
            max_temp_arr = dateSet[year][month]['max_temper']['value']
            dateSet[year][month]['max_temper']['max'] = max(max_temp_arr)
            dateSet[year][month]['max_temper']['min'] = min(max_temp_arr)
            dateSet[year][month]['max_temper']['average'] = int(sum(max_temp_arr)/len(max_temp_arr))
            #填充每个月的最小温度的最大值 最小温度的最小值 最小温度的平均值
            min_temp_arr = dateSet[year][month]['min_temper']['value']
            dateSet[year][month]['min_temper']['max'] = max(min_temp_arr)
            dateSet[year][month]['min_temper']['min'] = min(min_temp_arr)
            dateSet[year][month]['min_temper']['average'] = int(sum(min_temp_arr)/len(min_temp_arr))

    dataSimple = []

    for year in dateSet:
        for month in dateSet[year]:
            dataSimple.append(dateSet[year][month])
    return dataSimple
# 将给的文件转换为json
if __name__ == '__main__':

    dataJson = getDataFromCsv("./temperature_daily.xlsx")
    result = calcTempler(dataJson)
    with open("./temperature.json","w") as f:
        json.dump(result, f)
        print('转换完成')