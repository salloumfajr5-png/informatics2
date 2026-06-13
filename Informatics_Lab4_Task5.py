# Author = Саллум Фажр
# Group = P3106 
# Date = 06.06.2025
# Variant = 79: performance comparison x100

import time
import sys
import yaml
import configparser

sys.path.insert(0, '.')
import Informatics_Lab4_Task1 as task1

YAML_FILE = 'schedule.yaml'
N = 100


def run_manual():
    with open(YAML_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    data = task1.parse_yaml(lines)
    task1.serialize_ini(data)


def run_library():
    with open(YAML_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    config = configparser.ConfigParser()
    for item in data:
        day = item.get('day', 'day')
        for idx, lesson in enumerate(item.get('schedule', []), 1):
            flat = {}
            for k, v in lesson.items():
                if isinstance(v, dict):
                    for sk, sv in v.items():
                        flat[k + '_' + sk] = str(sv)
                elif isinstance(v, list):
                    flat[k] = str(v)
                else:
                    flat[k] = str(v)
            config[day + '_' + str(idx)] = flat


t0 = time.perf_counter()
for _ in range(N):
    run_manual()
t_manual = time.perf_counter() - t0

t0 = time.perf_counter()
for _ in range(N):
    run_library()
t_lib = time.perf_counter() - t0

print('N =', N)
print('manual: {:.4f} sec'.format(t_manual))
print('library: {:.4f} sec'.format(t_lib))
print('ratio: {:.2f}x'.format(t_lib / t_manual))
