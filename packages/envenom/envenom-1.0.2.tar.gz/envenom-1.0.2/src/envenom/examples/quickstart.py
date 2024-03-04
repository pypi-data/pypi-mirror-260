# `envenom` - an elegant application configurator for the more civilized age
# Copyright (C) 2024-  Artur Ciesielski <artur.ciesielski@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from envenom import config, optional, required, with_default
from envenom.parsers import as_boolean


@config(namespace="postgres")
class DatabaseCfg:
    host: str = required()
    port: int = with_default(int, default=5432)
    database: str = required()
    username: str | None = optional()
    password: str | None = optional()
    server_side_cursors: bool = with_default(as_boolean, default=True)


if __name__ == "__main__":
    db_cfg = DatabaseCfg()

    print(f"host: {repr(db_cfg.host)} {type(db_cfg.host)}")
    print(f"port: {repr(db_cfg.port)} {type(db_cfg.port)}")
    print(f"database: {repr(db_cfg.database)} {type(db_cfg.database)}")
    print(f"username: {repr(db_cfg.username)} {type(db_cfg.username)}")
    print(f"password: {repr(db_cfg.password)} {type(db_cfg.password)}")
    print(
        f"server_side_cursors: {repr(db_cfg.server_side_cursors)} "
        f"{type(db_cfg.server_side_cursors)}"
    )
