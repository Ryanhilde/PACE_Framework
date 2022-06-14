import pathlib

from pm4py.statistics.traces.generic.pandas import case_statistics
from pm4py.algo.filtering.pandas.variants import variants_filter
from pm4py.objects.log.importer.xes import importer as xes_importer
import Filter_Min_Frequency
import K_Anonymity
import timeit

start = timeit.default_timer()

# log = xes_importer.apply(str(pathlib.Path().resolve()) + "/Road_Traffic_Fine_Management_Process.xes")
log = xes_importer.apply(str(pathlib.Path().resolve()) + "/Event Logs/bpi_challenge_2013_incidents.xes")
filter_min_freq = Filter_Min_Frequency.Filter_Min_Frequency(log, 1)
filtered_log = filter_min_freq.filter()

# Apply k-anonymity
step_one = K_Anonymity.K_Anonymity(filtered_log, 20)
filter_log = step_one.get_variants()

variant_dict = {}

variants = case_statistics.get_variants_df(filter_log,
                                           parameters={case_statistics.Parameters.CASE_ID_KEY: "case:concept:name",
                                                       case_statistics.Parameters.ACTIVITY_KEY: "concept:name"})
variants.reset_index(level=0, inplace=True)
variants = variants['variant'].unique()

for i in variants:
    li = [i]
    filtered_variant = variants_filter.apply(filter_log, li,
                                             parameters={
                                                 variants_filter.Parameters.CASE_ID_KEY: "case:concept:name",
                                                 variants_filter.Parameters.ACTIVITY_KEY: "concept:name"})
    variant_dict[i] = filtered_variant

counter = 0

for i in variant_dict.values():
    test_log = str(pathlib.Path().resolve()) + "\\Trace Variants\\k = 20\\test_" + str(counter) + ".csv"
    i.to_csv(test_log, sep=',', encoding='utf-8', index=False)
    counter += 1

stop = timeit.default_timer()

print('Time: ', stop - start)
