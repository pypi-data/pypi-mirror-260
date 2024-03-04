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

# flake8: noqa

from functools import cached_property

from envenom import config, optional, required, subconfig, with_default
from envenom.parsers import as_boolean


@config(namespace=("myapp", "postgres"))
class DatabaseCfg:
    host: str = required()
    port: int = with_default(int, default=5432)
    database: str = required()
    username: str | None = optional()
    password: str | None = optional()
    connection_timeout: int | None = optional(int)
    sslmode_require: bool = with_default(as_boolean, default=False)

    @cached_property
    def connection_string(self) -> str:
        auth = f"{self.username}:{self.password}" if self.password else self.username

        query: dict[str, str] = {}

        if self.connection_timeout:
            query["timeout"] = str(self.connection_timeout)
        if self.sslmode_require:
            query["sslmode"] = "require"

        query_string = "&".join({f"{key}={value}" for key, value in query.items()})

        return (
            f"postgresql+psycopg://{auth}@{self.host}:{self.port}"
            f"/{self.database}?{query_string}"
        )


@config(namespace="myapp")
class AppCfg:
    secret_key: str = required()
    database: DatabaseCfg = subconfig(DatabaseCfg)


if __name__ == "__main__":
    cfg = AppCfg()

    # fmt: off
    print(f"myapp/secret_key: {repr(cfg.secret_key)} {type(cfg.secret_key)}")
    print(f"myapp/db/host: {repr(cfg.database.host)} {type(cfg.database.host)}")
    print(f"myapp/db/port: {repr(cfg.database.port)} {type(cfg.database.port)}")
    print(f"myapp/db/database: {repr(cfg.database.database)} {type(cfg.database.database)}")
    print(f"myapp/db/username: {repr(cfg.database.username)} {type(cfg.database.username)}")
    print(f"myapp/db/password: {repr(cfg.database.password)} {type(cfg.database.password)}")
    print(f"myapp/db/connection_timeout: {repr(cfg.database.connection_timeout)} {type(cfg.database.connection_timeout)}")
    print(f"myapp/db/sslmode_require: {repr(cfg.database.sslmode_require)} {type(cfg.database.sslmode_require)}")
    print(f"myapp/db/connection_string: {repr(cfg.database.connection_string)} {type(cfg.database.connection_string)}")
    # fmt: on
