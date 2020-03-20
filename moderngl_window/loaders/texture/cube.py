from collections import namedtuple

from moderngl_window.loaders.texture.pillow import PillowLoader, image_data
from moderngl_window.exceptions import ImproperlyConfigured

FaceInfo = namedtuple('FaceData', ['width', 'height', 'data', 'components'])


class Loader(PillowLoader):
    kind = 'cube'

    def __init__(self, meta):
        super().__init__(meta)

    def load(self):
        """Load a texture cube as described by the supplied ``TextureDescription```

        Returns:
            moderngl.TextureCube: The TextureArray instance
        """
        pos_x = self._load_face(self.meta.pos_x, face_name='pos_x')
        pos_y = self._load_face(self.meta.pos_y, face_name='pos_y')
        pos_z = self._load_face(self.meta.pos_z, face_name='pos_z')
        neg_x = self._load_face(self.meta.neg_x, face_name='neg_x')
        neg_y = self._load_face(self.meta.neg_y, face_name='neg_y')
        neg_z = self._load_face(self.meta.neg_z, face_name='neg_z')

        self._validate([pos_x, pos_y, pos_z, neg_x, neg_y, neg_z])

        texture = self.ctx.texture_cube(
            (pos_x.width, pos_x.height),
            pos_x.components,
            pos_x.data + neg_x.data + pos_y.data + neg_y.data + pos_z.data + neg_z.data,
        )
        texture.extra = {'meta': self.meta}

        if self.meta.mipmap_levels is not None:
            self.meta.mipmap = True

        if self.meta.mipmap:
            if isinstance(self.meta.mipmap_levels, tuple):
                texture.build_mipmaps(*self.meta.mipmap_levels)
            else:
                texture.build_mipmaps()

            if self.meta.anisotropy:
                texture.anisotropy = self.meta.anisotropy

        return texture

    def _load_face(self, path: str, face_name: str = None):
        """Obtain raw byte data for a face

        Returns:
            Tuple[int, bytes]: number of components, byte data
        """
        if not path:
            raise ImproperlyConfigured("{} texture face not supplied".format(face_name))

        image = self._load_texture(path)
        components, data = image_data(image)
        return FaceInfo(width=image.size[0], height=image.size[1], data=data, components=components)

    def _validate(self, faces):
        """Validates each face ensuring components and size it the same"""
        components = faces[0].components
        data_size = len(faces[0].data)
        for face in faces:
            if face.components != components:
                raise ImproperlyConfigured("Cubemap face textures have different number of components")
            if len(face.data) != data_size:
                raise ImproperlyConfigured("Cubemap face textures must all have the same size")

        return components
