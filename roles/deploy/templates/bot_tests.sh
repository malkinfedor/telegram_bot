#!/bin/bash
cd {{ path_app }}/{{ app_name }}
{{ path_app }}/{{ app_name }}/env/bin/python3 -m unittest  -v {{ path_app }}/{{ app_name }}/unit_tests.py
