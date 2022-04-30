import subprocess
import tempfile
import os

from gilito.plugins import Loader


class Plugin(Loader):
    @classmethod
    def can_handle(cls, filename: str) -> bool:
        return filename.lower().endswith("xlsx")

    def load(self, buffer: bytes) -> str:
        fd, tempfilepath = tempfile.mkstemp()
        with os.fdopen(fd, mode="wb") as fh:
            fh.write(buffer)

        # Run unoconv isolated from current environment (i.ex. virtualenv)
        call = subprocess.run(
            [
                "/usr/bin/unoconv",
                "--doctype",
                "spreadsheet",
                "--format",
                "csv",
                "--preserve",
                "--stdout",
                tempfilepath,
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            env={},  # type: ignore[arg-type]
        )
        os.unlink(tempfilepath)

        call.check_returncode()
        return call.stdout.decode("utf-8")
