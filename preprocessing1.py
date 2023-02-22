#This file preprocesses both the new and the old metagenome files in order to extract the abundance values for PRISM group and the category of diagnosis

import pandas as pd
import numpy as np

def preprocessing_old_file(file_name):                      #Preprocessing the old metagenome file to extract data to perform different statistical analysis.
    metagenome_csv = pd.read_excel(file_name)
    
    column_values = []
    columns = []                                            #Extracting columns data with the goal to store it in the form of a list. 
    
    for column in metagenome_csv:
        columns.append(column)
    
    columns = columns[1:]
    for column in columns:
        column_values.append([column,metagenome_csv[column]])

    new_column_values = []
    abundance_values = []
    for i in column_values:
        if i[0].startswith('PRISM'):
            abundance_values.append(i[1][8:])
            new_column_values.append(i)

    list_abundance_values = []                                #Storing all PRISM abundance values in the form of a list
    for i in abundance_values:
        values = []
        for j in i:
            values.append(j)
        list_abundance_values.append(values)

    category = []                                            #Finding the disease/control category of the corresponding abundance values
    for i in new_column_values:
        category.append(i[1][2])

    return list_abundance_values, category                   #Function returns abundance values in a 2D list along with the corresponding categories.

def preprocessing_new_file(mapping_file_name, old_file_name, new_file_name):
    mapping_file = open(mapping_file_name, 'r')
    new_file = pd.read_csv(new_file_name)
    old_metagenome_csv = pd.read_excel(old_file_name)

    new_file.rename(columns = {'Unnamed: 0':'SRA_metagenome_name'}, inplace = True)       #Preprocessing the new abundances file.
    new_metagenome_csv = new_file.T

    SRA_identities = []                                       #List later used to create mappings between SRA values and G values
    for i in range(0, len(new_metagenome_csv.columns)):
        SRA_identities.append(new_metagenome_csv[i]['SRA_metagenome_name'])

    mapping_file_lines = []
    for line in mapping_file:
        mapping_file_lines.append(line.split('\t'))

    G_identities = []
    for i in range(1,len(mapping_file_lines)):
        G_identities.append([mapping_file_lines[i][3],mapping_file_lines[i][6]])

    SRA_G_mapping = []                            #List containing the mapping of the G identities to the SRA identities
    for i in SRA_identities:
        for j in G_identities:
            if i == j[0]:
                SRA_G_mapping.append([i,j[1]])

    for i in SRA_G_mapping:
        new_metagenome_csv.replace(i[0],i[1], inplace=True)
    
    ordered_metagenome_names = []      #Ordering prism and validation groups with respect to the old file with the corresponding category of diagnosis
    for i in old_metagenome_csv:
        ordered_metagenome_names.append([i,old_metagenome_csv[i][0]])
    ordered_metagenome_names = ordered_metagenome_names[1:]

    prism_validation_order_with_name = []
    for i in new_metagenome_csv:
        for j in ordered_metagenome_names:
            if new_metagenome_csv[i][0] == j[1]:
                prism_validation_order_with_name.append([new_metagenome_csv[i][0],j[0]])
    
    prism_validation_order = []
    for i in prism_validation_order_with_name:
        prism_validation_order.append(i[1])

    ordered_diagnosis = []              #Ordering diagnosis 
    for i in old_metagenome_csv:
        ordered_diagnosis.append([old_metagenome_csv[i][0],old_metagenome_csv[i][2]])
    ordered_diagnosis = ordered_diagnosis[1:]

    diagnosis_with_name = []
    for i in new_metagenome_csv:
        for j in ordered_diagnosis:
            if new_metagenome_csv[i][0] == j[0]:
                diagnosis_with_name.append([new_metagenome_csv[i][0],j[1]])

    new_metagenome_csv.loc[len(new_metagenome_csv)] = prism_validation_order

    new_diagnosis_order = []
    for i in diagnosis_with_name:
        new_diagnosis_order.append(i[1])

    new_metagenome_csv.loc[len(new_metagenome_csv)] = new_diagnosis_order

    new_metagenome_csv.rename(index = {2141:'Feature'}, inplace = True)   #Creating a mapping in the new abundances between diagnosis and prism/validation group
    new_metagenome_csv.rename(index = {2142:'Diagnosis'}, inplace = True)

    abundance_values = []
    for i in new_metagenome_csv:
        if (new_metagenome_csv[i].loc['Feature'].startswith('PRISM')):
            abundance_values.append(new_metagenome_csv[i][1:2140])

    list_abundance_values = []          #Creating an array of the abundance values and the corresponding category of disease or control.
    for i in abundance_values:
        temp = []
        for j in i:
            temp.append(j)
        list_abundance_values.append(temp)

    category = []                            
    for i in new_metagenome_csv:
        if (new_metagenome_csv[i].loc['Feature'].startswith('PRISM')):
            category.append(new_metagenome_csv[i].loc['Diagnosis'])

    return list_abundance_values, category        #Return the same as the other preprocessing function for further analysis.