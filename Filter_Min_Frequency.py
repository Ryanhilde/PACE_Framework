import Variants
from pm4py.algo.filtering.log.variants import variants_filter


class Filter_Min_Frequency:
    def __init__(self, event_log, min_frequency):
        self.event_log = event_log
        self.min_frequency = min_frequency

    def filter(self):
        # Used remove any variants that violate the min. frequency
        variants_count = Variants.Variants(self.event_log)
        variants_count = variants_count.get_variants()
        variants = []
        for i in variants_count:
            if i['count'] > self.min_frequency:
                variants.append(i['variant'])
        # Once the minimum freq. variants have been eliminate, passed the filtered log to the LD method
        filtered_log = variants_filter.apply(self.event_log, variants, parameters={variants_filter.Parameters.POSITIVE: True})
        return filtered_log
