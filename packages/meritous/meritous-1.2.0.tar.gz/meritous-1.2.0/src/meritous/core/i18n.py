import os
import locale
import toml
from dotmap import DotMap


def get_locale_file():
    lang_code, encoding = locale.getlocale()
    lang_code, country_code = lang_code.split('_')
    with open('{0}/i18n_data/{1}.toml'.format(os.path.dirname(__file__), lang_code)) as f:
        data = toml.load(f)
        return DotMap(data)


text = get_locale_file()
