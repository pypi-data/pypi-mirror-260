import typing

from excel_models.typing import CellValue, ColumnValue, CellContext
from ._std import Column


class BaseTypedColumn(Column):
    def _convert_to_python(self, raw: CellValue) -> ColumnValue:
        raise NotImplementedError  # pragma: no cover

    def to_python(self, raw: CellValue, context: CellContext) -> ColumnValue:
        if raw is None:
            return None
        return self._convert_to_python(raw)

    def _convert_from_python(self, value: ColumnValue) -> CellValue:
        raise NotImplementedError  # pragma: no cover

    def from_python(self, value: ColumnValue, context: CellContext) -> CellValue:
        if value is None:
            return None
        return self._convert_from_python(value)


class BaseSimpleTypeColumn(BaseTypedColumn):
    def _convert(self, value: CellValue | ColumnValue) -> ColumnValue | CellValue:
        raise NotImplementedError  # pragma: no cover

    def _convert_to_python(self, raw: CellValue) -> ColumnValue:
        return self._convert(raw)

    def _convert_from_python(self, value: ColumnValue) -> CellValue:
        return self._convert(value)


class StringColumn(BaseSimpleTypeColumn):
    strip: bool = False

    def _convert(self, value) -> str:
        value = str(value)
        if self.strip:
            value = value.strip()
        return value


class IntColumn(BaseSimpleTypeColumn):
    float_strict: bool = True

    def _convert(self, value) -> int:
        if isinstance(value, int):
            return value

        if isinstance(value, float):
            value_int = int(value)
            if value_int != value and self.float_strict:
                raise ValueError(value)
            return value_int

        return int(value)


class FloatColumn(BaseSimpleTypeColumn):
    _convert = float


class BooleanColumn(BaseSimpleTypeColumn):
    truthy: typing.Collection[str] = ()  # values should be lowercase for case-insensitive comparison

    def _convert(self, value) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in self.truthy
        raise ValueError(value)
