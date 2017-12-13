import csv
import random
import math
from collections import Counter
from copy import deepcopy


class IrisKnnClassifier:
    def __init__(self, rand_split=0.75, k=3):
        self.rand_split = rand_split
        self.k = k

        self.predictions = None

        self.load_data()

    def load_data(self):
        with open('./iris.data', 'r') as f:
            data = list(csv.reader(f))
            self.train_set_x, self.train_set_y = [], []
            self.test_set_x, self.test_set_y = [], []

            self.normalize_data(data)

            # cast strings to floats
            for x, row in enumerate(self._normalized_data):
                for y, feature in enumerate(row[:-1]):
                    self._normalized_data[x][y] = feature

                if random.random() < self.rand_split:
                    self.train_set_x.append(row[:-1])
                    self.train_set_y.append(row[-1])
                else:
                    self.test_set_x.append(row[:-1])
                    self.test_set_y.append(row[-1])

            return self.train_set_x, self.train_set_y, self.test_set_x, self.test_set_y

    def normalize_data(self, data):
        self._normalized_data = deepcopy(data)

        iterrations = len(self._normalized_data[0]) - 1
        features = [[] for _ in range(iterrations)]

        for row in self._normalized_data:
            for i in range(iterrations):
                features[i].append(float(row[i]))

        max_features = [max(f) for f in features]

        for x, row in enumerate(self._normalized_data):
            for y in range(iterrations):
                max_feature = max_features[y]
                self._normalized_data[x][y] = float(row[y]) / max_feature

        return self._normalized_data

    def calculate_distance(self, vec_x, vec_y):
        distance = 0

        if len(vec_x) != len(vec_y):
            raise ValueError('Vectors with different length occured.')

        for x, y in zip(vec_x, vec_y):
            distance += pow((x - y), 2)

        return math.sqrt(distance)

    def get_k_nearest_neighbours(self, instance):
        distances = []

        for i, train_instance in enumerate(self.train_set_x):
            dist = self.calculate_distance(train_instance, instance)
            distances.append((dist, i))

        distances.sort(reverse=True, key=lambda t: t[0])
        return distances[:self.k]

    def get_prediction_for(self, instance):
        neighbours = self.get_k_nearest_neighbours(instance)

        neighbours_classes = [self.train_set_y[i] for _, i in neighbours]

        prediction = Counter(neighbours_classes).most_common(1)

        """
        Example prediction:
            ipdb> prediction
            [('Iris-virginica', 3)]
        """
        return prediction[0][0]

    def predict(self):
        self.predictions = [self.get_prediction_for(instance) for instance in self.test_set_x]

    def score(self):
        if self.predictions is None:
            raise ValueError('Call .predict() to use .score()')

        correct = 0

        import ipdb; ipdb.set_trace()
        for prediction, real_value in zip(self.predictions, self.test_set_y):
            if prediction == real_value:
                correct += 0

        accuracy = (correct / float(len(self.train_set_y))) * 100.0

        return round(accuracy, 2)


if __name__ == '__main__':
    clf = IrisKnnClassifier()
    clf.predict()

    print(clf.score())
