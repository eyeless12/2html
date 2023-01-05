class CodeGroup:
    def __init__(self, name: str, length: int = 1):
        self.name = name
        self.length = length


class Method(CodeGroup):
    def __init__(self, name: str, length=1, arguments=None, return_type: str = ''):
        super().__init__(name, length)
        self.arguments = {} if arguments is None else arguments
        self.return_type = return_type


class Field(CodeGroup):
    def __init__(self, name: str, var_type: str, length=1):
        super().__init__(name, length)
        self.type = var_type


# while property and field are treated as same here, it's possible for them to change, so model distinction must be made
class Property(Field):
    def __init__(self, name: str, var_type: str = '', length=1):
        super().__init__(name, var_type, length)


class Class(CodeGroup):
    def __init__(self, name: str, length=1, parents: list[str] = None,
                 methods: list[Method] = None, fields: list[Field] = None, properties: list[Property] = None):
        super().__init__(name, length)
        self.parents = [] if parents is None else parents
        self.methods = [] if methods is None else methods
        self.fields = [] if fields is None else fields
        self.properties = [] if properties is None else properties


class Namespace(CodeGroup):
    def __init__(self, name: str, length=1, classes: list[Class] = None):
        super().__init__(name, length)
        self.classes = [] if classes is None else classes
