
class abstract_forecast_model():

    name = 'abstract model'

    def forecast(self, data_frame, **kwargs):
        raise NotImplementedError()
