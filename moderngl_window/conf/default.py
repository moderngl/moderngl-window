# Window / context properties
WINDOW = {
    "gl_version": (3, 3),
    "class": "moderngl_window.context.pyglet.Window",
    "size": (1280, 720),
    "aspect_ratio": 16 / 9,
    "fullscreen": False,
    "resizable": True,
    "title": "ModernGL Window",
    "vsync": True,
    "cursor": True,
    "samples": 0,
}

SCREENSHOT_PATH = None

# Finders
PROGRAM_FINDERS = [
    "moderngl_window.finders.program.FileSystemFinder",
]

TEXTURE_FINDERS = [
    "moderngl_window.finders.texture.FileSystemFinder",
]

SCENE_FINDERS = [
    "moderngl_window.finders.scene.FileSystemFinder",
]

DATA_FINDERS = [
    "moderngl_window.finders.data.FileSystemFinder",
]

# Finder directories: Where finders look for their resources
PROGRAM_DIRS = []
TEXTURE_DIRS = []
SCENE_DIRS = []
DATA_DIRS = []


# Loaders
PROGRAM_LOADERS = [
    'moderngl_window.loaders.program.single.Loader',
    'moderngl_window.loaders.program.separate.Loader',
]

TEXTURE_LOADERS = [
    'moderngl_window.loaders.texture.t2d.Loader',
    'moderngl_window.loaders.texture.array.Loader',
]

SCENE_LOADERS = [
    "moderngl_window.loaders.scene.gltf.GLTF2",
    "moderngl_window.loaders.scene.wavefront.ObjLoader",
    # "moderngl_window.loaders.scene.stl_loader.STLLoader",
]

DATA_LOADERS = [
    'moderngl_window.loaders.data.binary.Loader',
    'moderngl_window.loaders.data.text.Loader',
    'moderngl_window.loaders.data.json.Loader',
]
