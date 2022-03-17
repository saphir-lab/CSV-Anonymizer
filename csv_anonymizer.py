##################
# Import Modules
##################
### Import standard modules
from cmath import nan
# import logging
import hashlib
import os

### Import external modules
import pandas as pd

### Import personal modules
from constants import *
import utils

###########
# Variables
###########
### See function get_parameters  for other global variables
bad_choice = False
is_finished = False
app_banner = ""
csv_stat = pd.DataFrame()
input_content = pd.DataFrame()
parameter_content = pd.DataFrame()

###########
# Functions
###########
def csv_overview_main(df):
    utils.print_msg("INFO", "\nSummarizing CSV", colored=colored)
    csv_stat = pd.DataFrame()
    csv_stat = csv_overview_stat(df)
    
    # Output CSV File
    if not csv_stat.empty:
        output_csv_file = utils.generate_outfile_name(input_csv_file, name_extension=output_name_ext_overview, name_sep=output_name_separator, timestamp=output_name_timestamp)
        if output_csv_location:
            output_csv_file = utils.change_filename_location(output_csv_file, output_csv_location)
        utils.csv_save(csv_stat, csv_file=output_csv_file, csv_separator=output_csv_separator, colored=colored)
        
def csv_overview_stat(df):
    """Return a DataFrame with various info on every columns from a source dataframe

    Args:
        df (DataFrame): Source DataFrame to Analyze

    Returns:
        DataFrame: A dataFrame with some statistics on each columns
    """
    df_stat=pd.DataFrame()
    if not df.empty:
        df_stat["column_name"]=list(df.columns)
        df_stat["nb_value"] = list(df.count())
        df_stat["nb_unique_value"] = list(df.nunique())
        
        df_len = df.applymap(lambda x: len(x), na_action="ignore")
        df_stat["min_length"]  = list(df_len.min())
        df_stat["max_length"] = list(df_len.max())
        df_stat["nb_unique_length"] = list(df_len.nunique())
        df_stat[["min_length", "max_length"]] = df_stat[["min_length", "max_length"]].fillna("0").astype(int)   ## Necessary step as numeric column with NaN value are considered as float
    return df_stat

def csv_transform_fields(df, fields_to_transform, algorithm="blake2s", salt=""):
    df_transformed = pd.DataFrame()
    algorithm_hash = ""
    missing_value = ""
    distinct_values = []

    if fields_to_transform:
        if algorithm in VALID_HASHING:
            print(f"Salt: {salt}")
            if salt is None:
                salt=""
            algorithm_hash = f"hashlib.{algorithm}(salt.encode() + x.encode()).hexdigest()"
            missing_value = nan
        elif algorithm=="length":
            algorithm_hash = f"len(x)"
            missing_value = 0
        elif algorithm=="index":
            for el in fields_to_transform:
                distinct_value_col=df[el].unique()
                distinct_values = distinct_values + list(set(distinct_value_col).difference(distinct_values))
            algorithm_hash = f"{distinct_values}.index(x)+1"
            missing_value = 0
        else:
            pass
        df_transformed = df[fields_to_transform].fillna("").applymap(
            lambda x: 
                eval(algorithm_hash) if not x == "" else missing_value
        )
        # if not keep_column_name:
        #     header_transformed=[fld + column_extension for fld in fields_to_transform if fld in df]
        #     df_transformed.columns = header_transformed
    return df_transformed

