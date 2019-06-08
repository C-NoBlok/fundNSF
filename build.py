"""Build script for fundNSF and pushes to PyPi."""
import os
import fileinput
import re

parsed_version = None
version_number = None


v_number = re.compile("version='[0-9]+\.[0-9]+\.[0-9]+'")

def increment_version(re_version):
    input_string = re_version.split('=')
    version_ = input_string[-1][1:-1]
    version_parts = version_.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    version_ = '.'.join(version_parts)
    output_string = "version='{}'".format(version_)
    return output_string

def get_version(re_version):
    input_string = re_version.split('=')
    version_ = input_string[-1][1:-1]
    return version_


with fileinput.FileInput('setup.py', inplace=True, backup='.bak') as file:
    for line in file:
        match = v_number.search(line)
        if match is not None:
            parsed_version = match[0]
            version_number = get_version(increment_version(parsed_version))
            line = re.sub(v_number, increment_version(parsed_version), line)
        print(line, end='')

'''
with open('setup.py', 'r') as f:
    for line in f:
        match = v_number.search(line)
        if match is not None:
            version = match[0]
            line = re.sub(v_number, increment_version(version), line)
        print(line)

print(increment_version(version))
'''

os.system('python3 setup.py sdist bdist_wheel')

push_to_PyPi = input('Would you like to deploy to PyPi? (y/n)\n')

if push_to_PyPi.lower() == 'y':
    os.system('twine upload dist/fundNSF-{}-py3-none-any.whl'.format(version_number))
