#!/bin/bash
cd {{ path_app }}/{{ app_name }}
{{ path_app }}/{{ app_name }}/env/bin/python3 {{ path_app }}/{{ app_name }}/bot.py
