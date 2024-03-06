import pandas as pd

def get_interaction_from_line(line: str) -> str:
    """
    Get pairwise interaction in format AtomNumber1AtomNumber2 from set of lines, it is to be used withing list comprehension
    """
    interaction =  line.split(':')[1].split('->')[0] + line.split(':')[1].split('->')[1].split('(')[0]
    return interaction

def get_indicator_from_path(path: str) -> str:
    """
    For ICOBILIST.lobster, ICOHPLIST.lobster, ICOOPLIST.lobster
    """
    END_LEN = len("LIST.lobster")
    filename = path.split('/')[-1]
    indicator = filename[:-END_LEN].lower()
    return indicator

def multiply_by_minus_one(df: pd.DataFrame, excluding='E') -> pd.DataFrame:
    """
    For COHPCAR.lobster, all values except energy must be multiplied by -1
    """
    out_df = df.copy()
    to_muliply = out_df.columns.difference([excluding])
    out_df[to_muliply] = -1 * out_df[to_muliply]
    return out_df
