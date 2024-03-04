#region Libraries

#%%
import pandas as pd
import numpy as np

from enum import Enum

from typing import Literal, Any

pd.options.display.max_columns = None
pd.options.display.max_rows = 8

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Type Conversion

#%%
def vector_to_series(vector: str|list|np.ndarray|pd.Series) -> pd.Series:
    '''Convert different types of vectors to series.

    Args:
        vector (str | list | array | Series): Vector.

    Returns:
        Series: Converted series. If unrecognized type is passed, np.nan is returned.

    Examples:
        >>> vector_to_series('a')
        >>> vector_to_series([1, 2, 3])
    '''
    if isinstance(vector, str):
        vector = pd.Series([vector])
    elif isinstance(vector, list):
        vector = pd.Series(vector)
    elif isinstance(vector, np.ndarray):
        vector = pd.Series(vector)
    elif isinstance(vector, pd.Series):
        pass
    elif isinstance(vector, pd.core.indexes.base.Index):
        vector = vector.to_series()
    else:
        vector = pd.Series(None) #np.nan

    return (vector)

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Slice

#%%
def pd_select(df: pd.DataFrame, 
              cols_before: str|list|np.ndarray|pd.Series=None, 
              cols_after: str|list|np.ndarray|pd.Series=None, 
              cols_drop: str|list|np.ndarray|pd.Series=None, 
              remaining=True) -> pd.DataFrame:
    '''Select columns to keep or drop from dataframe. Can be used to change order of columns.

    Args:
        df (DataFrame): Dataframe.
        cols_before (str | list | np.ndarray | Series, optional): Columns to keep at the start. Defaults to None.
        cols_after (str | list | np.ndarray | Series, optional): Columns to keep at the end. Defaults to None.
        cols_drop (str | list | np.ndarray | Series, optional): Columns to drop. Defaults to None.
        remaining (bool, optional): If true, the remaining columns (except the ones to drop) are placed between 'cols_before' and 'cols_after'. Defaults to True.

    Returns:
        DataFrame: Dataframe with specified columns.

    Examples:
        >>> df.pipe(pd_select, cols_before='type2', cols_after='value1', cols_drop='value5')
        >>> df.pipe(pd_select, cols_before=['value2', 'value4'], remaining=False)
        >>> df.pipe(pd_select, cols_before=pd_cols(df, 'value2', 'value4'))
        >>> df.pipe(pd_select, cols_before=['type1', *pd_cols(df, 'value2', 'value4')])
        >>> df.assign(var=0).pipe(lambda _: pd_select(_, cols_before=['var']))
        >>> df.assign(var1=0, var2=5, var3=10).pipe(lambda _: pd_select(_, cols_before=pd_cols(_, 'var1', 'var3')))
    '''
    if cols_before is None:
        cols_before = []
    else:
        cols_before = vector_to_series(cols_before).tolist()

    if cols_after is None:
        cols_after = []
    else:
        cols_after = vector_to_series(cols_after).tolist()

    if cols_drop is None:
        cols_drop = []
    else:
        cols_drop = vector_to_series(cols_drop).tolist()

    if remaining:
        cols_others = df.columns.difference(cols_before + cols_after, sort=False).tolist()
        cols_keep = (cols_before + cols_others + cols_after)
    else:
        cols_keep = (cols_before + cols_after)

    cols_keep = [x for x in cols_keep if x not in cols_drop]

    return df[cols_keep]

