import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
import csv


class anonymize_countries_encoding:
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
            resource_country_resource = 'resource country' + str(i)
            organization_country_resource = 'organization country' + str(i)
            attribute_header.append(resource_country_resource)
            attribute_header.append(organization_country_resource)

        for i in event_log:
            countries_attribute_value = []
            for j in range(self.trace_length):
                countries_attribute_value.append(i[j]['resource country'])
                countries_attribute_value.append(i[j]['organization country'])

            attributes.append(countries_attribute_value)

        with open("out_" + str(self.counter) + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(attribute_header)
            writer.writerows(attributes)

    def apply_privacy(self, privacy_log_csv, event_log):
        resource_country_resource = []
        organization_country_resource = []

        for i in range(self.trace_length):
            resource_country_resource.append(privacy_log_csv['resource country' + str(i)])
            organization_country_resource.append(privacy_log_csv['organization country' + str(i)])

        resource_country_df = pd.concat(resource_country_resource).reset_index()
        organization_country_df = pd.concat(organization_country_resource).reset_index()

        count = 0
        for i in event_log:
            for j in range(self.trace_length):
                i[j]['resource country'] = resource_country_df[0][count]
                i[j]['organization country'] = organization_country_df[0][count]
                count += 1

        return event_log
