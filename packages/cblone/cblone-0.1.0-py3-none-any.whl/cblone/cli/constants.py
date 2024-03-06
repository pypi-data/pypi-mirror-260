from pathlib import Path

from platformdirs import user_documents_dir

DEFAULT_ENV_VARIABLE = "CODEBERG_ACCESS_TOKEN"

BASE_URL = "https://codeberg.org/api/v1"
REPOS_ENDPOINT = "/user/repos"

BASE_OUTPUT_FOLDER = Path(user_documents_dir()) / "Backups" / "Repos" / "Codeberg"
