import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from data_generator import DataGenerator


class Interactive2DPlotter:
    def __init__(self, 
                 plot_config = {"title": "Title", "x_label": "X-axis", "y_label": "Y-axis", "x_range": (0, 1), "y_range": (0, 10)},
                 data_config = {"polynomial_degree": 2, "data_size": 100, "noise_level": 0.1, "seed": 42}):
        
        self.plot_config = plot_config
        self.data_config = data_config

        print(self.plot_config)

        self.data_generator = DataGenerator(self.data_config)

        # Crea la finestra
        self.fig = plt.figure(figsize=(16, 10))
        # Titolo generale
        self.fig.suptitle(self.plot_config["title"], fontsize=18)
        # Fullscreen
        try:
            self.manager = plt.get_current_fig_manager()
            if hasattr(self.manager, 'window'):
                if hasattr(self.manager.window, 'state'):
                    self.manager.window.state('zoomed')
                elif hasattr(self.manager.window, 'showMaximized'):
                    self.manager.window.showMaximized()
                elif hasattr(self.manager, 'full_screen_toggle'):
                    self.manager.full_screen_toggle()
        except:
            print("Fullscreen non disponibile")

        # Crea il subplot principale
        self.ax = plt.subplot(1, 1, 1)
        self.ax.set_xlim(self.plot_config["x_range"][0], self.plot_config["x_range"][1])
        self.ax.set_ylim(self.plot_config["y_range"][0], self.plot_config["y_range"][1])
        self.ax.set_xlabel(self.plot_config["x_label"])
        self.ax.set_ylabel(self.plot_config["y_label"])
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='best', fontsize=9)

        # Layout - do this BEFORE creating button axes
        plt.tight_layout()
        plt.subplots_adjust(top=0.93, bottom=0.12)
        
        # datapoints buttons
        self.datapoints_scatter_plot = None

        self.ax_generate = plt.axes([0.88, 0.01, 0.10, 0.04])
        self.button_generate = Button(self.ax_generate, 'Generate', color='lightblue')
        self.button_generate.on_clicked(self.generate_datapoints)

        # Bottone per rimuovere datapoint (Left)
        self.ax_minus_data = plt.axes([0.02, 0.01, 0.05, 0.04])
        self.button_minus_data = Button(self.ax_minus_data, 'Remove', color='lightcoral')
        # self.button_minus_data.on_clicked(self.remove_datapoint)

        # Etichetta "datapoints" sopra il counter
        self.ax_datapoint_label = plt.axes([0.08, 0.06, 0.06, 0.02])
        self.ax_datapoint_label.text(0.5, 0.5, 'datapoints', transform=self.ax_datapoint_label.transAxes, 
                                    ha='center', va='center', fontsize=10, weight='bold')
        self.ax_datapoint_label.axis('off')  # Rimuove gli assi per questa label

        # Testo per mostrare il numero di datapoints (invece di TextBox)
        self.ax_datapoint_counter = plt.axes([0.08, 0.01, 0.06, 0.04])
        self.ax_datapoint_counter.axis('off')
        self.datapoint_text = self.ax_datapoint_counter.text(0.5, 0.5, '0', transform=self.ax_datapoint_counter.transAxes, 
                                      ha='center', va='center', fontsize=16)
        
        # Bottone per aggiungere datapoint (Right)
        self.ax_plus_data = plt.axes([0.15, 0.01, 0.05, 0.04])
        self.button_plus_data = Button(self.ax_plus_data, 'Add', color='lightgreen')
        # self.button_plus_data.on_clicked(self.add_datapoint)

        # Inizializza il contatore datapoints
        self.update_datapoint_counter()

        plt.show()


    def generate_datapoints(self, event=None):
        # clear old
        self.clear_datapoints()
        # genera nuovi
        self.data_generator.generate_datapoints()

        # Plot data points
        self.datapoints_scatter_plot = self.scatter_plot = self.ax.scatter(
            self.data_generator.x_data, self.data_generator.y_data, 
            color='red', s=120, marker='+', linewidth=4, label='Data points', zorder=10)
        # Aggiorna la legenda
        self.update_legend()
        self.update_datapoint_counter()
        self.fig.canvas.draw()

    def clear_datapoints(self):
        # Rimuovi il plot delle croci se esiste
        if self.datapoints_scatter_plot is not None:
            self.data_generator.delete_datapoints()
            self.datapoints_scatter_plot.remove()
            self.datapoints_scatter_plot = None
        # Update legend
        self.update_legend()
        # Ridisegna il canvas
        self.fig.canvas.draw()
    
    def update_datapoint_counter(self):
        """Aggiorna il contatore dei datapoints"""
        if hasattr(self.data_generator, 'x_data') and self.data_generator.x_data is not None:
            count = len(self.data_generator.x_data)
        else:
            count = 0
        
        self.datapoint_text.set_text(str(count))
        self.fig.canvas.draw_idle()

    def update_legend(self):
        """Update legend only if there are artists with labels"""
        # Get all artists with labels (excluding those starting with underscore)
        handles, labels = self.ax.get_legend_handles_labels()
        
        if handles and labels:
            # Only create legend if there are labeled artists
            self.ax.legend(handles, labels, loc='best', fontsize=15)
        else:
            # Remove existing legend if no labeled artists
            legend = self.ax.get_legend()
            if legend:
                legend.remove()

        
        
        






if __name__ == "__main__":

    config = {"title": 'Gaussian Process Regression - Interactive Uncertainty Visualization', 
              "x_label": "X-axis",
              "y_label": "Y-axis"}
    
    plotter = Interactive2DPlotter(
        plot_config = {
            "title": "Title", 
            "x_label": "X-axis", 
            "y_label": "Y-axis",
            "x_range": (0, 1),
            "y_range": (0, 1)
            },
        data_config = {
            "polynomial_degree": 2,
            "data_size": 100,
            "noise_level": 0.01,
            "seed": 42}
    )