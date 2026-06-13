# Author = Саллум Фажр
# Group = P3106 
# Date = 06.06.2025
# Variant = 79: binary -> XML

import sys
from binary_storage import deserialize_binary


def escape_xml(s):
    s = str(s)
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    return s


def dict_to_xml(d, indent):
    lines = []
    for k, v in d.items():
        tag = k.replace(' ', '_')
        if isinstance(v, dict):
            lines.append(indent + '<' + tag + '>')
            lines.extend(dict_to_xml(v, indent + '  '))
            lines.append(indent + '</' + tag + '>')
        elif isinstance(v, list):
            lines.append(indent + '<' + tag + '>')
            for item in v:
                if isinstance(item, dict):
                    lines.append(indent + '  <item>')
                    lines.extend(dict_to_xml(item, indent + '    '))
                    lines.append(indent + '  </item>')
                else:
                    lines.append(indent + '  <item>' + escape_xml(item) + '</item>')
            lines.append(indent + '</' + tag + '>')
        else:
            lines.append(indent + '<' + tag + '>' + escape_xml(v) + '</' + tag + '>')
    return lines


def to_xml(data):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<schedule>']
    for item in data:
        day = item.get('day', 'day')
        lines.append('  <day name="' + escape_xml(day) + '">')
        for lesson in item.get('schedule', []):
            lines.append('    <lesson>')
            lines.extend(dict_to_xml(lesson, '      '))
            lines.append('    </lesson>')
        lines.append('  </day>')
    lines.append('</schedule>')
    return '\n'.join(lines)


def convert(binary_path, output_path):
    data = deserialize_binary(binary_path)
    xml = to_xml(data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    return xml


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'data.bin'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'schedule.xml'
    print(convert(src, dst))
