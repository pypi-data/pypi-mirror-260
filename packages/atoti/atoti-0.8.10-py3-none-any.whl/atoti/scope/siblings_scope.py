from atoti_core import (
    PYDANTIC_CONFIG as _PYDANTIC_CONFIG,
    HierarchyIdentifier,
    Identifiable,
    identify,
    keyword_only_dataclass,
)
from pydantic.dataclasses import dataclass

from .._measure_convertible import NonConstantMeasureConvertible
from .._measure_description import MeasureDescription
from .._measures.generic_measure import GenericMeasure


@keyword_only_dataclass
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class SiblingsScope:
    """Scope to perform a "siblings" aggregation.

    With a siblings scope, the value for the member of a given level in the hierarchy is computed by taking the contribution of all of the members on the same level (its siblings).

    A siblings aggregation is an appropriate tool for operations such as marginal aggregations (marginal VaR, marginal mean) for non-linear aggregation functions.

    Example:
        >>> from datetime import date
        >>> df = pd.DataFrame(
        ...     columns=["Date", "Quantity"],
        ...     data=[
        ...         (date(2019, 7, 1), 15),
        ...         (date(2019, 7, 2), 20),
        ...         (date(2019, 7, 3), 30),
        ...         (date(2019, 6, 1), 25),
        ...         (date(2019, 6, 2), 15),
        ...         (date(2018, 7, 1), 5),
        ...         (date(2018, 7, 2), 10),
        ...         (date(2018, 6, 1), 15),
        ...         (date(2018, 6, 2), 5),
        ...     ],
        ... )
        >>> table = session.read_pandas(df, table_name="Siblings")
        >>> cube = session.create_cube(table, mode="manual")
        >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
        >>> cube.create_date_hierarchy("Date", column=table["Date"])
        >>> m["Quantity.SUM"] = tt.agg.sum(table["Quantity"])
        >>> m["Siblings quantity"] = tt.agg.sum(
        ...     m["Quantity.SUM"], scope=tt.SiblingsScope(hierarchy=h["Date"])
        ... )
        >>> cube.query(
        ...     m["Quantity.SUM"],
        ...     m["Siblings quantity"],
        ...     levels=[l["Day"]],
        ...     include_totals=True,
        ... )
                        Quantity.SUM Siblings quantity
        Year  Month Day
        Total                    140               140
        2018                      35               140
              6                   20                35
                    1             15                20
                    2              5                20
              7                   15                35
                    1              5                15
                    2             10                15
        2019                     105               140
              6                   40               105
                    1             25                40
                    2             15                40
              7                   65               105
                    1             15                65
                    2             20                65
                    3             30                65
    """

    hierarchy: Identifiable[HierarchyIdentifier]
    """The hierarchy containing the levels along which the aggregation is performed."""

    exclude_self: bool = False
    """Whether to include the current member's contribution in its cumulative value.

    >>> m["Siblings quantity excluding self"] = tt.agg.sum(
    ...     m["Quantity.SUM"],
    ...     scope=tt.SiblingsScope(hierarchy=h["Date"], exclude_self=True),
    ... )
    >>> cube.query(
    ...     m["Quantity.SUM"],
    ...     m["Siblings quantity excluding self"],
    ...     levels=[l["Day"]],
    ...     include_totals=True,
    ... )
                    Quantity.SUM Siblings quantity excluding self
    Year  Month Day
    Total                    140                                0
    2018                      35                              105
          6                   20                               15
                1             15                                5
                2              5                               15
          7                   15                               20
                1              5                               10
                2             10                                5
    2019                     105                               35
          6                   40                               65
                1             25                               15
                2             15                               25
          7                   65                               40
                1             15                               50
                2             20                               45
                3             30                               35

    """

    def _create_aggregated_measure(
        self, measure: NonConstantMeasureConvertible, /, *, plugin_key: str
    ) -> MeasureDescription:
        return GenericMeasure(
            "SIBLINGS_AGG",
            measure,
            identify(self.hierarchy)._java_description,
            plugin_key,
            self.exclude_self,
        )
