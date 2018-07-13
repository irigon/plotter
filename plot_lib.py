from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np

def plot_bars(graph_name, bar_names_list, bar_value_list, bar_additional_info_list, y_axis_name, markers, outputfile):
    x_list = np.arange(1,len(bar_names_list)+1)
    plt.axis([0, len(bar_value_list)+1, 0, max(bar_value_list)])
    plt.bar(x_list, bar_value_list)
    #plt.xticks([x + 0.5 for x in x_list], bar_names_list, rotation=70)
    plt.xticks(x_list, bar_names_list, rotation=70)
    #plt.ylabel(y_axis_name)
    plt.suptitle(graph_name)
    plt.subplots_adjust(left=0.12, bottom=0.13, right=0.91, top=0.91, wspace=0.2, hspace=0.2)
    plt.savefig(outputfile)
    plt.clf()
    plt.cla()

    #plt.show()

def plot3d():
    pass
