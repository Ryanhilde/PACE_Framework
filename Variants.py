from pm4py.statistics.traces.generic.log import case_statistics


class Variants:
    def __init__(self, event_log):
        self.event_log = event_log

    def get_variants(self):
        variants_count = case_statistics.get_variant_statistics(self.event_log)
        variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)
        return variants_count
