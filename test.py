import fnmatch

genre = ['australian underground hip hop', 'australian hip hop', 'pop', 'pop rap']

print(fnmatch.filter(genre, '*hip hop*'))    