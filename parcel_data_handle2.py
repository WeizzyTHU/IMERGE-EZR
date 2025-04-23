"""处理导出后的parcel数据, 分年份输出到不同的文件"""
import pandas as pd
from collections import defaultdict
import csv

path = '/Users/weizzy/Desktop/Kaijing模型/模型输出/所有企业-1.028/parcel_params.csv'
output_path = '/Users/weizzy/Desktop/Kaijing模型/模型输出/所有企业-1.028/Parcel分年份/'
data = pd.read_csv(path)

"""获取所有时间和地块id"""
Year = data['t'].unique()
Parcel = data['OBJECTID'].unique()


def get_Sum(rows, col_string):
    Sum = defaultdict(dict)
    for index, row in rows.iterrows():
        if row['OBJECTID'] not in Sum[row['t']]:
            Sum[row['t']][row['OBJECTID']] = []
        Sum[row['t']][row['OBJECTID']].append(row[col_string])

    for t, v1 in Sum.items():
        for Parcel_id, v2 in v1.items():
            v1[Parcel_id] = sum(v2)
    return Sum


SUM_Water = get_Sum(data, 'PWater')
SUM_Energy = get_Sum(data, 'PEnergy')
SUM_SO2 = get_Sum(data, 'PEmi_SO2')
SUM_NOx = get_Sum(data, 'PEmi_NOx')
SUM_PM = get_Sum(data, 'PEmi_PM')
SUM_VOC = get_Sum(data, 'PEmi_VOC')
SUM_COD = get_Sum(data, 'PEmi_COD')
SUM_NH = get_Sum(data, 'PEmi_NH')

Out_dict = defaultdict(dict)

for i in Year:
    for j in Parcel:
        if j not in Out_dict[i]:
            Out_dict[i][j] = []
        Out_dict[i][j].append(SUM_Water[i][j])
        Out_dict[i][j].append(SUM_Energy[i][j])
        Out_dict[i][j].append(SUM_SO2[i][j])
        Out_dict[i][j].append(SUM_NOx[i][j])
        Out_dict[i][j].append(SUM_PM[i][j])
        Out_dict[i][j].append(SUM_VOC[i][j])
        Out_dict[i][j].append(SUM_COD[i][j])
        Out_dict[i][j].append(SUM_NH[i][j])
    #     parcel_params_writer.writerow([i, j] + Out_dict[i][j])
    # parcel_params_file.flush()

for i in Year:
    parcel_params_file = open(output_path + '第' + str(i) + '年_parcel_params_加总.csv', 'w', newline='')
    parcel_params_writer = csv.writer(parcel_params_file)
    parcel_params_writer.writerow(
        ['t', 'OBJECTID', 'SUM_Water', 'SUM_Energy', 'SUM_SO2', 'SUM_NOx',
         'SUM_PM', 'SUM_VOC', 'SUM_COD', 'SUM_NH', 'Standard_W', 'Standard_E',
         'Standard_PSO2', 'Standard_PCOD', 'PI_SO2', 'PI_COD', 'CI_SO2', 'CI_COD']
    )
    list_W = []
    list_E = []
    list_PSO2 = []
    list_PCOD = []
    for j in Parcel:
        list_W.append(Out_dict[i][j][0])
        list_E.append(Out_dict[i][j][1])
        list_PSO2.append(Out_dict[i][j][2])
        list_PCOD.append(Out_dict[i][j][6])
    Max_W = max(list_W)
    Max_E = max(list_E)
    Max_PSO2 = max(list_PSO2)
    Max_PCOD = max(list_PCOD)
    Min_W = min(list_W)
    Min_E = min(list_E)
    Min_PSO2 = min(list_PSO2)
    Min_PCOD = min(list_PCOD)

    for j in Parcel:
        Standard_W = (Out_dict[i][j][0] - Min_W) / (Max_W - Min_W)
        Standard_E = (Out_dict[i][j][1] - Min_E) / (Max_E - Min_E)
        Standard_PSO2 = (Out_dict[i][j][2] - Min_PSO2) / (Max_PSO2 - Min_PSO2)
        Standard_PCOD = (Out_dict[i][j][6] - Min_PCOD) / (Max_PCOD - Min_PCOD)
        """添加强度指标PI和耦合度指标CI"""
        K_SO2 = (Standard_W ** 2 + Standard_E ** 2 + Standard_PSO2 ** 2) ** 0.5
        K_COD = (Standard_W ** 2 + Standard_E ** 2 + Standard_PCOD ** 2) ** 0.5
        PI_SO2 = Standard_PSO2 / K_SO2 if K_SO2 != 0 else Standard_PSO2 / 1
        PI_COD = Standard_PCOD / K_COD if K_SO2 != 0 else Standard_PCOD / 1

        A_SO2 = (Standard_W * Standard_E * Standard_PSO2) ** (1 / 3)
        B_SO2 = (Standard_W + Standard_E + Standard_PSO2) / 3
        CI_SO2 = A_SO2 / B_SO2 if B_SO2 != 0 else A_SO2 / 0.001
        A_COD = (Standard_W * Standard_E * Standard_PCOD) ** (1 / 3)
        B_COD = Standard_W + Standard_E + Standard_PCOD / 3
        CI_COD = A_COD / B_COD if B_COD != 0 else A_COD / 0.001

        """追加写入PI和CI"""
        Out_dict[i][j].append(Standard_W)
        Out_dict[i][j].append(Standard_E)
        Out_dict[i][j].append(Standard_PSO2)
        Out_dict[i][j].append(Standard_PCOD)
        Out_dict[i][j].append(PI_SO2)
        Out_dict[i][j].append(PI_COD)
        Out_dict[i][j].append(CI_SO2)
        Out_dict[i][j].append(CI_COD)
        parcel_params_writer.writerow([i, j] + Out_dict[i][j])
    parcel_params_file.flush()
