from typing import Annotated, Optional, Union

from atoti_core import (
    PYDANTIC_CONFIG as _PYDANTIC_CONFIG,
    Identifiable,
    LevelIdentifier,
    identify,
    keyword_only_dataclass,
)
from pydantic import AfterValidator
from pydantic.dataclasses import dataclass

from .._measure_convertible import NonConstantMeasureConvertible
from .._measure_description import MeasureDescription
from .._measures.generic_measure import GenericMeasure


def _check_range_window(window: range, /) -> range:
    expected_step = 1

    if window.step != expected_step:
        raise ValueError(
            f"Aggregation windows only support ranges with step of size {expected_step}."
        )

    return window


_RangeWindow = Annotated[range, AfterValidator(_check_range_window)]

_TimePeriodWindow = Union[
    tuple[str, str], tuple[Optional[str], str], tuple[str, Optional[str]]
]


@keyword_only_dataclass
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class CumulativeScope:
    """Scope to perform a cumulative aggregation.

    Cumulative aggregations include cumulative sums (also called running sum or prefix sum), mean, min, max, etc.

    Example:
        >>> from datetime import date
        >>> df = pd.DataFrame(
        ...     columns=["Date", "Quantity"],
        ...     data=[
        ...         (date(2019, 7, 1), 15),
        ...         (date(2019, 7, 2), 20),
        ...         (date(2019, 6, 1), 25),
        ...         (date(2019, 6, 2), 15),
        ...         (date(2018, 7, 1), 5),
        ...         (date(2018, 7, 2), 10),
        ...         (date(2018, 6, 1), 15),
        ...         (date(2018, 6, 2), 5),
        ...     ],
        ... )
        >>> table = session.read_pandas(df, table_name="Cumulative")
        >>> cube = session.create_cube(table)
        >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
        >>> cube.create_date_hierarchy("Date", column=table["Date"])
        >>> h["Date"] = {
        ...     **h["Date"].levels,
        ...     "Date": table["Date"],
        ... }
        >>> m["Quantity.SUM"] = tt.agg.sum(table["Quantity"])
        >>> m["Cumulative quantity"] = tt.agg.sum(
        ...     m["Quantity.SUM"], scope=tt.CumulativeScope(level=l["Day"])
        ... )
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     m["Cumulative quantity"],
        ...     levels=[l["Day"]],
        ...     include_totals=True,
        ... )
                        Quantity.SUM Cumulative quantity
        Year  Month Day
        Total                    110                 110
        2018                      35                  35
              6                   20                  20
                    1             15                  15
                    2              5                  20
              7                   15                  35
                    1              5                  25
                    2             10                  35
        2019                      75                 110
              6                   40                  75
                    1             25                  60
                    2             15                  75
              7                   35                 110
                    1             15                  90
                    2             20                 110
    """

    level: Identifiable[LevelIdentifier]
    """The level along which the aggregation is performed."""

    dense: bool = False
    """When ``True``, all members of :attr:`level`, even those with no value for the underlying measure, will be taken into account for the cumulative aggregation (resulting in repeating values)."""

    partitioning: Optional[Identifiable[LevelIdentifier]] = None
    """The level in the hierarchy at which to start the aggregation over.

    >>> m["Partitioned by month"] = tt.agg.sum(
    ...     m["Quantity.SUM"],
    ...     scope=tt.CumulativeScope(level=l["Day"], partitioning=l["Month"]),
    ... )
    >>> cube.query(
    ...     m["Quantity.SUM"],
    ...     m["Partitioned by month"],
    ...     levels=[l["Day"]],
    ...     include_totals=True,
    ... )
                    Quantity.SUM Partitioned by month
    Year  Month Day
    Total                    110
    2018                      35
          6                   20                   20
                1             15                   15
                2              5                   20
          7                   15                   15
                1              5                    5
                2             10                   15
    2019                      75
          6                   40                   40
                1             25                   25
                2             15                   40
          7                   35                   35
                1             15                   15
                2             20                   35

    """

    window: Optional[Union[_RangeWindow, _TimePeriodWindow]] = None
    """The aggregation window defining the set of members before and after a given member (using the :attr:`level`'s :attr:`~atoti.Level.order`) to be considered in the computation of the cumulative aggregation.

    The window can be a:

    * :class:`range` starting with a <=0 value and ending with a >=0 value.

        >>> m["3 previous members window"] = tt.agg.sum(
        ...     m["Quantity.SUM"],
        ...     scope=tt.CumulativeScope(level=l["Day"], window=range(-3, 0)),
        ... )
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     m["3 previous members window"],
        ...     levels=[l["Day"]],
        ...     include_totals=True,
        ... )
                        Quantity.SUM 3 previous members window
        Year  Month Day
        Total                    110                        75
        2018                      35                        35
              6                   20                        20
                    1             15                        15
                    2              5                        20
              7                   15                        35
                    1              5                        25
                    2             10                        35
        2019                      75                        75
              6                   40                        55
                    1             25                        45
                    2             15                        55
              7                   35                        75
                    1             15                        65
                    2             20                        75

    * time period window as a two-element :class:`tuple` of either ``None`` or a period as specified by `Java's Period.parse() <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/Period.html#parse(java.lang.CharSequence)>`__.

        >>> m["2 days window"] = tt.agg.sum(
        ...     m["Quantity.SUM"],
        ...     scope=tt.CumulativeScope(level=l["Date"], window=("-P2D", None)),
        ... )
        >>> m["2 days window partitioned by month"] = tt.agg.sum(
        ...     m["Quantity.SUM"],
        ...     scope=tt.CumulativeScope(
        ...         level=l["Date"],
        ...         window=("-P2D", None),
        ...         partitioning=l["Month"],
        ...     ),
        ... )
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     m["2 days window"],
        ...     m["2 days window partitioned by month"],
        ...     levels=[l["Day"]],
        ...     include_totals=True,
        ... )
                        Quantity.SUM 2 days window 2 days window partitioned by month
        Year  Month Day
        Total                    110            35
        2018                      35            15
              6                   20            20                                 20
                    1             15            15                                 15
                    2              5            20                                 20
              7                   15            15                                 15
                    1              5             5                                  5
                    2             10            15                                 15
        2019                      75            35
              6                   40            40                                 40
                    1             25            25                                 25
                    2             15            40                                 40
              7                   35            35                                 35
                    1             15            15                                 15
                    2             20            35                                 35

    Default to ``range(-∞, 0)``, meaning that the value for a given member is computed using all of the members before it and none after it.
    """

    def _create_aggregated_measure(
        self, measure: NonConstantMeasureConvertible, /, *, plugin_key: str
    ) -> MeasureDescription:
        return GenericMeasure(
            "WINDOW_AGG",
            measure,
            identify(self.level)._java_description,
            identify(self.partitioning)._java_description
            if self.partitioning is not None
            else None,
            plugin_key,
            (self.window.start, self.window.stop)
            if isinstance(self.window, range)
            else self.window,
            self.dense,
        )
