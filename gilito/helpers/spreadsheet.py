#
# Copyright (C) 2022 Luis López <luis@cuarentaydos.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


import os
import subprocess
import tempfile


def spreadsheet_as_csv(buffer: bytes) -> bytes:
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
        capture_output=True,
        timeout=10,
        env={},  # type: ignore[arg-type]
    )
    os.unlink(tempfilepath)

    call.check_returncode()

    return call.stdout
