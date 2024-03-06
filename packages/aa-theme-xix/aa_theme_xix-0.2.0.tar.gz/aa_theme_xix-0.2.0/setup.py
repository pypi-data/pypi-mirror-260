# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aa_theme_xix']

package_data = \
{'': ['*'],
 'aa_theme_xix': ['static/aa_theme_xix/css/*',
                  'static/aa_theme_xix/icons/*',
                  'static/aa_theme_xix/img/*',
                  'templates/allianceauth/*',
                  'templates/public/*']}

install_requires = \
['allianceauth>=3.6']

setup_kwargs = {
    'name': 'aa-theme-xix',
    'version': '0.2.0',
    'description': 'Theme for auth.legionofdeath.ru',
    'long_description': '# Alliance Auth XIX Theme\n\n## Installation\n\n```shell\nsudo su allianceserver\ncd\nsource /home/allianceserver/venv/auth/bin/activate\ngit clone https://gitlab.com/legion-of-xxdeathxx/aa-theme-xix.git\npip install -e aa-theme-xix/\n```\n\nNow open your `local.py` and add the following right below your `INSTALLED_APPS`:\n```shell\nnano myauth/myauth/settings/local.py\n```\n```python\n# XIX Theme - https://gitlab.com/legion-of-xxdeathxx/aa-theme-xix\nINSTALLED_APPS.insert(0, "aa_theme_xix")\n```\n\nAfter installation, run the command:\n```shell\npython /home/allianceserver/myauth/manage.py collectstatic --noinput\n```\n\n**Important**\n\nIf you are using [aa-gdpr](https://gitlab.com/tactical-supremacy/aa-gdpr), the template stuff needs to be **after** the `aa-gdpr`\nentry, like this:\n\n```python\n# GDPR Compliance\nINSTALLED_APPS.insert(0, "aagdpr")\nAVOID_CDN = True\n\n\n# XIX Theme - https://gitlab.com/legion-of-xxdeathxx/aa-theme-xix\nINSTALLED_APPS.insert(0, "aa_theme_xix")\n```\n\n\n## Updating\n```shell\nsudo su allianceserver\ncd\nsource /home/allianceserver/venv/auth/bin/activate\ncd aa-theme-xix/\ngit pull\ncd ..\npip install -e aa-theme-xix/\n```\n\nAfter updating, run the command:\n```shell\npython /home/allianceserver/myauth/manage.py collectstatic --noinput\n```\n',
    'author': 'Boris Talovikov',
    'author_email': 'boris@talovikov.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/legion-of-xxdeathxx/aa-theme-xix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
