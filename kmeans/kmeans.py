import os
import random
from copy import deepcopy

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from colors import generate_k_random_colors
from gif import create_gif


plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')


FILES = {
    1: {'file': 'normal.txt', 'splitter': '\t'},
    2: {'file': 'unbalance.txt', 'splitter': ' '}
}


def eucliptic_distance(vec1, vec2, axis=None):
    return np.linalg.norm(vec1 - vec2, axis=axis)


class KMeans:
    def __init__(self, k, file, splitter):
        self.k = k
        self.handle_file(file=file, splitter=splitter)

        self.clusters = None
        self.cluster_files = []
        self.colors = generate_k_random_colors(self.k)

    def handle_file(self, file, splitter):
        data = []

        with open(os.path.join('data', file), 'r') as f:
            file_data = f.readlines()
            random.shuffle(file_data)

            for line in file_data:
                obj = line.split(splitter)
                # Convert strings to floats
                obj[0] = float(obj[0])
                # Remove new lines
                obj[1] = float(obj[1].rstrip())

                data.append(obj)

        self.data = pd.DataFrame(data, columns=['x', 'y'])

    def plot_start(self, centroids):
        X = self.data['x'].values
        Y = self.data['y'].values

        plt.title('Beginning')
        plt.grid(True)

        plt.scatter(X, Y, c='g', s=50)
        plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=100, c='b')
        beginning_file = os.path.join('output', 'images', 'beginning.png')
        plt.savefig(beginning_file)

        self.cluster_files.append(beginning_file)

    def plot_clusters(self, X, centroids, clusters, file_helper):
        fig, ax = plt.subplots()

        for i in range(self.k):
            points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
            ax.scatter(points[:, 0], points[:, 1], s=50, c=self.colors[i])

        ax.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=100, c='b')
        cluster_file = os.path.join('output', 'images', 'clusters_{}.png'.format(file_helper))
        plt.savefig(cluster_file)

        self.cluster_files.append(cluster_file)

    def get_random_centroids(self):
        random_centroids = []
        rows_count = len(self.data)

        for _ in range(self.k):
            centroid = self.data.iloc[random.randint(1, rows_count - 1)]
            random_centroids.append(centroid)

        return np.asarray(random_centroids)

    def find_clusters(self):
        data_length = len(self.data)
        X = self.data.as_matrix()

        centroids = self.get_random_centroids()
        self.plot_start(centroids)

        old_centroids = np.zeros(centroids.shape)
        clusters = np.zeros(data_length)

        error = eucliptic_distance(vec1=centroids, vec2=old_centroids)
        file_helper = 0

        while error != 0:
            # Assigning each value to its closest cluster
            for i in range(data_length):
                distances = eucliptic_distance(vec1=X[i], vec2=centroids, axis=1)
                cluster = np.argmin(distances)
                clusters[i] = cluster

            old_centroids = deepcopy(centroids)
            # Finding the new centroids by taking the average value
            for i in range(self.k):
                points = [X[j] for j in range(len(X)) if clusters[j] == i]
                centroids[i] = np.mean(points, axis=0)

            self.plot_clusters(X, centroids, clusters, file_helper)

            error = eucliptic_distance(vec1=centroids, vec2=old_centroids)
            file_helper += 1

        self.clusters = clusters
        self.plot_clusters(X, centroids, self.clusters, 'END')


if __name__ == '__main__':
    file_input_msg = "Choose file. Options:\n1 = `normal.txt`\n2 = `unbalance.txt`\nOption: "
    file_option = input(file_input_msg)

    file = FILES[int(file_option)]['file']
    # Uses `splitter` because the data in the files is separated in defferent way.
    splitter = FILES[int(file_option)]['splitter']

    k = input('Choose `k`: ')

    clf = KMeans(k=int(k), file=file, splitter=splitter)
    clf.find_clusters()

    create_gif(filenames=clf.cluster_files, duration=0.5)

    print('Open output/ directory to see the results.')
