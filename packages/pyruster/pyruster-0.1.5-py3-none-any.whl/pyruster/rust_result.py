from typing import TypeVar, Generic, Optional, Callable

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')
F = TypeVar('F')


class Result(Generic[T, E]):

    def __init__(self, val: Optional[T] = None, err: Optional[E] = None):
        self.__val: Optional[T] = val
        self.__err: Optional[E] = err

    @staticmethod
    def Ok(val: T) -> 'Result[T, E]':
        return Result(val=val)

    @staticmethod
    def Err(err: E) -> 'Result[T, E]':
        return Result(err=err)

    def is_ok(self) -> bool:
        return self.__err is None

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        if self.is_ok():
            return f(self.__val)
        else:
            return False

    def is_err(self) -> bool:
        return not self.is_ok()

    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        if self.is_ok():
            return False
        return f(self.__err)

    def ok(self):
        from .rust_option import Option
        if self.is_ok():
            return Option.Some(self.__val)
        else:
            return Option.None_()

    def err(self):
        from .rust_option import Option
        if self.is_err():
            return Option.Some(self.__err)
        else:
            return Option.None_()

    def map(self, op: Callable[[T], U]) -> 'Result[U, E]':
        if self.is_ok():
            return Result.Ok(op(self.__val))
        else:
            return Result.Err(self.__err)

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        if self.is_ok():
            return f(self.__val)
        else:
            return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        if self.is_ok():
            return f(self.__val)
        else:
            return default(self.__err)

    def map_err(self, op: Callable[[E], F]) -> 'Result[T, F]':
        if self.is_ok():
            return Result.Ok(self.__val)
        else:
            return Result.Err(op(self.__err))

    def inspect(self, f: Callable[[T], None]) -> 'Result[T, E]':
        if self.is_ok():
            f(self.__val)
        return self

    def inspect_err(self, f: Callable[[E], None]) -> 'Result[T, E]':
        if self.is_err():
            f(self.__err)
        return self

    def expect(self, msg: str) -> T:
        if self.is_ok():
            return self.__val
        else:
            raise ValueError(msg)

    def expect_err(self, msg: str) -> E:
        if self.is_err():
            return self.__err
        else:
            raise ValueError(msg)

    def unwrap(self) -> T:
        if self.is_ok():
            return self.__val
        else:
            raise ValueError(f"Result is Err: {str(self.__err)}")

    def unwrap_or(self, default: T) -> T:
        if self.is_ok():
            return self.__val
        else:
            return default

    def unwrap_or_else(self, op: Callable[[E], E]) -> T:
        if self.is_ok():
            return self.__val
        else:
            return op(E)

    def unwrap_err(self) -> E:
        if self.is_err():
            return self.__err
        else:
            raise ValueError(f"Result is Ok: {str(self.__val)}")

    def and_(self, res: 'Result[U, E]') -> 'Result[U, E]':
        if self.is_ok():
            return res
        else:
            return Result.Err(self.__err)

    def and_then(self, op: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        if self.is_ok():
            return op(self.__val)
        else:
            return Result.Err(self.__err)

    def or_(self, res: 'Result[T, F]') -> 'Result[T, F]':
        if self.is_ok():
            return Result.Ok(self.__val)
        else:
            return res

    def or_else(self, op: Callable[[E], 'Result[T, F]']) -> 'Result[T, F]':
        if self.is_ok():
            return Result.Ok(self.__val)
        else:
            return op(self.__err)