#%%
def pd_drop(df: pd.DataFrame, 
            cols: str|list|np.ndarray|pd.Series=None, 
            col_from: str=None, 
            col_to: str=None) -> pd.DataFrame:
    '''Drop selected columns from dataframe.

    Args:
        df (DataFrame): Dataframe.
        cols (str | list | array | Series, optional): Vector of columns to drop. Defaults to None.
        col_from (str, optional): First column in series of columns to drop. Defaults to None.
        col_to (str, optional): Last column in series of column to drop. Defaults to None.

    Returns:
        DataFrame: Dataframe after dropping specified columns.

    Notes:
        - Any value in 'cols' not in 'df' is ignored. 'col_from' and 'col_to' have to in in 'df'.

    Examples:
        >>> df.pipe(pd_drop, 'value2')
        >>> df.pipe(pd_drop, cols=['value2', 'type2'], col_from='value3', col_to='value5')
        >>> df.pipe(pd_drop, col_from='value3')
    '''
    if cols is not None:
        cols = vector_to_series(cols)
        cols_all = pd.Series(df.columns)
        cols = cols[cols.isin(cols_all)]
        df = df.drop(cols, axis=1)
    if (col_from is not None) | (col_to is not None):
        cols_all = pd.Series(df.columns)
        if col_from is not None:
            index_from = cols_all.tolist().index(col_from)
        else:
            index_from = 0
        if col_to is not None:
            index_to = cols_all.tolist().index(col_to) + 1
        else:
            index_to = len(cols_all)
        cols_to_drop = cols_all.iloc[index_from:index_to]

        df = df.drop(cols_to_drop, axis=1)
    return (df)

def pd_cols(df: pd.DataFrame, 
            col_from: str=None, 
            col_to: str=None) -> list:
    '''Get column names between two column names for given dataframe.

    Args:
        df (DataFrame): Dataframe.
        col_from (str, optional): First column in series of columns to return. Defaults to None.
        col_to (str, optional): Last column in series of column to return. Defaults to None.

    Returns:
        List: List of column names.

    Examples:
        >>> pd_cols(df, None, 'value2')
        >>> ['type1', *pd_cols(df, 'value2, 'value4')]
        >>> df.pipe(pd_select, cols_before=pd_cols(df, 'value2', 'value4'))
        >>> df.pipe(pd_drop, cols = pd_cols(df, 'value2'))
    '''
    cols = pd.Series(df.columns)
    if col_from is not None:
        index_from = cols.tolist().index(col_from)
    else:
        index_from = 0
    if col_to is not None:
        index_to = cols.tolist().index(col_to) + 1
    else:
        index_to = len(cols)
    cols_to_select = cols.iloc[index_from:index_to].to_list()
    return (cols_to_select)

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Concat

#%%
def pd_concat_series(v_values: pd.Series, values: float|list|np.ndarray|pd.Series) -> pd.Series:
    '''Append values to series.

    Args:
        v_values (Series): Series.
        values (float | list | array | Series): Vector of values to append.

    Returns:
        Series: Concatenated series.
        
    Examples:
        >>> v_values = pd.Series([0,1,2])
        >>> pd_concat_series(v_values, 3)
        >>> pd_concat_series(v_values, [3, 4])
        >>> v_values.pipe(pd_concat_series, 3)
        >>> v_values.pipe(pd_concat_series, [3, 4])
    '''
    v_values_concat = pd.concat([v_values, pd.Series(values)])
    return (v_values_concat)

#%%
def pd_concat_rows(df1: pd.DataFrame, df2: pd.DataFrame, ignore_index=True) -> pd.DataFrame:
    '''Concatenate dataframes by rows. Mainly useful for piping with 'pd.pipe()'. Wrapper around 'pd.concat()'. If one of the dataframes is blank, the other is returned, ensuring no change in datatype like with 'pd.concat()'.

    Args:
        df1 (DataFrame): Dataframe.
        df2 (DataFrame): Dataframe.
        ignore_index (bool):  If True, do not use the index values along the concatenation axis. The resulting axis will be labeled 0, ..., n - 1. Defaults to True.

    Returns:
        DataFrame: Concatenated dataframe.

    Examples:
        >>> pd_concat_rows(df1, df2)
        >>> df1.pipe(pd_concat_rows, df2)
    '''
    if df1.shape[0] == 0:
        return (df2)
    if df2.shape[0] == 0:
        return (df1)
    return (pd.concat([df1, df2], axis=0, ignore_index=ignore_index))

