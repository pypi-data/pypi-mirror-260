from _typeshed import Incomplete
from datasurface.md.Governance import InfrastructureLocation as InfrastructureLocation, URLSQLDatabase as URLSQLDatabase

class DataBricksWarehouse(URLSQLDatabase):
    httpPath: Incomplete
    catalogName: Incomplete
    schemaName: Incomplete
    def __init__(self, name: str, location: InfrastructureLocation, address: str, http_path: str, catalogName: str, schemaName: str) -> None: ...
    def __eq__(self, __value: object) -> bool: ...
    def __hash__(self) -> int: ...
