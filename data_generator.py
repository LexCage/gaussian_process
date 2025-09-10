import numpy as np





class DataGenerator:
    def __init__(self, config = {"polynomial_degree": 0, "data_size": 100, "noise_level": 0.1, "seed": 42}):
        self.config = config

        self.x_data = []
        self.y_data = []

    def generate_datapoints(self):
        print(f"Generating data with config: {self.config} ")

        if self.config["data_size"] <= 0:
            raise ValueError("Data size must be positive")

        # crea nuovi dati sintetici
        self.x_data = np.sort(np.random.uniform(0.0, 1.0, self.config["data_size"]))
        self.noise = np.random.normal(0.0, self.config["noise_level"], self.config["data_size"])

        if self.config["polynomial_degree"] < 0:
            raise ValueError("Polynomial degree must be non-negative")
        
        elif self.config["polynomial_degree"] == 0:
            self.q = np.random.uniform(0.0, 1.0)
            self.y_data = self.q + self.noise
            self.y_data = np.clip(self.y_data, 0, 1)

        elif self.config["polynomial_degree"] == 1:
            self.q = np.random.uniform(0.0, 1.0)
            self.m = np.random.uniform(-1, 1)
            self.y_data = self.m * self.x_data + self.q + self.noise
            self.y_data = np.clip(self.y_data, 0, 1)

        elif self.config["polynomial_degree"] == 2:
            """"
            da riprendere da qui, necessario settare i parametri a,b,c in modo che la parabola stia dentro [0,1]
            """

            self.a = np.random.uniform(-1.0, 1.0)
            self.b = np.random.uniform(-1.0, 1.0)
            self.c = np.random.uniform(0, 1)
            self.y_data = self.a * self.x_data**2 + self.b * self.x_data + self.c + self.noise
            self.y_data = np.clip(self.y_data, 0, 1)

        else:
            raise ValueError(f"{self.config['polynomial_degree']} degree not implemented yet")
        
    def delete_datapoints(self):
        if hasattr(self, 'x_data'):
            del self.x_data
        if hasattr(self, 'y_data'):
            del self.y_data


if __name__ == "__main__":



    data_gen = DataGenerator(config = {
        "polynomial_degree": 0,
        "data_size": 100,
        "noise_level": 0.1,
        "seed": 42})