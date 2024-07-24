import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import colors as mcolors

# Liste de couleurs disponibles dans matplotlib
colors = list(mcolors.cnames.keys())

def draw_chart(data):
    nb_row = len(data.keys())
    pos = np.arange(0.5, nb_row * 0.5 + 0.5, 0.5)
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)
    index = 0
    max_len = []

    for machine, operations in sorted(data.items()):
        for op in operations:
            max_len.append(op[1])
            c = random.choice(colors)
            rect = ax.barh((index * 0.5) + 0.5, op[1] - op[0], left=op[0], height=0.3, align='center',
                           edgecolor=c, color=c, alpha=0.8)

            # ajout du label
            width = int(rect[0].get_width())
            Str = "OP_{}".format(op[2])
            xloc = op[0] + 0.50 * width
            clr = 'black'
            align = 'center'
            yloc = rect[0].get_y() + rect[0].get_height() / 2.0
            ax.text(xloc, yloc, Str, horizontalalignment=align,
                    verticalalignment='center', color=clr, weight='bold',
                    clip_on=True)
        index += 1

    ax.set_ylim(ymin=-0.1, ymax=nb_row * 0.5 + 0.5)
    ax.grid(color='gray', linestyle=':')
    ax.set_xlim(0, max(10, max(max_len)))

    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=0, fontsize=10)

    locsy, labelsy = plt.yticks(pos, data.keys())
    plt.setp(labelsy, fontsize=14)

    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1, prop=font)

    ax.invert_yaxis()
    plt.title("Flexible Job Shop Solution")
    plt.savefig('gantt.svg')
    plt.show()

# Données du diagramme de Gantt
gantt_data = {
    'Machine-1': [[0, 2, '4-1'], [5, 8, '3-2'], [2, 3, '2-1'], [3, 5, '2-2'], [8, 10, '7-3'], [10, 11, '0-3'], [11, 13, '6-3'], [13, 17, '5-3'], [17, 19, '5-4'], [19, 20, '3-4'], [20, 24, '3-5'], [24, 28, '6-5']],
    'Machine-2': [[0, 2, '0-1'], [2, 8, '8-1'], [8, 14, '3-3'], [14, 20, '0-4'], [20, 26, '5-5'], [26, 27, '0-6']],
    'Machine-3': [[0, 3, '7-1'], [3, 7, '0-2'], [7, 11, '5-2'], [11, 15, '8-2'], [15, 17, '2-3'], [17, 20, '1-4'], [20, 22, '1-5'], [22, 25, '8-5'], [25, 28, '4-6']],
    'Machine-4': [[0, 3, '9-1'], [3, 9, '9-2'], [9, 12, '4-3'], [12, 13, '9-4'], [15, 17, '4-5'], [17, 22, '8-4'], [24, 25, '3-6'], [22, 23, '2-5']],
    'Machine-5': [[0, 3, '5-1'], [3, 5, '3-1'], [5, 7, '7-2'], [7, 9, '6-2'], [9, 12, '9-3'], [12, 14, '1-3'], [14, 17, '7-4'], [17, 19, '2-4'], [22, 25, '1-6'], [19, 22, '6-4'], [25, 28, '2-6']],
    'Machine-6': [[0, 3, '6-1'], [3, 6, '4-2'], [6, 7, '1-1'], [7, 10, '1-2'], [12, 15, '4-4'], [15, 16, '8-3'], [16, 19, '9-5'], [20, 23, '0-5'], [19, 20, '9-6'], [23, 26, '7-5'], [26, 27, '7-6'], [27, 28, '5-6']]
}

# Affichage du diagramme de Gantt
draw_chart(gantt_data)
