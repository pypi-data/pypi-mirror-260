"""A Python implementation of LINQ."""

from abc import ABC, abstractmethod
from collections.abc import Callable, Generator, Iterable
from itertools import chain
from typing import Optional, TypeVar
from typing import Union as UnionType

T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")
V = TypeVar("V")


class Unary(ABC):
    """Base class for unary operations."""

    @abstractmethod
    def __call__(self, source: Iterable[T]) -> Iterable[U]:
        """Applies an operation to a single source sequence.

        Args:
            source (Iterable[T]): The source sequence.

        Yields:
            Iterable[U]: The resulting sequence after applying the operation.
        """


class Binary(ABC):
    """Base class for binary operations."""

    @abstractmethod
    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[U],
    ) -> Iterable[T]:
        """Applies an operation to two source sequences.

        Args:
            source1 (Iterable[T]): The first source sequence.
            source2 (Iterable[U]): The second source sequence.

        Returns:
            Iterable[T]: The resulting sequence after applying the operation.
        """


class Where(Unary):
    def __init__(self, predicate: Callable[[T], bool]) -> None:
        """Initializes a new instance of the Where class.

        Args:
            predicate (Callable[[T], bool]): A function to test each element for a condition.
        """
        self.predicate = predicate

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Filters a sequence of values based on a predicate.

        Args:
            source (Iterable[T]): The source sequence.

        Yields:
            Iterable[T]: The resulting sequence after filtering elements based on the predicate.
        """
        yield from (item for item in source if self.predicate(item))


class Select(Unary):
    def __init__(self, selector: Callable[[T], U]) -> None:
        """Initializes a new instance of the Select class.

        Args:
            selector (Callable[[T], U]): A transform function to apply to each element.
        """
        self.selector = selector

    def __call__(self, source: Iterable[T]) -> Iterable[U]:
        """Projects each element of a sequence into a new form.

        Args:
            source (Iterable[T]): The source sequence.

        Yields:
            Iterable[U]: The resulting sequence after applying the transform function.
        """
        yield from (self.selector(item) for item in source)


class Take(Unary):
    def __init__(self, count: int) -> None:
        """Initializes a new instance of the Take class.

        Args:
            count (int): The number of elements to take from the source sequence.
        """
        self.count = count

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Returns a specified number of contiguous elements from the start of a
        sequence.

        Args:
            source (Iterable[T]): The source sequence.

        Yields:
            Iterable[T]: The resulting sequence with the specified number of elements.
        """
        yield from (item for _, item in zip(range(self.count), source))


class Skip(Unary):
    def __init__(self, count: int) -> None:
        """Initializes a new instance of the Skip class.

        Args:
            count (int): The number of elements to skip from the start of the source sequence.
        """
        self.count = count

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Skips the specified number of elements in the sequence.

        Args:
            source: The input sequence.

        Returns:
            An iterable representing the result of skipping the elements.
        """
        for index, item in enumerate(source):
            if index >= self.count:
                yield item


class Distinct(Unary):
    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Filters out duplicate elements from the source sequence.

        Args:
            source (Iterable[T]): The source sequence.

        Yields:
            T: The unique elements from the source sequence.
        """
        seen = set()
        for item in source:
            if item not in seen:
                seen.add(item)
                yield item


class SelectMany(Unary):
    def __init__(self, selector: Callable[[T], Iterable[U]]) -> None:
        """Initializes a new instance of the SelectMany class.

        Args:
            selector (Callable[[T], Iterable[U]]): A function that projects each element of the source sequence to an iterable.
        """
        self.selector = selector

    def __call__(self, source: Iterable[T]) -> Iterable[U]:
        """Projects each element of the source sequence to an iterable and flattens the
        resulting sequences into one sequence.

        Args:
            selector (Callable[[T], Iterable[U]]): A function that projects each element of the source sequence to an iterable.

        Yields:
            U: The flattened sequence of projected elements.
        """
        for item in source:
            yield from self.selector(item)


class OrderBy(Unary):
    """A class representing an order by operation on a sequence of elements."""

    def __init__(self, key_selector: Callable[[T], U]) -> None:
        """Initialize a new instance of the OrderBy class.

        Args:
            key_selector (Callable[[T], U]): A callable object that takes an element
                from the source sequence and returns a key used for sorting.

        Returns:
            None
        """
        self.key_selector = key_selector

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Apply the order by operation on the source sequence.

        Args:
            source (Iterable[T]): The source sequence to order.

        Yields:
            Iterable[T]: The ordered sequence of elements.

        Returns:
            None
        """
        yield from (item for item in sorted(source, key=self.key_selector))


class OrderByDescending(Unary):
    """Represents an operation that orders the elements in a sequence in descending
    order based on a key selector function.

    Args:
        key_selector: A callable that takes an element of type T and returns a key of type U.

    Returns:
        An iterable containing the elements in descending order based on the key selector.
    """

    def __init__(self, key_selector: Callable[[T], U]) -> None:
        """Initialize the OrderByDescending operation.

        Args:
            key_selector: A function that maps elements to keys used for sorting.
        """
        self.key_selector = key_selector

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Orders the elements in the source iterable in descending order based on the
        key selector.

        Args:
            source: An iterable of elements to be sorted.

        Returns:
            An iterable containing the elements in descending order based on the key selector.
        """
        yield from (item for item in sorted(source, key=self.key_selector, reverse=True))


