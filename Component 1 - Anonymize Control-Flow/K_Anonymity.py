import Convert_Log
import Variants
import stringdist
from pm4py.algo.filtering.log.variants import variants_filter
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


class K_Anonymity:
    def __init__(self, event_log, k_value):
        self.event_log = event_log
        self.k_value = k_value
        self.kept_traces = []
        self.variants_list = []

    def get_variants(self):
        def count(x):
            if x['count'] >= self.k_value:
                self.kept_traces.append(x['variant'])
            else:
                levenshtein(x)

        def levenshtein(trace):
            max_val = 10000000
            current_trace = ""
            for i in variants_count:
                if stringdist.levenshtein(trace['variant'], i['variant']) < max_val and stringdist.levenshtein(
                        trace['variant'], i['variant']) != 0:
                    max_val = stringdist.levenshtein(trace['variant'], i['variant'])
                    current_trace = i
            if current_trace['count'] - self.k_value + trace['count'] >= self.k_value:
                if current_trace['variant'] in self.kept_traces:
                    self.kept_traces.remove(current_trace['variant'])
                    self.variants_list.append(self.apply_k(trace, current_trace))

        # Grab each variant from the filtered log and pass it to check_k
        variants_count = Variants.Variants(self.event_log)
        variants_count = variants_count.get_variants()
        list(map(lambda x: count(x), variants_count))

        filtered_log_with_k = variants_filter.apply(self.event_log, self.kept_traces,
                                                    parameters={variants_filter.Parameters.POSITIVE: True})

        log_converter_func = Convert_Log.Convert_Log(filtered_log_with_k)
        traces_to_transform = log_converter_func.convert_from_xes_to_csv()

        if len(self.variants_list) != 0:
            ld_traces = pd.concat(self.variants_list)
            final_df = [ld_traces, traces_to_transform]
            filtered_log_with_k = pd.concat(final_df)
        else:
            filtered_log_with_k = traces_to_transform

        return filtered_log_with_k

    def apply_k(self, violating_trace, non_violating_trace):
        non_violating_variant = non_violating_trace['variant'].split(",")
        violating_variant = violating_trace['variant'].split(",")
        index_value = 0
        event_value = ""
        for index, (first, second) in enumerate(zip(non_violating_variant, violating_variant)):
            if first != second:
                index_value = index
                event_value = second

        traces_to_change = self.k_value - violating_trace['count']
        traces_to_transform = [violating_trace['variant'], non_violating_trace['variant']]
        filtered_log = variants_filter.apply(self.event_log, traces_to_transform,
                                             parameters={variants_filter.Parameters.POSITIVE: True})
        log_converter_func = Convert_Log.Convert_Log(filtered_log)
        traces_to_transform = log_converter_func.convert_from_xes_to_csv()

        for i in traces_to_transform['case:concept:name'].unique():
            trace = traces_to_transform.loc[traces_to_transform['case:concept:name'] == i]['concept:name'].tolist()
            for index, (first, second) in enumerate(zip(trace, violating_variant)):
                if first != second:
                    index_value = index
                    event_value = second
            if traces_to_change > 0 and trace == non_violating_variant:
                current_index = traces_to_transform.loc[traces_to_transform['case:concept:name'] == i].index.values[
                    index_value]
                traces_to_transform.at[current_index, 'concept:name'] = event_value
                traces_to_change -= 1
        return traces_to_transform
