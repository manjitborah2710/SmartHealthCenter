import pandas as pd
from pandas import datetime

class DataPreparationHelper():
    def __init__(self,date_format='%Y-%m-%d'):
        self.date_format=date_format
    def parser(self,x):
        return datetime.strptime(x,self.date_format)
    def prepare(self,dataset=None,group_by='W'):
        df = pd.read_csv(dataset, index_col=0, date_parser=self.parser, parse_dates=[0])
        df_weekly = df.resample(group_by).sum()
        last_week = df_weekly.iloc[-1, :]
        sorted_data = last_week.sort_values(ascending=False)
        significant = 5
        total = sorted_data.sum()
        week_percentages = {}
        for i in range(significant):
            value = float(round((sorted_data[i] / total) * 100, 1))
            ind = sorted_data.index[i]
            week_percentages[ind] = value
        others = float(round(sorted_data[significant:].sum() * 100 / total, 1))
        week_percentages["others"] = others
        week_percentages["total"] = int(sorted_data.sum())
        return week_percentages