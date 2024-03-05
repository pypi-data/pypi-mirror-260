# SPDX-FileCopyrightText: 2021 Dalibo
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated, Optional

import pydantic
from pydantic import Field

from .. import types


class ServiceManifest(types.ServiceManifest, service_name="powa"):
    password: Annotated[
        Optional[pydantic.SecretStr],
        Field(description="Password of PostgreSQL role for PoWA.", exclude=True),
    ] = None