class ThenBy(Unary):
    """Represents an operation that performs a subsequent ordering of elements in a
    sequence based on a key selector function.

    Args:
        key_selector: A callable that takes an element of type T and returns a key of type U.

    Returns:
        An iterable containing the elements with subsequent ordering based on the key selector.
    """

    def __init__(self, key_selector: Callable[[T], U]) -> None:
        """Initialize the ThenBy operation.

        Args:
            key_selector: A function that maps elements to keys used for sorting.
        """
        self.key_selector = key_selector

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Orders the elements in the source iterable with subsequent ordering based on
        the key selector.

        Args:
            source: An iterable of elements to be sorted.

        Returns:
            An iterable containing the elements with subsequent ordering based on the key selector.
        """
        yield from (item for item in sorted(source, key=self.key_selector, reverse=False))


class ThenByDescending(Unary):
    """Unary operation that performs a secondary descending order based on a key
    selector."""

    def __init__(self, key_selector: Callable[[T], U]) -> None:
        """Initialize the ThenByDescending operation.

        Args:
            key_selector: A function that maps elements to keys used for sorting.
        """
        self.key_selector = key_selector

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        """Apply the ThenByDescending operation to the source iterable.

        Args:
            source: The source iterable.

        Yields:
            The elements of the source iterable with a secondary descending order based on the key selector.
        """
        yield from (item for item in sorted(source, key=self.key_selector, reverse=True))


class Join(Binary):
    """Binary operation that joins two iterables based on key selectors and applies a
    result selector."""

    def __init__(
        self,
        inner: Iterable[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, U], V],
    ) -> None:
        self.inner = inner
        self.outer_key_selector = outer_key_selector
        self.inner_key_selector = inner_key_selector
        self.result_selector = result_selector

    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[U],
    ) -> Generator[V, None, None]:
        lookup = {self.inner_key_selector(item): item for item in self.inner}
        for item in source1:
            key = self.outer_key_selector(item)
            if key in lookup:
                yield self.result_selector(item, lookup[key])


class GroupJoin(Binary):
    def __init__(
        self,
        inner: Iterable[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, Iterable[U]], V],
    ) -> None:
        self.inner = inner
        self.outer_key_selector = outer_key_selector
        self.inner_key_selector = inner_key_selector
        self.result_selector = result_selector

    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[U],
    ) -> Generator[V, None, None]:
        lookup = {self.inner_key_selector(item): item for item in self.inner}
        for item in source1:
            key = self.outer_key_selector(item)
            inner_items = [lookup[key]] if key in lookup else []
            yield self.result_selector(item, inner_items)


class Zip(Binary):
    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[U],
    ) -> Generator[tuple[T, U], None, None]:
        yield from zip(source1, source2)


class All(Unary):
    def __init__(self, predicate: Callable[[T], bool]) -> None:
        self.predicate = predicate

    def __call__(self, source: Iterable[T]) -> bool:
        return all(self.predicate(item) for item in source)


class Any(Unary):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Iterable[T]) -> bool:
        if self.predicate is None:
            return any(source)

        return any(self.predicate(item) for item in source)


class Contains(Unary):
    def __init__(self, value: T) -> None:
        self.value = value

    def __call__(self, source: Iterable[T]) -> bool:
        return self.value in source


class Count(Unary):
    def __init__(self, predicate: Callable[[T], bool] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Iterable[T]) -> int:
        if self.predicate is not None:
            return sum(1 for item in source if self.predicate(item))
        else:
            return sum(1 for _ in source)


class Sum(Unary):
    def __call__(self, source: Iterable[T]) -> T:
        return sum(source)


class Min(Unary):
    def __call__(self, source: Iterable[T]) -> T:
        return min(source)


class Max(Unary):
    def __call__(self, source: Iterable[T]) -> T:
        return max(source)


class Average(Unary):
    def __call__(self, source: Iterable[T]) -> T:
        total, count = 0, 00
        for item in source:
            total += item
            count += 1

        if count > 0:
            return total / count

        return None


class Aggregate(Unary):
    def __init__(self, func: Callable[[T, T], T]) -> None:
        self.func = func

    def __call__(self, source: Iterable[T]) -> T:
        iterator = iter(source)

        try:
            result = next(iterator)
        except StopIteration:
            msg = "Sequence contains no elements."
            raise ValueError(msg)

        for item in iterator:
            result = self.func(result, item)

        return result


class Concat(Binary):
    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[T],
    ) -> Iterable[T]:
        yield from source1
        yield from source2


class Union(Binary):
    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[T],
    ) -> Iterable[T]:
        yield from set(source1).union(source2)


class Intersect(Binary):
    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[T],
    ) -> Iterable[T]:
        yield from set(source1).intersection(source2)


class Except(Binary):
    def __call__(
        self,
        source1: Iterable[T],
        source2: Iterable[T],
    ) -> Iterable[T]:
        yield from set(source1).difference(source2)


class First(Unary):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Iterable[T]) -> T:
        if self.predicate is None:
            try:
                return next(iter(source))
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)

        for item in source:
            if self.predicate(item):
                return item

        msg = "Sequence contains no matching element."
        raise ValueError(msg)


class FirstOrDefault(Unary):
    def __init__(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Optional[T] = None,
    ) -> None:
        self.predicate = predicate
        self.default = default

    def __call__(self, source: Iterable[T]) -> T:
        if self.predicate is None:
            try:
                return next(iter(source))
            except StopIteration:
                return self.default

        for item in source:
            if self.predicate(item):
                return item

        return self.default


class Last(Unary):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Iterable[T]) -> T:
        if self.predicate is None:
            try:
                result = None
                for item in source:
                    result = item
                return result
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)

        for item in source:
            if self.predicate(item):
                result = item

        if result is None:
            msg = "Sequence contains no matching element."
            raise ValueError(msg)

        return result


class LastOrDefault(Unary):
    def __init__(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Optional[T] = None,
    ) -> None:
        self.predicate = predicate
        self.default = default

    def __call__(self, source: Iterable[T]) -> T:
        if self.predicate is None:
            try:
                result = self.default
                for item in source:
                    result = item
                return result
            except StopIteration:
                return self.default

        for item in source:
            if self.predicate(item):
                return item

        return self.default


class Single(Unary):
    def __init__(self, predicate: Optional[Callable[[T], bool]] = None) -> None:
        self.predicate = predicate

    def __call__(self, source: Iterable[T]) -> T:
        items = iter(source)

        if self.predicate is None:
            try:
                result = next(items)
                try:
                    next(items)
                    msg = "Sequence contains more than one element."
                    raise ValueError(msg)
                except StopIteration:
                    return result
            except StopIteration:
                msg = "Sequence contains no elements."
                raise ValueError(msg)

        match_count = 0
        result = None
        for item in source:
            if self.predicate(item):
                match_count += 1
                result = item

        if match_count == 0:
            msg = "Sequence contains no matching element."
            raise ValueError(msg)

        if match_count > 1:
            msg = "Sequence contains more than one matching element."
            raise ValueError(msg)

        return result


class SingleOrDefault(Unary):
    def __init__(
        self,
        predicate: Optional[Callable[[T], bool]] = None,
        default: Optional[T] = None,
    ) -> None:
        self.predicate = predicate
        self.default = default

    def __call__(self, source: Iterable[T]) -> T:
        items = iter(source)

        if self.predicate is None:
            try:
                result = next(items)
                try:
                    next(items)
                    msg = "Sequence contains more than one element."
                    raise ValueError(msg)
                except StopIteration:
                    return result
            except StopIteration:
                return self.default

        match_count = 0
        result = self.default
        for item in source:
            if self.predicate(item):
                match_count += 1
                result = item

        if match_count > 1:
            msg = "Sequence contains more than one matching element."
            raise ValueError(msg)

        return result


class ElementAt(Unary):
    def __init__(self, index: int) -> None:
        self.index = index

    def __call__(self, source: Iterable[T]) -> T:
        try:
            return next(item for i, item in enumerate(source) if i == self.index)
        except StopIteration:
            msg = "Sequence contains no element at the specified index."
            raise ValueError(msg)


class ElementAtOrDefault(Unary):
    def __init__(self, index: int, default: Optional[T] = None) -> None:
        self.index = index
        self.default = default

    def __call__(self, source: Iterable[T]) -> T:
        try:
            return next(item for i, item in enumerate(source) if i == self.index)
        except StopIteration:
            return self.default


class DefaultIfEmpty(Unary):
    def __init__(self, default_value: Optional[T] = None) -> None:
        self.default_value = default_value

    def __call__(self, source: Iterable[T]) -> UnionType[T, Iterable[T]]:
        try:
            next(iter(source))
        except StopIteration:
            if self.default_value is not None:
                yield self.default_value
            return

        yield from source


class OfType(Unary):
    def __init__(self, type_filter: type[U]) -> None:
        self.type_filter = type_filter

    def __call__(self, source: Iterable[T]) -> Iterable[T]:
        yield from (item for item in source if isinstance(item, self.type_filter))


class Queryable(Iterable[T]):
    def __init__(self, collection: Iterable[T]) -> None:
        self.collection = collection

    def __iter__(self) -> Iterable[T]:
        yield from self.collection

    @classmethod
    def range(cls, start: int, stop: Optional[int] = None, step: int = 1) -> "Queryable":
        if stop is None:
            start, stop = 0, start

        return cls(range(start, stop, step))

    @classmethod
    def empty(cls) -> "Queryable":
        return cls([])

    def query(self) -> "Queryable":
        return Queryable(self)

    def where(self, predicate: Callable[[T], bool]) -> "Queryable":
        return Queryable(Where(predicate)(self))

    def select(self, selector: Callable[[T], U]) -> "Queryable":
        return Queryable(Select(selector)(self))

    def distinct(self) -> "Queryable":
        return Queryable(Distinct()(self))

    def skip(self, count: int) -> "Queryable":
        return Queryable(Skip(count)(self))

    def take(self, count: int) -> "Queryable":
        return Queryable(Take(count)(self))

    def of_type(self, type_filter: type[U]) -> "Queryable":
        return Queryable(OfType(type_filter)(self))

    def select_many(self, selector: Callable[[T], Iterable[U]]) -> "Queryable":
        return Queryable(SelectMany(selector)(self))

    def order_by(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(OrderBy(key_selector)(self))

    def order_by_descending(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(OrderByDescending(key_selector)(self))

    def then_by(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(ThenBy(key_selector)(self))

    def then_by_descending(self, key_selector: Callable[[T], U]) -> "Queryable":
        return Queryable(ThenByDescending(key_selector)(self))

    def group_join(
        self,
        inner: Iterable[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, Iterable[U]], V],
    ) -> "Queryable":
        return Queryable(
            GroupJoin(inner, outer_key_selector, inner_key_selector, result_selector)(self, inner),
        )

    def zip(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(Zip()(self, other))

    def concat(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(chain(self, other))

    def aggregate(self, func: Callable[[T, T], T]) -> T:
        return Aggregate(func)(self)

    def union(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(Union()(self, other))

    def intersect(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(Intersect()(self, other))

    def all(self, predicate: Callable[[T], bool]) -> bool:
        return All(predicate)(self)

    def any(self, predicate: Callable[[T], bool] = None) -> bool:
        return Any(predicate)(self)

    def contains(self, value: T) -> T:
        return Contains(value)(self)

    def count(self, predicate: Callable[[T], bool] = None) -> int:
        return Count(predicate)(self)

    def sum(self) -> int:
        return Sum()(self)

    def min(self) -> int:
        return Min()(self)

    def max(self) -> int:
        return Max()(self)

    def average(self) -> int:
        return Average()(self)

    def except_for(self, other: Iterable[T]) -> "Queryable[T]":
        return Queryable(Except()(self, other))

    def first(self, predicate: Callable[[T], bool] = None) -> T:
        return First(predicate)(self)

    def first_or_default(
        self,
        predicate: Callable[[T], bool] = None,
        default: Optional[T] = None,
    ) -> T:
        return FirstOrDefault(predicate, default)(self)

    def last(self, predicate: Callable[[T], bool] = None) -> T:
        return Last(predicate)(self)

    def last_or_default(
        self,
        predicate: Callable[[T], bool] = None,
        default: Optional[T] = None,
    ) -> T:
        return LastOrDefault(predicate, default)(self)

    def single(self, predicate: Callable[[T], bool] = None) -> T:
        return Single(predicate)(self)

    def single_or_default(
        self,
        predicate: Callable[[T], bool] = None,
        default: Optional[T] = None,
    ) -> T:
        return SingleOrDefault(predicate, default)(self)

    def element_at(self, index: int) -> T:
        return ElementAt(index)(self)

    def element_at_or_default(self, index: int, default: Optional[T] = None) -> T:
        return ElementAtOrDefault(index, default)(self)

    def default_if_empty(self, default: T) -> "Queryable[T]":
        return Queryable(DefaultIfEmpty(default)(self))

    def join(
        self,
        inner: Iterable[U],
        outer_key_selector: Callable[[T], K],
        inner_key_selector: Callable[[U], K],
        result_selector: Callable[[T, U], V],
    ) -> "Queryable":
        return Queryable(
            Join(inner, outer_key_selector, inner_key_selector, result_selector)(self, inner),
        )

    def to_list(self) -> list[T]:
        return list(self)

    def to_dictionary(
        self,
        key_selector: Callable[[T], K],
        value_selector: Optional[Callable[[T], V]] = None,
    ) -> dict[K, V]:
        if value_selector is None:
            return {key_selector(item): item for item in self}

        return {key_selector(item): value_selector(item) for item in self}
