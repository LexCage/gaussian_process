import numpy as np





class DataGenerator:
    def __init__(self, config = {
        "polynomial_degree": 0,
        "data_size": 100,
        "noise_level": 0.1,
        "seed": 42,
        "x_range": (0,1),
        "y_range": (0,1)
        }):

        self.config = config

        self.x_data = []
        self.y_data = []
        self.noises = []

        self.k = None

        self.q = None
        self.m = None

        if self.config.get("seed") is not None:
            np.random.seed(self.config["seed"])

    def generate_datapoints(self):
        print(f"Generating data with config: {self.config} ")

        # Validazione input
        if self.config["data_size"] <= 0:
            raise ValueError("Data size must be positive")
        if self.config["polynomial_degree"] < 0:
            raise ValueError("Polynomial degree must be non-negative")
        
        # Log iniziale con info essenziali
        print(f"\n{'='*50}")
        print(f"Generating {self.config['data_size']} datapoints")
        print(f"Polynomial degree: {self.config['polynomial_degree']}")
        print(f"Noise level: {self.config['noise_level']:.3f}")
        print(f"X range: [{self.config['x_range'][0]:.2f}, {self.config['x_range'][1]:.2f}]")
        print(f"Y range: [{self.config['y_range'][0]:.2f}, {self.config['y_range'][1]:.2f}]")
        if self.config.get("seed") is not None:
            print(f"Using seed: {self.config['seed']}")
        
        self.x_data = np.random.uniform(
        self.config["x_range"][0], 
        self.config["x_range"][1], 
        self.config["data_size"]
        )
        self.noises = np.random.normal(0.0, self.config["noise_level"], self.config["data_size"])

        if self.config["polynomial_degree"] < 0:
            raise ValueError("Polynomial degree must be non-negative")
        
        elif self.config["polynomial_degree"] == 0:
            self.k = np.random.uniform(self.config["y_range"][0], self.config["y_range"][1], 1)
            self.y_data = self.k + self.noises
            self.y_data = np.clip(self.y_data, self.config["y_range"][0], self.config["y_range"][1])
            print(f"Generated constant function: y = {self.k[0]:.3f}")

        elif self.config["polynomial_degree"] == 1:

            self.q = np.random.uniform(self.config["y_range"][0], self.config["y_range"][1])

            # Genera due punti casuali nel range e calcola la retta che li collega
            x1, x2 = self.config["x_range"]
            y1 = np.random.uniform(self.config["y_range"][0], self.config["y_range"][1])
            y2 = np.random.uniform(self.config["y_range"][0], self.config["y_range"][1])
            
            # Calcola m e q dalla retta passante per (x1,y1) e (x2,y2)
            self.m = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
            self.q = y1 - self.m * x1
            
            self.y_data = self.m * self.x_data + self.q + self.noises
            self.y_data = np.clip(self.y_data, self.config["y_range"][0], self.config["y_range"][1])
            print(f"Generated linear function: y = {self.m:.3f}x + {self.q:.3f}")

        elif self.config["polynomial_degree"] == 2:
            """
            Genera una parabola che passa per tre punti nel dominio
            """
            x_min, x_max = self.config["x_range"]
            y_min, y_max = self.config["y_range"]
            
            # Prendi tre punti x: inizio, metà e fine del dominio
            x_points = np.array([x_min, (x_min + x_max)/2, x_max])
            
            # Genera tre valori y casuali nel range valido
            y_points = np.random.uniform(y_min, y_max, 3)
            
            # Calcola i coefficienti a, b, c che fanno passare la parabola per questi tre punti
            # Sistema: y = ax^2 + bx + c per tre punti
            A = np.vstack([x_points**2, x_points, np.ones(3)]).T
            coeffs = np.linalg.solve(A, y_points)
            self.a, self.b, self.c = coeffs
            
            # Genera i dati
            self.y_data = self.a * self.x_data**2 + self.b * self.x_data + self.c + self.noises
            self.y_data = np.clip(self.y_data, y_min, y_max)
            print(f"Generated quadratic function: y = {self.a:.3f}x² + {self.b:.3f}x + {self.c:.3f}")

        else:
            raise ValueError(f"{self.config['polynomial_degree']} degree not implemented yet")
        
        # Statistiche finali
        print(f"\nData statistics:")
        print(f"  X: min={np.min(self.x_data):.3f}, max={np.max(self.x_data):.3f}, mean={np.mean(self.x_data):.3f}")
        print(f"  Y: min={np.min(self.y_data):.3f}, max={np.max(self.y_data):.3f}, mean={np.mean(self.y_data):.3f}")
        print(f"  Points clipped: {np.sum((self.y_data == self.config['y_range'][0]) | (self.y_data == self.config['y_range'][1]))}")
        print(f"{'='*50}\n")

    def add_selected_point(self, x_coord, y_coord, noise=0.0):
        """
        Aggiunge un punto specifico al dataset
        """
        # Verifica che le coordinate siano nel range valido
        x_coord = np.clip(x_coord, self.config["x_range"][0], self.config["x_range"][1])
        y_coord = np.clip(y_coord, self.config["y_range"][0], self.config["y_range"][1])
        
        # Inizializza gli array se non esistono
        if not hasattr(self, 'x_data') or self.x_data is None:
            self.x_data = np.array([x_coord])
            self.y_data = np.array([y_coord])
            self.noises = np.array([noise])
        else:
            # Aggiungi il punto agli array esistenti
            self.x_data = np.append(self.x_data, x_coord)
            self.y_data = np.append(self.y_data, y_coord)
            self.noises = np.append(self.noises, noise)
        
        print(f"Punto aggiunto: ({x_coord:.3f}, {y_coord:.3f})")
        return True

    def remove_selected_point(self, x_coord, y_coord, tolerance=0.05):
        """
        Rimuove il punto più vicino alle coordinate specificate
        """
        if not hasattr(self, 'x_data') or self.x_data is None or len(self.x_data) == 0:
            print("Nessun punto da rimuovere")
            return False
        
        # Calcola le distanze da tutti i punti
        distances = np.sqrt((self.x_data - x_coord)**2 + (self.y_data - y_coord)**2)
        
        # Trova l'indice del punto più vicino
        closest_index = np.argmin(distances)
        
        # Verifica se il punto è abbastanza vicino (entro la tolleranza)
        if distances[closest_index] <= tolerance:
            # Rimuovi il punto
            removed_x = self.x_data[closest_index]
            removed_y = self.y_data[closest_index]
            
            self.x_data = np.delete(self.x_data, closest_index)
            self.y_data = np.delete(self.y_data, closest_index)
            self.noises = np.delete(self.noises, closest_index)
            
            print(f"Punto rimosso: ({removed_x:.3f}, {removed_y:.3f})")
            return True
        else:
            print("Nessun punto trovato nelle vicinanze")
            return False
        
    def remove_datapoint(self, event=None):
        """
        Rimuove il primo punto dati dai dati esistenti.
        Se c'è solo un punto, lo rimuove completamente.
        """
        # Controlla se ci sono dati da rimuovere
        if not hasattr(self, 'x_data') or self.x_data is None or len(self.x_data) == 0:
            print("Nessun punto da rimuovere")
            return False
        
        removed_x = self.x_data[0]
        removed_y = self.y_data[0]
        removed_noise = self.noises[0] 

        if len(self.x_data) == 1:
            # Se c'è solo un punto, rimuovi tutto
            self.x_data = np.array([])
            self.y_data = np.array([])
            self.noises = np.array([])
            print(f"Ultimo punto rimosso: ({removed_x:.3f}, {removed_y:.3f}, noise: {removed_noise:.3f})")
        else:
            # Rimuovi sempre il primo punto (indice 0)
            self.x_data = self.x_data[1:]  # Rimuovi il primo elemento
            self.y_data = self.y_data[1:]  # Rimuovi il primo elemento
            self.noises = self.noises[1:]  # Rimuovi il primo elemento
            print(f"Primo punto rimosso: ({removed_x:.3f}, {removed_y:.3f}, noise: {removed_noise:.3f})")
        
        return True
    
    def add_datapoint(self, event=None):
        """`
        Aggiunge un nuovo punto casuale al dataset seguendo la funzione corrente
        """
        # Genera coordinate x casuali nel range
        new_x = np.random.uniform(self.config["x_range"][0], self.config["x_range"][1])
        
        # Genera rumore
        noise = np.random.normal(0.0, self.config["noise_level"])
        
        # Calcola y in base al grado del polinomio
        if self.config["polynomial_degree"] == 0:
            if self.k is None:
                self.k = np.random.uniform(self.config["y_range"][0], self.config["y_range"][1], 1)
            new_y = self.k + noise
        elif self.config["polynomial_degree"] == 1:
            if self.q is None or self.m is None:
                # Se non ci sono parametri, genera una retta casuale
                x1, x2 = self.config["x_range"]
                y1 = np.random.uniform(self.config["y_range"][0], self.config["y_range"][1])
                y2 = np.random.uniform(self.config["y_range"][0], self.config["y_range"][1])
                self.m = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
                self.q = y1 - self.m * x1
            new_y = self.m * new_x + self.q + noise
        elif self.config["polynomial_degree"] == 2:
            if not hasattr(self, 'a') or not hasattr(self, 'b') or not hasattr(self, 'c'):
                # Se non ci sono parametri, genera una parabola casuale
                x_min, x_max = self.config["x_range"]
                y_min, y_max = self.config["y_range"]
                x_points = np.array([x_min, (x_min + x_max)/2, x_max])
                y_points = np.random.uniform(y_min, y_max, 3)
                A = np.vstack([x_points**2, x_points, np.ones(3)]).T
                coeffs = np.linalg.solve(A, y_points)
                self.a, self.b, self.c = coeffs
            new_y = self.a * new_x**2 + self.b * new_x + self.c + noise
        else:
            raise ValueError(f"{self.config['polynomial_degree']} degree not implemented yet")
        
        # Applica clipping al valore y
        new_y = np.clip(new_y, self.config["y_range"][0], self.config["y_range"][1])
        
        # Aggiungi il punto ai dati
        if not hasattr(self, 'x_data') or self.x_data is None or len(self.x_data) == 0:
            self.x_data = np.array([new_x])
            self.y_data = np.array([new_y])
            self.noises = np.array([noise])
        else:
            self.x_data = np.append(self.x_data, new_x)
            self.y_data = np.append(self.y_data, new_y)
            self.noises = np.append(self.noises, noise)
        
        print(f"Nuovo punto aggiunto: ({float(new_x):.3f}, {float(new_y):.3f})")
        return True
    
    def increase_poly_degree(self):
        """
        Aumenta il grado del polinomio di 1 (massimo 2)
        """
        if self.config["polynomial_degree"] < 2:
            self.config["polynomial_degree"] += 1
            # Reset dei parametri della funzione
            self.k = None
            self.q = None
            self.m = None
            if hasattr(self, 'a'):
                delattr(self, 'a')
            if hasattr(self, 'b'):
                delattr(self, 'b')
            if hasattr(self, 'c'):
                delattr(self, 'c')
            print(f"Grado polinomio aumentato a: {self.config['polynomial_degree']}")
            return True
        else:
            print("Grado massimo raggiunto (2)")
            return False

    def decrease_poly_degree(self):
        """
        Diminuisce il grado del polinomio di 1 (minimo 0)
        """
        if self.config["polynomial_degree"] > 0:
            self.config["polynomial_degree"] -= 1
            # Reset dei parametri della funzione
            self.k = None
            self.q = None
            self.m = None
            if hasattr(self, 'a'):
                delattr(self, 'a')
            if hasattr(self, 'b'):
                delattr(self, 'b')
            if hasattr(self, 'c'):
                delattr(self, 'c')
            print(f"Grado polinomio diminuito a: {self.config['polynomial_degree']}")
            return True
        else:
            print("Grado minimo raggiunto (0)")
            return False
        
    def increase_noise_level(self, step=0.01):
        """
        Aumenta il livello di rumore di uno step (massimo 1.0)
        """
        if self.config["noise_level"] < 1.0:
            self.config["noise_level"] = min(1.0, self.config["noise_level"] + step)
            print(f"Livello di rumore aumentato a: {self.config['noise_level']:.3f}")
            return True
        else:
            print("Livello di rumore massimo raggiunto (1.0)")
            return False

    def decrease_noise_level(self, step=0.01):
        """
        Diminuisce il livello di rumore di uno step (minimo 0.0)
        """
        if self.config["noise_level"] > 0.0:
            self.config["noise_level"] = max(0.0, self.config["noise_level"] - step)
            print(f"Livello di rumore diminuito a: {self.config['noise_level']:.3f}")
            return True
        else:
            print("Livello di rumore minimo raggiunto (0.0)")
            return False


            
    # def delete_datapoints(self):
    #     if hasattr(self, 'x_data'):
    #         del self.x_data
    #     if hasattr(self, 'y_data'):
    #         del self.y_data

    # def add_datapoint(self, new_x = None, new_y = None):

    #     if new_x is None:
    #         new_x = np.random.uniform(0.0, 1.0, 1)

    #     if new_y is None:
    #         noise = np.random.normal(0.0, self.config["noise_level"], 1)
    #         if self.config["polynomial_degree"] == 0:
    #             if self.k is None:
    #                 self.k = np.random.uniform(0.0, 1.0)    
    #             new_y = self.k + noise
    #         elif self.config["polynomial_degree"] == 1:
    #             if self.q is None:
    #                 self.q = np.random.uniform(0.0, 1.0)
    #                 self.m = np.random.uniform(0.0, 1.0)
    #             new_y = self.m * new_x + self.q + noise
    #         elif self.config["polynomial_degree"] == 2:
    #             if not all(hasattr(self, attr) for attr in ['a', 'b', 'c']):
    #                 self.a = np.random.uniform(-1.0, 1.0)
    #                 self.b = np.random.uniform(-1.0, 1.0)
    #                 self.c = np.random.uniform(0, 1)
    #             new_y = self.a * new_x**2 + self.b * new_x + self.c + noise
    #         else:
    #             raise ValueError(f"{self.config['polynomial_degree']} degree not implemented yet")

    #     new_y = np.clip(new_y, 0, 1)
    #     self.noises = np.append(self.noises, noise)
    #     if not hasattr(self, 'x_data') or self.x_data is None:
    #         self.x_data = np.array([new_x])
    #         self.y_data = np.array([new_y])
    #     else:
    #         self.x_data = np.append(self.x_data, new_x)
    #         self.y_data = np.append(self.y_data, new_y)
        
    #     # Ensure x_data is sorted
    #     # sorted_indices = np.argsort(self.x_data)
    #     # self.x_data = self.x_data[sorted_indices]
    #     # self.y_data = self.y_data[sorted_indices]
    #     # self.noises = self.noises[sorted_indices]

    #     print(f"Nuovo punto aggiunto: ({float(new_x):.3f}, {float(new_y):.3f})")
    #     print(f"Numero totale di punti: {len(self.x_data)}")

    # def remove_datapoint(self, event=None):
    #     """
    #     Rimuove il primo punto dati dai dati esistenti.
    #     Se c'è solo un punto, lo rimuove completamente.
    #     """
    #     # Controlla se ci sono dati da rimuovere
    #     if not hasattr(self, 'x_data') or self.x_data is None or len(self.x_data) == 0:
    #         print("Nessun punto da rimuovere")
    #         return
    #     removed_x = self.x_data[0]
    #     removed_y = self.y_data[0]
    #     removed_noise = self.noises[0] 

    #     if len(self.x_data) == 1:
    #         # Se c'è solo un punto, rimuovi tutto
    #         self.x_data = None
    #         self.y_data = None
    #         self.noises = None
    #         print(f"Ultimo punto rimosso: ({removed_x:.3f}, {removed_y:.3f}, noise: {removed_noise:.3f})")
    #     else:
    #         # Rimuovi sempre il primo punto (indice 0)
    #         self.x_data = self.x_data[1:]  # Rimuovi il primo elemento
    #         self.y_data = self.y_data[1:]  # Rimuovi il primo elemento
    #         self.noises = self.noises[1:]  # Rimuovi il primo elemento
    #         print(f"Primo punto rimosso: ({removed_x:.3f}, {removed_y:.3f}, noise: {removed_noise:.3f})")



if __name__ == "__main__":

    data_gen = DataGenerator(config = {
        "polynomial_degree": 0,
        "data_size": 200,
        "noise_level": 0.1,
        "seed": 42,
        "x_range": (0,1),
        "y_range": (0,1),
        }
    )