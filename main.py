#Main entry point for the program. All functions called here.

#Importing all necessary black box functions
import preprocessing1
import preprocessing2
import pcoa_analysis
import plot_figures
import random_forest
import hyperparameter_search
import daa

def main():
    old_file_name = 'data/FranzosaMetagenome.xlsx'
    new_file_name = 'data/Franzosa_MAGinator_abundances.csv'
    mapping_file_name = 'data/filereport_read_run_PRJNA400072_tsv.txt'

    old_prism_abundance_values, old_category = preprocessing1.preprocessing1_old_file(old_file_name)
    new_metagenome_csv, new_prism_abundance_values, new_category = preprocessing1.preprocessing1_new_file(mapping_file_name, old_file_name, new_file_name)

    old_pcoa_analysis, old_permanova_analysis = pcoa_analysis.perform_pcoa_analysis(old_prism_abundance_values, old_category)
    new_pcoa_analysis, new_permanova_analysis = pcoa_analysis.perform_pcoa_analysis(new_prism_abundance_values, new_category)

    plot_figures.plot_pcoa(old_pcoa_analysis, old_category)
    plot_figures.plot_pcoa(new_pcoa_analysis, new_category)

    old_validation_abundance_values, old_target, old_target_cd_uc, old_target_test, old_target_test_cd_uc = preprocessing2.preprocessing2_old_file(old_file_name)
    new_validation_abundance_values, new_target, new_target_cd_uc, new_target_test, new_target_test_cd_uc = preprocessing2.preprocessing2_new_file(mapping_file_name, old_file_name, new_file_name)

    #Comparison between prism and validation abundance values between IBD and Control groups
    predicted_old_target, old_metrics_score = random_forest.perform_random_forest_classification(old_prism_abundance_values, old_target, old_validation_abundance_values, old_target_test)
    predicted_new_target, new_metrics_score = random_forest.perform_random_forest_classification(new_prism_abundance_values, new_target, new_validation_abundance_values, new_target_test)

    predicted_old_target_cd_uc, old_metrics_score_cd_uc = random_forest.perform_random_forest_classification(old_prism_abundance_values, old_target_cd_uc, old_validation_abundance_values, old_target_test_cd_uc)
    predicted_new_target_cd_uc, new_metrics_score_cd_uc = random_forest.perform_random_forest_classification(new_prism_abundance_values, new_target_cd_uc, new_validation_abundance_values, new_target_test_cd_uc)

    auc_score_old, false_positive_rate_independent_old, true_positive_rate_independent_old, false_positive_rate_old, true_positive_rate_old = random_forest.get_auc_score(old_prism_abundance_values, old_target, old_validation_abundance_values, old_target_test, predicted_old_target)
    auc_score_new, false_positive_rate_independent_new, true_positive_rate_independent_new, false_positive_rate_new, true_positive_rate_new = random_forest.get_auc_score(new_prism_abundance_values, new_target, new_validation_abundance_values, new_target_test, predicted_new_target)

    plot_figures.plot_fpr_tpr(false_positive_rate_old, true_positive_rate_old)
    plot_figures.plot_fpr_tpr(false_positive_rate_new, true_positive_rate_new)

    auc_scores_old, false_positive_rates_old, true_positive_rates_old = random_forest.perform_cross_fold_validation(old_prism_abundance_values, old_target, old_validation_abundance_values, old_target_test)
    auc_scores_new, false_positive_rates_new, true_positive_rates_new = random_forest.perform_cross_fold_validation(new_prism_abundance_values, new_target, new_validation_abundance_values, new_target_test)

    plot_figures.plot_roc_curve(false_positive_rates_old, true_positive_rates_old)
    plot_figures.plot_roc_curve(false_positive_rates_new, true_positive_rates_new)

    mean_aucs_old = hyperparameter_search.hyperparameter_search(old_prism_abundance_values, old_target, old_validation_abundance_values, old_target_test)
    mean_aucs_new = hyperparameter_search.hyperparameter_search(new_prism_abundance_values, new_target, new_validation_abundance_values, new_target_test)

    plot_figures.plot_mean_aucs(mean_aucs_old)
    plot_figures.plot_mean_aucs(mean_aucs_new)

main()