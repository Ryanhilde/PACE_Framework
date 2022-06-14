import collections
import pathlib

import numpy
from pm4py.algo.organizational_mining.sna import algorithm as sna
from pm4py.objects.log.util import dataframe_utils
from pm4py.visualization.sna import visualizer as sna_visualizer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter

import Convert_Log

# Event Log Variants
original_log = xes_importer.apply(str(pathlib.Path().resolve()) + "\\Event Logs\\bpi_challenge_2013_incidents.xes")
resource_country_privacy_log = xes_importer.apply(
    str(pathlib.Path().resolve()) + "\\Final Resource Country\\final_resource_country_log_k_15.xes")


# organization_country_privacy_log = xes_importer.apply(
#    str(pathlib.Path().resolve()) + "\\Final Organization Country\\final_organization_country_log_k_20.xes")
# organization_involved_privacy_log = xes_importer.apply(
#    str(pathlib.Path().resolve()) + "\\Final Organization Involved\\final_organization_involved_log_k_20.xes")
# org_role_privacy_log = xes_importer.apply(
#    str(pathlib.Path().resolve()) + "\\Final Org Role Logs\\final_organization_role_log_k_2.xes")


def generate_handovers(log, attribute):
    csv_log = Convert_Log.Convert_Log(log)
    csv_log = csv_log.convert_from_xes_to_csv()

    log_csv = dataframe_utils.convert_timestamp_columns_in_df(csv_log)
    log_csv.rename(columns={'org:resource': 'name', attribute: 'org:resource'}, inplace=True)

    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'concept:name'}
    event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)

    hw_values = sna.apply(event_log, variant=sna.Variants.HANDOVER_LOG)
    value_list = hw_values[1]
    return hw_values, value_list


def generate_log(log, threshold, attribute):
    try:
        hw_values, countries = generate_handovers(log, attribute)
        values = []
        counter = 0
        country_mapping = {}

        for i in hw_values[0]:
            country_mapping[countries[counter]] = i
            counter += 1

        for key, value in country_mapping.items():
            for i in range(value.shape[0]):
                if value[i] - threshold >= 0.0:
                    values.append([key, countries[i]])

    except TypeError as e:
        print(e)

    return values


def calculate_precision(privacy_log, attribute):
    hw_values, countries = generate_handovers(privacy_log, attribute)
    # gviz_hw_py = sna_visualizer.apply(hw_values, variant=sna_visualizer.Variants.PYVIS)
    # sna_visualizer.view(gviz_hw_py, variant=sna_visualizer.Variants.PYVIS)

    privacy_values = []
    counter = 0
    country_mapping = {}

    for i in hw_values[0]:
        country_mapping[countries[counter]] = i
        counter += 1

    for key, value in country_mapping.items():
        for i in range(value.shape[0]):
            if value[i] > 0.0:
                privacy_values.append([key, countries[i]])

    return privacy_values


organization_country_generalization_values_dict = {'0': ['World', 'World', 'World', 'World'],
                                                   'SE': ['Northern Europe', 'Europe', 'Eurasia', 'World'],
                                                   'au': ['South Asia', 'Asia', 'Euraisa', 'World'],
                                                   'be': ['Western Europe', 'Europe', 'Eurasia', 'World'],
                                                   'br': ['Southern America', 'The Americas', 'World', 'World'],
                                                   'ca': ['Northern America', 'The Americas', 'World', 'World'],
                                                   'cl': ['Southern America', 'The Americas', 'World', 'World'],
                                                   'cn': ['East Asia', 'Asia', 'Euraisa', 'World'],
                                                   'de': ['Northern Europe', 'Europe', 'Eurasia', 'World'],
                                                   'fr': ['Western Europe', 'Europe', 'Eurasia', 'World'],
                                                   'gb': ['Western Europe', 'Europe', 'Eurasia', 'World'],
                                                   'in': ['South Asia', 'Asia', 'Euraisa', 'World'],
                                                   'jp': ['East Asia', 'Asia', 'Euraisa', 'World'],
                                                   'kr': ['East Asia', 'Asia', 'Euraisa', 'World'],
                                                   'my': ['South Asia', 'Asia', 'Euraisa', 'World'],
                                                   'nl': ['Western Europe', 'Europe', 'Eurasia', 'World'],
                                                   'pe': ['Southern America', 'The Americas', 'World', 'World'],
                                                   'pl': ['Western Europe', 'Europe', 'Eurasia', 'World'],
                                                   'ru': ['Eastern Europe', 'Europe', 'Eurasia', 'World'],
                                                   'se': ['Northern Europe', 'Europe', 'Eurasia', 'World'],
                                                   'th': ['South Asia', 'Asia', 'Euraisa', 'World'],
                                                   'tr': ['Eastern Europe', 'Europe', 'Eurasia', 'World'],
                                                   'us': ['Northern America', 'The Americas', 'World', 'World']}

