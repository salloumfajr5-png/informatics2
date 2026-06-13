# Author = Саллум Фажр
# Group = P3106
# Date = 06.06.2025
# Variant = 79: YAML -> INI with libraries

import sys
import yaml
import configparser


def convert(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    config = configparser.ConfigParser()
    for item in data:
        day = item.get('day', 'day')
        schedule = item.get('schedule', [])
        for idx, lesson in enumerate(schedule, 1):
            section = day + '_' + str(idx)
            flat = {}
            for k, v in lesson.items():
                if isinstance(v, dict):
                    for sk, sv in v.items():
                        flat[k + '_' + sk] = str(sv)
                elif isinstance(v, list):
                    flat[k] = str(v)
                else:
                    flat[k] = str(v)
            config[section] = flat

    with open(output_path, 'w', encoding='utf-8') as f:
        config.write(f)


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'schedule.yaml'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'schedule_lib.ini'
    convert(src, dst)
    with open(dst, 'r', encoding='utf-8') as f:
        print(f.read())
