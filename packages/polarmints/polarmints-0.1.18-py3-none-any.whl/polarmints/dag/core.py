import logging
from itertools import chain
from typing import Iterable, Literal

import pandas as pd
import polars as pl
from networkx import NetworkXNoCycle
from polars import exclude, Expr
import numpy as np  # required for curve builder eval
import networkx as nx
from swarkn.helpers import timer
from polarmints.sugar import c
s = c # aliasing as a convention for distinguishing raw inputs (c) and derived columns (s), even though they are effectively the same.


__all__ = [np]
logger = logging.getLogger(__name__)

DFPd = pd.DataFrame
DF = pl.DataFrame
DEF_INDEX = 'date'


def _parse(expr: Expr | list[str | Expr], args: list) -> tuple[list[str], dict[str, Expr]]:
    """
    convenience function to split strings from pl.Exprs so they can be handled separately
    "expr" is passed in separately in case it's a singular Expr
    """
    if expr is None:
        expr = []
    elif not isinstance(expr, list):
        expr = [expr]

    strings, map = [], {}
    for e in expr + list(args):
        if isinstance(e, str):
            strings.append(e)
        else:
            map[e.meta.output_name()] = e
    return strings, map

class DagBase:
    def __init__(self):
        pass

    def dag(self, exprs: Iterable) -> nx.DiGraph:
        """
        create a DAG from list of expressions that depend on each other.
        """
        que = list(exprs)
        parsed = set([None])
        dag = nx.DiGraph()

        while que:
            expr = que.pop()
            key = expr.meta.output_name()
            children = {x for x in expr.meta.root_names() if hasattr(self, x)}
            child_exprs = [getattr(self, x) for x in children - parsed]
            # print(key, expr.meta.root_names(), children)
            dag.add_node(key)
            for child in children:
                dag.add_edge(child, key)
            que += child_exprs
            parsed.update(children)

        dag.remove_edges_from(nx.selfloop_edges(dag))
        try:
            cycle = nx.find_cycle(dag)
            raise RuntimeError(f'found cycle: {cycle}')
        except NetworkXNoCycle:
            pass

        return dag

    def ordered_exprs(self, exprs: dict | list, exclude=tuple()) -> list[list[Expr]]:
        """
        groups expressions into a chunks that can be executed in parallel.
        """
        fallback = {e.meta.output_name(): e for e in exprs}
        dag = self.dag(exprs)
        order = nx.topological_generations(dag)
        return [[
            getattr(self, expr) if hasattr(self, expr) else fallback[expr]
                for expr in level if expr not in exclude
        ] for level in order]



    def _select(self, is_select: bool, df: DF, expr=None, *args,
                include_deps=False,
                override_existing=False,
                **kwargs) -> DF:
        """

        """
        rename = {}
        for k, v in kwargs.items():
            alias = v.meta.output_name()
            if hasattr(self, alias):
                rename[alias] = k
            else:
                kwargs[k] = v.alias(k) #set alias to avoid overriding original col.

        strings, map = _parse(expr, args)
        mapping = map | kwargs
        colnames = list(mapping.keys())
        exprs = mapping.values()
        ordered_exprs = self.ordered_exprs(exprs, [] if override_existing else df.columns)

        fulldf = df.pm.with_cols(ordered_exprs
        ).rename(rename)

        if is_select:
            selection = strings
            if include_deps:
                allcols = [e.meta.output_name() for e in list(chain(*ordered_exprs))]
                selection += [rename.get(col, col) for col in allcols]
            else:
                selection += colnames
        else:
            if include_deps:
                selection = pl.all()
            else:
                selection = df.columns + [col for col in colnames if col not in df.columns]
        return fulldf.select(selection)

    def select(self, *args, **kwargs) -> DF:
        return self._select(True, *args, **kwargs)

    def with_cols(self, *args, **kwargs) -> DF:
        return self._select(False, *args, **kwargs)


def node(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs).alias(func.__name__)
    return property(inner)
