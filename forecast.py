from datetime import datetime
from dateutil import parser
from scipy import stats
import numpy as np
from analytics.forecasting.naive_forecast_model import naive_forecast_model
from analytics.forecasting.average_forecast_model import average_forecast_model
from analytics.outliers_detection.three_sigma_outlier_detector import three_sigma_outlier_detector
from analytics.outliers_detection.five_sigma_outlier_detector import five_sigma_outlier_detector

def get_forecast_model_list():
    models = [
        naive_forecast_model(),
        average_forecast_model()
    ]

    return list(map(lambda x: x.name, models))

def get_outlier_detectors_list():
    detectors = [
        three_sigma_outlier_detector(),
        five_sigma_outlier_detector()
    ]

    return list(map(lambda x: x.name, detectors))

def produce_forecast(data, **kwargs):

    column_number = kwargs['column_number']
    horizon = kwargs['horizon']
    count = kwargs['count']
    forecast_model = kwargs['forecast_model']
    outlier_detector = kwargs['outlier_detector']

    dataRow = list(map(lambda x: float(x[column_number]), data['data']))
    
    dataRowBig = list(dataRow)
    if count == 0: 
        count = int(len(dataRow) * 0.75) - 1
    max_length = len(dataRow)

    dataRow = dataRow[:count]

    forecast = []
    if forecast_model == naive_forecast_model().name:
        forecast = naive_forecast_model().forecast(
            data['data'], 
            horizon = horizon, 
            column_index = column_number,
            count = count
        )
    elif forecast_model == average_forecast_model().name:
        forecast = average_forecast_model().forecast(
            data['data'],
            horizon = horizon, 
            column_index = column_number,
            lag = 4,
            count = count
        )
    
    timestamps = list(map(lambda x: parser.parse(x[0]), data['data']))
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
    outlier = []
    if outlier_detector == three_sigma_outlier_detector().name:
        outlier = three_sigma_outlier_detector().detect(allData)
    elif outlier_detector == five_sigma_outlier_detector().name:
        outlier = five_sigma_outlier_detector().detect(allData)            

    return {
        'timestamp': timestamps,
        'horizon': horizon,
        'data': dataRow, 
        'forecast': forecast if horizon > 0 else [],
        'confidence_interval_upper': ciUpper,
        'confidence_interval_lower': ciLower,
        'outlier': outlier,
        'data_count': count + 1,
        'stop_condition': max_length <= count,
        'total_count' : len(data['data']) + horizon
    }

