from opengl_registry.registry import Registry


class Writer:

    def __init__(self, *args, **kwargs):
        pass

    def write(self, registry: Registry):
        self.write_header()
        self.write_types()
        self.write_enums()
        self.write_commands()

    def write_header(self):
        pass

    def write_types(self):
        pass

    def write_enums(self):
        pass

    def write_commands(self):
        pass
