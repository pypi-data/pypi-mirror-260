import requests
import gzip
import io
import re

import darklink.tools


class chisel(darklink.tools.Tool):
    """Chisel is a fast TCP/UDP tunnel, transported over HTTP, secured via SSH."""

    @staticmethod
    def fetch(platform: str, arch: str):
        platform = "windows" if platform is None else platform
        arch = "amd64" if arch is None else arch

        release_url = "https://api.github.com/repos/jpillora/chisel/releases/latest"

        response = requests.get(release_url)

        if not response.ok:
            raise Exception(response.text)

        for asset in response.json()["assets"]:
            # Example: chisel_1.9.1_windows_amd64.gz
            if re.match(rf"chisel_\d+\.\d+\.\d+_{platform}_{arch}\.gz", asset["name"]):
                download_url = asset["browser_download_url"]
                break
        else:
            raise Exception("Could not find asset in GitHub release")

        response = requests.get(download_url)

        if not response.ok:
            raise Exception(response.text)

        z = gzip.GzipFile(fileobj=io.BytesIO(response.content))

        if platform == "windows":
            return "chisel.exe", z.read()
        else:
            return "chisel", z.read()
