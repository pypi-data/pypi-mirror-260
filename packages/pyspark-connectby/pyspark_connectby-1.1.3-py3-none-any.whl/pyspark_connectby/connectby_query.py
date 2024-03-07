from dataclasses import dataclass
from typing import Union, List

from pyspark.sql import DataFrame

COLUMN_START_WITH = 'START_WITH'
COLUMN_LEVEL = 'LEVEL'
COLUMN_CONNECT_BY_ISLEAF = 'CONNECT_BY_ISLEAF'


@dataclass
class Path:
    steps: [str]
    is_leaf: bool = False

    @classmethod
    def path_start_with(cls, start_id: str) -> 'Path':
        return cls(steps=[start_id])

    @property
    def start_id(self) -> str:
        return self.steps[0]

    @property
    def end_id(self) -> str:
        return self.steps[-1]

    @property
    def level(self) -> int:
        return len(self.steps)


@dataclass
class Node:
    node_id: str
    parent_id: str


class ConnectByQuery:
    def __init__(self, df: DataFrame, child_col: str, parent_col: str, start_with: Union[List[str], str] = None):
        self.df: DataFrame = df
        self.child_col = child_col
        self.parent_col = parent_col
        self.start_with = start_with

        self._start_paths: [Path] = None
        self._all_nodes: [Node] = None

    @property
    def start_paths(self) -> [Path]:
        if self._start_paths is None:
            if self.start_with is None:
                paths = []
            elif isinstance(self.start_with, list):
                paths = [Path.path_start_with(i) for i in self.start_with]
            else:
                assert isinstance(self.start_with, str)
                paths = [Path.path_start_with(self.start_with)]
            self._start_paths = paths or self.__default_start_paths()

        return self._start_paths

    @property
    def all_nodes(self) -> [Node]:
        if self._all_nodes is None:
            rows = self.df.select(self.child_col, self.parent_col).collect()
            self._all_nodes = [Node(node_id=r[self.child_col], parent_id=r[self.parent_col]) for r in rows]
        return self._all_nodes

    def __children_with_parent(self, parent_id: str) -> [Node]:
        children = list(filter(lambda n: n.parent_id == parent_id, self.all_nodes))
        return children

    def __default_start_paths(self) -> [Path]:
        rows = self.df.collect()
        return [Path.path_start_with(r[self.child_col]) for r in rows]

    def __fetch_descendants(self, path: Path) -> []:
        children_nodes: [Node] = self.__children_with_parent(path.end_id)
        is_leaf = len(children_nodes) == 0
        if is_leaf:
            path.is_leaf = True
            return []

        children = [Path(steps=path.steps + [c.node_id]) for c in children_nodes]
        grandchildren = list(map(lambda c: self.__fetch_descendants(c), children))

        descendants = children + grandchildren
        return descendants

    @staticmethod
    def __flatten_list(nested_list: []) -> []:
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list += ConnectByQuery.__flatten_list(item)
            else:
                flat_list.append(item)
        return flat_list

    def __run(self) -> [Path]:
        descendants = list(map(lambda e: self.__fetch_descendants(e), self.start_paths))
        descendants_paths: [Path] = self.__flatten_list(descendants)

        return self.start_paths + descendants_paths

    def get_result_df(self) -> DataFrame:
        result_paths: [Path] = self.__run()
        schema = f'''
            {COLUMN_START_WITH} string, 
            {self.child_col} string, 
            {COLUMN_LEVEL} int, 
            {COLUMN_CONNECT_BY_ISLEAF} boolean
        '''
        spark = self.df._session

        result_df = spark.createDataFrame([(p.start_id, p.end_id, p.level, p.is_leaf) for p in result_paths],
                                          schema=schema)
        return result_df.join(self.df, on=self.child_col)
