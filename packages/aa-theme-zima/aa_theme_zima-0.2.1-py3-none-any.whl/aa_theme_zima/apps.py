"""
App Config
"""

# Django
from django.apps import AppConfig

# AA Zima Theme
from aa_theme_zima import __version__


class AaThemeConfig(AppConfig):
    """
    App config
    """

    name = "aa_theme_zima"
    label = "aa_theme_zima"
    verbose_name = 'The Zima theme for Alliance Auth v{version}'.format(
        version=__version__
    )