#%%
def pd_concat_rows_multiple(*l_df) -> pd.DataFrame:
    '''Concatenate multiple dataframes by rows. Wrapper around 'pd_concat_rows()'.

    Args:
        *l_df: List of dataframes.

    Returns:
        DataFrame: Concatenated dataframe.

    Examples:
        >>> pd_concat_rows_multiple(df1, df2, df3)
        >>> df1.pipe(pd_concat_rows, df2, df3)
    '''
    df = pd.DataFrame()
    for df2 in l_df:
        df = df.pipe(pd_concat_rows, df2)

    return (df)

#%%
def pd_concat_cols(df1: pd.DataFrame, 
                   df2: pd.DataFrame, 
                   ignore_index = True, 
                   drop_index = True) -> pd.DataFrame:
    '''Concatenate dataframes by columns. Mainly useful for piping with 'pd.pipe()'. Wrapper around 'pd.concat()'.

    Args:
        df1 (DataFrame): Dataframe.
        df2 (DataFrame): Dataframe.
        ignore_index (bool): Reset index for the two dataframes. Defaults to True.
        drop_index (bool): Drop the index when resetting index. Defaults to True.

    Returns:
        DataFrame: Concatenated dataframe.

    Examples
        >>> pd_concat_cols(df1, df2)
        >>> df1.pipe(pd_concat_cols, df2)
    '''
    if ignore_index:
        return pd.concat([df1.reset_index(drop=drop_index), df2.reset_index(drop=drop_index)], axis=1)

    return pd.concat([df1, df2], axis=1)

#%%
def pd_concat_cols_multiple(*l_df) -> pd.DataFrame:
    '''Concatenate multiple dataframes by cols. Wrapper around 'pd_concat_cols()' with 'ignore_index' and 'drop_index' set to True.

    Args:
        *l_df: List of dataframes.

    Returns:
        DataFrame: Concatenated dataframe.

    Examples:
        >>> pd_concat_rows_multiple(df1, df2, df3)
        >>> df1.pipe(pd_concat_rows, df2, df3)
    '''
    df = pd.DataFrame()
    for df2 in l_df:
        df = df.pipe(pd_concat_cols, df2)

    return (df)

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Merge

#%%
def pd_merge_asof(df1: pd.DataFrame, 
                  df2: pd.DataFrame, 
                  on: str= None, 
                  left_on: str= None, 
                  right_on: str= None, 
                  direction: Literal['backward', 'forward', 'nearest'] = 'forward', 
                  one_to_many = False):
    '''Perform a merge by key direction. Wrapper around 'pandas.merge_asof()'. Unlike 'pandas.merge_asof()', default direction is 'forward'. Additionally, 'one_to_many' is an additional option. Finally, if one of the two dataframes are blank, 'df1' is still returned along with columns from 'df2' added and set to np.nan, and no error is raised

    Args:
        df1 (DataFrame): Dataframe.
        df2 (DataFrame): Dataframe.
        on (str, optional): Common column name from 'df1' and 'df2' to join on. Defaults to None.
        left_on (str, optional): Column name from 'df1' to be joined on. Defaults to None.
        right_on (str, optional): Column name from 'df2' to be joined on. Defaults to None.
        direction (str, optional): Whether to search for prior, subsequent, or closest matches. Defaults to 'forward'. Acceptable values: 'forward', 'backward', or 'closest'.
        one_to_many (bool, optional): Whether to join one-to-one or one-to-many. Defaults to False (i.e. perform one-to-one join, default behavior of 'pandas.merge_asof()').

    Returns:
        DataFrame: Merged Dataframe.

    Notes:
        - Either 'on' or both of 'left_on' and 'right_on' needs to be specified.
        - If 'one_to_many' is False, a value from 'df2' is only matched once with a value (closest) from 'df2'.
        - If 'one_to_many' is True, a value from 'df2' is matched multiple times with values from 'df1' until there is another match. 
    '''
    if on is not None:
        left_on = on
        right_on = on
    if (df1.shape[0] > 1) & (df2.shape[0] > 0):
        if one_to_many:
            direction_rev = np.select(direction == np.array(['forward', 'backward', 'nearest']),
                                    ['backward', 'forward', 'nearest']).item()
            temp_df = pd.merge_asof(left = df2, right = df1.loc[:, [left_on]].eval(left_on + '_new = ' + left_on), left_on = right_on, right_on = left_on, direction = direction_rev).pipe(pd_drop, left_on)
            df = df1.merge(temp_df, left_on = left_on, right_on = left_on + '_new', how = 'left').pipe(pd_drop, left_on + '_new')
        else:
            df = pd.merge_asof(left = df1, right = df2, left_on = left_on, right_on = right_on, direction = direction)
    else:
        df = df1
        df2 = df2.drop(right_on, axis=1)
        for col_name in df2.columns.to_series():
            df = df.assign(**{col_name: np.nan})

    return (df)

