import platform
from pathlib import Path
import urllib.request
from zipfile import ZipFile


ARCHITECTURES = {
    "x86_64": "x86_64",
    "amd64": "x86_64",
    "aarch64": "aarch64",
    "arm64": "aarch64",
}

OPERATING_SYSTEMS = {
    "windows": "windows",
    "linux": "linux",
    "darwin": "macos",
}

BASE_URL = "https://github.com/Chnoblouch/banjo-releases/releases/latest/download"

arch = ARCHITECTURES[platform.machine().lower()]
os = OPERATING_SYSTEMS[platform.system().lower()]
target = f"{arch}-{os}"

print(f"Platform: {target}")

install_dir = Path.home() / ".banjo"
if not install_dir.exists():
    install_dir.mkdir()

print(f"Install directory: {install_dir}")

zip_name = f"banjo-{target}.zip"
url = f"{BASE_URL}/{zip_name}"
print(f"Download URL: {url}")

print(f"\nDownloading...")

zip_path = install_dir / zip_name
urllib.request.urlretrieve(url, zip_path)

print(f"Extracting...")

zip_ref = ZipFile(zip_path, "r")

for member in zip_ref.filelist:
    prefix = f"banjo-{target}/"
    if member.filename == prefix or not member.filename.startswith(prefix):
        continue

    member.filename = member.filename[len(prefix):]
    zip_ref.extract(member, install_dir)

zip_ref.close()
zip_path.unlink()

print("All done!")

print("\nRun this to add banjo to your path:")

bin_dir = install_dir / "bin"

if os == "windows":
    print(f"$ENV:PATH=\"$ENV:PATH;{bin_dir}\"")
else:
    print(f"export PATH=\"$PATH:{bin_dir}\"")