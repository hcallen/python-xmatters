import inspect
import xmatters.objects
import xmatters.utils
import re
import os

OUTPUT_PATH = '../test'


def main():
    # compile all class names
    class_names = []
    for module_name, module in inspect.getmembers(xmatters.objects, inspect.ismodule):
        for name, class_ in inspect.getmembers(module, inspect.isclass):
            class_names.append(name)
    for name, class_ in inspect.getmembers(xmatters.utils, inspect.isclass):
        class_names.append(name)

    for module_name, module in inspect.getmembers(xmatters.objects, inspect.ismodule):

        source_out = []
        source_lines = inspect.getsourcelines(module)
        for line in source_lines[0]:

            is_instance_attr = re.match('\s+[^#]self\.[a-z_]+\s=\s', line)
            has_comment = re.match('^.*\s+#:(?P<comment>.*)\n$', line)
            has_comment_text = has_comment.group('comment').strip() if has_comment else None

            if is_instance_attr:

                if not has_comment:
                    outline = line.rstrip() + '    #:'
                else:
                    outline = line


                is_dict_assigned = re.match('\s+[^#](?P<attr_name>self\.[a-z_]+)\s=\s[a-z_]+\.get\(\'', line)
                is_class_assigned = re.match('\s+[^#]self\.\w+\s=\s[a-z\.]*(?P<class_name>[A-Z]\w+)\(.*\)', line)
                is_list_assigned = re.match('\s+[^#]self\.\w+\s=\s\[[a-z\.]*(?P<class_name>[A-Z]\w+)\(.*\).*\]', line)

                if is_class_assigned:
                    class_name = is_class_assigned.group('class_name').strip()
                elif is_list_assigned:
                    class_name = is_list_assigned.group('class_name').strip()
                else:
                    class_name = None

                if class_name not in class_names:
                    class_name = None

                if not has_comment_text and not is_dict_assigned:

                    if is_class_assigned:
                        outline = outline.rstrip() + ' :class:`{}`'.format(class_name)
                    elif is_list_assigned:
                        outline = outline.rstrip() + ' [:class:`{}`]'.format(class_name)

                outline = outline + '\n' if not outline.endswith('\n') else outline

            else:
                outline = line

            source_out.append(outline)

        out_filepath = os.path.join(OUTPUT_PATH, '{}.py'.format(module_name))
        with open(out_filepath, 'w') as f:
            f.writelines(source_out)


if __name__ == '__main__':
    main()
