#This file contains the black box for the PCoA and permanova analysis for the parameters obtained in the preprocessing1 file. 

from scipy.spatial.distance import pdist, squareform,cdist
import skbio
import numpy as np

def perform_pcoa_analysis(abundance_values, category):              #Function to perform PCoA analysis
    distance_matrix = squareform(pdist(abundance_values,'braycurtis'))
    pcoa_analysis = skbio.stats.ordination.pcoa(distance_matrix)

    new_distance_matrix = []         #Creating a numpy array for the Permanova analysis
    for i in distance_matrix:
        row = []
        for j in i:
            row.append(j)
        new_distance_matrix.append(row)
    
    new_distance_matrix = np.array(new_distance_matrix)
    distance_matrix_structure = skbio.stats.distance.DistanceMatrix(new_distance_matrix)
    permanova_analysis = skbio.stats.distance.permanova(distance_matrix_structure, category, column=None, permutations=999)

    return pcoa_analysis, permanova_analysis               #Return the PCoA and Permanova analysis variables.