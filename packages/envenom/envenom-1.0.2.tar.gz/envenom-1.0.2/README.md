<!-- `envenom` - an elegant application configurator for the more civilized age
Copyright (C) 2024-  Artur Ciesielski <artur.ciesielski@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. -->

# `envenom`

[![pipeline status](https://gitlab.com/python-arcana/envenom/badges/main/pipeline.svg)](https://gitlab.com/python-arcana/envenom/-/commits/main)
[![coverage report](https://gitlab.com/python-arcana/envenom/badges/main/coverage.svg)](https://gitlab.com/python-arcana/envenom/-/commits/main)
[![latest release](https://gitlab.com/python-arcana/envenom/-/badges/release.svg)](https://gitlab.com/python-arcana/envenom/-/releases)

---

`envenom` is an elegant application configurator for the more civilized age.

`envenom` is written with simplicity and type safety in mind. It allows
you to express your application configuration declaratively in a dataclass-like
format while providing your application with type information about each entry,
its nullability and default values.

`envenom` is designed with modern usecases in mind, allowing for pulling configuration
from environment variables or files for more sophisticated deployments on platforms
like Kubernetes.

## Quickstart guide

`main.py`:

```python
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
```

Run `python main.py`:

```
Traceback (most recent call last):
    ...
    raise MissingConfiguration(self.env_name)
envenom.errors.MissingConfiguration: 'POSTGRES__HOST'
```

Run:

```bash
POSTGRES__HOST="postgres" \
POSTGRES__DATABASE="database-name" \
POSTGRES__USERNAME="user" \
POSTGRES__SERVER_SIDE_CURSORS="f" \
python main.py
```

```
host: 'postgres' <class 'str'>
port: 5432 <class 'int'>
database: 'database-name' <class 'str'>
username: 'user' <class 'str'>
password: None <class 'NoneType'>
server_side_cursors: False <class 'bool'>
```

## Getting started

See the [wiki](https://gitlab.com/python-arcana/envenom/-/wikis/Home) for more info.
