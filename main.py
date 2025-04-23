import random
import time
from collections import defaultdict
from dataclasses import dataclass
import copy
import logging
from multiprocessing import Process, Queue
import csv

from sko.GA import GA
import pandas as pd

# 全局变量
Rank = {}
Attract = {}
FIRMS = {}  # {Firm_id: Firm对象}
firm_queue = Queue()
# calibrate_process_num = 4

# 情景参数
FirmEYE = 0.5
Eco_rate = 0.08

# 系统参数
T = 15
P = defaultdict(float)
N = defaultdict(int)
Supply = defaultdict(float)
Demand = defaultdict(float)
SProfit = defaultdict(float)
USProfit = defaultdict(float)
N_fine = defaultdict(int)
SProvalue = defaultdict(float)
SWater = defaultdict(float)
SEnergy = defaultdict(float)
SEmi_SO2 = defaultdict(float)
SEmi_NOx = defaultdict(float)
SEmi_VOC = defaultdict(float)
SEmi_COD = defaultdict(float)
SEmi_NH = defaultdict(float)
SEmi_PM = defaultdict(float)
AllProvalue = 0
AllWater = 0
AllEnergy = 0
AllEmi = defaultdict(float)

# 地块参数
PWater = defaultdict(dict)
PEnergy = defaultdict(dict)
PEmi_SO2 = defaultdict(dict)
PEmi_NOx = defaultdict(dict)
PEmi_VOC = defaultdict(dict)
PEmi_COD = defaultdict(dict)
PEmi_NH = defaultdict(dict)
PEmi_PM = defaultdict(dict)


class MyGA(GA):
    def ranking(self):
        self.FitV = self.Y


@dataclass
class Parcel:
    OBJECTID: int
    HJGKDYBM: float
    Parcel_id: int
    Region: str
    City: str
    Category: int
    Sub_category: int
    Longitude: float
    Latitude: float
    IsPark: int
    Uprofit1: float
    Uprofit2: float
    Uprofit3: float
    Uprofit4: float
    Uprofit5: float
    Uprofit6: float
    Uprofit7: float
    Uprofit8: float
    Uprofit9: float
    Uprofit10: float
    Attract1: float
    Attract2: float
    Attract3: float
    Attract4: float
    Attract5: float
    Attract6: float
    Attract7: float
    Attract8: float
    Attract9: float
    Attract10: float
    Num1: float
    Num2: float
    Num3: float
    Num4: float
    Num5: float
    Num6: float
    Num7: float
    Num8: float
    Num9: float
    Num10: float
    Water1: float
    Water2: float
    Water3: float
    Water4: float
    Water5: float
    Water6: float
    Water7: float
    Water8: float
    Water9: float
    Water10: float
    Energy1: float
    Energy2: float
    Energy3: float
    Energy4: float
    Energy5: float
    Energy6: float
    Energy7: float
    Energy8: float
    Energy9: float
    Energy10: float
    Emi_SO2_1: float
    Emi_SO2_2: float
    Emi_SO2_3: float
    Emi_SO2_4: float
    Emi_SO2_5: float
    Emi_SO2_6: float
    Emi_SO2_7: float
    Emi_SO2_8: float
    Emi_SO2_9: float
    Emi_SO2_10: float
    Emi_NOx_1: float
    Emi_NOx_2: float
    Emi_NOx_3: float
    Emi_NOx_4: float
    Emi_NOx_5: float
    Emi_NOx_6: float
    Emi_NOx_7: float
    Emi_NOx_8: float
    Emi_NOx_9: float
    Emi_NOx_10: float
    Emi_PM_1: float
    Emi_PM_2: float
    Emi_PM_3: float
    Emi_PM_4: float
    Emi_PM_5: float
    Emi_PM_6: float
    Emi_PM_7: float
    Emi_PM_8: float
    Emi_PM_9: float
    Emi_PM_10: float
    Emi_VOC_1: float
    Emi_VOC_2: float
    Emi_VOC_3: float
    Emi_VOC_4: float
    Emi_VOC_5: float
    Emi_VOC_6: float
    Emi_VOC_7: float
    Emi_VOC_8: float
    Emi_VOC_9: float
    Emi_VOC_10: float
    Emi_COD_1: float
    Emi_COD_2: float
    Emi_COD_3: float
    Emi_COD_4: float
    Emi_COD_5: float
    Emi_COD_6: float
    Emi_COD_7: float
    Emi_COD_8: float
    Emi_COD_9: float
    Emi_COD_10: float
    Emi_NH_1: float
    Emi_NH_2: float
    Emi_NH_3: float
    Emi_NH_4: float
    Emi_NH_5: float
    Emi_NH_6: float
    Emi_NH_7: float
    Emi_NH_8: float
    Emi_NH_9: float
    Emi_NH_10: float


