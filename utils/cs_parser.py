import utils.cs_objects as cs_obj


class CsharpParser(object):
    def parse_field(self, line: str) -> cs_obj.Field:
        if '=' in line:
            line = line.split('=')[0]
        field_arr = line.split()
        field_type = field_arr[-2]
        field_name = field_arr[-1].strip().strip(';')
        return cs_obj.Field(field_name, field_type)

    def adjust_brace_level(self, line: str, braces='{}') -> int:
        lvl = 0
        if braces[0] in line:
            lvl += 1
        if braces[1] in line:
            lvl -= 1
        return lvl

    def parse_property(self, prop: list[str]) -> cs_obj.Property:
        line = prop[0]
        line = line.split('{')[0]
        prop_arr = line.split()
        prop_type = prop_arr[-2]
        prop_name = prop_arr[-1].strip()
        length = 1
        if len(prop) > 1:
            brace_lvl = 0
            for line in prop[1:]:
                length += 1
                self.adjust_brace_level(line)
                if brace_lvl == 0:
                    break
        return cs_obj.Property(prop_name, prop_type, length)

    def get_method_arguments(self, args: str) -> dict:
        types_names = args.split(',')
        result = {}
        if len(args) > 2:  # if method has arguments
            for pair in types_names:
                p = pair.split()
                result[p[1].strip(' )')] = p[0].strip()
        return result

    def parse_method(self, method: list[str]) -> cs_obj.Method:
        curly_brace_level = 0

        declaration_length = 1
        for i in range(len(method)):
            if ')' in method[i]:
                declaration_length += i
                break
        full_declaration = ''.join(method[:declaration_length])
        split = full_declaration.split('(')
        name = split[0].split()[-1]
        return_type = split[0]
        arguments = self.get_method_arguments(split[1][:-1])
        body_length = 0
        for i in range(len(method[declaration_length:])):
            curly_brace_level += self.adjust_brace_level(method[i])
            if curly_brace_level == 0 and i > 0:
                body_length = i
                break
        result = cs_obj.Method(name)
        result.return_type = return_type
        result.length = declaration_length + body_length
        result.arguments = arguments
        return result

    def get_class_name_and_parents(self, declaration: list[str]) -> (str, list[str]):
        declaration_length = 1
        for i in range(len(declaration)):
            if '{' in declaration[i]:
                declaration_length = i
                break
        full_declaration = ''.join(declaration[:declaration_length])
        split = full_declaration.split(':')
        name = split[0].split()[-1]
        parents = []
        if len(split) > 1:  # If class inherits classes/interfaces
            parents = split[1].split(',')
        parents_no_whitespaces = []
        for parent in parents:
            parents_no_whitespaces.append(parent.strip())
        return name, parents_no_whitespaces

    def parse_class(self, sharp_class: list[str]) -> cs_obj.Class:
        loop_mark = 1
        brace_level = 0
        class_length = 0
        name_parents = self.get_class_name_and_parents(sharp_class)
        parsed_class = cs_obj.Class(name_parents[0], parents=name_parents[1])
        for i in range(1, len(sharp_class)):
            brace_level += self.adjust_brace_level(sharp_class[i])
            if i < loop_mark:
                continue
            if brace_level == 0 and i > 3:
                class_length = i + 1
                break
            if '(' in sharp_class[i] and ')' in sharp_class[i] and '=' not in sharp_class[i] and ';' not in sharp_class[
                i]:
                method = self.parse_method(sharp_class[i:])
                parsed_class.methods.append(method)
                loop_mark += method.length
            elif ';' in sharp_class[i]:  # it's not an abstract method since those are parsed earlier
                if '{' in sharp_class[i]:  # if line is one-line property
                    parsed_class.properties.append(self.parse_property([sharp_class[i]]))
                else:  # if line is a field (we suppose every field is one line long)
                    parsed_class.fields.append(self.parse_field(sharp_class[i]))
                loop_mark += 1
            elif len((sharp_class[i].split())) > 1:  # if line is multi-line property
                parsed_class.properties.append(self.parse_property(sharp_class[i:]))
                loop_mark += parsed_class.properties[-1].length
            else:  # if line is empty or consists of a brace
                loop_mark += 1
        parsed_class.length = class_length

        return parsed_class

    def get_namespace_name(self, declaration: str):
        return declaration.split()[-1]

    def parse_namespace(self, namespace: list[str]) -> cs_obj.Namespace:
        brace_level = 0
        loop_mark = 0
        parsed_namespace = cs_obj.Namespace(self.get_namespace_name(namespace[0]))
        for i in range(len(namespace)):
            if i < loop_mark:
                continue
            brace_level += self.adjust_brace_level(namespace[i])
            if 'class' in namespace[i]:
                parsed_class = self.parse_class(namespace[i:])
                parsed_namespace.classes.append(parsed_class)
                loop_mark += parsed_class.length
            elif brace_level == 0 and i > 2:
                parsed_namespace.length = loop_mark
                return parsed_namespace
            else:
                loop_mark += 1

    def parse_file(self, code: list[str]) -> list[cs_obj.CodeGroup]:
        loop_mark = 0
        namespaces = []
        no_namespace_classes = []
        for i in range(len(code)):
            if i < loop_mark or 'using' in code[i]:
                continue
            elif 'namespace' in code[i]:
                namespace = self.parse_namespace(code[i:])
                namespaces.append(namespace)
                loop_mark += namespace.length
            elif 'class' in code[i]:
                n_n_class = self.parse_class(code[i:])
                no_namespace_classes.append(n_n_class)
                loop_mark += n_n_class.length
        return namespaces + no_namespace_classes
