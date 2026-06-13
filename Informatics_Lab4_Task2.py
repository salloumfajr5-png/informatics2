# Author = Саллум Фажр
# Group = P3106 
# Date = 06.06.2025
# Variant = 79: binary -> INI

import sys
from binary_storage import deserialize_binary


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


def convert(binary_path, output_path):
    data = deserialize_binary(binary_path)
    ini = serialize_ini(data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ini)
    return data, ini


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'data.bin'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'schedule_from_bin.ini'
    data, result = convert(src, dst)
    print(result)
