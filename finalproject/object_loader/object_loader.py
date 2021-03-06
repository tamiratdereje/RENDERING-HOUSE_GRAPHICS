import numpy as np
#  done with object loader

class ObjectLoader:

    def __init__(self, path):
        self.path = path
        self.vertices = {}
        self.normals = {}
        self.texture = {}
        self.all_points = []
        self.all_indices = 0

    def enter_the_number(self, index, data, condition='vertices'):

        if condition == 'vertices':
            for val in data:
                if index not in self.vertices:
                    self.vertices[index] = [float(val)]
                else:
                    self.vertices[index].append(float(val))

        elif condition == 'texture':
            for val in data:
                if index not in self.texture:
                    self.texture[index] = [float(val)]
                else:
                    self.texture[index].append(float(val))

        elif condition == 'normal':
            for val in data:
                if index not in self.normals:
                    self.normals[index] = [float(val)]
                else:
                    self.normals[index].append(float(val))

        elif condition == 'face':
            i = 0
            for val in data:
                val = int(val)
                self.all_indices += 1

                if i == 0:
                    for ver in self.vertices[val]:
                        self.all_points.append(ver)
                    i += 1
                elif i == 1:
                    for ver in self.texture[val]:
                        self.all_points.append(ver)
                    i += 1

                elif i == 2:
                    for ver in self.normals[val]:
                        self.all_points.append(ver)
                

    def load_the_model(self):
        with open(self.path, 'r') as read:
            line = read.readline()

            vrt_inx, tex_inx, nor_inx = 1, 1, 1
            condition = "ta"

            while line:
                given_input = line.split()
                if len(given_input) == 0:
                    continue

                data = given_input[1:]

                if given_input[0] == 'v':

                    self.enter_the_number(vrt_inx, data, 'vertices')
                    vrt_inx += 1

                elif given_input[0] == 'vt':

                    self.enter_the_number(tex_inx, data, 'texture')
                    tex_inx += 1

                elif given_input[0] == 'vn':
                    self.enter_the_number(nor_inx, data, 'normal')
                    nor_inx += 1

                elif given_input[0] == 'f':
                    for value in given_input[1:]:
                        face_index = value.split('/')
                        self.enter_the_number(0, face_index, 'face')

                line = read.readline()
        all_points = self.all_points.copy()
        self.all_points = []
        return self.all_indices, np.array(all_points, dtype='float32')
