import polars as pl
class PolarsCol:
    """
    pl.col('colname') overly verbose and less readable, this is an alternative
    Example usage:
    from polarmints import c
    expr = c.a == 1
    expr2 = c['a'] > 2

    My opinion is that square brackets is more readable than round ones, since round brackets are used extensively for
    expression precedence and grouping
    """
    def __getattr__(self, item):
        return pl.col(item)

    def __getitem__(self, item):
        return pl.col(item)

c = PolarsCol() #to be imported


