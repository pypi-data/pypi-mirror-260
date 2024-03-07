import inspect
import io
import re
from abc import ABC, abstractmethod
from enum import Enum, auto
from functools import partial
from typing import Any, Iterator, Optional, Protocol, Type, TypeVar, runtime_checkable

import numpy as np
import torch
from orca_common import ImageFormat, NumericType, NumericTypeAlternative
from PIL import Image as PILImage


class OrcaTypeHandle(ABC):
    """Base class for all Orca types. Derived classes represent the types of columns in a table.

    ---- How to declare new types ----
    1. Create a new class that inherits from OrcaTypeHandle
    2. Decorate the class with the `@register_column_type` decorator
    3. Implement the `parameters` property to return the type parameters as a list
    4. Make sure that the constructor takes the type parameters as arguments in the same order as they are returned by the `parameters` property
    4. Make sure the constructor can accept type parameters as `ActualType | str | None` (where `ActualType` is the type of the parameter)
    5. Implement the `__getitem__` method to allow type parameters to be specified using the `[]` operator

    ---- How to use the derived classes ----
    >>> column.type = VectorT[768]
    >>> column.type = VectorT[768].notnull
    >>> column.type = VectorT[768].unique
    >>> column.type = VectorT[768].notnull.unique

    """

    # NOTE: This is updated by the @register_column_type decorator and manually for numeric types
    _name_to_type: dict[str, Type] = {}  # Maps type names to their corresponding classes

    def __init__(self, t_name: str, notnull: bool = False, unique: bool = False):
        self.t_name = t_name
        self._notnull = notnull
        self._unique = unique

    @classmethod
    def from_string(cls, type_str: str) -> "OrcaTypeHandle":
        """Parses a type string into an OrcaTypeHandle.
        Examples: `float`, `vector[128] NOT NULL UNIQUE`, or `image[PNG] UNIQUE`.
        NOTE: Essentially, you can reconstruct a type after using str(), repr(), or the type's `full_name` property.
        """

        # This regex has 4 capture groups that match the following for "vector[128] NOT NULL UNIQUE":
        # 1. The type name (e.g., "vector") - required
        # 2. The type parameters (e.g., "128" for a vector) - optional
        # 3. The NOT NULL constraint - optional
        # 4. The UNIQUE constraint - optional
        match = re.match(r"(\w+)(?:\[(.*?)\])?(?:\s(NOT NULL))?(?:\s(UNIQUE))?$", type_str)
        if not match:
            raise ValueError(f"Invalid type string: {type_str}")
        t_name, params, notnull, unique = match.groups()
        notnull = notnull is not None
        unique = unique is not None
        params = params.split(",") if params else []
        if t_name not in cls._name_to_type:
            raise ValueError(f"Unknown type: {t_name}")

        return cls._name_to_type[t_name](*params, notnull=notnull, unique=unique)

    def __eq__(self, other: Any):
        """Returns True if the two types are equal, False otherwise."""
        if not isinstance(other, OrcaTypeHandle):
            return False
        return (
            self.t_name == other.t_name
            and self._unique == other._unique
            and self._notnull == other._notnull
            and self.parameters == other.parameters
        )

    def __hash__(self):
        """Returns a hash of the type."""
        return hash((self.t_name, self._unique, self._notnull, *self.parameters))

    def __str__(self):
        """Returns the type name, including type parameters and constraints.
        Example: `vector[128] NOT NULL UNIQUE` or `image[PNG] UNIQUE`."""
        return f"{self.full_name}" + (" NOT NULL" if self._notnull else "") + (" UNIQUE" if self._unique else "")

    def __repr__(self):
        return self.__str__()

    def _clone_with_overrides(self, **kwargs):
        """Returns a copy of this type with the specified overrides."""
        cls = type(self)
        args = inspect.signature(cls.__init__).parameters

        def get_arg(arg):
            if arg in kwargs:
                return kwargs[arg]
            elif arg in args:
                if arg == "unique" or arg == "notnull":
                    return getattr(self, "_" + arg)
                # First check for a private field, then a public one
                return getattr(self, arg)
            else:
                return None

        init_args = {arg: get_arg(arg) for arg in args if arg != "self"}
        return cls(**init_args)

    @property
    def is_vector(self) -> bool:
        return False

    @property
    def vector_shape(self) -> None | int | tuple[int, ...]:
        """Returns the shape of the vector, or None if this is not a vector type."""
        return None

    @property
    def numpy_dtype(self) -> Optional[np.dtype]:
        """Returns the corresponding numpy type, or None if it doesn't exist."""
        return object

    @property
    def parameters(self) -> list[Any]:
        """Returns the type parameters as a tuple.
        NOTE: These should be in the same order as the parameters in the constructor"""
        return []  # by default, there are no parameters

    @property
    def notnull(self):
        """Returns a copy of this type with the NOT NULL constraint."""
        return self._clone_with_overrides(notnull=True)

    @property
    def unique(self):
        """Returns a copy of this type with the UNIQUE constraint."""
        return self._clone_with_overrides(unique=True)

    def _get_param_strings(self) -> Iterator[str]:
        """Iterates through the string representations of the type parameters."""
        if any(param is None for param in self.parameters):
            assert all(
                param is None for param in self.parameters
            ), "Either all parameters must be None or none of them can be None"
            return

        for param in self.parameters:
            if isinstance(param, Enum):
                yield param.name
            else:
                yield str(param)

    @property
    def full_name(self):
        """Returns the full name of the type, including type parameters.
        For example, `vector[128]` or `image[PNG]`."""
        param_strings = list(self._get_param_strings())
        if len(param_strings) > 0:
            return f"{self.t_name}[{','.join(param_strings)}]"
        else:
            return self.t_name


