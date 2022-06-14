from pm4py.objects.conversion.log import converter as log_converter


class Convert_Log:
    def __init__(self, event_log):
        self.event_log = event_log

    def convert_from_xes_to_csv(self):
        dataframe = log_converter.apply(self.event_log, variant=log_converter.Variants.TO_DATA_FRAME)
        return dataframe
