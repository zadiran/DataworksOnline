from main import db
from models import Dataset
import datautil as du
from datetime import datetime
from dateutil import parser
from scipy import stats
import numpy as np

def forecast(datasetId, columnNumber, horizon):
    dataset = Dataset.query.get(datasetId)
    if dataset is not None:
        data = du.get_parsed_file(dataset.data, dataset.separator)['data']

        dataRow = list(map(lambda x: float(x[columnNumber]), data))

        forecast = dataRow[-horizon : ] 
        
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
            interval = stats.norm.interval(0.95, loc=x, scale=sigma)
            ciLower.append(interval[0])
            ciUpper.append(interval[1])
            

        return {
            'timestamp': timestamps,
            'horizon': horizon,
            'data': dataRow, 
            'forecast': forecast if horizon > 0 else [],
            'confidence_interval_upper': ciUpper,
            'confidence_interval_lower': ciLower
        }
    else:
        return { 'error': 'Dataset not found.'}