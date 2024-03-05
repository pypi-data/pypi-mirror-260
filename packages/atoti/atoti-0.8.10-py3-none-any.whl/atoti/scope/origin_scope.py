from collections import defaultdict
from collections.abc import Set as AbstractSet
from typing import Annotated, Any
from warnings import warn

from atoti_core import (
    DEPRECATED_WARNING_CATEGORY as _DEPRECATED_WARNING_CATEGORY,
    PYDANTIC_CONFIG as _PYDANTIC_CONFIG,
    HierarchyIdentifier,
    Identifiable,
    LevelIdentifier,
    identify,
)
from pydantic import AfterValidator, Field, model_validator
from pydantic.dataclasses import dataclass

from .._measure_convertible import NonConstantMeasureConvertible
from .._measure_description import MeasureDescription
from .._measures.calculated_measure import AggregatedMeasure


def _check_unique_hierarchies(
    levels: AbstractSet[Identifiable[LevelIdentifier]], /
) -> AbstractSet[Identifiable[LevelIdentifier]]:
    levels_grouped_by_hierarchy: dict[HierarchyIdentifier, set[str]] = defaultdict(set)

    for level in levels:
        level_identifier = identify(level)
        levels_grouped_by_hierarchy[level_identifier.hierarchy_identifier].add(
            level_identifier.level_name
        )

    duplicate_hierarchies = {
        hierarchy_identifier
        for hierarchy_identifier, level_names in levels_grouped_by_hierarchy.items()
        if len(level_names) > 1
    }
    if duplicate_hierarchies:
        raise ValueError(
            f"The passed levels must belong to different hierarchies but several levels were given for {duplicate_hierarchies}."
        )

    return levels


@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class OriginScope:  # pylint: disable=keyword-only-dataclass, make it keyword only when dropping the deprecated constructor.
    """Scope to perform an aggregation starting from the specified levels.

    The passed levels define a boundary above and under which the aggregation is performed differently.
    When those levels are not expressed in a query, the queried measure will drill down until finding the value for all members of these levels, and then aggregate those values using the defined aggregation function.

    This allows for defining measures computing:

    * the yearly mean when looking at the grand total
    * the sum of each month's value when looking at each year individually

    Example:
      >>> df = pd.DataFrame(
      ...     columns=["Year", "Month", "Day", "Quantity"],
      ...     data=[
      ...         (2019, 7, 1, 15),
      ...         (2019, 7, 2, 20),
      ...         (2019, 7, 3, 30),
      ...         (2019, 6, 1, 25),
      ...         (2019, 6, 2, 15),
      ...         (2018, 7, 1, 5),
      ...         (2018, 7, 2, 10),
      ...         (2018, 6, 1, 15),
      ...         (2018, 6, 2, 5),
      ...     ],
      ... )
      >>> table = session.read_pandas(
      ...     df, table_name="Origin", default_values={"Year": 0, "Month": 0, "Day": 0}
      ... )
      >>> cube = session.create_cube(table, mode="manual")
      >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
      >>> h["Date"] = [table["Year"], table["Month"], table["Day"]]
      >>> m["Quantity.SUM"] = tt.agg.sum(table["Quantity"])
      >>> m["Average of monthly quantities"] = tt.agg.mean(
      ...     m["Quantity.SUM"], scope=tt.OriginScope(levels={l["Month"]})
      ... )
      >>> cube.query(
      ...     m["Quantity.SUM"],
      ...     m["Average of monthly quantities"],
      ...     levels=[l["Day"]],
      ...     include_totals=True,
      ... )
                      Quantity.SUM Average of monthly quantities
      Year  Month Day
      Total                    140                         35.00
      2018                      35                         17.50
            6                   20                         20.00
                  1             15                         15.00
                  2              5                          5.00
            7                   15                         15.00
                  1              5                          5.00
                  2             10                         10.00
      2019                     105                         52.50
            6                   40                         40.00
                  1             25                         25.00
                  2             15                         15.00
            7                   65                         65.00
                  1             15                         15.00
                  2             20                         20.00
                  3             30                         30.00
    """

    levels: Annotated[
        AbstractSet[Identifiable[LevelIdentifier]],
        Field(min_length=1),
        AfterValidator(_check_unique_hierarchies),
    ]
    """The levels defining the dynamic aggregation domain."""

    @model_validator(mode="before")
    def _validate(cls, values: Any) -> Any:  # noqa: N805
        if values.kwargs:
            assert not values.args
            return values.kwargs

        warn(
            "The variadic constructor is deprecated, pass a named `levels` parameter instead.",
            category=_DEPRECATED_WARNING_CATEGORY,
            stacklevel=2,
        )
        return {"levels": values.args}

    def _create_aggregated_measure(
        self, measure: NonConstantMeasureConvertible, /, *, plugin_key: str
    ) -> MeasureDescription:
        return AggregatedMeasure(
            _underlying_measure=measure,
            _plugin_key=plugin_key,
            _on_levels=frozenset(identify(level) for level in self.levels),
        )
