import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from data_generator import DataGenerator
import numpy as np  

class Interactive2DPlotter:
        def __init__(self, 
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
                        "noise_level": 0.1, 
                        "seed": 42,
                        "x_range": (0,1),
                        "y_range": (0,1)
                        }):
              

            self.plot_config = plot_config
            self.data_config = data_config

            # Inizializza il DataGenerator
            self.data_generator = DataGenerator(config=self.data_config)

            # init finestra interattiva
            self.set_window()
            self.set_subplot()
            self.set_control_panel()

            # Variabili per la selezione del punto
            self.selected_point = None
            self.point_marker = None
            # Aggiungi event handler per il click sul subplot
            self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.on_click)

            # Genera i dati iniziali e plottali
            self.generate_data(None)

            plt.show()

        def set_window(self):
            # Crea la finestra con sfondo chiaro
            self.fig = plt.figure(figsize=(14, 9), facecolor='#f0f0f0')
            # Titolo generale
            self.fig.suptitle(self.plot_config["title"], fontsize=20, y=0.98)
            
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
                print("Fullscreen not available")

        def set_subplot(self):
            # Crea il subplot principale con bordo e sfondo
            self.ax = plt.axes([0.05, 0.05, 0.75, 0.88], facecolor='#e6f2ff')
            self.ax.set_xlim(self.plot_config["x_range"][0], self.plot_config["x_range"][1])
            self.ax.set_ylim(self.plot_config["y_range"][0], self.plot_config["y_range"][1])
            self.ax.set_xlabel(self.plot_config["x_label"], fontsize=12)
            self.ax.set_ylabel(self.plot_config["y_label"], fontsize=12)
            self.ax.grid(True, alpha=0.3, linestyle='--')
            
            # Aggiungi bordo al plot
            for spine in self.ax.spines.values():
                spine.set_edgecolor('#333333')
                spine.set_linewidth(2)
            
        def set_control_panel(self):
            self.control_panel_x = 0.81
            self.control_panel_width = 0.16
            self.button_width = 0.025  # Ridotto da 0.035
            self.counter_width = 0.04  # Ridotto da 0.05
            self.spacing = 0.005       # Ridotto da 0.01
            total_width = self.button_width * 2 + self.counter_width + self.spacing * 2
            self.start_x = self.control_panel_x + (self.control_panel_width - total_width) / 2
            self.button_gen_width = self.control_panel_width 
            self.contro_panel_ys = [0.60, 0.50, 0.40, 0.33, 0.10, 0.03, -0.13, -0.19, 0.8, 0.85, 0.75]  
            self.add_datagenerator_controls()

        def add_datagenerator_controls(self):
            self.add_datapoints_controls()
            self.add_poly_degree_controls()
            self.add_noise_levels_controls()
            self.add_generation_button()
            self.add_fit_gp_button()
            self.add_pred_gp_button()
            self.add_remove_point_button()
            self.selected_point_display()
            self.add_add_point_button()

        


        def add_datapoints_controls(self):
            # Label "Datapoints"
            ax_label = plt.axes([self.control_panel_x, self.contro_panel_ys[0] + 0.05, self.control_panel_width, 0.03], facecolor='none')
            ax_label.text(0.5, 0.5, 'Datapoints', transform=ax_label.transAxes,
                        ha='center', va='center', fontsize=13, weight='bold')
            ax_label.axis('off')
            
            
            # Bottone decrease (-)
            self.ax_minus_data = plt.axes([self.start_x, self.contro_panel_ys[0], self.button_width, 0.04])
            self.button_minus_data = Button(self.ax_minus_data, '◄', 
                                        color='#ffcccc', hovercolor='#ff9999')
            self.button_minus_data.label.set_fontsize(12)
            self.button_minus_data.on_clicked(self.decrease_datapoints)
            
            # Counter
            self.ax_counter = plt.axes([self.start_x + self.button_width + self.spacing, self.contro_panel_ys[0], 
                                        self.counter_width, 0.04], facecolor='white')
            self.ax_counter.axis('off')
            self.counter_text = self.ax_counter.text(0.5, 0.5, 
                                                    str(self.data_config["data_size"]),
                                                    transform=self.ax_counter.transAxes,
                                                    ha='center', va='center', 
                                                    fontsize=14, weight='bold')
            
            # Bottone increase (+)
            self.ax_plus_data = plt.axes([self.start_x + self.button_width + self.counter_width + self.spacing * 2, 
                                        self.contro_panel_ys[0], self.button_width, 0.04])
            self.button_plus_data = Button(self.ax_plus_data, '►', 
                                        color='#ccffcc', hovercolor='#99ff99')
            self.button_plus_data.label.set_fontsize(12)
            self.button_plus_data.on_clicked(self.increase_datapoints)

        def add_poly_degree_controls(self):
            # Label "Poly degree"
            ax_label2 = plt.axes([self.control_panel_x, self.contro_panel_ys[1] + 0.05, self.control_panel_width, 0.03], facecolor='none')
            ax_label2.text(0.5, 0.5, 'Poly degree', transform=ax_label2.transAxes,
                        ha='center', va='center', fontsize=13, weight='bold')
            ax_label2.axis('off')
            
            # Bottone decrease (-)
            self.ax_minus_poly = plt.axes([self.start_x, self.contro_panel_ys[1], self.button_width, 0.04])
            self.button_minus_poly = Button(self.ax_minus_poly, '◄', 
                                        color='#ffcccc', hovercolor='#ff9999')
            self.button_minus_poly.label.set_fontsize(12)
            self.button_minus_poly.on_clicked(self.decrease_poly_degree)
            
            # Counter
            self.ax_poly_counter = plt.axes([self.start_x + self.button_width + self.spacing, self.contro_panel_ys[1], 
                                            self.counter_width, 0.04], facecolor='white')
            self.ax_poly_counter.axis('off')
            self.poly_counter_text = self.ax_poly_counter.text(0.5, 0.5, 
                                                            str(self.data_config["polynomial_degree"]),
                                                            transform=self.ax_poly_counter.transAxes,
                                                            ha='center', va='center', 
                                                            fontsize=14, weight='bold')
            
            # Bottone increase (+)
            self.ax_plus_poly = plt.axes([self.start_x + self.button_width + self.counter_width + self.spacing * 2, 
                                        self.contro_panel_ys[1], self.button_width, 0.04])
            self.button_plus_poly = Button(self.ax_plus_poly, '►', 
                                        color='#ccffcc', hovercolor='#99ff99')
            self.button_plus_poly.label.set_fontsize(12)
            self.button_plus_poly.on_clicked(self.increase_poly_degree)

        def add_noise_levels_controls(self):

            # Label "Noise level"
            ax_label3 = plt.axes([self.control_panel_x, self.contro_panel_ys[2] + 0.05, self.control_panel_width, 0.03], facecolor='none')
            ax_label3.text(0.5, 0.5, 'Noise level', transform=ax_label3.transAxes,
                        ha='center', va='center', fontsize=13, weight='bold')
            ax_label3.axis('off')
            
            # Bottone decrease (-)
            self.ax_minus_noise = plt.axes([self.start_x, self.contro_panel_ys[2], self.button_width, 0.04])
            self.button_minus_noise = Button(self.ax_minus_noise, '◄', color='#ffcccc', hovercolor='#ff9999')
            self.button_minus_noise.label.set_fontsize(12)
            self.button_minus_noise.on_clicked(self.decrease_noise)
            
            # Counter (mostra come percentuale)
            self.ax_noise_counter = plt.axes([self.start_x + self.button_width + self.spacing, self.contro_panel_ys[2], 
                                            self.counter_width, 0.04], facecolor='white')
            self.ax_noise_counter.axis('off')
            noise_display = self.data_config["noise_level"]
            self.noise_counter_text = self.ax_noise_counter.text(0.5, 0.5, 
                                                                str(noise_display),
                                                                transform=self.ax_noise_counter.transAxes,
                                                                ha='center', va='center', 
                                                                fontsize=14, weight='bold')
            
            # Bottone increase (+)
            self.ax_plus_noise = plt.axes([self.start_x + self.button_width + self.counter_width + self.spacing * 2, 
                                        self.contro_panel_ys[2], self.button_width, 0.04])
            self.button_plus_noise = Button(self.ax_plus_noise, '►', 
                                        color='#ccffcc', hovercolor='#99ff99')
            self.button_plus_noise.label.set_fontsize(12)
            self.button_plus_noise.on_clicked(self.increase_noise)

        def add_generation_button(self):
            
            self.ax_generate = plt.axes([self.control_panel_x + 0.01, self.contro_panel_ys[3], self.button_gen_width, 0.05])
            self.button_generate = Button(self.ax_generate, 'Generate', 
                                        color='#cce6ff', hovercolor="#2993f7")
            self.button_generate.label.set_fontsize(14)
            self.button_generate.label.set_weight('bold')
            self.button_generate.on_clicked(self.generate_data)

        def add_fit_gp_button(self):
            self.ax_fit_gp = plt.axes([self.control_panel_x + 0.01, self.contro_panel_ys[4], self.button_gen_width, 0.05])
            self.button_fit_gp = Button(self.ax_fit_gp, 'Fit GP', 
                                        color='#eeff99', hovercolor="#fca7a3")
            self.button_fit_gp.label.set_fontsize(14)
            self.button_fit_gp.label.set_weight('bold')
            # self.button_fit_gp.on_clicked(self.generate_data)

        def add_pred_gp_button(self):
            self.ax_pred_gp = plt.axes([self.control_panel_x + 0.01, self.contro_panel_ys[5], self.button_gen_width, 0.05])
            self.button_pred_gp = Button(self.ax_pred_gp, 'Pred GP', 
                                        color='#eeff99', hovercolor='#fca7a3')
            self.button_pred_gp.label.set_fontsize(14)
            self.button_pred_gp.label.set_weight('bold')
            # self.button_pred.on_clicked(self.generate_data)

        def selected_point_display(self):
            # Text box per mostrare il punto selezionato
            self.ax_selected = plt.axes([self.control_panel_x, self.contro_panel_ys[8], self.control_panel_width, 0.04], 
                                facecolor='white')
            self.ax_selected.axis('off')
            self.selected_text = self.ax_selected.text(0.5, 0.5, 'No point selected',
                                                transform=self.ax_selected.transAxes,
                                                ha='center', va='center',
                                                fontsize=11, style='italic')
            
            # Bordo per la text box
            for spine in ['top', 'right', 'bottom', 'left']:
                self.ax_selected.spines[spine].set_visible(True)
                self.ax_selected.spines[spine].set_edgecolor('#cccccc')
                self.ax_selected.spines[spine].set_linewidth(1)

        def on_click(self, event):
            # Se il click è dentro il subplot principale
            if event.inaxes == self.ax:
                # Salva le coordinate del punto selezionato
                self.selected_point = (event.xdata, event.ydata)
                
                # Rimuovi il marker precedente se esiste
                if self.point_marker is not None:
                    self.point_marker.remove()
                
                # Aggiungi un nuovo marker per il punto selezionato
                self.point_marker, = self.ax.plot(event.xdata, event.ydata, 'ro', 
                                                 markersize=10, markeredgecolor='darkred', 
                                                 markeredgewidth=2, alpha=0.7)
                
                # Aggiorna il testo con le coordinate del punto
                self.selected_text.set_text(f'Selected point: ({event.xdata:.3f}, {event.ydata:.3f})')
                self.selected_text.set_style('normal')
                self.selected_text.set_weight('bold')
            
            elif event.inaxes not in [self.ax_minus_data, self.ax_plus_data, self.ax_minus_poly, 
                         self.ax_plus_poly, self.ax_minus_noise, self.ax_plus_noise,
                         self.ax_generate, self.ax_fit_gp, self.ax_pred_gp,
                         self.ax_counter, self.ax_poly_counter, self.ax_noise_counter,
                         self.ax_selected, self.ax_remove_point, self.ax_add_point]:
                # Deseleziona il punto
                self.selected_point = None
                
                # Rimuovi il marker se esiste
                if self.point_marker is not None:
                    self.point_marker.remove()
                    self.point_marker = None
                
                # Ripristina il testo di default
                self.selected_text.set_text('No point selected')
                self.selected_text.set_style('italic')
                self.selected_text.set_weight('normal')
            
            # Ridisegna il canvas
            plt.draw()

        def plot_data(self):
            # Pulisci il subplot dai dati precedenti (mantieni griglia e labels)
            self.ax.clear()
            self.ax.set_xlim(self.plot_config["x_range"][0], self.plot_config["x_range"][1])
            self.ax.set_ylim(self.plot_config["y_range"][0], self.plot_config["y_range"][1])
            self.ax.set_xlabel(self.plot_config["x_label"], fontsize=12)
            self.ax.set_ylabel(self.plot_config["y_label"], fontsize=12)
            self.ax.grid(True, alpha=0.3, linestyle='--')
            
            # Plotta i nuovi punti se esistono
            if hasattr(self.data_generator, 'x_data') and self.data_generator.x_data is not None:
                self.ax.scatter(self.data_generator.x_data, self.data_generator.y_data, 
                            color='blue', s=50, alpha=0.6, edgecolors='darkblue', linewidth=1)
            
            # Ridisegna il marker del punto selezionato se esiste
            if self.selected_point is not None:
                self.point_marker, = self.ax.plot(self.selected_point[0], self.selected_point[1], 'ro', 
                                                markersize=10, markeredgecolor='darkred', 
                                                markeredgewidth=2, alpha=0.7)
            
            # Ridisegna il canvas
            plt.draw()

        def add_remove_point_button(self):
            self.ax_remove_point = plt.axes([self.control_panel_x + 0.01, self.contro_panel_ys[9], self.button_gen_width, 0.04])
            self.button_remove_point = Button(self.ax_remove_point, 'Remove Selected Point', 
                                            color='#ffcccc', hovercolor='#ff9999')
            self.button_remove_point.label.set_fontsize(11)
            self.button_remove_point.label.set_weight('bold')
            self.button_remove_point.on_clicked(self.remove_selected_point)

        def add_add_point_button(self):
            self.ax_add_point = plt.axes([self.control_panel_x + 0.01, self.contro_panel_ys[10], self.button_gen_width, 0.04])
            self.button_add_point = Button(self.ax_add_point, 'Add Selected Point', 
                                        color='#ccffcc', hovercolor='#99ff99')
            self.button_add_point.label.set_fontsize(11)
            self.button_add_point.label.set_weight('bold')
            self.button_add_point.on_clicked(self.add_selected_point)

        def generate_data(self, event):
            """Wrapper per gestire l'evento del bottone"""
            self.data_generator.generate_datapoints()
            self.plot_data()

        def add_selected_point(self, event):
            """
            Aggiunge il punto selezionato al dataset
            """
            if self.selected_point is None:
                print("Nessun punto selezionato da aggiungere")
                return
            
            # Aggiunge il punto usando il metodo del data_generator
            success = self.data_generator.add_selected_point(
                self.selected_point[0], 
                self.selected_point[1]
            )
            
            if success:
                # Aggiorna il counter
                self.data_config["data_size"] = len(self.data_generator.x_data)
                self.counter_text.set_text(str(self.data_config["data_size"]))
                
                # Ridisegna il plot
                self.plot_data()
            

        def remove_selected_point(self, event):
            """
            Rimuove il punto selezionato dal dataset
            """
            if self.selected_point is None:
                print("Nessun punto selezionato da rimuovere")
                return
            
            # Prova a rimuovere il punto selezionato
            success = self.data_generator.remove_selected_point(
                self.selected_point[0], 
                self.selected_point[1]
            )
            
            if success:
                # Aggiorna il counter
                self.data_config["data_size"] = len(self.data_generator.x_data)
                self.counter_text.set_text(str(self.data_config["data_size"]))
                
                # Deseleziona il punto
                self.selected_point = None
                if self.point_marker is not None:
                    self.point_marker.remove()
                    self.point_marker = None
                
                # Ripristina il testo di default
                self.selected_text.set_text('No point selected')
                self.selected_text.set_style('italic')
                self.selected_text.set_weight('normal')
                
                # Ridisegna il plot
                self.plot_data()

        def decrease_datapoints(self, event):
            """
            Rimuove un punto dal dataset e aggiorna l'interfaccia
            """
            success = self.data_generator.remove_datapoint()
            
            if success:
                # Aggiorna il counter
                if hasattr(self.data_generator, 'x_data') and self.data_generator.x_data is not None:
                    self.data_config["data_size"] = len(self.data_generator.x_data)
                else:
                    self.data_config["data_size"] = 0
                
                self.counter_text.set_text(str(self.data_config["data_size"]))
                
                # Ridisegna il plot
                self.plot_data()

        def increase_datapoints(self, event):
            """
            Aggiunge un nuovo punto casuale al dataset e aggiorna l'interfaccia
            """
            success = self.data_generator.add_datapoint()
            
            if success:
                # Aggiorna il counter
                self.data_config["data_size"] = len(self.data_generator.x_data)
                self.counter_text.set_text(str(self.data_config["data_size"]))
                
                # Ridisegna il plot
                self.plot_data()

        def increase_poly_degree(self, event):
            """
            Aumenta il grado del polinomio e aggiorna l'interfaccia
            """
            success = self.data_generator.increase_poly_degree()
            
            if success:
                # Aggiorna il counter nel data_config
                self.data_config["polynomial_degree"] = self.data_generator.config["polynomial_degree"]
                self.poly_counter_text.set_text(str(self.data_config["polynomial_degree"]))
                
                # Rigenera i dati con il nuovo grado
                self.data_generator.generate_datapoints()
                self.plot_data()

        def decrease_poly_degree(self, event):
            """
            Diminuisce il grado del polinomio e aggiorna l'interfaccia
            """
            success = self.data_generator.decrease_poly_degree()
            
            if success:
                # Aggiorna il counter nel data_config
                self.data_config["polynomial_degree"] = self.data_generator.config["polynomial_degree"]
                self.poly_counter_text.set_text(str(self.data_config["polynomial_degree"]))
                
                # Rigenera i dati con il nuovo grado
                self.data_generator.generate_datapoints()
                self.plot_data()

        def increase_noise(self, event):
            """
            Aumenta il livello di rumore e aggiorna l'interfaccia
            """
            success = self.data_generator.increase_noise_level()
            
            if success:
                # Aggiorna il counter nel data_config
                self.data_config["noise_level"] = self.data_generator.config["noise_level"]
                self.noise_counter_text.set_text(f"{self.data_config['noise_level']:.3f}")
                
                # Rigenera i dati con il nuovo livello di rumore
                self.data_generator.generate_datapoints()
                self.plot_data()

        def decrease_noise(self, event):
            """
            Diminuisce il livello di rumore e aggiorna l'interfaccia
            """
            success = self.data_generator.decrease_noise_level()
            
            if success:
                # Aggiorna il counter nel data_config
                self.data_config["noise_level"] = self.data_generator.config["noise_level"]
                self.noise_counter_text.set_text(f"{self.data_config['noise_level']:.3f}")
                
                # Rigenera i dati con il nuovo livello di rumore
                self.data_generator.generate_datapoints()
                self.plot_data()

            













if __name__ == "__main__":
    
    plot_config = {
        "title": "Gaussian Process Regression in 2D: prediction and uncertainty", 
        "x_label": "X-axis", 
        "y_label": "Y-axis",
        "x_range": (0, 1),
        "y_range": (0, 1)
        }
    
    data_config = {
        "polynomial_degree": 2,
        "data_size": 300,
        "noise_level": 0.01,
        "seed": 42,
        "x_range": (plot_config["x_range"][0], plot_config["x_range"][1]),
        "y_range": (plot_config["y_range"][0], plot_config["y_range"][1])
    }
    
    plotter = Interactive2DPlotter(
        plot_config = plot_config,
        data_config = data_config
    )