def pd_merge_between_indices(df1: pd.DataFrame, 
                             df2: pd.DataFrame, 
                             left_min_col: str, 
                             left_max_col :str, 
                             right_col: str) -> pd.DataFrame:
    '''Merge two dataframe where a value in column, 'right_col', in 'df2' has to be between two columns, 'left_min_col' and 'left_max_col', in 'df1'.

    Args:
        df1 (DataFrame): Dataframe.
        df2 (DataFrame): Dataframe.
        left_min_col (str): Numeric column in 'df1' indicating lower limit for 'right_col'.
        left_max_col (str): Numeric column in 'df1' indicating upper limit for 'right_col'.
        right_col (str): Numeric column in 'df2'.

    Returns:
        DataFrame: Joined dataframe.
    '''
    if (df1.shape[0] > 1) and (df2.shape[0] > 0):
        temp_df = \
            (df1
                .loc[:, [left_min_col, left_max_col]]
                .pipe(pd_merge_asof, df2, left_on = left_min_col, right_on = right_col, one_to_many=True)
                .loc[lambda _: _[left_max_col] >= _[right_col]]
                .pipe(pd_drop, [left_max_col, right_col])
            )
        df = df1.merge(temp_df, how='left', on=left_min_col)
    else:
        df = df1
    
    return (df)

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Reshape

#%%
def pd_pivot_longer(df_wide: pd.DataFrame,
                    id_vars: str|list|np.ndarray|pd.Series,
                    value_vars: str|list|np.ndarray|pd.Series=None,
                    var_name: str=None,
                    value_name: str=None) -> pd.DataFrame:
    '''Reshape table from wide to long. Wrapper around 'pd.melt()' but provides easier documentation.

    Args:
        df_wide (DataFrame): Dataframe in wide format.
        id_vars (str | list | np.ndarray | pd.Series): Columns that uniquely identify each observation.
        value_vars (str | list | np.ndarray | pd.Series, optional): Columns to unpivot. Defaults to None. If set to None, all of the other columns are used.
        var_name (str, optional): Name to use for the 'variable' column. Defaults to None. If set to None, new column is named 'variable'.
        value_name (str, optional): Name to use for the 'value' column. Defaults to None. If set to None, new column is named 'value'.

    Returns:
        DataFrame: Dataframe in long format.

    Examples:
        >>> df_wide.pipe(pd_pivot_longer, id_vars='type1')
        >>> df_wide.pipe(pd_pivot_longer, id_vars='type1', var_name='type2', value_name='value1')
        >>> df_wide.pipe(pd_pivot_longer,
                         id_vars='type1',
                         value_vars=['t1', 't2'],
                         var_name='type2',
                         value_name='value1')
    '''
    if value_name is not None:
        df_long = df_wide.melt(id_vars=id_vars,
                               value_vars=value_vars,
                               var_name=var_name,
                               value_name=value_name)
    else:
        df_long = df_wide.melt(id_vars=id_vars,
                               value_vars=value_vars,
                               var_name=var_name)
        
    return (df_long)

