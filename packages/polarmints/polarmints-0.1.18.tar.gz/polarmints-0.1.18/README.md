# Polarmints
Syntactic sugar for [polars](https://docs.pola.rs/user-guide/migration/pandas/) <br>
Apologies, not all features documented so feel free to explore codebase 

## Extensions
extends polars Dataframes with additional namespaces for convenience functions<br>
example:
```python
import polars as pl
from polarmints import PolarMints, c, DF
__all__ = [PolarMints] # required for extending DFs with polarmints, even though not explicitly used  

df = DF({
    'a': [1, 2, 3],
    'b': [1, 2, 3],
})

df2 = DF({
    'a': [1, 2, 3],
    'c': [1, 2, 3],
}, schema_overrides={'a': pl.Int16})

# df.pm: convenience helper funcs
joined = df2.pm.join(df, 'a') # implicitly converts datatypes before joining two DFs whose column types don't match

# this is contrived example since it's more efficient to do in polars: pl.DataFrame.with_column(pl.col('a') + 1) 
# however pandas may have other dataframe and series methods not yet implemented in polars
added_col = df.pd.assign(a2=1)
```

## DAG
Given an input _pl.DataFrame_ each _@node_ decorated method on a SubClass of _DagBase_ represents a derived column which could themselves depend on other derived columns. A dag is required to represent this hierarchy of dependencies, i.e. which columns to derive first and which ones can be done in parallel. this framework is inspired by [MDF](https://github.com/man-group/mdf) and the gromit dag in [beacon.io](https://www.beacon.io/) except the nodes represent [polars expressions](https://docs.pola.rs/py-polars/html/reference/expressions/index.html) instead of plain python. 

Example usage : 
```python
from polarmints.dag.core import DagBase, node, s
from polarmints import c, DF

class DagExample(DagBase):

    @node
    def DerivedCol(self):
        return c['raw2'] + 2

    @node
    def OverridenCol(self):
        """
        input column with this name will be overridden by this method if instance is initialized with
        override_existing=True
        """
        return c['raw1'] + 1

    @node
    def DerivedCol_2ndOrder(self):
        """
        NOTE: 's' and 'c' are effectively the same, 's' is merely for readability to distinguish derived columns (s)
        from raw inputs (c)
        """
        return s['OverridenCol'] + c['raw3']

    @node
    def DerivedCol_2ndOrder_B(self):
        return s['OverridenCol'] + s['DerivedCol']


if __name__ == '__main__':
    # this is an instance instead of class because some usages may require initializing the dag with instance specific
    # params when multiple instances are used in the same process.
    example = DagExample()

    # mock inputs
    df = DF({
        'raw1': [1, 2, 3],
        'raw2': [1, 2, 3],
        'raw3': [1, 2, 3],
        'OverridenCol': [10, 11, 12]
    })

    # select desired derived columns from mock inputs using dag
    df1 = example.with_cols(df,
        # func siganture: *args and **kwargs expresisons behave the same way as pl.DataFrame.with_column() and .select()          
        example.DerivedCol_2ndOrder,
        example.OverridenCol, #this will not be overridden
        'raw2',  # can be mixed with raw pl.Exprs that don't depend on the DAG nodes
        c['raw3'] + 2,
        
        **{
            'd1': example.DerivedCol,
            'd2': example.DerivedCol_2ndOrder_B,
            'd3': c['raw1'] * c['raw2']
        },
    )
    print(df1)

    """
    shape: (3, 8)
    ┌──────┬──────┬──────┬──────────────┬─────────────────────┬─────┬─────┬─────┐
    │ raw1 ┆ raw2 ┆ raw3 ┆ OverridenCol ┆ DerivedCol_2ndOrder ┆ d1  ┆ d2  ┆ d3  │
    │ ---  ┆ ---  ┆ ---  ┆ ---          ┆ ---                 ┆ --- ┆ --- ┆ --- │
    │ i64  ┆ i64  ┆ i64  ┆ i64          ┆ i64                 ┆ i64 ┆ i64 ┆ i64 │
    ╞══════╪══════╪══════╪══════════════╪═════════════════════╪═════╪═════╪═════╡
    │ 1    ┆ 1    ┆ 1    ┆ 10           ┆ 11                  ┆ 3   ┆ 13  ┆ 1   │
    │ 2    ┆ 2    ┆ 2    ┆ 11           ┆ 13                  ┆ 4   ┆ 15  ┆ 4   │
    │ 3    ┆ 3    ┆ 3    ┆ 12           ┆ 15                  ┆ 5   ┆ 17  ┆ 9   │
    └──────┴──────┴──────┴──────────────┴─────────────────────┴─────┴─────┴─────┘
    """

    # another example with more params yielding more implicitly derived columns
    expressions = [
        example.DerivedCol_2ndOrder, example.DerivedCol_2ndOrder_B,
    ]
    df2 = example.select(df, 'raw2', *expressions,
         include_deps=True, # include intermediate dependencies as columns in result DF for higher order nodes
         override_existing=True, # override the existing column if dict key or node name conflicts with raw input column
    )
    print(df2)

    """
    shape: (3, 5)
    ┌──────┬────────────┬──────────────┬───────────────────────┬─────────────────────┐
    │ raw2 ┆ DerivedCol ┆ OverridenCol ┆ DerivedCol_2ndOrder_B ┆ DerivedCol_2ndOrder │
    │ ---  ┆ ---        ┆ ---          ┆ ---                   ┆ ---                 │
    │ i64  ┆ i64        ┆ i64          ┆ i64                   ┆ i64                 │
    ╞══════╪════════════╪══════════════╪═══════════════════════╪═════════════════════╡
    │ 1    ┆ 3          ┆ 2            ┆ 5                     ┆ 3                   │
    │ 2    ┆ 4          ┆ 3            ┆ 7                     ┆ 5                   │
    │ 3    ┆ 5          ┆ 4            ┆ 9                     ┆ 7                   │
    └──────┴────────────┴──────────────┴───────────────────────┴─────────────────────┘
    """

    # for debugging: examine which derived expressions can be evaluated in parallel for each step
    ordered_exprs = example.ordered_exprs(expressions)
    print([[str(e) for e in oe] for oe in ordered_exprs])

    """
    [
        [
            '[(col("raw1")) + (1)].alias("OverridenCol")', 
            '[(col("raw2")) + (2)].alias("DerivedCol")'
        ], [
            '[(col("OverridenCol")) + (col("raw3"))].alias("DerivedCol_2ndOrder")',
            '[(col("OverridenCol")) + (col("DerivedCol"))].alias("DerivedCol_2ndOrder_B")'
        ]
    ]
    """


```
