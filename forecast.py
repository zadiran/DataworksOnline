from main import db
from models import Dataset
import datautil as du
from datetime import datetime
from dateutil import parser
from scipy import stats
import numpy as np

def forecast(datasetId, columnNumber, horizon, count):
    dataset = Dataset.query.get(datasetId)
    if dataset is not None:
        data = du.get_parsed_file(dataset.data, dataset.separator)['data']

        dataRow = list(map(lambda x: float(x[columnNumber]), data))
        dataRowBig = list(dataRow)
        if count == 0: 
            count = int(len(dataRow) * 0.75) - 1
        max_length = len(dataRow)

        dataRow = dataRow[:count]

        forecast = dataRow[-horizon : ]
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
        for x in forecast:
            ciData.append(x)
            
            mean, sigma = np.mean(ciData), np.std(ciData)
            interval = stats.norm.interval(0.997, loc=x, scale=sigma)
            ciLower.append(interval[0])
            ciUpper.append(interval[1])

        allData = dataRow + forecast
        allMean, allSigma = np.mean(allData), np.std(allData)
        outlier = list(map(lambda x: x if abs(x - allMean) > 2 * allSigma else None, allData))
            

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