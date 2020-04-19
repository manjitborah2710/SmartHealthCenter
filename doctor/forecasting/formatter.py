import pandas as pd

class ToForecastFormat():
    def __init__(self,dataFrame=None):
        self.data=dataFrame

    def fit_transform(self,date_format='%d-%m-%Y'):
        demo = self.data
        demo = demo.dropna()
        demo.head()

        diagnosis = []

        for d in demo['Diagnosis']:
            temp = d.split(',')
            diagnosis.append(temp)

        date = [d for d in demo['Date']]
        from collections import defaultdict
        data = defaultdict(list)
        for i, key in enumerate(date):
            for d in diagnosis[i]:
                data[key].append(d.strip())

        unique_diagnosis = set()
        for i in diagnosis:
            for j in i:
                unique_diagnosis.add(j.strip())
        unique_diagnosis = list(unique_diagnosis)
        unique_date = sorted(list(set(date)))

        diag_list = []
        for dia in unique_diagnosis:
            disease_count = []
            for day in unique_date:
                disease_count.append(data[day].count(dia))
            diag_list.append(disease_count)

        diagnosis_data = dict(zip(unique_diagnosis, diag_list))

        from pandas import datetime

        for i, val in enumerate(unique_date):
            unique_date[i] = datetime.strptime(val, date_format)
        date_dict = {
            'Date': unique_date
        }

        data_csv = {**date_dict, **diagnosis_data}

        df = pd.DataFrame(data_csv)

        return df