import os
import imageio


def create_gif(filenames, duration):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = os.path.join('output', 'gif', 'kMeans.gif')
    imageio.mimsave(output_file, images, duration=duration)