def csv_transform_main(df, algorithm="blake2s", salt=""):
    utils.print_msg("INFO", "\nTransforming CSV", colored=colored)
    (fields_to_transform, fields_to_keep, fields_missing) = get_field_selection(df)
    if not fields_to_transform:
        utils.print_msg(severity="ERROR", msg=f"No field to transform found in input file. No Output will be generated.", colored=colored)
    else:
        result = pd.DataFrame()
        csv_transformed = pd.DataFrame()
        csv_transformed = csv_transform_fields(df, fields_to_transform=fields_to_transform, algorithm=algorithm, salt=salt)
        if not csv_transformed.empty:
            # Original version with all transformed data at the beginning of dataframe
            # -------------------------------
            # if keep_original_values:
            #     result = pd.concat([csv_transformed, df], axis=1)
            # else:
            #     result = pd.concat([csv_transformed, df[fields_to_keep]], axis=1)


            # New version keeping original columns order
            # -------------------------------
            for col in df:
                if col in fields_to_keep:
                    result[col] = df[col]
                
                if col in fields_to_transform:
                    if keep_original_values:
                        result[col] = df[col]
                    result[col+column_extension] = csv_transformed[col]

            # Output CSV File
            if not result.empty:
                output_csv_file = utils.generate_outfile_name(input_csv_file, name_extension=output_name_ext_transform, name_sep=output_name_separator, timestamp=output_name_timestamp)
                if output_csv_location:
                    output_csv_file = utils.change_filename_location(output_csv_file, output_csv_location)
                utils.csv_save(result, csv_file=output_csv_file, csv_separator=output_csv_separator, colored=colored)

def get_field_selection(df):
    """[Get Field name from header and classify to be hashed or not following parameter provided]

    Args:
        df ([DataFrame]): [DataFrame with CSV File content]
    """
    lst_fields_include = []
    lst_fields_exclude = []
    lst_fields_expected_missing = []

    if selection_type == "ALL":
        lst_fields_include=df.columns.to_list()
    elif selection_type == "INCLUSIONLIST":
        lst_fields_expected = include_list
        # Fields specified and present in dataframe
        lst_fields_include = [fld for fld in lst_fields_expected if fld in df]
        # Fields specified and NOT present in dataframe
        lst_fields_expected_missing = [fld for fld in lst_fields_expected if fld not in df]
        # Fields NOT specified but present in dataframe
        lst_fields_exclude = [fld for fld in df if fld not in lst_fields_expected]    
    elif selection_type == "EXCLUSIONLIST":
        lst_fields_expected = exclude_list
        # Fields specified and present in dataframe
        lst_fields_exclude = [fld for fld in lst_fields_expected if fld in df]
        # Fields specified and NOT present in dataframe
        lst_fields_expected_missing = [fld for fld in lst_fields_expected if fld not in df]
        # Fields NOT specified but present in dataframe
        lst_fields_include = [fld for fld in df if fld not in lst_fields_expected]    
    elif selection_type == "PARAMETERFILE":
        lst_fields_expected = parameter_content[parameter_content["Transform"] == "Y"].get("Fields",{}).to_list() 
        # Fields specified and present in dataframe
        lst_fields_include = [fld for fld in lst_fields_expected if fld in df]
        # Fields specified and NOT present in dataframe
        lst_fields_expected_missing = [fld for fld in lst_fields_expected if fld not in df]
        # Fields specified to be excluded and present in original dataframe
        lst_fields_exclude = [fld for fld in parameter_content.get("Fields",{}).to_list() if fld not in lst_fields_expected]    
    else:
        pass
    
    print(f"Option: {selection_type}")
    # print(f"Expected Fields Missing: {lst_fields_expected_missing}")
    # print(f"Include Fields: {lst_fields_include}")
    # print(f"Exclude Fields: {lst_fields_exclude}")
    print(f"- Columns specified but not present in CSV: {lst_fields_expected_missing}")
    print(f"- Columns to transform: {lst_fields_include}")
    print(f"- Columns to keep unchanged: {lst_fields_exclude}")
    if selection_type == "PARAMETERFILE":
        lst_fields_dropped = [fld for fld in df if fld not in parameter_content.get("Fields",{}).to_list()]    
        print(f"- Columns to drop (not specified in parameter file): {lst_fields_dropped}")
    
    return lst_fields_include, lst_fields_exclude, lst_fields_expected_missing