parcels = {}


@dataclass
class Firm:
    Firm_id: int
    Parcel_id: int
    Sector: str
    Ownership: str
    Longitude: str
    Latitude: str
    IfWP: int
    IfAP: int
    Production: float
    Proparam: float
    Provalue: float
    Total_cost: float
    Profit: float
    Unit_profit: float
    Risk: float
    Permit_SO2: float
    Permit_NOx: float
    Permit_PM: float
    Permit_VOC: float
    Permit_COD: float
    Permit_NH: float
    PG_SO2: float
    PG_NOx: float
    PG_PM: float
    PG_VOC: float
    PG_COD: float
    PG_NH: float
    RR_SO2: float
    RR_NOx: float
    RR_PM: float
    RR_VOC: float
    RR_COD: float
    RR_NH: float
    Gen_SO2: float
    Gen_NOx: float
    Gen_PM: float
    Gen_VOC: float
    Gen_COD: float
    Gen_NH: float
    Emi_SO2: float
    Emi_NOx: float
    Emi_PM: float
    Emi_VOC: float
    Emi_COD: float
    Emi_NH: float
    Excess_SO2: float
    Excess_NOx: float
    Excess_PM: float
    Excess_VOC: float
    Excess_COD: float
    Excess_NH: float
    Wparam: float
    Eparam: float
    Wconsume: float
    Econsume: float
    UnitEmi_SO2: float
    UnitEmi_NOx: float
    UnitEmi_PM: float
    UnitEmi_VOC: float
    UnitEmi_COD: float
    UnitEmi_NH: float
    UnitW: float
    UnitE: float
    EmiRank_SO2: float
    EmiRank_NOx: float
    EmiRank_PM: float
    EmiRank_VOC: float
    EmiRank_COD: float
    EmiRank_NH: float
    WRank: float
    ERank: float
    TRank: float
    Govcheck: float
    Techcost: float
    Techprob: float
    RTechcost: float
    Fine: float
    Beta: float
    Utility: float
    Alpha1: float
    Alpha2: float
    Alpha3: float
    Gamma1: float
    Gamma2: float

    def init(self):
        self.tmp_vars = {}
        self.Govcheck = 0.5
        self.Fine = 0
        self.Beta = self.get_random_float(0.45, 0.55)
        self.Proparam = 1
        self.update_Excesses()
        self.update_Units()
        self.Total_cost = self.get_Total_cost(self.Production)
        self.Profit = self.get_Profit(self.Provalue, self.Total_cost)
        self.Unit_profit = self.Profit / self.Provalue

    @staticmethod
    def get_random_float(a, b):
        return random.uniform(a, b)

    def get_parcel(self) -> Parcel:
        return parcels[self.Parcel_id]

    def update_permits(self):
        coefficient = 0.85
        if self.IfWP == 1:
            self.Permit_COD *= coefficient
            self.Permit_NH *= coefficient
        if self.IfAP == 1:
            self.Permit_SO2 *= coefficient
            self.Permit_NOx *= coefficient
            self.Permit_PM *= coefficient
            self.Permit_VOC *= coefficient

    def update_Excess(self, Emi, Permit):
        return 0 if Emi <= Permit else Emi - Permit

    def update_UnitEmi(self, Emi):
        return Emi / self.Provalue

    def get_Proparam(self, Proparam, Beta, Unit_profit, TRank, a1, a2, a3):
        return Proparam * (1 + Beta * (
                (1 / (1 + a1 ** Unit_profit)) ** a2 - 0.5 ** (
                a3 / TRank)))

    def update_Proparam(self, a1, a2, a3):
        return self.Proparam * (1 + self.Beta * (
                (1 / (1 + a1 ** self.Unit_profit)) ** a2 - 0.5 ** (
                a3 / self.TRank)))

    def update_Demand(self, last_Demand, Eco_rate):
        return last_Demand * (1 + Eco_rate)

    def get_Production(self, Production, Proparam):
        return Production * Proparam

    def get_Provalue(self, Production):
        return Production * P[self.Sector]

    def get_Total_cost(self, Production):
        return Production * random.uniform(0.7, 0.75)

    def get_Profit(self, Provalue, Total_cost):
        return Provalue - Total_cost

    def update_production_mod(self):
        # 生产模块
        self.tmp_vars['last_Production'] = self.Production

        self.Production = self.get_Production(self.Production, self.Proparam)
        self.Provalue = self.get_Provalue(self.Production)
        self.Total_cost = self.get_Total_cost(self.Production)
        self.Profit = self.get_Profit(self.Provalue, self.Total_cost)
        self.Unit_profit = self.Profit / self.Provalue

    def update_Excesses(self):
        if self.IfWP == 1:
            self.Excess_COD = self.update_Excess(self.Emi_COD, self.Permit_COD)
            self.Excess_NH = self.update_Excess(self.Emi_NH, self.Permit_NH)

        if self.IfAP == 1:
            self.Excess_SO2 = self.update_Excess(self.Emi_SO2, self.Permit_SO2)
            self.Excess_NOx = self.update_Excess(self.Emi_NOx, self.Permit_NOx)
            self.Excess_PM = self.update_Excess(self.Emi_PM, self.Permit_PM)
            self.Excess_VOC = self.update_Excess(self.Emi_VOC, self.Permit_VOC)

    def update_Units(self):
        if self.IfWP == 1:
            self.UnitEmi_COD = self.update_UnitEmi(self.Emi_COD)
            self.UnitEmi_NH = self.update_UnitEmi(self.Emi_NH)
        if self.IfAP == 1:
            self.UnitEmi_SO2 = self.update_UnitEmi(self.Emi_SO2)
            self.UnitEmi_NOx = self.update_UnitEmi(self.Emi_NOx)
            self.UnitEmi_PM = self.update_UnitEmi(self.Emi_PM)
            self.UnitEmi_VOC = self.update_UnitEmi(self.Emi_VOC)
        self.UnitW = self.Wconsume / self.Provalue
        self.UnitE = self.Econsume / self.Provalue

    def update_environment_mod(self, t):
        # 环境模块
        if t % 3 == 0:
            self.update_permits()

        if self.IfWP == 1:
            self.Gen_COD = self.Production * self.PG_COD
            self.Gen_NH = self.Production * self.PG_NH

            self.Emi_COD = self.Gen_COD * (1 - self.RR_COD)
            self.Emi_NH = self.Gen_NH * (1 - self.RR_NH)

        if self.IfAP == 1:
            self.Gen_SO2 = self.Production * self.PG_SO2
            self.Gen_NOx = self.Production * self.PG_NOx
            self.Gen_PM = self.Production * self.PG_PM
            self.Gen_VOC = self.Production * self.PG_VOC

            self.Emi_SO2 = self.Gen_SO2 * (1 - self.RR_SO2)
            self.Emi_NOx = self.Gen_NOx * (1 - self.RR_NOx)
            self.Emi_PM = self.Gen_PM * (1 - self.RR_PM)
            self.Emi_VOC = self.Gen_VOC * (1 - self.RR_VOC)

        self.Wconsume = self.Wconsume / self.tmp_vars[
            'last_Production'] * self.Production * self.Wparam
        self.Econsume = self.Econsume / self.tmp_vars[
            'last_Production'] * self.Production * self.Eparam

        self.update_Excesses()
        self.update_Units()

    def update_Rank(self):
        self.EmiRank_NH = self.get_Rank('NH')
        self.EmiRank_COD = self.get_Rank('COD')
        self.EmiRank_PM = self.get_Rank('PM')
        self.EmiRank_SO2 = self.get_Rank('SO2')
        self.EmiRank_NOx = self.get_Rank('NOx')
        self.EmiRank_VOC = self.get_Rank('VOC')
        self.WRank = self.get_Rank('W')
        self.ERank = self.get_Rank('E')
        self.TRank = self.get_Rank('T')

    def get_Rank(self, kind):
        return Rank[kind][self.Firm_id]

    def get_Beta(self, Beta, Fine):
        return Beta + 0.1 * (1 - Beta) if Fine == 0 else Beta * 0.9

    def update_risk_mod(self):
        """调整风险偏好"""
        if random.random() <= self.Govcheck and any(
                [self.Excess_VOC, self.Excess_PM, self.Excess_NH,
                 self.Excess_SO2,
                 self.Excess_NOx, self.Excess_COD]):
            self.Fine = self.get_random_float(0.3, 0.5) * self.Provalue
            self.Govcheck = 0.8
        else:
            self.Fine = 0

        self.Beta = self.get_Beta(self.Beta, self.Fine)

    def update_output_multiplier_mod(self):
        self.Proparam = self.get_Proparam(self.Proparam, self.Beta,
                                          self.Unit_profit, self.TRank,
                                          self.Alpha1,
                                          self.Alpha2, self.Alpha3)

    def get_Techcost(self, Provalue):
        return self.get_random_float(0.3, 0.5) * Provalue

    def get_Techprob(self, y1, y2, Beta, Techcost, TRank):
        return 1 - 0.5 * Beta * (
                1 / (1 + y1 ** Techcost)) ** y2 - 0.1 ** TRank

    def get_RTechcost(self, Techprob, Techcost):
        return Techprob * Techcost

    def update_env_tech_mod1(self):
        self.Techprob = 1 - 0.5 * self.Beta * (
                1 / (
                1 + self.Gamma1 ** self.Techcost)) ** self.Gamma2 - 0.1 ** self.TRank

    def get_PG(self, Techprob, target_PG, my_PG):
        return min(my_PG, max(0.000001,
                              Techprob * target_PG + (1 - Techprob) * my_PG))

    def get_RR(self, Techprob, target_RR, my_RR):
        return min(0.999, self.get_PG(Techprob, target_RR, my_RR))

    def update_env_tech_mod2(self):
        global Rank

        eye_firm_num = FirmEYE * N[self.Sector]
        left = self.TRank - eye_firm_num // 2
        if left < 0:
            left = 0
        pos = left + 10
        if pos > len(Rank['T_reverse'][self.Sector]):
            pos = len(Rank['T_reverse'][self.Sector])

        target_firm = FIRMS[Rank['T_reverse'][self.Sector][int(pos)]]
        self.PG_COD = self.get_PG(self.Techprob, target_firm.PG_COD,
                                  self.PG_COD)
        self.PG_VOC = self.get_PG(self.Techprob, target_firm.PG_VOC,
                                  self.PG_VOC)
        self.PG_SO2 = self.get_PG(self.Techprob, target_firm.PG_SO2,
                                  self.PG_SO2)
        self.PG_NOx = self.get_PG(self.Techprob, target_firm.PG_NOx,
                                  self.PG_NOx)
        self.PG_NH = self.get_PG(self.Techprob, target_firm.PG_NH, self.PG_NH)
        self.PG_PM = self.get_PG(self.Techprob, target_firm.PG_PM, self.PG_PM)

        self.RR_COD = self.get_RR(self.Techprob, target_firm.RR_COD,
                                  self.RR_COD)
        self.RR_VOC = self.get_RR(self.Techprob, target_firm.RR_VOC,
                                  self.RR_VOC)
        self.RR_SO2 = self.get_RR(self.Techprob, target_firm.RR_SO2,
                                  self.RR_SO2)
        self.RR_NOx = self.get_RR(self.Techprob, target_firm.RR_NOx,
                                  self.RR_NOx)
        self.RR_NH = self.get_RR(self.Techprob, target_firm.RR_NH, self.RR_NH)
        self.RR_PM = self.get_RR(self.Techprob, target_firm.RR_PM, self.RR_PM)

        self.Wparam = self.Techprob * target_firm.Wparam + (
                1 - self.Techprob) * self.Wparam
        self.Eparam = self.Techprob * target_firm.Eparam + (
                1 - self.Techprob) * self.Eparam

        self.RTechcost = self.get_RTechcost(self.Techprob, self.Techcost)

    def update_site_select_mod(self):
        my_parcel = self.get_parcel()
        if my_parcel.Category in {2, 3} and random.random() < 0.7:
            return

        same_city_parcels = []
        other_parcels = []
        for p in parcels.values():
            if p.Category == 1:
                continue

            if p.City == my_parcel.City:
                same_city_parcels.append(p)
            else:
                other_parcels.append(p)

        same_sub_category_parcels = []
        other_parcels.clear()
        prior_parcels = same_city_parcels or other_parcels
        for p in prior_parcels:
            if p.Sub_category == my_parcel.Sub_category:
                same_sub_category_parcels.append(p)
            else:
                other_parcels.append(p)

        prior_parcels = same_sub_category_parcels or other_parcels
        parcel_attracts = {Attract[p.Parcel_id].get(self.Sector, -9999): p
                           for p in prior_parcels}
        target_parcel = max(parcel_attracts.items())[1]
        self.Parcel_id = target_parcel.Parcel_id
        self.Longitude = target_parcel.Longitude
        self.Latitude = target_parcel.Latitude

    def update(self, t):
        self.update_risk_mod()
        self.update_output_multiplier_mod()
        self.update_env_tech_mod1()
        self.update_env_tech_mod2()
        self.update_site_select_mod()
        self.update_production_mod()
        self.update_environment_mod(t)

    def get_Risk(self, RTechcost, Fine):
        return 0.5 * RTechcost + 0.5 * Fine

    def get_Utility(self, Beta, Profit, Risk):
        return Beta * Profit - (1 - Beta) * Risk