class NumericTypeHandle(OrcaTypeHandle):
    """Represents a numeric column type, such as `integer` or `float` that has
    a specific data type, e.g., float16 or int32."""

    def __init__(
        self,
        dtype: NumericType | NumericTypeAlternative,
        length: Optional[int] = None,
        notnull: bool = False,
        unique: bool = False,
    ):
        if length is not None and isinstance(length, str):
            try:
                length = int(length)
            except ValueError:
                raise ValueError(f"Invalid length: {length}. Use None, an integer or a int string.")
        if not isinstance(dtype, NumericType):
            try:
                dtype = NumericType.from_type(dtype)
                assert isinstance(dtype, NumericType), f"Invalid dtype: {dtype}"
            except ValueError:
                raise ValueError(f"Invalid dtype: {dtype}. Use a torch/numpy type, a string, or a NumericType.")

        super().__init__(dtype.name, notnull, unique)

        self.dtype = dtype
        self.length = length

    def __getitem__(self, length: int) -> "NumericTypeHandle":
        return self._clone_with_overrides(length=length)

    @property
    def is_vector(self) -> bool:
        """Returns True if this is a vector type, False otherwise."""
        return self.length is not None

    @property
    def vector_shape(self) -> None | int | tuple[int, ...]:
        """Returns the shape of the vector, or None if this is not a vector type."""
        return self.length

    @property
    def is_scalar(self) -> bool:
        """Returns True if this is a scalar type, False otherwise."""
        return self.length is None

    @property
    def parameters(self):
        return [self.dtype, self.length]

    @property
    def torch_dtype(self) -> Optional[torch.dtype]:
        """Returns the corresponding torch type, or None if it doesn't exist."""
        return self.dtype.torch_dtype

    @property
    def numpy_dtype(self) -> Optional[np.dtype]:
        """Returns the corresponding numpy type, or None if it doesn't exist."""
        return self.dtype.numpy_dtype

    @property
    def full_name(self) -> str:
        """Returns the full name of the type, e.g., `int32`."""
        if self.length is None:
            return self.t_name
        return f"{self.t_name}[{self.length}]"


# Add all numeric types to the type dictionary
numeric_type_dict = {name: partial(NumericTypeHandle, dtype) for name, dtype in NumericType.__members__.items()}
# These are added for backwards compatibility
numeric_type_dict.update(
    {
        "integer": partial(NumericTypeHandle, NumericType.int32),
        "float": partial(NumericTypeHandle, NumericType.float32),
        "vector": partial(NumericTypeHandle, NumericType.float64),
    }
)

OrcaTypeHandle._name_to_type.update(numeric_type_dict)


def register_column_type(type_name: str):
    """Decorator for registering a new OrcaTypeHandle
    NOTE: This is required to be able to instantiate the type using OrcaHandle.from_string(...)
    """

    def wrapper(cls: Type[OrcaTypeHandle]):
        OrcaTypeHandle._name_to_type[type_name] = cls
        return cls

    return wrapper


T = TypeVar("T")


