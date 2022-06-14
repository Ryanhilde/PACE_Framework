from pm4py.algo.organizational_mining.sna import algorithm as sna
import pathlib
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.visualization.sna import visualizer as sna_visualizer
import Convert_Log
from pm4py.objects.log.util import dataframe_utils

# Event Log Variants
# log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Event Logs\\bpi_challenge_2013_incidents.xes")
log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Event Logs\\bpi_challenge_2013_incidents_epsilon_0.1_k20_anonymized.xes")
# log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Final Org Role Logs\\final_organization_role_log_k_2.xes")

hw_values = sna.apply(log, variant=sna.Variants.HANDOVER_LOG)

csv_log = Convert_Log.Convert_Log(log)
csv_log = csv_log.convert_from_xes_to_csv()
attribute = 'org:role'
log_csv = dataframe_utils.convert_timestamp_columns_in_df(csv_log)
log_csv.rename(columns={'org:resource': 'name', attribute: 'org:resource'}, inplace=True)

parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'concept:name'}
event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)

hw_values = sna.apply(event_log, variant=sna.Variants.HANDOVER_LOG)

gviz_hw_py = sna_visualizer.apply(hw_values, variant=sna_visualizer.Variants.PYVIS)
sna_visualizer.view(gviz_hw_py, variant=sna_visualizer.Variants.PYVIS)
