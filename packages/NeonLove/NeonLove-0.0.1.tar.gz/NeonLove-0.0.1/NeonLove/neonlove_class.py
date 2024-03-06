import matplotlib.pyplot as plt
import numpy as np
import os

class NeonLove:
    def __init__(self, save_fig = True, fig_name = 'NeonLove.png'):
        self.save_fig = save_fig
        self.fig_name = fig_name
        
    def plot_obj(self):
        theta = np.linspace(0, 2 * np.pi, 1000)

        # Generating x and y data
        x = 16 * ( np.sin(theta) ** 3 )
        y = 13 * np.cos(theta) - 5* np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)

        # Plotting
        fig = plt.figure(facecolor='#ebc6db')
        ax = fig.add_subplot(111)
        for i in range(6):
            ax.plot(x + i*x/2, y + i*y/2, c='#e100c8', lw = 3)
            ax.fill(x + i*x/2, y + i*y/2, color='#a6005c')
        ax.fill(x + (i+1)*x/2, y + (i+1)*y/2, color='#a6005c')
        ax.set_aspect('equal')
        ax.axis('off')
        if self.save_fig:
            plt.savefig(f'{os.getcwd()}/{self.fig_name}', transparent=True)
        return fig

    def show(self):
        self.plot_obj()
        plt.show()