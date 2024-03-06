import pandas as pd
import logging


def master_data_check(
    master_df,
    column_excel_df,
    lookup_column_name,
    excel_column_name,
    primary_key_in_excel="",
    primary_key_in_master="",
):
    logging.info("master data check is started")

    if primary_key_in_master != "":
        # logging.info("master data check is started\n inside if ")
        column_excel_df = column_excel_df.rename(
            columns={primary_key_in_excel: primary_key_in_master}
        )
        # logging.info(f"{column_excel_df.head()}")

        merged_df = pd.merge(
            column_excel_df, master_df, on=primary_key_in_master, how="left"
        )
        # logging.info("merged dfs")
        # logging.info(f"{merged_df}")
        master_count = master_df[lookup_column_name].duplicated().sum()
        # logging.info(f"master count: {master_count}")
        merged_df[lookup_column_name] = (
            merged_df[lookup_column_name].fillna("").astype(str)
        )
        merged_df[excel_column_name] = (
            merged_df[excel_column_name].fillna("").astype(str)
        )

        def certification_concat_check(row):

            certifications_set = set(row[lookup_column_name].lower().split(", "))
            return row[excel_column_name].lower() in certifications_set

        error_column_name = lookup_column_name.lower()
        merged_df[error_column_name] = merged_df.apply(
            certification_concat_check, axis=1
        )
        # print(merged_df)
        logging.info("merged_df of lookup column done")
        failed_master_data_check_rows = merged_df[
            ~merged_df[error_column_name]
        ].index.tolist()
        # logging.info(f"{failed_master_data_check_rows}")
        if len(failed_master_data_check_rows) == 0:
            return True
        wrong_master_data_rows = failed_master_data_check_rows
        wrong_master_data_rows = [x + 2 for x in wrong_master_data_rows]
        return {
            "No of rows failed": len(wrong_master_data_rows),
            "rows_which_failed": wrong_master_data_rows,
            # "total rows": len(master_data_column_df)
        }

    else:
        master_data_column_df = master_df[lookup_column_name]
        column_df = column_excel_df[excel_column_name]

        def lowercase_if_string(value):
            if isinstance(value, str):
                return value.lower()
            return value

        master_data_column_df = master_data_column_df.apply(lowercase_if_string)
        column_df = column_df.apply(lowercase_if_string)

        is_in_master_data_df = column_df.isin(master_data_column_df)

        is_in_master_data_df = is_in_master_data_df.dropna()

        failed_master_data_check_rows = is_in_master_data_df[
            ~is_in_master_data_df
        ].index.tolist()

        if len(failed_master_data_check_rows) == 0:
            return True
        wrong_master_data_rows = failed_master_data_check_rows
        wrong_master_data_rows = [x + 2 for x in wrong_master_data_rows]
        return {
            "No of rows failed": len(wrong_master_data_rows),
            "rows_which_failed": wrong_master_data_rows,
            # "total rows": len(master_data_column_df)
        }
