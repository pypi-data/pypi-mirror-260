import numpy


def autocategorize1D(raster, iterations=200, centers=[0.1, 0.35, 0.50, 0.70]):
    # cluster pixels in given classes
    iterations = max([1, min([iterations, 200])])
    shape = raster.shape
    raster = raster.reshape(-1, 1)
    for i in range(iterations):
        clusters = numpy.argmin(numpy.abs(raster - centers), axis=1)
        centers = [numpy.mean(raster[clusters == j]) for j in range(len(centers))]
    return clusters.reshape(shape)
