import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.metrics import roc_curve, auc

def plot_pcoa(pcoa_analysis, category):       #Function to plot the PCoA analysis as a scatter plot
    colors = []
    for i in category:
        if i == 'UC':
            colors.append('red')
        elif i == 'CD':
            colors.append('green')
        else:
            colors.append('blue')

    for i in range(len(colors)):
        plt.scatter(pcoa_analysis.samples['PC1'][i],pcoa_analysis.samples['PC2'][i], color = colors[i])
    plt.show()
    return 0

def plot_fpr_tpr(fpr,tpr):
    plt.plot(fpr, tpr, label="ROC Curve") 
    plt.xlabel("False Positive Rate") 
    plt.ylabel("True Positive Rate") 
    plt.title("FPR vs TPR for cross-fold validation") 
    plt.show()

def plot_roc_curve(fprs, tprs):
    
    tprs_interp = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    f, ax = plt.subplots(figsize=(14,10))
    
    for i, (fpr, tpr) in enumerate(zip(fprs, tprs)):
        tprs_interp.append(np.interp(mean_fpr, fpr, tpr))
        tprs_interp[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        ax.plot(fpr, tpr, lw=1, alpha=0.3,
                 label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
        
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
             label='Luck', alpha=.8)
    
    mean_tpr = np.mean(tprs_interp, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    ax.plot(mean_fpr, mean_tpr, color='b',
             label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
             lw=2, alpha=.8)
    
    std_tpr = np.std(tprs_interp, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    ax.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                     label=r'$\pm$ 1 std. dev.')
    
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver operating characteristic')
    ax.legend(loc="lower right")
    plt.show()
    return (f, ax)

def plot_mean_aucs(mean_aucs):
    plt.plot(mean_aucs, label = "AUC values plot")
    plt.xlabel("Samples")
    plt.ylabel("Mean AUC scores")
    plt.title("Mean AUC scores for 50 iterations of random hyperparameter search")
    plt.show()