firms: list[Firm] = []


class Utils:
    @staticmethod
    def get_random_float(a, b):
        return random.uniform(a, b)

    def update_Supply(self, firms):
        for firm in firms:
            Supply[firm.Sector] += firm.Production

    def update_Demand(self):
        for k in Demand:
            Demand[k] = Demand[k] * (1 + Eco_rate)

    @staticmethod
    def get_Rank(firms):
        def get_rank(Emis, emi_index):
            return {elem[0]: (0 if elem[emi_index] == 0 else i) for i, elem in
                    enumerate(sorted(Emis, key=lambda x: x[emi_index]), 1)}

        Emis = defaultdict(list)
        for firm in firms:
            Emis[firm.Sector].append([firm.Firm_id,
                                      firm.UnitEmi_SO2, firm.UnitEmi_NOx,
                                      firm.UnitEmi_PM, firm.UnitEmi_VOC,
                                      firm.UnitEmi_COD, firm.UnitEmi_NH,
                                      firm.UnitW, firm.UnitE])

        result = defaultdict(dict)
        for value in Emis.values():
            result['SO2'].update(get_rank(value, 1))
            result['NOx'].update(get_rank(value, 2))
            result['VOC'].update(get_rank(value, 4))
            result['COD'].update(get_rank(value, 5))
            result['PM'].update(get_rank(value, 3))
            result['NH'].update(get_rank(value, 6))
            result['W'].update(get_rank(value, 7))
            result['E'].update(get_rank(value, 8))

        return result

    def get_TRank(self, firms):
        Tresult = defaultdict(list)
        for firm in firms:
            T = (firm.EmiRank_SO2 + firm.EmiRank_NOx + firm.EmiRank_PM
                 + firm.EmiRank_VOC + firm.EmiRank_COD + firm.EmiRank_NH) / 6 \
                + firm.WRank + firm.ERank
            Tresult[firm.Sector].append([firm.Firm_id, T])

        result = {}
        result_reverse = {}
        for sector, ls in Tresult.items():
            sector_tranks = {firm_info[0]: i for i, firm_info in
                             enumerate(sorted(ls, key=lambda x: x[1]), 1)}
            result.update(sector_tranks)
            result_reverse[sector] = {v: k for k, v in sector_tranks.items()}
        return result, result_reverse

    def update_Rank(self, firms):
        global Rank

        Rank.update(self.get_Rank(firms))
        TRank, T_reverse = self.get_TRank(firms)
        Rank.update({'T': TRank, 'T_reverse': T_reverse})

    def update_firm_rank(self, firms):
        for firm in firms:
            firm.update_Rank()

    def update_P(self):
        for k in N:
            if Demand[k] <= Supply[k]:
                P[k] = self.get_random_float(0.7, 0.95)
            else:
                P[k] = self.get_random_float(1.05, 1.3)

    def get_Uprofit(self, firms):
        Uprofit = defaultdict(dict)
        for firm in firms:
            if firm.Sector not in Uprofit[firm.Parcel_id]:
                Uprofit[firm.Parcel_id][firm.Sector] = []
            Uprofit[firm.Parcel_id][firm.Sector].append(firm.Profit)

        for parcel_id, v in Uprofit.items():
            for sector, ls in v.items():
                v[sector] = sum(ls) / len(ls)
        return Uprofit

    def update_USProfit(self):
        for sector, sprofit in SProfit.items():
            USProfit[sector] = sprofit / N[sector]

    def update_Attract(self, firms):
        global Attract

        Uprofit = self.get_Uprofit(firms)
        Attract = copy.deepcopy(Uprofit)
        for parcel_id, v in Uprofit.items():
            for sector, uprofit in v.items():
                Attract[parcel_id][sector] = uprofit / USProfit[sector]

    def update_SProfit(self, firms):
        for firm in firms:
            SProfit[firm.Sector] += firm.Profit

    def _update_parcel_params(self, data, firm, add_data):
        if firm.Sector not in data[firm.Parcel_id]:
            data[firm.Parcel_id][firm.Sector] = 0
        data[firm.Parcel_id][firm.Sector] += add_data

    def update_parcel_params(self, firm: Firm):
        self._update_parcel_params(PWater, firm, firm.Wconsume)
        self._update_parcel_params(PEnergy, firm, firm.Econsume)
        self._update_parcel_params(PEmi_SO2, firm, firm.Emi_SO2)
        self._update_parcel_params(PEmi_NOx, firm, firm.Emi_NOx)
        self._update_parcel_params(PEmi_VOC, firm, firm.Emi_VOC)
        self._update_parcel_params(PEmi_COD, firm, firm.Emi_COD)
        self._update_parcel_params(PEmi_NH, firm, firm.Emi_NH)
        self._update_parcel_params(PEmi_PM, firm, firm.Emi_PM)

    def clear_params(self):
        for i in [P, Supply, Demand, SProfit, USProfit, N_fine, SProvalue,
                  SWater, SEnergy, SEmi_SO2, SEmi_NOx, SEmi_VOC, SEmi_COD,
                  SEmi_NH, SEmi_PM, AllProvalue, AllWater, AllEnergy, AllEmi,
                  PWater, PEnergy, PEmi_SO2, PEmi_NOx, PEmi_VOC, PEmi_COD,
                  PEmi_NH, PEmi_PM, ]:
            if isinstance(i, dict):
                i.clear()


