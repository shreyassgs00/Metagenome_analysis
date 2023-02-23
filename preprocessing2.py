#Preprocessing file for the RandomForest analysis
import preprocessing1
import pandas as pd

def preprocessing2_old_file(old_file_name):
    target = []                        #The mapping values for the Random Forest Classifier.
    prism_abundance_values, category = preprocessing1.preprocessing1_old_file(old_file_name)
    metagenome_csv = pd.read_excel(old_file_name) 

    for i in category:                #Mapping of only IBD vs Control to a value
        if i == 'Control':
            target.append(0)
        else:
            target.append(1)

    target_cd_uc = []                    #Mapping of all categories to a value
    for i in category:
        if i == 'Control':
            target_cd_uc.append(0)
        elif i == 'UC':
            target_cd_uc.append(1)
        else:
            target_cd_uc.append(2)
    
    validation_abundance = []            #Finding the abundance values for the validation group
    for i in metagenome_csv:
        if i.startswith('Validation'):
            validation_abundance.append(metagenome_csv[i][8:209])
    
    validation_abundance_values = []
    for i in validation_abundance:
        temp = []
        for j in i:
            temp.append(j)
        validation_abundance_values.append(temp)
    
    target_test = []                  #Finding the target categories in order to map it to an integer value as done before.
    for i in metagenome_csv:
        if i.startswith('Validation'):
            if metagenome_csv[i][2] == 'Control':
                target_test.append(0)
            else:
                target_test.append(1)
    
    target_test_cd_uc = []
    for i in metagenome_csv:
        if i.startswith('Validation'):
            if metagenome_csv[i][2] == 'Control':
                target_test_cd_uc.append(0)
            elif metagenome_csv[i][2] == 'UC':
                target_test_cd_uc.append(1)
            else:
                target_test_cd_uc.append(2)

    return validation_abundance_values, target, target_cd_uc, target_test, target_test_cd_uc

def preprocessing2_new_file(mapping_file, old_file_name,new_file_name):
    metagenome_csv, abundance_values, category = preprocessing1.preprocessing1_new_file(mapping_file, old_file_name, new_file_name)

    target = []                   #Mapping the diagnosis category of PRISM groups to values
    for i in category:
        if i == 'Control':
            target.append(0)
        else:
            target.append(1)

    target_cd_uc = []
    for i in category:
        if i == 'Control':
            target.append(0)
        elif i == 'UC':
            target.append(1)
        else:
            target.append(2)
    
    validation_abundances = []        #Finding abundance values for the validation groups to enable Random Forest analysis
    for i in metagenome_csv:
        if (metagenome_csv[i].loc['Feature'].startswith('Validation')):
            validation_abundances.append(metagenome_csv[i][1:2140])
    
    validation_abundances_values= []
    for i in validation_abundances:
        temp = []
        for j in i:
            temp.append(j)
        validation_abundances_values.append(temp)

    target_test_diagnosis = []     #Mapping diagnosis of Validation groups to values
    for i in metagenome_csv:
        if (metagenome_csv[i].loc['Feature'].startswith('Validation')):
            target_test_diagnosis.append(metagenome_csv[i].loc['Diagnosis'])

    target_test = []
    for i in target_test_diagnosis:
        if i == 'Control':
            target_test.append(0)
        else:
            target_test.append(1)

    target_test_cd_uc = []
    for i in target_test_diagnosis:
        if i == 'Control':
            target_test_cd_uc.append(0)
        elif i == 'UC':
            target_test_cd_uc.append(1)
        else:
            target_test_cd_uc.append(2)

    return validation_abundances_values, target, target_cd_uc, target_test, target_test_cd_uc