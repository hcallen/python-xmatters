import inspect
import xmatters.objects
import xmatters.utils
import xmatters.factories
import re
import os

# OUTPUT_PATH = '../xmatters/objects/'
OUTPUT_PATH = './test'

def main():
    # compile all class names
    class_names = {}
    for module_name, module in inspect.getmembers(xmatters.objects, inspect.ismodule):
        # only get classes defined in module; not imported classes
        for name, class_ in inspect.getmembers(module, lambda x: inspect.isclass(x) and x.__module__ == module.__name__):
            class_names[name] = 'xmatters.objects.{}.{}'.format(module_name, name)
    for name, class_ in inspect.getmembers(xmatters.utils, inspect.isclass):
        class_names[name] = 'xmatters.utils.{}'.format(name)
    for name, class_ in inspect.getmembers(xmatters.factories, inspect.isclass):
        class_names[name] = 'xmatters.utils.{}'.format(name)

    for module_name, module in inspect.getmembers(xmatters.objects, inspect.ismodule):

        source_lines_out = []
        source_lines_in = inspect.getsourcelines(module)[0]
        for line in source_lines_in:

            is_ivar = re.match('\s+[^#]self\.[a-z_]+\s=\s', line)

            if is_ivar:

                source_line_out = line.split('#:')[0].rstrip() + '    #:'

                is_assigned_from_dict = re.match('\s+[^#](?P<attr_name>self\.[a-z_]+)\s=\s[a-z_]+\.get\(\'', line)
                is_assigned_class = re.match('\s+[^#]self\.\w+\s=\s[a-z\.]*[A-Z]\w+\(.*\)', line)
                is_assigned_list = re.match('\s+[^#]self\.\w+\s=\s\[[a-z\.]*[A-Z]\w+\(.*\).*\]', line)

                class_match = re.match('\s+[^#]self\.\w+\s=\s\[?[a-z\.]*(?P<class_name>[A-Z]\w+)\(.*\).*\]?', line)
                class_name = class_match.group('class_name') if class_match else None

                if class_name not in class_names.keys():
                    class_name = None

                if not is_assigned_from_dict and class_name:

                    if is_assigned_class:
                        source_line_out += ' :vartype: :class:`{}`'.format(class_names[class_name])
                        if class_name == 'Pagination':
                            page_class_match = re.match('.*Pagination\([a-z.,\s]+(?P<page_class>[A-Z]\w+)\)', line)
                            page_class = page_class_match.group('page_class') if page_class_match else None
                            if page_class in class_names.keys():
                                source_line_out += ' of :class:`{}`'.format(class_names[page_class])
                    elif is_assigned_list:
                        source_line_out = source_line_out.rstrip() + ' :vartype: [:class:`{}`]'.format(class_names[class_name])
                    elif is_assigned_from_dict:
                        list_match = re.match('\s+[^#](?P<attr_name>self\.[a-z_]+)\s=\s[a-z_]+\.get\(\'\w+\',\[\]', line)
                        if list_match:
                            source_line_out += ':vartype: list'

                source_line_out = source_line_out + '\n' if not source_line_out.endswith('\n') else source_line_out

            else:
                source_line_out = line

            source_lines_out.append(source_line_out)

        for outline, inline in zip(source_lines_out, source_lines_in):
            assert outline.split('#:')[0].rstrip() == inline.split('#:')[0].rstrip()

        out_filepath = os.path.join(OUTPUT_PATH, '{}.py'.format(module_name))
        with open(out_filepath, 'w') as f:
            f.writelines(source_lines_out)


if __name__ == '__main__':
    main()
