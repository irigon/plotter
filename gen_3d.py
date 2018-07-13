from os import listdir
import os.path
from os.path import isfile, join
import copy
import itertools
import plot3d
import sys
import numpy as np
import matplotlib.pyplot as plt



reports_dir = '/home/jose/Programming/Java/the-one-scripts/reports/'

# sort_router: None
sort_dict = dict()
sort_dict['Group.bufferSize'] = lambda x: float(x.split('M')[0])
sort_dict['Group3.speed'] = lambda x: float(x.split(',')[0])
sort_dict['Group3.waitTime'] = lambda x: float(x.split(',')[0])

# dict define what the graphic will show: x_axis, y_axis, metric. The rest
# should be put in sv dict
in_dic = {'x':'Group3.waitTime',
          'y':'Group3.speed',
          'z':'delivered',
          'sv':{'Group.bufferSize':['10M']}
          }

# given the filename, return the desired metric
def get_z_val(fName, metric):
    abs_path = reports_dir + fName
    if not os.path.isfile(abs_path):
        return None
    with open(abs_path, 'r') as mfile:
        for line in mfile.readlines():
            if line.startswith('Message stats for scenario'):
                continue
            val = None
            k, v = line.split(':')
            if metric == k:
                val = v.strip()
                break
        if val is None:
            print('Error: Metric {} not found in file {}. Exiting...'.format(z, f))
            sys.exit(-1)
        return val


# verify in the list of the files if variable x and y coincide.
# if the file is not found exit, there is some error
#   otherwise, return the filename
def get_fName(xy_dic, variables, file_list):
    for f in file_list:
        xkey, ykey = xy_dic.keys()
        if xy_dic[xkey] == get_val_from_filename(xkey, f) and \
            xy_dic[ykey] == get_val_from_filename(ykey, f) and \
                variables['Group.router'] == get_val_from_filename('Group.router', f):
                return f

    print('Metric not found, exiting')
    sys.exit(-1)

def isValidChar(char):
    if not (char.isalnum() or char in [' ', ',', '-', '_', '.']):
        print('Invalid char in filename found: {}'.format(char))
        return False
    else:
        return True

def get_file_list():
    return [f for f in listdir(reports_dir) if isfile(join(reports_dir, f)) and f.endswith('_MessageStatsReport.txt')]

def get_var_order():
    example_file = get_file_list()[0]
    variables = example_file.split('_')[1:-1]
    return [x.split(':')[0] for x in variables]

def get_val_from_filename(attributeName, fileName):
    fields = fileName.split('_')[:-1]
    dict = {x:y for x,y in [pair.split(':') for pair in fields]}
    return dict[attributeName]

# -- for example, if I want a graph:
#   x = Group.bufferSize
#   y = Group3.speed
#   z = 'delivered'
#   static_vars = [Group.router:ProphetRouter, Group3.waitTime:1,1]
def get_data (d):
    local_sv = copy.deepcopy(d['sv'])
    file_list = get_file_list()
    # at first, gather all infos needed
    for f in file_list:
        for sv_k in d['sv']:
            for v in d['sv'][sv_k]:
                sv_str = sv_k + ':' + v
                if sv_str not in f:
                    continue
                # split the fname in key:val pairs
                tokens = f.split('_')[1:-1]
                for token in tokens:
                    k, v = token.split(':')
                    if k == d['x'] or k == d['y']:
                        if k not in local_sv:
                            local_sv[k] = set()
                        local_sv[k].add(v)

    # transform the dict of sets in a dict of lists and sort them
    for k in local_sv.keys():
        if isinstance(local_sv[k], set):
            local_sv[k] = sorted(list(local_sv[k]), key = sort_dict[k])
    return local_sv

def get_graph_data(dic):
    variables = get_data(dic)
    order = get_var_order()

    lista = []
    for k in order:
        lista.append(variables[k])

    prefix = get_file_list()[0].split('_')[0]
    postfix = get_file_list()[0].split('_')[-1]

    file_list = []
    for l in itertools.product(*lista):
        new_lista = ['{}:{}'.format(x, y) for x, y in zip (order, l) ]
        file_list.append('{}_{}_{}'.format(prefix, '_'.join(new_lista), postfix))



    x_list = variables[dic['x']]
    y_list = variables[dic['y']]

    data = []
    for y_val in y_list:
        y_line = []
        for x_val in x_list:
            fName = get_fName({dic['x']:x_val, dic['y']:y_val}, variables, file_list)
            z_val = get_z_val(fName, dic['z'])
            if z_val is None:
                z_val = 0
                print('Warning, z_val None')
            y_line.append(float(z_val))
        data.append(y_line)

    return np.array(data)

#plt.figure(1)
fig = plt.figure(1)
for count, name in enumerate(['EpidemicRouter', 'ProphetRouter', 'ContactGraphRouter']):
    # set metric to the type of router
    in_dic['sv']['Group.router'] = name
    data = get_graph_data(in_dic)

    # set plot number
    plotnum = 311 + count
    plt.subplot(plotnum)
    #plt.title('{}'.format(name))
    plot3d.plot(data, in_dic, fig, plotnum)

plt.show()