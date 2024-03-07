from qablet_contracts.timetable import EVENT_SCHEMA


def test_base():
    assert EVENT_SCHEMA.names == ["track", "time", "op", "quantity", "unit"]
