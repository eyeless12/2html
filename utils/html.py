from utils.cs_objects import *

tab = '  '


class HtmlMaker(object):
    def _html_start(self, title):
        return f'''
    <html>
    {tab}<head>
    {tab * 2}<title>{title}</title>
    {tab}</head>
    {tab}<body>
    '''

    @property
    def _html_end(self):
        return f'''
    {tab}</body>
    </html>
    '''

    def _get_class_start(self, c: Class, lvl: int = 2):
        parents = ', '.join(c.parents)
        return f'{tab * 3}<h{lvl}>Класс {c.name}, наследуется от {parents}</h{lvl}>\n'

    def _get_method(self, m: Method, lvl: int = 2):
        arguments_list = []
        for a in m.arguments:
            arguments_list.append(f'{a}: {m.arguments[a]}')
        arguments_view = ', '.join(arguments_list)
        return f'{tab * 5}<li>{m.return_type} {m.name}({arguments_view})</li>\n'

    def _get_field(self, f: Field):
        return f'{tab * 5}<li>{f.name}: {f.type}</li>\n'

    def _get_end_list(self, lvl=1):
        return f'{tab * lvl}</ul>\n'

    @property
    def _methods_start(self):
        return f'{tab * 4}<p>Методы:</p> <ul>\n'

    @property
    def _fields_start(self):
        return f'{tab * 4}<p>Поля: <ul>\n'

    def _make_class_html(self, c: Class, lvl: int = 2):
        result = self._get_class_start(c, lvl)
        fields = c.fields + c.properties
        if len(fields) > 0:
            result += self._fields_start
            for f in fields:
                result += self._get_field(f)
            result += self._get_end_list(4)
        if len(c.methods) > 0:
            result += self._methods_start
            for m in c.methods:
                result += self._get_method(m, lvl)
            result += self._get_end_list(4)
        return result

    def format_documentation(self, cgs: list[CodeGroup], file_name: str) -> str:
        result = self._html_start(file_name)
        for g in cgs:
            if type(g) is Namespace:
                for c in g.classes:
                    result += self._make_class_html(c)
            elif type(g) is Class:
                result += self._make_class_html(g, 1)
            else:
                raise NotImplementedError
        return result
