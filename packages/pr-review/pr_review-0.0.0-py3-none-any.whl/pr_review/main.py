from os.path import join
from pr_review.definitions import ROOT_DIR  

from pr_review.config import settings

print(f"USER_TEMPLATE:\n{settings.USER_TEMPLATE}")

# setting_files = join(ROOT_DIR, 'pr_review/settings/check_coding_standards.toml')
# print(setting_files)
