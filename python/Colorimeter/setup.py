"""
Copyright 2010  IO Rodeo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from setuptools import setup

setup(
    name='Colorimeter',
    version='0.1.0',
    author='Will Dickson',
    author_email='will@iorodeo.com',
    packages=[
        'colorimeter',
        'colorimeter/gui',
        'colorimeter/gui/basic',
        'colorimeter/gui/plot',
        'colorimeter/gui/measure',
        'colorimeter/gui/dialog',
        ],
    package_data = { 'colorimeter': ['data/*.yaml']},
    scripts=[
        'bin/colorimeter-main',
        'bin/colorimeter-basic', 
        'bin/colorimeter-plot', 
        'bin/colorimeter-measure',
        ],
    license='LICENSE.txt',
    description="Serial interface and measurement software for IO Rodeo's colorimeter",
    long_description=open('README.txt').read(),
    install_requires= [],
)

