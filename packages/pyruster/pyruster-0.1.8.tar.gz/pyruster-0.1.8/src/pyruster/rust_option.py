from typing import TypeVar, Generic, Optional, Callable, Tuple

T = TypeVar('T')
U = TypeVar('U')
R = TypeVar('R')


class Option(Generic[T]):

    def __init__(self, val: Optional[T]):
        self.__val: Optional[T] = val

    @staticmethod
    def Some(val: T) -> 'Option[T]':
        return Option(val=val)

    @staticmethod
    def None_() -> 'Option[T]':
        return Option(val=None)

    def is_some(self) -> bool:
        return self.__val is not None

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        return f(self.__val) if self.is_some() else False

    def is_none(self) -> bool:
        return not self.is_some()

    def expect(self, msg: str) -> T:
        if self.is_some():
            return self.__val
        else:
            raise ValueError(msg)

    def unwrap(self) -> T:
        if self.is_some():
            return self.__val
        else:
            raise ValueError("Option is None.")

    def unwrap_or(self, default: T) -> T:
        if self.is_some():
            return self.__val
        else:
            return default

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        if self.is_some():
            return self.__val
        else:
            return f()

    def map(self, f: Callable[[T], U]) -> 'Option[U]':
        if self.is_some():
            return Option.Some(f(self.__val))
        else:
            return Option.None_()

    def inspect(self, f: Callable[[T], None]):
        if self.is_some():
            f(self.__val)
        return self

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        if self.is_some():
            return f(self.__val)
        else:
            return default

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        if self.is_some():
            return f(self.__val)
        else:
            default()

    def ok_or(self, err: str):
        from .rust_result import Result
        if self.is_some():
            return Result.Ok(self.__val)
        else:
            return Result.Err(err)

    def ok_or_else(self, err: Callable[[], str]):
        from .rust_result import Result
        if self.is_some():
            return Result.Ok(self.__val)
        else:
            return Result.Err(err())

    def and_(self, optb: 'Option[U]') -> 'Option[U]':
        if self.is_some():
            return optb
        else:
            return Option.None_()

    def and_then(self, f: Callable[[T], 'Option[U]']) -> 'Option[U]':
        if self.is_some():
            return f(self.__val)
        else:
            return Option.None_()

    def filter(self, predicate: Callable[[T], bool]) -> 'Option[T]':
        if self.is_some():
            if predicate(self.__val):
                return Option.Some(self.__val)
        return Option.None_()

    def or_(self, optb: 'Option[T]') -> 'Option[T]':
        if self.is_none():
            return optb
        return Option.Some(self.__val)

    def or_else(self, f: Callable[[], 'Option[T]']) -> 'Option[T]':
        if self.is_none():
            return f()
        return Option.Some(self.__val)

    def xor(self, optb: 'Option[T]') -> 'Option[T]':
        if self.is_some() and optb.is_none():
            return Option.Some(self.__val)
        elif self.is_none() and optb.is_some():
            return optb
        else:
            return Option.None_()

    def zip(self, other: 'Option[U]') -> 'Option[Tuple[T, U]]':
        if self.is_some() and other.is_some():
            return Option.Some((self.__val, other.__val))
        return Option.None_()

    def zip_with(self, other: 'Option[U]', f: Callable[[T, U], R]) -> 'Option[R]':
        if self.is_some() and other.is_some():
            return Option.Some(f(self.__val, other.__val))
        return Option.None_()

    def unzip(self) -> 'Tuple[Option[T], Option[U]]':
        if self.is_some() and isinstance(self.__val, tuple):
            return self.__val[0], self.__val[1]
        return Option.None_(), Option.None_()
