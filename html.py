from objects import *
import os

tab = '  '


class HtmlMaker(object):
    def html_start(self, title):
        return f'''
    <html>
    {tab}<head>
    {tab * 2}<title>{title}</title>
    {tab}</head>
    {tab}<body>
    '''

    @property
    def html_end(self):
        return f'''
    {tab}</body>
    </html>
    '''

    def embed_namespace(self, n: Namespace):
        return f'{tab * 2}<h1>Part of {n.name} namespace</h1><ul>\n'

    def embed_class_start(self, c: Class, lvl: int = 2):
        parents = ', '.join(c.parents)
        return f'{tab * 3}<h{lvl}>class {c.name}: {parents}</h{lvl}>\n'

    def embed_method(self, m: Method, lvl: int = 2):
        arguments_list = []
        for a in m.arguments:
            arguments_list.append(f'{a}: {m.arguments[a]}')
        arguments_view = ', '.join(arguments_list)
        return f'{tab * 5}<li>{m.name}({arguments_view}) -> {m.return_type}</li>\n'

    def embed_field(self, f: Field):
        return f'{tab * 5}<li>{f.name}: {f.type}</li>\n'

    def end_list(self, lvl=1):
        return f'{tab * lvl}</ul>\n'

    @property
    def embed_methods_start(self):
        return f'{tab * 4}<p>Methods:</p> <ul>\n'

    @property
    def embed_fields_start(self):
        return f'{tab * 4}<p>Fields: <ul>\n'

    def make_class_html(self, c: Class, lvl: int = 2):
        result = self.embed_class_start(c, lvl)
        fields = c.fields + c.properties
        if len(fields) > 0:
            result += self.embed_fields_start
            for f in fields:
                result += self.embed_field(f)
            result += self.end_list(4)
        if len(c.methods) > 0:
            result += self.embed_methods_start
            for m in c.methods:
                result += self.embed_method(m, lvl)
            result += self.end_list(4)
        return result

    def make_html_file(self, cgs: list[CodeGroup], file_name: str) -> list[str]:
        result = self.html_start(file_name)
        for g in cgs:
            if type(g) is Namespace:
                result += self.embed_namespace(g)
                for c in g.classes:
                    result += self.make_class_html(c)
            elif type(g) is Class:
                result += self.make_class_html(g, 1)
            else:
                raise NotImplementedError
        name = file_name + '.html'
        f = open(name, "w")
        f.write(result)
        f.close()
        print("\nYour file is at", os.getcwd() + os.sep + name, '\n\n')
        return result
