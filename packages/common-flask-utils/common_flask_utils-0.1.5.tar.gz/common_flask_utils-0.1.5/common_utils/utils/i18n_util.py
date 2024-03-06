import i18n
from i18n import t
from os.path import join, dirname, abspath

i18n.set("file_format", "yaml")
i18n.set("locale", "zh")
i18n.load_path.append(join(abspath(dirname(dirname(__file__))), "i18n"))

__all__ = ["t"]
