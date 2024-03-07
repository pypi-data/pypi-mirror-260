from typing import Union

from orca_common import Order

LiteralType = Union[int, str, float, bool]


OperableType = Union[LiteralType, "Operable"]


class Operable:
    def __eq__(self, value: OperableType):
        return OrcaExpr("$EQ", (self, value))

    def __ne__(self, value: OperableType):
        return OrcaExpr("$NEQ", (self, value))

    def __lt__(self, value: OperableType):
        return OrcaExpr("$LT", (self, value))

    def __le__(self, value: OperableType):
        return OrcaExpr("$LTE", (self, value))

    def __gt__(self, value: OperableType):
        return OrcaExpr("$GT", (self, value))

    def __ge__(self, value: OperableType):
        return OrcaExpr("$GTE", (self, value))

    def __add__(self, value: OperableType):
        return OrcaExpr("$ADD", (self, value))

    def __radd__(self, value: OperableType):
        return OrcaExpr("$ADD", (value, self))

    def __sub__(self, value: OperableType):
        return OrcaExpr("$SUB", (self, value))

    def __rsub__(self, value: OperableType):
        return OrcaExpr("$SUB", (value, self))

    def __mul__(self, value: OperableType):
        return OrcaExpr("$MUL", (self, value))

    def __rmul__(self, value: OperableType):
        return OrcaExpr("$MUL", (value, self))

    def __truediv__(self, value: OperableType):
        return OrcaExpr("$DIV", (self, value))

    def __rtruediv__(self, value: OperableType):
        return OrcaExpr("$DIV", (value, self))

    def __and__(self, value: OperableType):
        return OrcaExpr("$&", (self, value))

    def __or__(self, value: OperableType):
        return OrcaExpr("$|", (self, value))

    def _in(self, *value: OperableType):
        if len(value) == 1 and isinstance(value[0], OrcaExpr) and value[0].op == "$ARRAY":
            val = value[0]
        else:
            val = OrcaExpr("$ARRAY", value)
        return OrcaExpr("$CONTAINS", (val, self))


class OrcaExpr(Operable):
    op: str
    args: tuple[OperableType, ...]

    def __init__(self, op: str, args: tuple[OperableType, ...]):
        self.op = op
        self.args = args

    def _serialize_arg(self, arg: OperableType):
        if isinstance(arg, OrcaExpr):
            return arg.as_serializable()
        elif isinstance(arg, ColumnHandle):
            return arg.as_serializable()
        elif isinstance(arg, str):
            return f"'{arg}'"
        else:
            return arg

    def as_serializable(self):
        return {
            "op": self.op,
            "args": [self._serialize_arg(arg) for arg in self.args],
        }

    def __repr__(self):
        return f"OrcaExpr<{self.op}({', '.join(repr(arg) for arg in self.args)})>"


class ColumnHandle(Operable):
    def __init__(self, db_name: str, table_name: str, column_name: str):
        self.db_name = db_name
        self.table_name = table_name
        self.column_name = column_name

    def __repr__(self):
        return f"ColumnHandle<{self.table_name}.{self.column_name}>"

    def as_serializable(self):
        return f"{self.table_name}.{self.column_name}"

    @property
    def ASC(self) -> tuple[str, Order]:
        """Return a tuple of the column name and the ascending order.
        This can be used with TableHandle.order_by() to sort this column in ascending order
        """
        return (self.column_name, Order.ASCENDING)

    @property
    def DESC(self) -> tuple[str, Order]:
        """Return a tuple of the column name and the descending order.
        This can be used with TableHandle.order_by() to sort this column in descending order
        """
        return (self.column_name, Order.DESCENDING)