#%%
def pd_pivot_wider(df_long: pd.DataFrame, 
                   index: str|list|np.ndarray|pd.Series, 
                   columns: str, 
                   values: str|list|np.ndarray|pd.Series=None,
                   keep_val:bool = False,
                   join_sep: str = '_',
                   col_first:bool = True) -> pd.DataFrame:
    '''Reshape table from long to wide. Wrapper around 'pd.pivot()' but prevents multiindex and provides easier documentation.

    Args:
        df_long (DataFrame): Dataframe in long format.
        index (str | list | array | Series): Columns that uniquely identify each observation.
        columns (str): Column to get names from.
        values (str | list | np.ndarray | pd.Series, optional): Column to get values from. Defaults to None. If set to None, all remaining columns are used.
        keep_val (bool, optional): See notes. Defaults to False.
        join_sep (str, optional): See notes. Defaults to '_'.
        col_first (bool, optional): See notes. Defaults to True.

    Returns:
        DataFrame: Dataframe in wide format.

    Notes:
        - If there is a single 'values' column and 'keep_val' is False, widened column names are taken from values in 'columns'.
        - If 'keep_val' is True or if there are multiple 'values' column, values in 'columns' column is joined with column names provided in 'values', separated by 'join_str'. Values in 'columns' column precede if 'col_first' is True.

    Examples:
        >>> df_long.pipe(pd_pivot_wider, index='type1', columns='type2')
        >>> df_long2.pipe(pd_pivot_wider, 
                          index=['type1', 'type1_'], 
                          columns='type2', 
                          values=['value1', 'value2'], 
                          join_sep='__', 
                          col_first=False)
    '''
    if values is None:
        columns_all = df_long.columns.to_series()
        values = columns_all[~columns_all.isin(vector_to_series(index))][columns_all != columns]

    values = vector_to_series(values)

    if values.__len__() == 1 and not keep_val:
        values = values.iloc[0]

    df_wide = df_long.pivot(index=index, columns = columns, values = values)

    df_wide = \
        (df_wide
            .pipe(pd_reset_column, rev=col_first, join_sep=join_sep)
            .reset_index()
        )

    return df_wide

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Conditionals

#%%
def pd_if_else(condition: bool|list|np.ndarray|pd.Series, v_true: Any|list|np.ndarray|pd.Series, v_false: Any|list|np.ndarray|pd.Series) -> Any | np.ndarray:
    '''If-else statement. Wrapper around 'np.where()'. Returns either single value or array instead of array.

    Args:
        condition (bool | list | np.ndarray | pd.Series): Vector of conditions.
        v_true (Any | list | np.ndarray | pd.Series): Vector of values if condition is true.
        v_false (Any | list | np.ndarray | pd.Series): Vector of values if condition is false.

    Returns:
        Any | np.ndarray: Resulting vector. If condition is 'condition' is bool, single value is returned, otherwise Series is returned.
    
    Notes:
        - Use 'pd_if_else_series()' to get output as series. 
        - 'pd_if_else()' is preferred since it does not cause index conflict during dataframe assignment.

    Examples:
        >>> pd_if_else(5 > 6, 5, 6)
        >>> pd_if_else(v < 0, 0, v)
    '''
    result = np.where(condition, v_true, v_false)

    if isinstance(condition, bool):
        result = result.tolist()

    return result

#%%
def pd_if_else_series(condition: bool|list|np.ndarray|pd.Series, v_true: Any|list|np.ndarray|pd.Series, v_false: Any|list|np.ndarray|pd.Series) -> Any | pd.Series:
    '''If-else statement. Wrapper around 'np.where()'. Returns either single value or Series instead of array.

    Args:
        condition (bool | list | np.ndarray | pd.Series): Vector of conditions.
        v_true (Any | list | np.ndarray | pd.Series): Vector of values if condition is true.
        v_false (Any | list | np.ndarray | pd.Series): Vector of values if condition is false.

    Returns:
        Any | pd.Series: Resulting vector. If condition is 'condition' is bool, single value is returned, otherwise Series is returned.
    
    Notes:
        - Use 'pd_if_else()' to get output as list.
        - 'pd_if_else()' is preferred since it does not cause index conflict during dataframe assignment.

    Examples:
        >>> pd_if_else(5 > 6, 5, 6)
        >>> pd_if_else(v < 0, 0, v)
    '''
    result = np.where(condition, v_true, v_false)

    if isinstance(condition, bool):
        result = result.tolist()
    else:
        result = pd.Series(result)

    return result

