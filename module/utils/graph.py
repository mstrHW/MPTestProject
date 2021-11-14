import matplotlib.pyplot as plt
import os


SMALL_SIZE = 8
MEDIUM_SIZE = 12
BIGGER_SIZE = 14

plt.rc('font', size=BIGGER_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


class Graph:
    def __init__(self, figsize, title, x_label, y_label, images_dir='', DEMO=False):
        plt.figure(figsize=figsize)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        self.title = title
        self.images_dir = images_dir
        self.DEMO = DEMO

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        plt.grid()
        plt.legend()
        plt.savefig(os.path.join(self.images_dir, self.title + '.png'))

        if self.DEMO:
            plt.show()


if __name__ == '__main__':
    with Graph((16, 9), 'Example', 'x', 'y'):
        plt.plot([1, 2, 3], label='for_legend')