def calibrate(firm, a1, a2, a3, y1, y2):
    """参数率定"""
    Beta = firm.get_Beta(firm.Beta, firm.Fine)
    Proparam = firm.get_Proparam(firm.Proparam, Beta, firm.Unit_profit,
                                 firm.TRank, a1, a2, a3)
    Techprob = firm.get_Techprob(y1, y2, Beta, firm.Techcost,
                                 firm.TRank)
    if Proparam < 0.7 or Proparam > 1.5 or Techprob <= 0 or Techprob >= 1:
        return -9999999

    RTechcost = firm.get_RTechcost(Techprob, firm.Techcost)

    Production = firm.get_Production(firm.Production, Proparam)
    Provalue = firm.get_Provalue(Production)
    Total_cost = firm.get_Total_cost(Production)
    Profit = firm.get_Profit(Provalue, Total_cost)

    Risk = firm.get_Risk(RTechcost, firm.Fine)
    Utility = firm.get_Utility(Beta, Profit, Risk)
    return Utility


def main(parcel_excel, firm_excel):
    global firms, parcels, Supply, Demand, P, AllProvalue, AllWater, AllEnergy, \
        AllEmi

    def calibrate_inner(p):
        return calibrate(firm, *[float(i) for i in p])

    system_params_file = open('system_params.csv', 'w', newline='')
    system_params_writer = csv.writer(system_params_file)
    system_params_writer.writerow(
        ['t', 'Sector', 'SWater', 'SEnergy', 'SEmi_SO2', 'SEmi_NOx',
         'SEmi_VOC', 'SEmi_COD', 'SEmi_NH', 'SEmi_PM', 'AllProvalue',
         'AllWater', 'AllEnergy', 'AllEmi_SO2', 'AllEmi_NOx', 'AllEmi_VOC',
         'AllEmi_COD', 'AllEmi_NH', 'AllEmi_PM']
    )
    parcel_params_file = open('parcel_params.csv', 'w', newline='')
    parcel_params_writer = csv.writer(parcel_params_file)
    parcel_params_writer.writerow(
        ['t', 'Parcel_id', 'Sector', 'PWater', 'PEnergy', 'PEmi_SO2',
         'PEmi_NOx', 'PEmi_VOC', 'PEmi_COD', 'PEmi_NH', 'PEmi_PM']
    )
    firm_params_file = open('firm_params.csv', 'w', newline='')
    firm_params_writer = csv.writer(firm_params_file)
    firm_params_writer.writerow(
        ['t', 'Firm_id', 'Parcel_id', 'Production', 'Provalue', 'Profit',
         'Risk', 'PG_SO2', 'PG_NOx', 'PG_VOC', 'PG_COD', 'PG_NH', 'PG_PM',
         'RR_SO2', 'RR_NOx', 'RR_VOC', 'RR_COD', 'RR_NH', 'RR_PM', 'Gen_SO2',
         'Gen_NOx', 'Gen_VOC', 'Gen_COD', 'Gen_NH', 'Gen_PM', 'Emi_SO2',
         'Emi_NOx', 'Emi_VOC', 'Emi_COD', 'Emi_NH', 'Emi_PM', 'Wconsume',
         'Econsume', 'Beta']
    )

    parcel_infos = pd.read_excel(parcel_excel)
    for row in parcel_infos.iterrows():
        args = [arg if str(arg) != 'nan' else 0 for arg in row[1]]
        parcel = Parcel(*args)
        parcels[parcel.Parcel_id] = parcel

    firm_infos = pd.read_excel(firm_excel)
    for row in firm_infos.iterrows():
        # if len(firms) > 1000:
        #     break
        args = [arg if str(arg) != 'nan' else 0 for arg in row[1]]
        firm = Firm(*args)
        firm.init()
        firms.append(firm)

        N[firm.Sector] += 1
        P[firm.Sector] = 1
        FIRMS[firm.Firm_id] = firm

    # 初始化系统参数
    utils = Utils()
    utils.update_Rank(firms)
    utils.update_firm_rank(firms)
    P = {sector: 1 for sector in N}
    utils.update_Supply(firms)
    Demand = copy.deepcopy(Supply)
    utils.update_SProfit(firms)
    utils.update_USProfit()
    utils.update_Attract(firms)

    # 开始迭代
    for t in range(1, T + 1):
        logging.info(f'开始第{t}期迭代')

        time1 = time.time()
        # 更新企业属性
        for firm in firms:
            # Techcost由随机数生成，先确定下来，否则率定中每次都更新的话将导致函数不稳定
            firm.Techcost = firm.get_Techcost(firm.Provalue)

            # 率定
            ga = MyGA(func=calibrate_inner, n_dim=5, lb=[0, 0, 0, 0, 0],
                      ub=[1, 1, 1, 1, 1], max_iter=1000)
            result = ga.run()
            a1, a2, a3, y1, y2 = result[0]
            firm.Utility = result[1]
            firm.Alpha1 = a1
            firm.Alpha2 = a2
            firm.Alpha3 = a3
            firm.Gamma1 = y1
            firm.Gamma2 = y2

            logging.info(f'[第{t}期]更新企业{firm.Firm_id}属性')
            firm.update(t)

        logging.info(f'更新耗时：{time.time() - time1}s')

        logging.info('清理系统参数')
        utils.clear_params()

        logging.info('更新系统参数')
        utils.update_Rank(firms)
        utils.update_firm_rank(firms)
        utils.update_Supply(firms)
        utils.update_P()
        utils.update_Demand()
        utils.update_SProfit(firms)
        utils.update_USProfit()
        utils.update_Attract(firms)

        for firm in firms:
            if firm.Fine > 0:
                N_fine[firm.Sector] += 1
            SProvalue[firm.Sector] += firm.Provalue
            SWater[firm.Sector] += firm.Wconsume
            SEnergy[firm.Sector] += firm.Econsume
            SEmi_SO2[firm.Sector] += firm.Emi_SO2
            SEmi_NOx[firm.Sector] += firm.Emi_NOx
            SEmi_VOC[firm.Sector] += firm.Emi_VOC
            SEmi_COD[firm.Sector] += firm.Emi_COD
            SEmi_NH[firm.Sector] += firm.Emi_NH
            SEmi_PM[firm.Sector] += firm.Emi_PM
            AllProvalue += firm.Provalue
            AllWater += firm.Wconsume
            AllEnergy += firm.Econsume
            AllEmi['SO2'] += firm.Emi_SO2
            AllEmi['NOx'] += firm.Emi_NOx
            AllEmi['VOC'] += firm.Emi_VOC
            AllEmi['COD'] += firm.Emi_COD
            AllEmi['NH'] += firm.Emi_NH
            AllEmi['PM'] += firm.Emi_PM
            utils.update_parcel_params(firm)

        # 输出系统参数
        for sector in N:
            row = [param[sector] for param in
                   [SWater, SEnergy, SEmi_SO2, SEmi_NOx, SEmi_VOC, SEmi_COD,
                    SEmi_NH, SEmi_PM]]
            system_params_writer.writerow([t, sector] + row)
        system_params_writer.writerow(
            [t] + [None] * 9 + [AllProvalue, AllWater, AllEnergy,
                                AllEmi['SO2'], AllEmi['NOx'], AllEmi['VOC'],
                                AllEmi['COD'], AllEmi['NH'], AllEmi['PM']])
        system_params_file.flush()

        # 输出地块参数
        for parcel_id in parcels:
            for sector in N:
                row = [param[parcel_id].get(sector, 0) for param in
                       (PWater, PEnergy, PEmi_SO2, PEmi_NOx, PEmi_VOC,
                        PEmi_COD, PEmi_NH, PEmi_PM)]
                parcel_params_writer.writerow([t, parcel_id, sector] + row)
        parcel_params_file.flush()

        # 输出企业参数
        for f in firms:
            firm_params_writer.writerow(
                [t, f.Firm_id, f.Parcel_id, f.Production, f.Provalue, f.Profit,
                 f.Risk, f.PG_SO2, f.PG_NOx, f.PG_PM, f.PG_VOC, f.PG_COD,
                 f.PG_NH, f.RR_SO2, f.RR_NOx, f.RR_PM, f.RR_VOC, f.RR_COD,
                 f.RR_NH, f.Gen_SO2, f.Gen_NOx, f.Gen_PM, f.Gen_VOC, f.Gen_COD,
                 f.Gen_NH, f.Emi_SO2, f.Emi_NOx, f.Emi_PM, f.Emi_VOC,
                 f.Emi_COD, f.Emi_NH, f.Wconsume, f.Econsume, f.Beta])
        firm_params_file.flush()


if __name__ == '__main__':
    main('/Users/weizzy/Downloads/附件/地块参数表/地块参数表.xlsx',
         '/Users/weizzy/Downloads/附件/企业参数表/2017(t=0).xlsx')
