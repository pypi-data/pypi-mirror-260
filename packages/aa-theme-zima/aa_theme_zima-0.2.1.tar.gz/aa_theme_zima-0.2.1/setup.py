# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aa_theme_zima']

package_data = \
{'': ['*'],
 'aa_theme_zima': ['static/aa_theme_zima/css/*',
                   'static/aa_theme_zima/icons/*',
                   'static/aa_theme_zima/img/*',
                   'templates/allianceauth/*',
                   'templates/mumbletemps/*',
                   'templates/public/*']}

install_requires = \
['allianceauth>=3.6']

setup_kwargs = {
    'name': 'aa-theme-zima',
    'version': '0.2.1',
    'description': 'Theme for zimacorp.space',
    'long_description': '# Alliance Auth Zima Theme\n\n## Installation\n\n```shell\npip install git+https://gitlab.com/zima-corp/aa-theme-zima.git\n```\n\nNow open your `local.py` and add the following right below your `INSTALLED_APPS`:\n```python\n# Zima Theme - https://gitlab.com/zima-corp/aa-theme-zima\nINSTALLED_APPS.insert(0, "aa_theme_zima")\n```\n\nAfter installation, run the command:\n```shell\npython manage.py collectstatic\n```\n\n## Upgrade\n\n```shell\npython manage.py collectstatic\n```\n\n**Important**\n\nIf you are using [aa-gdpr](https://gitlab.com/tactical-supremacy/aa-gdpr), the template stuff needs to be **after** the `aa-gdpr`\nentry, like this:\n\n```python\n# GDPR Compliance\nINSTALLED_APPS.insert(0, "aagdpr")\nAVOID_CDN = True\n\n\n# Zima Theme - https://gitlab.com/zima-corp/aa-theme-zima\nINSTALLED_APPS.insert(0, "aa_theme_zima")\n```\n',
    'author': 'Boris Talovikov',
    'author_email': 'boris@talovikov.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/zima-corp/aa-theme-zima',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
