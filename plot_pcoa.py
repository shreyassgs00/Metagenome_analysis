import matplotlib.pyplot as plt

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

    return 0