def get_parameters():
    """ Retrieve parameters from setting file if exists, otherwise apply default settings.
    """
    # all variables to initialize
    global banner_selection, colored, debug_level       # Console Parameters
    global input_csv_file, input_csv_separator          # Source Parameters
    global output_csv_location, output_csv_separator, do_overview # Output Parameters
    global output_name_separator, output_name_timestamp # Output FileName Parameters
    global algorithm, salt, keep_original_values, keep_column_name, selection_type # Transform Parameters
    global include_list, exclude_list, parameter_csv_file, parameter_csv_separator # Selection Parameters
    global output_name_ext_transform, output_name_ext_overview, column_extension # Force Parameters

    # Retrieve parameters from setting file if exists, othrewise apply default settings
    settings={}
    settings=utils.get_settings(SETTING_FILE)
    if not settings:
        utils.print_msg("WARNING",f"'{SETTING_FILE}' not found. Default settings applied")
        settings={}

    ### Assign setting dictionnay to indivisual variables

    # Console Parameters
    banner_selection = settings.get("Console", {}).get("Banner", "random")
    banner_selection = str(banner_selection)
    colored = settings.get("Console", {}).get("ColoredOutput", True)
    debug_level = settings.get("Console", {}).get("Debug", "WARNING").upper()
    debug_level = "WARNING" if debug_level is None else debug_level.upper()


    # Source Parameters
    input_csv_file = settings.get("Source", {}).get("CSVFile", NULL)            # if NULL, user will be prompted
    input_csv_separator = settings.get("Source", {}).get("CSVSeparator", ";")
    
    # Output Parameters
    output_csv_location = settings.get("Output", {}).get("CSVLocation", NULL)   # if NULL, will be same location as input_csv_file
    output_csv_separator = settings.get("Output", {}).get("CSVSeparator", input_csv_separator)
    do_overview = settings.get("Output", {}).get("OverviewFile", False)

    # Output FileName Parameters
    output_name_separator = settings.get("Output", {}).get("FileNameSeparator", "_")
    output_name_timestamp = settings.get("Output", {}).get("FileNameTimeStamp", True)
    
    # Transform Parameters
    algorithm = settings.get("Transform", {}).get("Algorithm","blake2s")
    if algorithm is None:
        if not do_overview:
            algorithm = "blake2s" 
    else:
        algorithm.lower()
    salt = settings.get("Transform", {}).get("Salt","")
    salt = "" if salt is None else salt
    keep_original_values = settings.get("Transform", {}).get("KeepOriginalValues", False)
    keep_column_name = settings.get("Transform", {}).get("KeepColumnName", True)
    selection_type = settings.get("Transform", {}).get("Selection","ALL")
    selection_type = "" if selection_type is None else selection_type.upper()

    include_list = settings.get("SelectionParameters", {}).get("InclusionList", [])
    exclude_list = settings.get("SelectionParameters", {}).get("ExclusionList", [])
    parameter_csv_file = settings.get("SelectionParameters", {}).get("ParameterFile", {}).get("CSVFile", NULL)
    parameter_csv_separator = settings.get("SelectionParameters", {}).get("ParameterFile", {}).get("CSVSeparator", input_csv_separator)

    # Forced Parameters:
    # output_name_ext_transform = algorithm
    output_name_ext_transform = "hashed"
    output_name_ext_overview = "overview"
    if algorithm:
        column_extension = "_" + algorithm

def validate_parameters(scope='all'):
    scope = scope.lower()
    valid = True

    global input_csv_file, input_content
    global parameter_csv_file, parameter_content
    global output_name_ext_transform, keep_column_name, column_extension
    global output_csv_separator, parameter_csv_separator
    global output_csv_location, output_csv_file

    if not output_csv_separator:
        output_csv_separator = input_csv_separator

    if not parameter_csv_separator:
        parameter_csv_separator = input_csv_separator

 # Missing Input CSV File
    if scope=='all' or scope=='input_file':
        print()
        if input_csv_file:
            utils.print_msg(severity="INFO", msg=f"Load CSV File to transform", colored=colored)
        else: 
            input_csv_file = utils.ask_file(question="CSV File to transform: ",colored=colored)
        input_content = utils.csv_load(csv_file=input_csv_file, csv_separator=input_csv_separator, colored=colored)
        while input_content.empty:
            input_csv_file = utils.ask_file(question="CSV File to transform: ",colored=colored)
            input_content = utils.csv_load(csv_file=input_csv_file, csv_separator=input_csv_separator, colored=colored)
        if len(input_content.columns) == 1:
            utils.print_msg(severity="WARNING", msg=f"CSV File loaded contains only 1 column. Verify if CSV Separator '{input_csv_separator}' parameter is correct one.", colored=colored)
            if utils.menu_choice_YN(msg="Do you want to process file", colored=colored) == "N":                
                exit()

