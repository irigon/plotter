
from plot_lib import plot_bars
import sys
import re
from os import listdir
from os.path import isfile, join

base_dir = "/home/jose/Programming/Java/the-one-scripts/reports/"

metrics = sys.argv[1].split()
sorted_files = sys.argv[2:]

for metric_name in metrics:
    value_list, legend_name = [], []
    # sort files by size taken from its name.
    #sorted_files = sorted(files, key=lambda f: int(re.split('-|M', f)[1]))
    for f in sorted_files:
        routingAlgo, msgSize, reportName = re.split('-|_', f)
        with open(base_dir+f, 'r') as mfile:
            for line in mfile.readlines():
                if line.startswith('Message stats for scenario'):
                    continue
                val = None
                k, v = line.split(':')
                if metric_name == k:
                    val = v.strip()
                    break
            if val is None:
                print('Error: Metric {} not found in file {}. Exiting...'.format(metric_name, f))
                sys.exit(-1)
            value_list.append(float(val))
            legend_name.append(msgSize)



#    print([(a, b) for a, b in zip(legend_name, value_list)])
    title = '{}: Metric "{}" on {}'.format(reportName.split('Report.txt')[0], metric_name, routingAlgo)
    outFilename = '{}_{}.png'.format(routingAlgo, metric_name)
    plot_bars(title, legend_name, value_list, 'additional info', 'some numbers', [], outFilename)


# subplot params:
# left 0.12
# bottom 0.13
# right 0.91
# top 0.91
# wspace 0.2
# hspace 0.2