@runtime_checkable
class CustomSerializable(Protocol[T]):
    """Protocol for column types that should be transferred as a file instead of a value."""

    @abstractmethod
    def binary_serialize(self, value: T) -> io.BytesIO:
        """Serializes the value as a binary stream, so we can send it to the server."""
        pass

    @abstractmethod
    def msgpack_deserialize(self, value: dict[str, Any]) -> T:
        """Deserializes the value from a msgpack-compatible dictionary."""
        pass


@register_column_type("text")
class TextTypeHandle(OrcaTypeHandle):
    """Represents a text column type, such as `text` or `text NOT NULL UNIQUE`."""

    def __init__(self, notnull: bool = False, unique: bool = False):
        super().__init__("text", notnull, unique)

    @property
    def numpy_dtype(self) -> Optional[np.dtype]:
        """Returns the corresponding numpy type: np.str_"""
        return np.str_


@register_column_type("bool")
class BoolTypeHandle(OrcaTypeHandle):
    """Represents a boolean column type, such as `bool` or `bool NOT NULL UNIQUE`."""

    def __init__(self, notnull: bool = False, unique: bool = False):
        super().__init__("bool", notnull, unique)

    @property
    def numpy_dtype(self) -> Optional[np.dtype]:
        """Returns the corresponding numpy type: np.bool_"""
        return np.bool_


@register_column_type("document")
class DocumentTypeHandle(OrcaTypeHandle):
    """Represents a document column type, such as `document` or `document NOT NULL UNIQUE`."""

    def __init__(self, notnull: bool = False, unique: bool = False):
        super().__init__("document", notnull, unique)

    @property
    def numpy_dtype(self) -> Optional[np.dtype]:
        """Returns the corresponding numpy type, or None if it doesn't exist."""
        return np.str_


@register_column_type("image")
class ImageTypeHandle(
    OrcaTypeHandle,
    CustomSerializable[PILImage.Image],
):
    """Represents an image column type, such as `image[PNG]` or `image[PNG] NOT NULL UNIQUE`."""

    def __init__(
        self,
        format: ImageFormat | str | None,
        notnull: bool = False,
        unique: bool = False,
    ):
        super().__init__("image", notnull, unique)
        if isinstance(format, str):
            format = ImageFormat(format)

        self.format = format

    @property
    def parameters(self):
        return [self.format]

    def __getitem__(self, format: ImageFormat | str) -> "ImageTypeHandle":
        return self._clone_with_overrides(format=format)

    ##### CustomSerializable methods #####

    def binary_serialize(self, value: PILImage.Image) -> io.BytesIO:
        """Serializes the image as a binary stream, so we can send it to the server."""
        # We're not using a context manager clarify that the stream is open after this function returns
        byte_stream = io.BytesIO()
        value.save(byte_stream, format=self.format.name)
        byte_stream.seek(0)  # Reset the pointer to the beginning of the stream
        return byte_stream

    def msgpack_deserialize(self, value: dict[str, Any]) -> PILImage.Image:
        """Deserializes the image from a msgpack-compatible dictionary."""
        image_data = value.get(f"__{self.full_name}__", None)
        assert image_data is not None, f"Expected image data for type {self.full_name}, got {value} instead"
        byte_stream = io.BytesIO(image_data)
        image = PILImage.open(byte_stream, formats=[self.format.name])
        return image


# Numeric Types
IntT = NumericTypeHandle(dtype=NumericType.int32)
FloatT = NumericTypeHandle(dtype=NumericType.float32)

Int8T = NumericTypeHandle(dtype=NumericType.int8)
Int16T = NumericTypeHandle(dtype=NumericType.int16)
Int32T = NumericTypeHandle(dtype=NumericType.int32)
Int64T = NumericTypeHandle(dtype=NumericType.int64)

UInt8T = NumericTypeHandle(dtype=NumericType.uint8)
UInt16T = NumericTypeHandle(dtype=NumericType.uint16)
UInt32T = NumericTypeHandle(dtype=NumericType.uint32)
UInt64T = NumericTypeHandle(dtype=NumericType.uint64)

Float16T = NumericTypeHandle(dtype=NumericType.float16)
Float32T = NumericTypeHandle(dtype=NumericType.float32)
Float64T = NumericTypeHandle(dtype=NumericType.float64)

BFloat16T = NumericTypeHandle(NumericType.bfloat16)


# Primitive types
TextT = TextTypeHandle()
BoolT = BoolTypeHandle()
DocumentT = DocumentTypeHandle()

# Parameterized types
VectorT = Float64T
ImageT = ImageTypeHandle(None)
