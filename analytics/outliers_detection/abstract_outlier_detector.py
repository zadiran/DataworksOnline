
class abstract_outlier_detector():

    name = 'abstract outlier detector'
    
    def detect(self, data_frame, **kwargs):
        raise NotImplementedError()