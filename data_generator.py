import numpy as np





class DataGenerator:
    def __init__(self, config = {"polynomial_degree": 0, "data_size": 100, "noise_level": 0.1, "seed": 42}):
        self.config = config

        self.x_data = []
        self.y_data = []
        self.noises = []

        self.k = None
        self.q = None
        self.m = None

    def generate_datapoints(self):
        print(f"Generating data with config: {self.config} ")

        if self.config["data_size"] <= 0:
            raise ValueError("Data size must be positive")

        # crea nuovi dati sintetici
        self.x_data = np.sort(np.random.uniform(0.0, 1.0, self.config["data_size"]))
        self.noises = np.random.normal(0.0, self.config["noise_level"], self.config["data_size"])

        if self.config["polynomial_degree"] < 0:
            raise ValueError("Polynomial degree must be non-negative")
        
        elif self.config["polynomial_degree"] == 0:
            self.k = np.random.uniform(0.0, 1.0)
            self.y_data = self.k + self.noises
            self.y_data = np.clip(self.y_data, 0, 1)

        elif self.config["polynomial_degree"] == 1:
            self.q = np.random.uniform(0.0, 1.0)
            self.m = np.random.uniform(-1, 1)
            self.y_data = self.m * self.x_data + self.q + self.noises
            self.y_data = np.clip(self.y_data, 0, 1)

        elif self.config["polynomial_degree"] == 2:
            """"
            da riprendere da qui, necessario settare i parametri a,b,c in modo che la parabola stia dentro [0,1]
            """

            self.a = np.random.uniform(-1.0, 1.0)
            self.b = np.random.uniform(-1.0, 1.0)
            self.c = np.random.uniform(0, 1)
            self.y_data = self.a * self.x_data**2 + self.b * self.x_data + self.c + self.noises
            self.y_data = np.clip(self.y_data, 0, 1)

        else:
            raise ValueError(f"{self.config['polynomial_degree']} degree not implemented yet")
        
    def delete_datapoints(self):
        if hasattr(self, 'x_data'):
            del self.x_data
        if hasattr(self, 'y_data'):
            del self.y_data

    def add_datapoint(self, new_x = None, new_y = None):

        if new_x is None:
            new_x = np.random.uniform(0.0, 1.0, 1)

        if new_y is None:
            noise = np.random.normal(0.0, self.config["noise_level"], 1)
            if self.config["polynomial_degree"] == 0:
                if self.k is None:
                    self.k = np.random.uniform(0.0, 1.0)    
                new_y = self.k + noise
            elif self.config["polynomial_degree"] == 1:
                if self.q is None:
                    self.q = np.random.uniform(0.0, 1.0)
                    self.m = np.random.uniform(0.0, 1.0)
                new_y = self.m * new_x + self.q + noise
            elif self.config["polynomial_degree"] == 2:
                if not all(hasattr(self, attr) for attr in ['a', 'b', 'c']):
                    self.a = np.random.uniform(-1.0, 1.0)
                    self.b = np.random.uniform(-1.0, 1.0)
                    self.c = np.random.uniform(0, 1)
                new_y = self.a * new_x**2 + self.b * new_x + self.c + noise
            else:
                raise ValueError(f"{self.config['polynomial_degree']} degree not implemented yet")

        new_y = np.clip(new_y, 0, 1)
        self.noises = np.append(self.noises, noise)
        if not hasattr(self, 'x_data') or self.x_data is None:
            self.x_data = np.array([new_x])
            self.y_data = np.array([new_y])
        else:
            self.x_data = np.append(self.x_data, new_x)
            self.y_data = np.append(self.y_data, new_y)
        
        # Ensure x_data is sorted
        sorted_indices = np.argsort(self.x_data)
        self.x_data = self.x_data[sorted_indices]
        self.y_data = self.y_data[sorted_indices]
        self.noises = self.noises[sorted_indices]

        print(f"Nuovo punto aggiunto: ({float(new_x):.3f}, {float(new_y):.3f})")
        print(f"Numero totale di punti: {len(self.x_data)}")

    def remove_datapoint(self, event=None):
        """
        Rimuove il primo punto dati dai dati esistenti.
        Se c'è solo un punto, lo rimuove completamente.
        """
        # Controlla se ci sono dati da rimuovere
        if not hasattr(self, 'x_data') or self.x_data is None or len(self.x_data) == 0:
            print("Nessun punto da rimuovere")
            return
        removed_x = self.x_data[0]
        removed_y = self.y_data[0]
        removed_noise = self.noises[0] 

        if len(self.x_data) == 1:
            # Se c'è solo un punto, rimuovi tutto
            self.x_data = None
            self.y_data = None
            self.noises = None
            print(f"Ultimo punto rimosso: ({removed_x:.3f}, {removed_y:.3f}, noise: {removed_noise:.3f})")
        else:
            # Rimuovi sempre il primo punto (indice 0)
            self.x_data = self.x_data[1:]  # Rimuovi il primo elemento
            self.y_data = self.y_data[1:]  # Rimuovi il primo elemento
            self.noises = self.noises[1:]  # Rimuovi il primo elemento
            print(f"Primo punto rimosso: ({removed_x:.3f}, {removed_y:.3f}, noise: {removed_noise:.3f})")



if __name__ == "__main__":



    data_gen = DataGenerator(config = {
        "polynomial_degree": 0,
        "data_size": 100,
        "noise_level": 0.1,
        "seed": 42})