#%%
def pd_case_when(*args) -> list:
    '''Vectorized if-else statement. Wrapper around 'np.select()'. Inputs include even number of arguments, each separated by comma in the format: condition1, output1, condition2, output2, ... Final argument can be True, outputn for default output.

    Returns:
        list: Resulting list.

    Notes:
        - Use 'pd_case_when_series()' to get output as series.
        - 'pd_case_when()' is preferred since it does not cause index conflict during dataframe assignment.

    Examples:
        >>> df.assign(col_updated = lambda _: pd_case_when(_['col'] > 30, 'Good',
                                                           _['col'] > 20, 'Ok',
                                                           True, _['col']))
    '''
    conditions = args[0::2]
    values = args[1::2]

    result = np.select(conditions, values)

    return result

#%%
def pd_case_when_series(*args) -> pd.Series:
    '''Vectorized if-else statement. Wrapper around 'np.select()'. Inputs include even number of arguments, each separated by comma in the format: condition1, output1, condition2, output2, ... Final argument can be True, outputn for default output.

    Returns:
        Series: Resulting series.

    Notes:
        - Use 'pd_case_when()' to get output as list.
        - 'pd_case_when()' is preferred since it does not cause index conflict during dataframe assignment.

    Examples:
        >>> df.assign(col_updated = lambda _: pd_case_when_series(_['col'] > 30, 'Good',
                                                                  _['col'] > 20, 'Ok',
                                                                  True, _['col']).reset_index(drop=True))
    '''
    result = pd_case_when(*args)

    result = pd.Series(result)

    return result

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: View

#%%
def pd_style(df: pd.DataFrame, 
             negative = True, 
             max = True, 
             min = True, 
             precision: int=None):
    '''Return tabular visualization.

    Args:
        df (DataFrame): Dataframe.
        negative (bool, optional): Show negative numbers in red font. Defaults to True.
        max (bool, optional): Highlight max column values in purple. Defaults to True.
        min (bool, optional): Highlight min column vlaues in blue. Defaults to True.
        precision (int, optional): Number of decimals to show. Defaults to None. None means show all decimals.

    Examples:
        >>> df.pipe(style)
    '''
    def style_negative(v, props=''):
        return props if v < 0 else None
    def highlight_max(s, props=''):
        return np.where(s == np.nanmax(s.values), props, '')
    def highlight_min(s, props=''):
        return np.where(s == np.nanmin(s.values), props, '')
    v_col_num = df.select_dtypes('number').columns.to_series()
    df_style = \
        (df
            .assign(value2 = lambda _: _['value2'] - 5)
            .style
        )
    
    if precision is not None:
        df_style = df_style.format(precision = 3)
    if negative:
        df_style = df_style.map(style_negative, props='color:red;', subset=v_col_num)
    if max:
        df_style = df_style.apply(highlight_max, props='color:white;background-color:blue;', axis=0, subset=v_col_num)
    if min:
        df_style = df_style.apply(highlight_min, props='color:white;background-color:purple;', axis=0, subset=v_col_num)
    
    return (df_style)

#%%
def pd_print(df: pd.DataFrame, title: str=None) -> pd.DataFrame:
    '''Print and return dataframe. This is mainly to be used to print and assign or print and pipe at the same time.

    Args:
        df (pd.DataFrame): Dataframe to print and return.
        title (str, optional): Text to print before printing dataframe. Defaults to None.

    Returns:
        pd.DataFrame: Returns same dataframe as the input.

    Examples:
        >>> df.assign(x = 5).pipe(pd_print).query('y > 5')
    '''
    print ('')
    if title is not None:
        print (title)
    print (df)

    return df

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Index

