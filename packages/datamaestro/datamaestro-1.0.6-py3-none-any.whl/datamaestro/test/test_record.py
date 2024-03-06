import pickle
from datamaestro.record import (
    Record,
    Item,
    RecordTypesCache,
    recordtypes,
    SingleRecordTypeCache,
)
from attrs import define
import pytest


@define
class AItem(Item):
    a: int


@define
class A1Item(AItem):
    a1: int


@define
class BItem(Item):
    b: int


@define
class B1Item(BItem):
    b1: int


@define
class CItem(Item):
    c: int


@recordtypes(A1Item)
class BaseRecord(Record):
    ...


@recordtypes(BItem)
class MyRecord(BaseRecord):
    ...


@recordtypes(CItem)
class MyRecord2(MyRecord):
    pass


def test_record_simple():
    a = A1Item(1, 2)
    b = BItem(4)
    r = MyRecord(a, b)
    assert r[AItem] is a
    assert r[A1Item] is a
    assert r[BItem] is b


def test_record_missing_init():
    with pytest.raises(KeyError):
        # A1Item is missing
        MyRecord(AItem(1), BItem(2))

    with pytest.raises(KeyError):
        MyRecord(A1Item(1, 2))


def test_record_update():
    a = A1Item(1, 2)
    b = BItem(4)
    r = MyRecord(a, b)

    r2 = r.update(BItem(3))
    assert r is not r2
    assert r2[BItem] is not b

    r3 = MyRecord2.from_record(r, CItem(2), BItem(5))
    assert r[BItem].b == 4
    assert r3[BItem].b == 5


def test_record_decorator():
    MyRecord2(A1Item(1, 2), BItem(2), CItem(3))


def test_record_type_update():
    itemtypes = MyRecord2.from_types("Test", B1Item).itemtypes
    assert itemtypes == frozenset((A1Item, B1Item, CItem))


def test_record_onthefly():
    cache = RecordTypesCache("OnTheFly", CItem)

    MyRecord2 = cache(MyRecord)
    MyRecord2(A1Item(1, 2), BItem(2), CItem(3))

    assert cache(MyRecord) is MyRecord2

    r = MyRecord(A1Item(1, 2), BItem(2))
    assert cache(r.__class__) is MyRecord2

    r = cache.update(r, CItem(3))

    # Same record type
    cache2 = RecordTypesCache("OnTheFly", CItem)

    cache2.update(r, CItem(4))


def test_record_pickled():
    # First,
    MyRecord2 = BaseRecord.from_types("MyRecordBis", BItem)
    r = MyRecord2(A1Item(1, 2), BItem(2))
    r = pickle.loads(pickle.dumps(r))

    assert isinstance(r, BaseRecord) and not isinstance(r, MyRecord2)
    cache = RecordTypesCache("OnTheFly", CItem)

    assert r.is_pickled()

    r2 = cache.update(r, CItem(4))
    assert not r2.is_pickled()

    # Test with cls update
    with pytest.raises(KeyError):
        cache.update(r, CItem(4), cls=BaseRecord)

    # This is OK
    cache.update(r, CItem(4), cls=MyRecord)

    # --- Test when we update a pickled record with an of a sub-class
    cache = RecordTypesCache("OnTheFly", B1Item)
    r2 = cache.update(r, B1Item(1, 2))


def test_record_pickled_single():
    MyRecord2 = BaseRecord.from_types("MyRecordBis", BItem)
    r = MyRecord2(A1Item(1, 2), BItem(2))
    r = pickle.loads(pickle.dumps(r))

    cache = SingleRecordTypeCache("OnTheFly", CItem)

    updated = cache.update(r, CItem(4))

    assert updated.itemtypes == frozenset((A1Item, BItem, CItem))

    # Even with the wrong record, no change now
    assert cache(BaseRecord).itemtypes == frozenset((A1Item, BItem, CItem))
