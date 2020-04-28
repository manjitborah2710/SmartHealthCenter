import pandas as pd
from pandas import datetime
import pickle
from datetime import timedelta
from matplotlib import pyplot as plt


class DataPreparationHelper:
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

def getPlottableData(path:str,steps:int):
    f = open(path, "rb")
    pkl = pickle.load(f)
    f.close()
    items = pkl.getItems()
    label = items[0]
    train = items[1]
    model = items[2]
    preds = model.forecast(steps)
    preds = preds[0]
    last_date = train.index[-1].date()
    date_range = last_date
    pred_dates = []
    for i in range(len(preds)):
        date_range += timedelta(weeks=1)
        pred_dates.append(date_range)
    pred_dates=pd.DatetimeIndex(pred_dates)
    pred_df = pd.DataFrame(data=preds, index=pred_dates, columns=[list(train.columns)[-1]])
    total_df_index = pd.DatetimeIndex(train.index.append(pred_df.index))
    total_values = train[list(train.columns)[-1]].append(pred_df[list(pred_df.columns)[-1]]).values
    total_df = pd.DataFrame(data=total_values, index=total_df_index)

    data={
        'train_data':train,
        'predicted_data':pred_df,
        'total_data':total_df,
        'disease_name':label,
        'last_train_date':last_date,
        'first_predicted_date':last_date+timedelta(weeks=1)
    }
    return data
