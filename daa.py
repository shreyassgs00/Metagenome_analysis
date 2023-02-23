import skbio
import pandas as pd
from skbio.stats.composition import ancom, multiplicative_replacement
import numpy as np

def perform_daa(abundance_values, target):
    abundance_values_array = np.array(abundance_values)
    new_list_abundance = multiplicative_replacement(abundance_values_array)
    table = pd.DataFrame(new_list_abundance)
    grouping = pd.Series(target)
    results_daa = ancom(table,grouping)
    return results_daa