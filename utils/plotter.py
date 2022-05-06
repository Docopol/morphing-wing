import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Plotter:

    def __init__(self, x, y, x_label, y_label, legend_labels=None) -> None:
        if any(isinstance(i, list) for i in x):
            self.x = x
            self.y = y
        elif any(isinstance(i, pd.DataFrame) for i in x):
            self.x = x
            self.y = y
        elif any(isinstance(i, pd.Series) for i in x):
            self.x = x
            self.y = y
        elif any(isinstance(i, np.ndarray) for i in x):
            self.x = x
            self.y = y
        else:
            self.x = [x]
            self.y = [y]
        self.x_label = str(x_label)
        self.y_label = str(y_label)
        if legend_labels:
            self.legend = legend_labels
        else:
            self.legend = [None] * 2

    def plotgraphs(self) -> None:
        """
        call this function to plot the graphs related to this class
        """
        for i, j, k in zip(self.x, self.y, self.legend):
            if len(i) != len(j):
                raise Exception(f"Can't create graph, with irregular points ({len(i)}x{len(j)})")
            if k:
                plt.plot(i, j, label=k)
            else:
                plt.plot(i, j)
        plt.ylabel(self.y_label)
        plt.xlabel(self.x_label)
        if None not in self.legend:
            plt.legend()
        plt.show()

    @classmethod
    def commaformat(cls,):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass