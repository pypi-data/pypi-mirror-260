from os.path import join
from dynaconf import Dynaconf

from pr_review.definitions import ROOT_DIR

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[join(ROOT_DIR, f) for f in [
        'pr_review/settings/check_coding_standards.toml',
    ]]
)


# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
