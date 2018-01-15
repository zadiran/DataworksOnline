import numpy as np
from .abstract_forecast_model import abstract_forecast_model

class average_forecast_model(abstract_forecast_model):

    name = 'Average'

    def forecast(self, data_frame, **kwargs):
        column_index = kwargs['column_index']
        horizon = kwargs['horizon']
        lag = kwargs['lag']
        count = kwargs['count']

        col_data = list(map(lambda x: float(x[column_index]), data_frame))
        col_data = col_data[:count] # hack to make step by step forecast work
        forecast = []
        for x in range(0, horizon):
                if (x >= lag):
                    forecast.append(np.mean(forecast[-lag:]))
                else:
                    forecast.append(np.mean(forecast + col_data[-lag + x:]))

        return forecast