import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
import csv


class organization_role_encoding:
    def __init__(self, log_csv, counter):
        self.log_csv = log_csv
        self.counter = counter
        self.trace_length = int(len(self.log_csv) / len(self.log_csv['case:concept:name'].unique()))

    def write_variant(self):
        attributes = []
        attribute_header = []

        log_csv = dataframe_utils.convert_timestamp_columns_in_df(self.log_csv)
        log_csv = log_csv.sort_values('time:timestamp')

        parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:concept:name'}
        event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)

        for i in range(self.trace_length):
            organization_role = 'org:role' + str(i)
            attribute_header.append(organization_role)

        for i in event_log:
            attribute_value = []
            for j in range(self.trace_length):
                attribute_value.append(i[j]['org:role'])
            attributes.append(attribute_value)

        with open("out_" + str(self.counter) + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(attribute_header)
            writer.writerows(attributes)

    def apply_privacy(self, privacy_log_csv, event_log):
        organization_role = []

        for i in range(self.trace_length):
            organization_role.append(privacy_log_csv['org:role' + str(i)])

        organization_role_df = pd.concat(organization_role).reset_index()
        count = 0
        for i in event_log:
            for j in range(self.trace_length):
                i[j]['org:role'] = organization_role_df[0][count]
                count += 1

        return event_log