

class Material:
    def __init__(self, name):
        self.name = name
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.mat_texture = None
        self.double_sided = True

    def __str__(self):
        return "<Material {}>".format(self.name)

    def __repr__(self):
        return str(self)


class MaterialTexture:
    def __init__(self, texture=None, sampler=None):
        self.texture = texture
        self.sampler = sampler
