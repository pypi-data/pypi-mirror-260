from __future__ import annotations
import awswrangler as wr
import logging
from deltalake import DeltaTable
from concurrent.futures import ThreadPoolExecutor
from itertools import product, chain
import pyarrow.parquet as pq
from pyarrow import fs
from swarkn.helpers import init_logger, timer
from swarkn.aws.s3 import session_storage_options
from functools import reduce, lru_cache
import polars as pl
from polars import DataFrame as DF
try:
    from loguru import logger
except:
    logger = logging.getLogger(__name__)

######################################### HELPERS #########################################
@lru_cache
def fs3():
    return fs.S3FileSystem()

def strip_s3_prefix(path: str) -> str:
    return path.replace('s3://', '')

######################################### MEAT #########################################
def read_delta_s3(paths: str | list, exprs: list[list[tuple]] = [None], storage_options: dict = None, version: int = None,
               **kwargs) -> DF:
    """

    workaround until DeltaTable can read s3 as fast as pyarrow. and when it supports DNF predicates
    """
    if isinstance(paths, str):
        paths = [paths]

    # TODO use single expression when delta-rs filter supports true DNF https://github.com/delta-io/delta-rs/issues/1479
    fn = lambda ep: DeltaTable(ep[1],
        storage_options=storage_options or session_storage_options(),
        version=version,
    ).file_uris(ep[0])
    expr_paths = product(exprs, paths)

    with timer('list files {cost}s'):
        with ThreadPoolExecutor(len(exprs)) as pool:
            files = [f.replace('s3://', '') for f in chain(
                *pool.map(fn, expr_paths)
            )]

    with timer(f'total s3 fetch {len(files)} files time: ' + '{cost}s'):
        df = pl.from_arrow(
            pq.read_table(files, filesystem=fs3(), **kwargs)
        )
    return df



def get_paths(path: str | list[str], strip=True):
    if '*' in path:
        if not path.startswith('s3'):
            path = 's3://' + path
        with timer(f'listing files in {path} took ' + '{cost}s'):
            path = wr.s3.list_objects(path)
    if strip:
        path_ = strip_s3_prefix(path) if isinstance(path, str) else [strip_s3_prefix(p) for p in path]
        return path_
    return path

def read_parquet_s3(
    path: str | list[str],
    **kwargs
) -> pl.DataFrame:

    path_ = get_paths(path)
    with timer(f'reading files {path} took ' + '{cost}s'):
        kwargs['use_pyarrow'] = True
        kwargs['pyarrow_options'] = (kwargs.get('pyarrow_options') or {}) | {'filesystem': fs3()}
        return pl.read_parquet(path_, **kwargs)