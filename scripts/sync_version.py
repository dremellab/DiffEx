# scripts/sync_version.py
import re
from pathlib import Path

# Read version from __init__.py
version_file = Path("diffex/__init__.py").read_text()
version = re.search(r'__version__\s*=\s*["\'](.*?)["\']', version_file).group(1)

# Update pyproject.toml
pyproject_path = Path("pyproject.toml")
pyproject = pyproject_path.read_text()
pyproject = re.sub(r'version\s*=\s*["\'].*?["\']', f'version = \"{version}\"', pyproject)
pyproject_path.write_text(pyproject)

print(f"✅ Synced pyproject.toml to version {version}")

