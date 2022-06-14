import pathlib

import pandas as pd
import anonymize_countries_encoding
import os
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
import Convert_Log
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

k_value = 2

path, dirs, files = next(os.walk(str(pathlib.Path().resolve()) + "\\Trace Variants\\k = " + str(k_value)))
file_count = len(files)


def encode_log():
    for i in range(file_count):
        try:
            log_csv = pd.read_csv(str(pathlib.Path().resolve()) +
                                  "\\Trace Variants\\k = " + str(k_value) + "\\test_" + str(i) + ".csv",
                                  sep=',')

            encoding = anonymize_countries_encoding.anonymize_countries_encoding(log_csv, i)
            encoding.write_variant()
        except Exception as e:
            print(e)


def apply_privacy():
    total_event_log = []
    for i in range(file_count):
        try:
            privacy_log = pd.read_csv(str(pathlib.Path().resolve()) +
                                      "\\Anonymize Countries\\k = " + str(k_value) + "\\anonymized_data_" + str(i) + ".csv", sep=',')

            log_csv = pd.read_csv(str(pathlib.Path().resolve()) +
                                  "\\Trace Variants\\k = " + str(k_value) + "\\test_" + str(i) + ".csv", sep=',')

            log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
            log_csv = log_csv.sort_values('time:timestamp')
            parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:concept:name'}
            event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)
            encoding = anonymize_countries_encoding.anonymize_countries_encoding(log_csv, i)
            csv_file = Convert_Log.Convert_Log(encoding.apply_privacy(privacy_log, event_log))
            csv_file_df = csv_file.convert_from_xes_to_csv()
            total_event_log.append(csv_file_df)

        except Exception as e:
            print(e)
            continue

    merged_event_log_df = pd.concat(total_event_log)
    merged_event_log_df = dataframe_utils.convert_timestamp_columns_in_df(merged_event_log_df)
    total_parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:concept:name'}
    event_log = log_converter.apply(merged_event_log_df, parameters=total_parameters,
                                    variant=log_converter.Variants.TO_EVENT_LOG)
    xes_exporter.apply(event_log, str(pathlib.Path().resolve()) + '/final_countries_log_' + str(k_value) +'_.xes')


# encode_log()
apply_privacy()