# Missing Parameter File
    if scope=='all' or scope=='parameter_file':
        if selection_type == "PARAMETERFILE":
            print()
            if parameter_csv_file:
                utils.print_msg(severity="INFO", msg="Load Parameter File", colored=colored)
            else: 
                parameter_csv_file = utils.ask_file(question="Parameter File with fields to hash/not hash: ",colored=colored) 
            
            parameter_content = utils.csv_load(csv_file=parameter_csv_file, csv_separator=parameter_csv_separator, colored=colored)
            while parameter_content.empty:
                parameter_csv_file = utils.ask_file(question="Parameter File with fields to hash/not hash: ",colored=colored)
                parameter_content = utils.csv_load(csv_file=parameter_csv_file, csv_separator=parameter_csv_separator, colored=colored)
            
            if len(parameter_content.columns) == 1:
                utils.print_msg(severity="ERROR", msg=f"CSV File loaded contains only 1 column while 2 columns are required. Verify if CSV Separator '{parameter_csv_separator}' parameter is correct one.", colored=colored)
                valid=False
                exit()
            elif len(parameter_content.columns) > 2:
                utils.print_msg(severity="WARNING", msg=f"Parameter File contains more than 2 columns. Extra columns will be ignored. Verify if CSV Separator '{parameter_csv_separator}' parameter is correct one.", colored=colored)
                if utils.menu_choice_YN(msg="Do you want to process file", colored=colored) == "N":                
                    valid=False
                else:
                    parameter_content = parameter_content.iloc[: , :2] # Keep only the 2 first columns (other considered as comment)
            if valid:
                parameter_content.columns = ["Fields", "Transform"]
                parameter_content["Transform"] = parameter_content["Transform"].str.upper().str[0]

    if scope=='all' or scope=='algorithm':
        if algorithm not in VALID_ALGORITHM and algorithm is not None:
            utils.print_msg(severity="ERROR", msg=f"Invalid algorithm specified ({algorithm}).\nPossible values are : {VALID_ALGORITHM}", colored=colored)
            valid = False

    if scope=='all' or scope=='output_name_separator':
        if any(invalid_char in output_name_separator for invalid_char in INVALID_SEPARATOR):
            utils.print_msg(severity="ERROR", msg=f"Invalid character as FileNameSeparator ({output_name_separator}).\nProhibited characters are : {INVALID_SEPARATOR}", colored=colored)
            valid = False
    
    # We need to have a column name extension if we want to keep original values
    if scope=='all' or scope=='keep_original_values':
        if keep_original_values: 
            keep_column_name = False    # Force to change column name for transformed columns
            if not output_name_ext_transform:
                output_name_ext_transform = algorithm
    
    if scope=="all" or scope=='keep_column_name':
        if keep_column_name:
            column_extension=""


    return valid

##############
# Main program
##############
if __name__ == "__main__":
    os.system("cls||clear")
    get_parameters()
    app_banner = utils.get_app_banner(selection=banner_selection, banner_lst=banner_lst, colored=colored, appversion=APP_VERSION, creator=DESIGNED_BY)
    print(app_banner)
    if validate_parameters():
        if do_overview:
            csv_overview_main(input_content)
        if algorithm is None:
            utils.print_msg(severity="WARNING", msg=f"\nParameter algorithm not specied. Asusuming OverViewFile is needed. Skip Anonymization process !", colored=colored)
        else:
            csv_transform_main(input_content, algorithm, salt)