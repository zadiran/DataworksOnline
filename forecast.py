from main import db
from models import Dataset
import datautil as du
from datetime import datetime
from dateutil import parser
from scipy import stats
import numpy as np

def forecast(datasetId, columnNumber, horizon, count, forecast_model, outlier_detector):
    dataset = Dataset.query.get(datasetId)
    if dataset is not None:
        data = du.get_parsed_file(dataset.data, dataset.separator)['data']

        dataRow = list(map(lambda x: float(x[columnNumber]), data))
        dataRowBig = list(dataRow)
        if count == 0: 
            count = int(len(dataRow) * 0.75) - 1
        max_length = len(dataRow)

        dataRow = dataRow[:count]

        forecast = []
        if forecast_model == "Naive":
            forecast = dataRow[-horizon : ]
        elif forecast_model == "Average":
            lag = 4
            for x in range(0, horizon):
                if (x >= lag):
                    forecast.append(np.mean(forecast[-lag:]))
                else:
                    forecast.append(np.mean(forecast + dataRow[-lag + x:]))
        # for x in range(0, len(forecast)):
        #     forecast[x] = forecast[x] + 3 * x 
        
        timestamps = list(map(lambda x: parser.parse(x[0]), data))
        timestep =  timestamps[1] - timestamps[0]

        last_real_timestamp = timestamps[-1]
        for x in range (0, horizon):
            last_real_timestamp = last_real_timestamp + timestep
            timestamps.append(last_real_timestamp)

        ciLower = []
        ciUpper = []
        ciData = list(dataRow)
        for x in range(0, len(forecast)):
            ciData.append(forecast[x])
            
            mean, sigma = np.mean(ciData), np.std(ciData)
            interval = stats.norm.interval(0.95, loc=forecast[x], scale=sigma)
            ciLower.append(interval[0] / (1.004 ** x))
            ciUpper.append(interval[1] * (1.004 ** x))

        allData = dataRow + forecast
        allMean, allSigma = np.mean(allData), np.std(allData)

        constraint = 3 * allSigma
        if outlier_detector == "5sigma":
            constraint = 5 * allSigma

        outlier = list(map(lambda x: x if abs(x - allMean) > constraint else None, allData))
            

        return {
            'timestamp': timestamps,
            'horizon': horizon,
            'data': dataRow, 
            'forecast': forecast if horizon > 0 else [],
            'confidence_interval_upper': ciUpper,
            'confidence_interval_lower': ciLower,
            'outlier': outlier,
            'data_count': count + 1,
            'stop_condition': max_length <= count ,
            'all_data' :dataRowBig
        }
    else:
        return { 'error': 'Dataset not found.'}