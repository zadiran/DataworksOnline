from .abstract_forecast_model import abstract_forecast_model

class naive_forecast_model(abstract_forecast_model):

    name = 'Naive'

    def forecast(self, data_frame, **kwargs):
        column_index = kwargs['column_index']
        horizon = kwargs['horizon']
        count = kwargs['count']

        col_data = list(map(lambda x: float(x[column_index]), data_frame))
        col_data = col_data[:count] # hack to make step by step forecast work

        return col_data[ -horizon : ]