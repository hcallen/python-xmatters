import inspect
import xmatters.objects
import xmatters.objects.devices
import re
import os

OUTPUT_PATH = '../test'


def main():
    # compile all class names
    class_names = []
    for module_name, module in inspect.getmembers(xmatters.objects, inspect.ismodule):
        for name, class_ in inspect.getmembers(module, inspect.isclass):
            class_names.append(name)

    for module_name, module in inspect.getmembers(xmatters.objects, inspect.ismodule):

        source_out = []
        source_lines = inspect.getsourcelines(module)
        for line in source_lines[0]:

            # check for instance attributes assigned from a dict
            is_dict_assigned = re.match('\s+[^#](?P<attr_name>self\.[a-z_]+)\s=\s[a-z_]+\.get\(\'', line)
            attr_name = is_dict_assigned.group('attr_name') if is_dict_assigned else None

            # check for instance attributes assigned to a class
            is_class_assigned_match = re.match('\s+[^#]self\.\w+\s=\s[a-z\.]*(?P<class_name>[A-Z]\w+)\(.*\)', line)
            class_name = is_class_assigned_match.group('class_name').strip() if is_class_assigned_match else None
            is_class_assigned = class_name in class_names

            has_comment = re.match('^.*\s+#:(?P<comment>.*)\n$', line)
            comment_text = has_comment.group('comment').strip() if has_comment else None

            if is_class_assigned or is_dict_assigned:

                if not has_comment:
                    outline = line.rstrip() + '    #:'
                else:
                    outline = line

                if is_class_assigned and class_name and not comment_text:
                    outline = outline.rstrip() + ' :class:`{}`'.format(class_name)

                outline = outline + '\n' if not outline.endswith('\n') else outline

            else:
                outline = line

            source_out.append(outline)

        out_filepath = os.path.join(OUTPUT_PATH, '{}.py'.format(module_name))
        with open(out_filepath, 'w') as f:
            f.writelines(source_out)


if __name__ == '__main__':
    main()
