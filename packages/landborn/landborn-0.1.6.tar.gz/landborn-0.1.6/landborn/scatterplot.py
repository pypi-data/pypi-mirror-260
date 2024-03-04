import matplotlib.patches as patches
from matplotlib.path import Path
import matplotlib.pyplot as plt

def scatterplot(df, xvar, yvar, color='k',colormap='viridis', size=1, marker='.', ax=None, save_path=None):
    if ax is None:
        fig, ax = plt.subplots()
    if isinstance(xvar, str):
        xdata = df[xvar]
    else:
        xdata = xvar
        
    if isinstance(yvar, str):
        ydata = df[yvar]
    else:
        ydata = yvar
    x_data_length = max(xdata) - min(xdata)
    x_patch_length = (x_data_length / len(xdata)) / 10
    print(x_patch_length)
    
    y_data_length = max(ydata) - min(ydata)
    y_patch_length = (y_data_length / len(ydata)) / 10
    print(y_patch_length)
    patches_li = []
    for i, (x, y) in enumerate(zip(xdata, ydata)):
        #creating small square for "point"
        verts = [
        (x - x_patch_length, y - y_patch_length),  #left, bottom
        (x - x_patch_length, y + y_patch_length),  #left, top
        (x + x_patch_length, y + y_patch_length),  #right, top
        (x + x_patch_length, y - y_patch_length),  #right, bottom
        (x, y),  #back to start
        ]

        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY,
        ]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, lw=1, color=color)
        patches_li.append(patch)
    
    for patch in patches_li:
        ax.add_patch(patch)
    ax.set_xlim(min(xdata), max(xdata))
    ax.set_ylim(min(ydata), max(ydata))
    # ax.autoscale()
    ax.legend()
    
    if save_path:
        plt.savefig(save_path)
        
    # plt.show()
    return ax

if __name__ == "__main__":
    x = [1, 2, 3, 4, 5]
    y = [10, 15, 7, 10, 5]
    plt = scatterplot(None, x, y,save_path="test_scatterplot.png")