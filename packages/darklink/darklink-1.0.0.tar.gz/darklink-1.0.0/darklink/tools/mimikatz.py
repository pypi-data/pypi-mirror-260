import requests
import zipfile
import io

import darklink.tools


class mimikatz(darklink.tools.Tool):
    """A little tool to play with Windows security. It's now well known to extract plaintexts passwords, hash, PIN code and kerberos tickets from memory"""

    @staticmethod
    def fetch(platform: str, arch: str):
        url = "https://github.com/gentilkiwi/mimikatz/releases/latest/download/mimikatz_trunk.zip"

        response = requests.get(url)

        if not response.ok:
            raise Exception(response.text)

        z = zipfile.ZipFile(io.BytesIO(response.content))

        return "mimikatz.exe", z.read('x64/mimikatz.exe')
