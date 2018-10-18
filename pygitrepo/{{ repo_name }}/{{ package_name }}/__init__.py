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
{% if author_email -%}
__author_email__ = "{{ author_email }}"
{% endif -%}
{% if maintainer_name -%}
__maintainer__ = "{{ maintainer_name }}"
{% endif -%}
{% if maintainer_email -%}
__maintainer_email__ = "{{ maintainer_email }}"
{% endif -%}
__github_username__ = "{{ github_username }}"
