"""
App Config
"""

# Django
from django.apps import AppConfig

# AA Theme XIX XIX
from aa_theme_xix import __version__


class AaThemeConfig(AppConfig):
    """
    App config
    """

    name = "aa_theme_xix"
    label = "aa_theme_xix"
    verbose_name = 'The XIX theme for Alliance Auth v{version}'.format(
        version=__version__
    )