resource_country_generalization_values_dict = {'0': ['World', 'World', 'World'],
                                               'Argentina': ['South America', 'The Americas', 'World'],
                                               'Australia': ['Asia', 'Eurasia', 'World'],
                                               'Austria': ['Europe', 'Eurasia', 'World'],
                                               'Belgium': ['Europe', 'Eurasia', 'World'],
                                               'Brazil': ['South America', 'The Americas', 'World'],
                                               'Canada': ['North America', 'The Americas', 'World'],
                                               'Chile': ['South America', 'The Americas', 'World'],
                                               'China': ['Asia', 'Eurasia', 'World'],
                                               'Czech Republic': ['Europe', 'Eurasia', 'World'],
                                               'Denmark': ['Europe', 'Eurasia', 'World'],
                                               'France': ['Europe', 'Eurasia', 'World'],
                                               'Germany': ['Europe', 'Eurasia', 'World'],
                                               'INDIA': ['Asia', 'Euraisa', 'World'],
                                               'INDONESIA': ['Asia', 'Eurasia', 'World'],
                                               'Italy': ['Europe', 'Eurasia', 'World'],
                                               'Japan': ['Asia', 'Euraisa', 'World'],
                                               'Korea': ['Asia', 'Euraisa', 'World'],
                                               'MALAYSIA': ['Asia', 'Euraisa', 'World'],
                                               'Netherlands': ['Europe', 'Eurasia', 'World'],
                                               'PERU': ['South America', 'The Americas', 'World'],
                                               'POLAND': ['Europe', 'Eurasia', 'World'],
                                               'RUSSIAN FEDERATION': ['Europe', 'Eurasia', 'World'],
                                               'Romania': ['Europe', 'Eurasia', 'World'],
                                               'Singapore': ['Asia', 'Euraisa', 'World'],
                                               'South Africa': ['Africa', 'Africa', 'World'],
                                               'Spain': ['Europe', 'Eurasia', 'World'],
                                               'Sweden': ['Europe', 'Eurasia', 'World'],
                                               'THAILAND': ['Asia', 'Eurasia', 'World'],
                                               'Turkey': ['Europe', 'Eurasia', 'World'],
                                               'USA': ['North America', 'The Americas', 'World'],
                                               'United Kingdom': ['Europe', 'Eurasia', 'World']}

org_role_generalization_values_dict = {'nan': ['*', '*', '*'],
                                       '': ['*', '*', '*'],
                                       'A2_1': ['A2*', 'A-M', '*'],
                                       'A2_2': ['A2*', 'A-M', '*'],
                                       'A2_3': ['A2*', 'A-M', '*'],
                                       'A2_4': ['A2*', 'A-M', '*'],
                                       'A2_5': ['A2*', 'A-M', '*'],
                                       'C_1': ['C*', 'A-M', '*'],
                                       'C_3': ['C*', 'A-M', '*'],
                                       'C_5': ['C*', 'A-M', '*'],
                                       'C_6': ['C*', 'A-M', '*'],
                                       'D_1': ['D*', 'A-M', '*'],
                                       'D_2': ['D*', 'A-M', '*'],
                                       'E_1': ['E*', 'A-M', '*'],
                                       'E_10': ['E*', 'A-M', '*'],
                                       'E_2': ['E*', 'A-M', '*'],
                                       'E_3': ['E*', 'A-M', '*'],
                                       'E_4': ['E*', 'A-M', '*'],
                                       'E_5': ['E*', 'A-M', '*'],
                                       'E_6': ['E*', 'A-M', '*'],
                                       'E_7': ['E*', 'A-M', '*'],
                                       'E_8': ['E*', 'A-M', '*'],
                                       'E_9': ['E*', 'A-M', '*'],
                                       'V3_2': ['V*', 'N-Z', '*'],
                                       'V3_3': ['V*', 'N-Z', '*']}

