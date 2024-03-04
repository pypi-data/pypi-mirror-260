from os.path import abspath, dirname


# 末尾の "/pr_review"を削除. これでプロジェクトのルートへの正しいパスとなる。(pyproject.tomlがあるディレクトリ)
def remove_trailing_path(original_path: str, trailing_path: str = "/pr_review") -> str:
    if original_path.endswith(trailing_path):
        # 末尾のパターンを削除
        return original_path[:-len(trailing_path)]
    else:
        # 末尾のパターンが見つからなければ、元の文字列をそのまま返す
        return original_path

here = dirname(abspath(__file__))

# PR-Reviewプロジェクトのルートディレクトリへの相対パス 
# 他のファイルから from pr_review.definitions import ROOT_DIRでアクセスできる
ROOT_DIR = remove_trailing_path(here) 
