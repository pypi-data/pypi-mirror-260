import logging

import pandas as pd
import polars as pl
from networkx import NetworkXNoCycle
from polars import exclude, Expr
import numpy as np  # required for curve builder eval
import networkx as nx
from swarkn.helpers import timer
from polarmints.sugar import c

__all__ = [np]
logger = logging.getLogger(__name__)

DFPd = pd.DataFrame
DF = pl.DataFrame
DEF_INDEX = 'date'



####################### CLASS OVERRIDE #######################
@pl.api.register_dataframe_namespace("dag")
class Dagger:
    def __init__(self, df: DF):
        self._df = df

    def _dag(self) -> nx.DiGraph:
        dag = nx.DiGraph()
        for row in self._df.to_dicts():
            dag.add_node(row['index'])  # handle singular nodes with no deps
            args = set(filter(None, row.get('inputs_parsed') or []))
            logger.info(f'{row["index"]}: {args}')
            for e in args:
                dag.add_edge(e, row['index'])
        return dag

    def dag(self) -> nx.DiGraph:
        dag = self._dag()
        dag.remove_edges_from(nx.selfloop_edges(dag))
        try:
            cycle = nx.find_cycle(dag)
            raise RuntimeError(f'found cycle: {cycle}')
        except NetworkXNoCycle:
            pass
        return dag

    def sort(self) -> DF:
        dag = self.dag()
        layers = dict(enumerate(nx.topological_generations(dag)))
        order = DF([(v, i) for i, lst in layers.items() for v in lst], columns=['index', 'step'])
        mapping_df = self._df.select(
            exclude('step')
        ).join(order, on='index'
               ).sort('step')
        return mapping_df

    ####################### BUILD #######################
    def _build(self, mapping: DF) -> DF:
        # log
        curve_strs = '\n'.join(str(x) for x in self._df['index', 'expr_str', 'inputs_parsed'].rows())
        logger.info(f"building polars \n{curve_strs}")
        # meat
        with timer('built polars {cost}s'):
            res = self._df.lazy().with_columns([  # lazy()
                exp.alias(idx) for exp, idx in
                mapping[['expr', 'index']].rows()
                if exp is not None
            ])
            return res.collect()

    def with_columns(self, mapping: DF) -> DF:
        with timer(f'built {len(self._df)} curves in ' + '{cost}s'):
            for step in mapping['step'].unique():
                logger.info(f'building curves step {step}')
                submap = mapping.filter(c.step == step)
                res = self._build(submap)

        return res

    def select(self, mapping: DF) -> DF:
        cols = list(mapping['index'])
        return self.with_columns(mapping)[cols]
