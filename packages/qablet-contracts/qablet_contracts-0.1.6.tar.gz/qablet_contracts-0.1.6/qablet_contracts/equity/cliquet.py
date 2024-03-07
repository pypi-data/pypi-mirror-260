"""
This module contains examples of creating timetables for equity cliquet contracts.
"""

import numpy as np
import pyarrow as pa
from qablet_contracts.timetable import EVENT_SCHEMA
from typing import List


def clique_timetable(
    ccy: str,
    asset_name: str,
    fixings: List[float],
    global_floor: float,
    local_floor: float,
    local_cap: float,
    track: str = "",
) -> dict:
    """Create timetable for an **Accumulator Cliquet**.

    Args:
        ccy: the currency of the bond.
        asset_name: the name of the underlying asset.
        fixings: the fixing times of the cliquet.
        global_floor: the global floor of the cliquet.
        local_floor: the local floor of the cliquet.
        local_cap: the local cap of the cliquet.
        track: an optional identifier for the contract.

    Examples:
        >>> tt = clique_timetable("USD", "SPX", [1.0, 2.0, 3.0], 0.01, -0.03, 0.05)
        >>> tt["events"].to_pandas()
          track  time op  quantity     unit
        0   NaN   1.0  s      0.00    _INIT
        1   NaN   2.0  s      0.00  _UPDATE
        2   NaN   3.0  s      0.00  _UPDATE
        3         3.0  >      0.01      USD
        4         3.0  +      1.00       _A
    """

    maturity = fixings[-1]

    # define timetable
    events = [
        {
            "track": None,
            "time": fixings[0],
            "op": "s",
            "quantity": 0,
            "unit": "_INIT",  # initialize accumulator
        }
    ]
    for fixing_time in fixings[1:]:
        events.append(
            {
                "track": None,
                "time": fixing_time,
                "op": "s",
                "quantity": 0,
                "unit": "_UPDATE",  # update accumulator
            }
        )
    events.append(
        {
            "track": track,
            "time": maturity,
            "op": ">",  # global floor
            "quantity": global_floor,
            "unit": ccy,
        }
    )
    events.append(
        {
            "track": track,
            "time": maturity,
            "op": "+",  # pay the accumulated amount
            "quantity": 1,
            "unit": "_A",
        }
    )

    # define accumulator functions
    def accumulator_init_fn(inputs):
        [s] = inputs
        return [0, s]  # [A, S_last]

    def accumulator_update_fn(inputs):
        [s, s_last, a] = inputs

        ret = s / s_last - 1.0  # ret = S / S_last - 1
        ret = np.maximum(local_floor, ret)
        ret = np.minimum(local_cap, ret)

        return [a + ret, s]  # [A, S_last]

    return {
        "events": pa.RecordBatch.from_pylist(events, schema=EVENT_SCHEMA),
        "expressions": {
            "_INIT": {
                "type": "snapper",
                "inp": [asset_name],
                "fn": accumulator_init_fn,
                "out": ["_A", "_S_last"],
            },
            "_UPDATE": {
                "type": "snapper",
                "inp": [asset_name, "_S_last", "_A"],
                "fn": accumulator_update_fn,
                "out": ["_A", "_S_last"],
            },
        },
    }


if __name__ == "__main__":
    # Create the cliquet
    global_floor = 0.0
    fixings = np.linspace(0, 3, 7).tolist()  # T = 3 years, N = 6 fixings
    local_floor = -0.03
    local_cap = 0.05
    timetable = clique_timetable(
        "USD", "SPX", fixings, global_floor, local_floor, local_cap
    )

    print(timetable["events"].to_pandas())
