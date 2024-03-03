from _typeshed import Incomplete
from datasurface.md.Governance import InfrastructureLocation as InfrastructureLocation, URLSQLDatabase as URLSQLDatabase
from typing import Optional

class SnowFlakeDatabase(URLSQLDatabase):
    account: Incomplete
    warehouse: Incomplete
    def __init__(self, name: str, location: InfrastructureLocation, url: str, databaseName: str, account: str, warehouse: Optional[str] = None) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, __value: object) -> bool: ...
