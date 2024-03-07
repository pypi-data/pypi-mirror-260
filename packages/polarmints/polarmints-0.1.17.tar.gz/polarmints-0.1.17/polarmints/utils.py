from __future__ import annotations

import logging
from contextlib import contextmanager
from operator import and_
from polarmints import c, DF
import pyarrow.dataset as ds
from typing import Iterable
from functools import reduce
import polars as pl
from polars import lit, Expr, struct, DataFrame as DF

from polarmints.aws import read_delta_s3

logger = logging.getLogger()

def hconcat_exc(dfs: list[DF]) -> DF:
    existing_cols = set(dfs[0].columns)
    cols = [existing_cols]
    for df in dfs[1:]:
        current_cols = set(df.columns) - existing_cols
        cols.append(current_cols)
        existing_cols = existing_cols.union(current_cols)

    res = pl.concat([df[list(colset)] for df, colset in zip(dfs, cols)], how='horizontal')
    return res

def dict2pred(predicates: dict) -> list[Expr]:
    res = []
    for raw_k, v in predicates.items():
        k = raw_k.replace('~', '')
        if isinstance(v, (tuple, set, list)):
            expr = c[k].is_in(v)
        elif isinstance(v, str):
            expr = c[k].str.contains(v)
        elif v is None:
            expr = c[k].is_null()
        else:
            expr = c[k] == v

        if raw_k.startswith('~'):
            expr = expr.is_not()

        res.append(expr)
    return reduce(Expr.__and__, res)


def dict2pafilter(predicates: dict) -> list[tuple]:
    res = []
    for raw_k, v in predicates.items():
        k = raw_k.replace('~', '')
        neg = raw_k.startswith('~')

        if isinstance(v, (tuple, set, list)):
            op = 'not in' if neg else 'in'
            v = list(v)
        else:
            op = '!=' if neg else '='
        res.append((k, op, v))
    return res


def dict2dspred(predicates: dict) -> ds.Expression:
    res = []
    f = ds.field
    for raw_k, v in predicates.items():
        k = raw_k.replace('~', '')
        if isinstance(v, (tuple, set, list)):
            expr = f(k).isin(v)
        elif v is None:
            expr = f(k).is_null()
        else:
            expr = f(k) == v

        if raw_k.startswith('~'):
            expr = ~expr
        res.append(expr)

    return reduce(and_, res)



def read_delta(*args, **kwargs):
    """
    DEPRECATED
    """
    logger.warning('polarmints read_delta() is deprecated renamed to aws.read_delta_s3')
    return read_delta_s3(*args, **kwargs)

def where(conditions: list[tuple[Expr, Expr]], default=None) -> Expr:
    res = pl
    for pred, val_ in conditions:
        val = val_ if isinstance(val_, Expr) else lit(val_)
        if pred is None:
            default = val
        else:
            res = res.when(pred).then(val)

    return res.otherwise(default)

def combine_struct(dfs: dict[str, DF], exclude: Iterable[str] = None, include: Iterable[str] = None) -> DF:
    """
    assumes dfs are same shape and combines into df of the same shape with structs as values

    Example Usage:
    dfs = {
        'd1': pl.DataFrame({
            'a': [1, 2, 3],
            'b': [1, 2, 3],
            'd': [1, 2, 3],
            'c': [1, 2, 3],
        }),
        'd2': pl.DataFrame({
            'd': [1, 2, 3],
            'a': [2, 2, 2],
            'c': [2, 2, 2],
        }),
        'd3': pl.DataFrame({
            'a': [3, 2, 1],
            'b': [3, 2, 1],
        }),
    }
    combined = combine_struct(dfs, ['d'])
    """
    primary_df = list(dfs.values())[0]
    cols = primary_df.columns
    include = include or set(cols) - set(exclude)
    res = primary_df.select([
        struct([df[col].rename(k)
            for k, df in dfs.items() if col in df
        ]).alias(col) if col in include else col
    for col in cols])
    return res

def plv(cfg: pl.config.Config = None, rows=200, cols=25):
    cfg = cfg or pl.Config()
    cfg.set_tbl_rows(rows)
    cfg.set_tbl_cols(cols)

@contextmanager
def plverbose(**kwargs):
    with pl.Config() as cfg:
        plv(cfg, **kwargs)
        yield
