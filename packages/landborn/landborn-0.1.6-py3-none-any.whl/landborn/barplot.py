import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import pandas as pd

def barplot(df, xvar, yvar, orientation='vertical', color='lightblue', axis=None, save_path=None):
    if axis is None:
        fig, axis = plt.subplots()

    if orientation == 'vertical':
        if isinstance(xvar, str):
            categories = df[xvar].unique()
            x = np.arange(len(categories))
            heights = df.groupby(xvar)[yvar].mean()
            errors = df.groupby(xvar)[yvar].sem()
        else:
            x = xvar
            heights = x.mean()
            errors = x.sem()
        bars = []
        for i, (category, height) in enumerate(zip(categories, heights)):
            error_line = mlines.Line2D([x[i], x[i]], [height-(errors[category]/2), height+(errors[category]/2)], color='black')
            error_line_top = mlines.Line2D([x[i] - 0.1, x[i] + 0.1], [height+(errors[category]/2), height+(errors[category]/2)], color='black')
            error_line_bottom = mlines.Line2D([x[i] - 0.1, x[i] + 0.1], [height-(errors[category]/2), height-(errors[category]/2)], color='black')
            rect = mpatches.Rectangle((x[i] - 0.4, 0), 0.8, height,facecolor=color, edgecolor='black')
            bars.append(rect)
            axis.add_patch(rect)
            axis.add_line(error_line)
            axis.add_line(error_line_top)
            axis.add_line(error_line_bottom)

        axis.set_xticks(x)
        axis.set_xticklabels(categories)
        axis.set_xlabel(xvar)
        axis.set_ylabel(yvar)
        axis.autoscale()
        axis.set_ylim(bottom=0)

    elif orientation == 'horizontal':
        # Horizontal bar plot
        categories = df[yvar].unique()
        y = np.arange(len(categories))
        heights = df.groupby(yvar)[xvar].mean()
        errors = df.groupby(yvar)[xvar].sem()

        bars = []
        for i, (category, height) in enumerate(zip(categories, heights)):
            rect = mpatches.Rectangle((0, y[i] - 0.4), height, 0.8,facecolor=color, edgecolor='black')
            bars.append(rect)
            axis.add_patch(rect)

        axis.set_yticks(y)
        axis.set_yticklabels(categories)
        axis.set_ylabel(yvar)
        axis.set_xlabel(xvar)
        axis.autoscale()
        axis.set_xlim(0)
    if save_path:
        plt.savefig(save_path)

    return axis



if __name__ == "__main__":
    x = [1, 2, 3, 4, 5]
    y = [10, 15, 7, 10, 5]
    # plt = barplot(None, x, y, orientation="vertical" ,save_path="test_scatterplot.png")
    
    df = pd.DataFrame({
        'data values': np.random.normal(5,1,100),
        'categories': np.random.choice(['a','b','c'],replace=True, size=100)
    })
    df.loc[df['categories'] == 'a','data values'] = df.loc[df['categories'] == 'a']['data values'] * 2 - 6
    ax = barplot(df, 'categories', 'data values', orientation='vertical', save_path="test_barplot.png")
    
    