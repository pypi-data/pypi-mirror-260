import pandas as pd


def value_restriction_check(value_restriction_column_df, column_df):

    def lowercase_if_string(value):
        if isinstance(value, str):
            return value.lower()
        return value
        
    column_df = column_df.fillna("").astype(str)
    value_restriction_column_df = value_restriction_column_df.apply(lowercase_if_string)
    column_df = column_df.apply(lowercase_if_string)
    non_empty_column_df = column_df[column_df != ""]
    is_in_lookup_df = non_empty_column_df.isin(value_restriction_column_df)

    

    failed_value_restriction_check_rows = is_in_lookup_df[
        ~is_in_lookup_df
    ].index.tolist()

    if len(failed_value_restriction_check_rows) == 0:
        return True
    wrong_value_restriction_check = failed_value_restriction_check_rows
    wrong_value_restriction_check = [x + 2 for x in wrong_value_restriction_check]
    return {
        "No of rows failed": len(wrong_value_restriction_check),
        "rows_which_failed": wrong_value_restriction_check,
    }
