from typing import Union, List

from pyspark.sql import DataFrame

from pyspark_connectby.connectby_query import ConnectByQuery


def connectBy(df: DataFrame, prior: str, to: str, start_with: Union[List[str], str] = None) -> DataFrame:
    query = ConnectByQuery(df, child_col=prior, parent_col=to, start_with=start_with)
    return query.get_result_df()


DataFrame.connectBy = connectBy
