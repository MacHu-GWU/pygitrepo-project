#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package Description.
"""

__version__ = "0.0.1"
__short_description__ = "Package short description."
__license__ = "{{ license }}"
{% if author_name -%}
__author__ = "{{ author_name }}"
{% endif -%}
{% if __author_email__ -%}
__author_email__ = "{{ author_email }}"
{% endif -%}
{% if __maintainer__ -%}
__maintainer__ = "{{ maintainer_name }}"
{% endif -%}
{% if __maintainer_email__ -%}
__maintainer_email__ = "{{ maintainer_email }}"
{% endif -%}
__github_username__ = "{{ github_username }}"
