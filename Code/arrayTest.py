import numpy as numpy
a = numpy.arange(150)

# a[0::2] *= numpy.sqrt(2)/2.0 * (numpy.cos(2) - numpy.sin(2))
a[0::2] *= 2

print(a)