#%%
def pd_reset_column(df: pd.DataFrame, 
                    rev: bool = False,
                    join_sep: str = '_',
                    keep_name: bool = False,
                    join_sep_name:str = '_') -> pd.DataFrame:
    '''Flatten multi-level column and remove column index name.

    Args:
        df (pd.DataFrame): Dataframe.
        rev (bool, optional): Whether to join in reverse order (down to up). Defaults to False.
        join_sep (str, optional): Separator string between column levels when joining. Defaults to '_'.
        keep_name (str, optional): Whether to join column index names to column names. Defaults to False.
        join_sep_name (str, optional): Separator string between column index names and column names when joining. Defaults to '_'.        

    Returns:
        pd.DataFrame: Dataframe with single-level column an dno column index name.
    '''
    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):
        df_columns = df.columns.to_list()
        if keep_name:
            df_columns_updated = []
            for i, name in enumerate(df.columns.names):
                if name is not None:
                    df_columns
                    for item in df_columns:
                            new_item = list(item)
                            new_item[i] = name + join_sep_name + new_item[i]
                            df_columns_updated.append(tuple(new_item))
            df_columns = df_columns_updated
        if rev:
            df.columns = [join_sep.join(col[::-1]) for col in df_columns]
        else:
            df.columns = [join_sep.join(col) for col in df_columns]
    else:
        if keep_name:
            df.columns = [(df.columns.name + join_sep_name + col) for col in df.columns]
        else:
            df.columns = df.columns.rename(None)

    return df

#endregion -------------------------------------------------------------------------------------------------
#region Functions: Pandas: Others

#%%
def pd_set_colnames(df: pd.DataFrame, 
                    col_names: str|list|np.ndarray|pd.Series):
    '''Set column names. Wrapper around 'pd.concat()'. Works with length mismatches.

    Args:
        df (DataFrame): Dataframe.
        col_names (str | list | np.ndarray | Series): Vector of column names.

    Returns:
        DataFrame: Dataframe with updated column names.

    Notes:
        - If len(col_names) > len(df), additional 'col_names' are excluded.
        - If len(df) > len(col_names), remaning column names are filled with sequence of numbers based on position.

    Examples:
        >>> df = pd.DataFrame({'c1': [1,2],
                               'c2': [3,4]})
        >>> df.pipe(pd_set_colnames, 'c1')
        >>> df.pipe(pd_set_colnames, ['c1', 'c2', 'c3'])
    '''
    col_names = vector_to_series(col_names)

    len_df = df.shape[1]
    len_col_names = len(col_names)

    if len_df > len_col_names:
        col_names = pd.concat([col_names, pd.Series(np.arange(len_col_names, len_df))], ignore_index=True)
    if len_col_names > len_df:
        col_names = col_names.iloc[:len_df]

    df = df.set_axis(col_names, axis=1)

    return (df)

#%%
def pd_split_column(df: pd.DataFrame, 
                    delim: str, 
                    column_original: str, 
                    columns_new: list|np.ndarray|pd.Series, 
                    drop_original = False) -> pd.DataFrame:
    '''Split a column into multiple columns based on deliminator.

    Args:
        df (DataFrame): Dataframe.
        delim (str): Deliminator.
        column_original (str): Name of column to split.
        columns_new (list | array | Series): Names of columns after split.
        drop_original (bool, optional): Whether or not to drop the original column. Defaults to False.

    Returns:
        DataFrame: Dataframe with split columns.

    Examples:
        >>> pd_split_column(df, '_', 'id', ['name', 'type'], drop_original = True)
        >>> df.pipe(lambda _: pd_split_column(_, '_', 'id', ['name', 'type']))
    '''
    df[columns_new] = df[column_original].str.split(delim, expand = True)
    if drop_original:
        df = pd_drop(df, column_original)

    return (df)

#endregion -------------------------------------------------------------------------------------------------


