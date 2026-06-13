# Author = Саллум Фажр
# Group = P3106
# Date = 06.06.2025
# Variant = 79: YAML -> binary -> INI

import sys
from binary_storage import serialize_binary


def parse_value(s):
    s = s.strip()
    if not s:
        return None
    if (s.startswith('"') and s.endswith('"')) or \
       (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if s == 'true':
        return True
    if s == 'false':
        return False
    if s.lstrip('-').isdigit():
        return int(s)
    return s


def get_indent(line):
    count = 0
    for ch in line:
        if ch == ' ':
            count += 1
        else:
            break
    return count


def next_non_empty(lines, start):
    for i in range(start, len(lines)):
        stripped = lines[i].strip()
        if stripped and not stripped.startswith('#'):
            return lines[i]
    return None


def parse_yaml(lines):
    stack = [({}, -1)]

    for i, raw in enumerate(lines):
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue

        indent = get_indent(raw)
        line = raw.strip()

        while len(stack) > 1 and indent <= stack[-1][1]:
            stack.pop()

        parent, parent_indent = stack[-1]

        if line.startswith('- '):
            value = line[2:].strip()

            if isinstance(parent, dict):
                lst = []
                stack[-1] = (lst, stack[-1][1])
                parent = lst

            if ':' in value:
                colon = value.index(':')
                key = value[:colon].strip()
                val = value[colon+1:].strip()
                obj = {key: parse_value(val)}
                parent.append(obj)
                stack.append((obj, indent))
            elif value == '':
                obj = {}
                parent.append(obj)
                stack.append((obj, indent))
            else:
                parent.append(parse_value(value))
            continue

        if line.startswith('-'):
            value = line[1:].strip()
            if isinstance(parent, dict):
                lst = []
                stack[-1] = (lst, stack[-1][1])
                parent = lst
            parent.append(parse_value(value))
            continue

        if ':' in line:
            colon = line.index(':')
            key = line[:colon].strip()
            value = line[colon+1:].strip()

            if value == '':
                nxt = next_non_empty(lines, i + 1)
                if nxt and nxt.lstrip().startswith('-'):
                    obj = []
                else:
                    obj = {}
                parent[key] = obj
                stack.append((obj, indent))
            else:
                parent[key] = parse_value(value)

    return stack[0][0]


def serialize_ini(data):
    lines = []
    if isinstance(data, list):
        for idx, item in enumerate(data, 1):
            day = item.get('day', 'day_' + str(idx))
            schedule = item.get('schedule', [])
            for jdx, lesson in enumerate(schedule, 1):
                section = day + '_' + str(jdx)
                lines.append('[' + section + ']')
                for k, v in lesson.items():
                    if isinstance(v, dict):
                        for sk, sv in v.items():
                            lines.append(k + '_' + sk + ' = ' + str(sv))
                    elif isinstance(v, list):
                        lines.append(k + ' = ' + str(v))
                    else:
                        lines.append(k + ' = ' + str(v))
                lines.append('')
    return '\n'.join(lines)


def convert(input_path, output_path, binary_path='data.bin'):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    data = parse_yaml(lines)
    serialize_binary(data, binary_path)
    ini = serialize_ini(data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ini)
    return ini


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'schedule.yaml'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'schedule.ini'
    print(convert(src, dst))