organization_involved_generalization_values_dict = {
    'Org line A2': ['Org line A-F', 'Org line A-M', 'Org line *'],
    'Org line B': ['Org line A-F', 'Org line A-M', 'Org line * '],
    'Org line C': ['Org line A-F', 'Org line A-M', 'Org line *'],
    'Org line D': ['Org line A-F', 'Org line A-M', 'Org line *'],
    'Org line E': ['Org line A-F', 'Org line A-M', 'Org line *'],
    'Org line F': ['Org line A-F', 'Org line A-M', 'Org line *'],
    'Org line G1': ['Org line G', 'Org line A-M', 'Org line *'],
    'Org line G2': ['Org line G', 'Org line A-M', 'Org line *'],
    'Org line G3': ['Org line G', 'Org line A-M', 'Org line *'],
    'Org line G4': ['Org line G', 'Org line A-M', 'Org line *'],
    'Org line H': ['Org line H-M', 'Org line A-M', 'Org line *'],
    'Org line I': ['Org line H-M', 'Org line A-M', 'Org line *'],
    'Org line V': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V1': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V10': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V11': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V2': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V3': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V4': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V5': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V7': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V7n': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V8': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Org line V9': ['Org line V', 'Org line V-Z', 'Org line *'],
    'Other': ['Org line *', 'Org line *', 'Org line *']}

organization_country_generalization_dict = {'World': 23, 'Northern Europe': 3, 'Europe': 10, 'Southern America': 3,
                                            'South America': 3, 'Northern America': 2, 'East Asia': 3,
                                            'Western Europe': 5, 'South Asia': 4, 'Eastern Europe': 2, 'Asia': 7,
                                            'Eurasia': 17, 'Euraisa': 17, 'The Americas': 5, 'se': 1}

resource_country_generalization_dict = {'World': 32, 'Europe': 15, 'South America': 4, 'Northern America': 2,
                                        'Asia': 9, 'Eurasia': 17, 'Euraisa': 24, 'The Americas': 6, 'Africa': 1,
                                        'North America': 1, '0': 1}

org_role_generalization_dict = {'*': 25, 'A2*': 5, 'C*': 4, 'D*': 2, 'E*': 10, 'V*': 2, 'A-M': 21, 'N-Z': 2, 'V3_2': 1}

organization_involved_generalization_dict = {'Org line A-F': 6, 'Org line G': 4, 'Org line H-M': 2, 'Org line V': 12,
                                             'Org line *': 25, 'Org line A-M': 12, 'Org line V-Z': 13, 'Org line G1': 1}


def calculate_score(log, attribute, dict, dict_size, dict_values, max_dict_value):
    original_list = generate_log(original_log, numpy.float64(0.0001), attribute)
    privacy_list = calculate_precision(log, attribute)
    retained_relations = [element for element in original_list if element in privacy_list]
    generalized_elements = []

    for element in original_list:
        if element not in retained_relations:
            generalized_elements.append(element)
    generalizations_count = dict_size
    generalized_values = []

    for i in generalized_elements:
        for j in range(generalizations_count):
            breaker = False
            for k in range(generalizations_count):
                if [dict[i[0]][j], dict[i[1]][k]] in privacy_list:
                    generalized_values.append([dict[i[0]][j], dict[i[1]][k]])
                    breaker = True
                    break
                elif [i[0], dict[i[1]][k]] in privacy_list:
                    generalized_values.append([i[0], dict[i[1]][k]])
                    breaker = True
                    break
                elif [dict[i[0]][j], i[1]] in privacy_list:
                    generalized_values.append([dict[i[0]][j], i[1]])
                    breaker = True
                    break
            if breaker:
                break

    score = len(retained_relations)
    for i in generalized_values:
        score += ((1 - (dict_values[i[0]] / max_dict_value) + (1 / max_dict_value)) +
                  (1 - (dict_values[i[1]] / max_dict_value) + (1 / max_dict_value))) / 2
    return score / len(original_list)


resource_country_total_score = calculate_score(resource_country_privacy_log, 'resource country',
                                               resource_country_generalization_values_dict,
                                               len(resource_country_generalization_values_dict['0']),
                                               resource_country_generalization_dict,
                                               resource_country_generalization_dict['World'])
# organization_country_total_score = calculate_score(original_log, 'organization country',
#                                                   organization_country_generalization_values_dict,
#                                                   len(organization_country_generalization_values_dict['0']),
#                                                   organization_country_generalization_dict,
#                                                   organization_country_generalization_dict['World'])
# org_role_total_score = calculate_score(org_role_privacy_log, 'org:role', org_role_generalization_values_dict,
#                                       len(org_role_generalization_values_dict['A2_5']),
#                                       org_role_generalization_dict, org_role_generalization_dict['*'])
# organization_involved_total_score = calculate_score(organization_involved_privacy_log, 'organization involved',
#                                                    organization_involved_generalization_values_dict,
#                                                    len(organization_involved_generalization_values_dict[
#                                                            'Org line A2']),
#                                                    organization_involved_generalization_dict,
#                                                    organization_involved_generalization_dict['Org line *'])
print(resource_country_total_score)
