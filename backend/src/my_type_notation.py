import datetime
from typing import Annotated

from sqlalchemy import text  # , ForeignKey
from sqlalchemy.orm import mapped_column

added_at = Annotated[
    datetime.datetime,
    mapped_column(
        nullable=True, server_default=text("TIMEZONE('utc', now())")
    ),
]

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

# intfk = Annotated[int, mapped_column(ForeignKey(
#   "match.id", primary_key=True)
# )]
