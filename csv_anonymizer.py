##################
# Import Modules
##################
### Import standard modules

### Import external modules
import pandas as pd

### Import personal modules
from constants import *
import utils

###########
# Variables
###########
### See function get_parameters  for other global variables
console=utils.Console(colored=False)
bad_choice = False
is_finished = False
csv_stat = pd.DataFrame()

###########
# Functions
###########
     
def csv_transform(df, algorithm="blake2s", salt=""):
    (fields_to_transform, fields_to_keep, fields_missing) = get_field_selection(df)
    if not fields_to_transform:
        console.print_msg(severity="ERROR", msg=f"No field to transform found in input file. No Output will be generated.")
        return pd.DataFrame()
    else:
        col_order = []
        csv_transformed = pd.DataFrame()
        csv_transformed = input_csv_file.hash_content(fields_to_transform=fields_to_transform, algorithm=algorithm, salt=salt)
        if not csv_transformed.empty:
            # Rename columns if needed
            # -------------------------
            if not keep_column_name:
                header_transformed=[fld + column_extension for fld in fields_to_transform if fld in df]
                csv_transformed.columns = header_transformed

            # Determine final column order
            # ----------------------------
            for col in df:
                if col in fields_to_keep:
                    col_order.append(col)               
                if col in fields_to_transform:
                    if keep_original_values:
                        col_order.append(col)
                    col_order.append(col+column_extension)

            # Add transformed data at the beginning of dataframe
            # ---------------------------------------------------
            if keep_original_values:
                df = pd.concat([csv_transformed, df], axis=1)
            else:
                df = pd.concat([csv_transformed, df[fields_to_keep]], axis=1)
            df = df[col_order]      # Columns re-ordering following original source
    return df

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
        lst_fields_expected = parameter_csv_file.content[parameter_csv_file.content["Transform"] == "Y"].get("Fields",{}).to_list() 
        # Fields specified and present in dataframe
        lst_fields_include = [fld for fld in lst_fields_expected if fld in df]
        # Fields specified and NOT present in dataframe
        lst_fields_expected_missing = [fld for fld in lst_fields_expected if fld not in df]
        # Fields specified to be excluded and present in original dataframe
        lst_fields_exclude = [fld for fld in parameter_csv_file.content.get("Fields",{}).to_list() if fld not in lst_fields_expected]    
    else:
        pass
    
    print(f"Option: {selection_type}")
    print(f"- Columns specified but not present in CSV: {lst_fields_expected_missing}")
    print(f"- Columns to transform: {lst_fields_include}")
    print(f"- Columns to keep unchanged: {lst_fields_exclude}")
    if selection_type == "PARAMETERFILE":
        lst_fields_dropped = [fld for fld in df if fld not in parameter_csv_file.content.get("Fields",{}).to_list()]    
        print(f"- Columns to drop (not specified in parameter file): {lst_fields_dropped}")
    
    return lst_fields_include, lst_fields_exclude, lst_fields_expected_missing

def get_parameters():
    """ Retrieve parameters from setting file if exists, otherwise apply default settings.
    """
    # all variables to initialize
    global banner_selection, colored, debug_level       # Console Parameters
    global input_csv_filename, input_csv_separator          # Source Parameters
    global output_csv_location, output_csv_separator, do_overview # Output Parameters
    global output_name_separator, output_name_timestamp # Output FileName Parameters
    global algorithm, salt, keep_original_values, keep_column_name, selection_type # Transform Parameters
    global include_list, exclude_list, parameter_csv_filename, parameter_csv_separator # Selection Parameters
    global output_name_ext_transform, output_name_ext_overview, column_extension # Force Parameters

    # Retrieve parameters from setting file if exists, othrewise apply default settings
    settings_file=utils.ParameterFile(filename=SETTING_FILE, colored=False)
    settings=settings_file.parameters
    if not settings:
        console.print_msg("WARNING",f"'{SETTING_FILE}' not found. Default settings applied")
        settings={}

    ### Assign setting dictionnay to indivisual variables

    # Console Parameters
    banner_selection = settings.get("Console", {}).get("Banner", "random")
    colored = settings.get("Console", {}).get("ColoredOutput", True)
    console.colored=colored
    debug_level = settings.get("Console", {}).get("Debug", "WARNING").upper()
    debug_level = "WARNING" if debug_level is None else debug_level.upper()

    # Source Parameters
    input_csv_filename = settings.get("Source", {}).get("CSVFile", None)           # if None, user will be prompted
    input_csv_separator = settings.get("Source", {}).get("CSVSeparator", ";")
    
    # Output Parameters
    output_csv_location = settings.get("Output", {}).get("CSVLocation", None)   # if None, will be same location as input_csv_filename
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
    parameter_csv_filename = settings.get("SelectionParameters", {}).get("ParameterFile", {}).get("CSVFile", None)
    parameter_csv_separator = settings.get("SelectionParameters", {}).get("ParameterFile", {}).get("CSVSeparator", input_csv_separator)

    # Forced Parameters:
    # output_name_ext_transform = algorithm
    output_name_ext_transform = "hashed"
    output_name_ext_overview = "overview"
    if algorithm:
        column_extension = "_" + algorithm

def validate_parameters_and_load_files(scope='all'):
    scope = scope.lower()
    valid = True

    global input_csv_filename, input_csv_file
    global parameter_csv_filename, parameter_csv_file
    global output_name_ext_transform, output_name_ext_overview, keep_column_name, column_extension
    global output_csv_separator, parameter_csv_separator
    global output_csv_location, output_csv_filename, output_csv_file, overview_csv_filename, overview_csv_file

    if not output_csv_separator:
        output_csv_separator = input_csv_separator

    if not parameter_csv_separator:
        parameter_csv_separator = input_csv_separator

# Format problem with some parameter value
    if scope=='all' or scope=='algorithm':
        if algorithm not in VALID_ALGORITHM and algorithm is not None:
            console.print_msg(severity="ERROR", msg=f"Invalid algorithm specified: '{algorithm}'.\nPossible values are: {VALID_ALGORITHM}")
            valid = False

    if scope=='all' or scope=='output_name_separator':
        if any(invalid_char in output_name_separator for invalid_char in INVALID_SEPARATOR):
            console.print_msg(severity="ERROR", msg=f"Invalid character as FileNameSeparator ({output_name_separator}).\nProhibited characters are: {INVALID_SEPARATOR}")
            valid = False

    if valid:
    # Missing Input CSV File
        if scope=='all' or scope=='input_file':
            print()
            if input_csv_filename:
                input_csv_file = utils.CSVFile(csv_filename=input_csv_filename, sep=input_csv_separator,colored=colored)
                input_csv_file.load()
            while not input_csv_filename or input_csv_file.content.empty:
                input_csv_filename = utils.FileName(colored=colored).ask_input_file("CSV File to transform: ")
                input_csv_file = utils.CSVFile(csv_filename=input_csv_filename, sep=input_csv_separator,colored=colored)
                input_csv_file.load()
            if len(input_csv_file.content.columns) == 1:
                console.print_msg(severity="WARNING", msg=f"CSV File loaded contains only 1 column. Verify if CSV Separator '{input_csv_separator}' parameter is correct one.")
                if utils.Menu(colored=colored).menu_choice_YN("Do you want to process file") == "N":                
                    exit()
    # Set same location for output files as input file in case not specified 
        if output_csv_location is None:
            output_csv_location=utils.FileName(input_csv_filename).filepath
        
        overview_csv_filename = utils.FileName(input_csv_filename, colored=colored)
        overview_csv_filename.add_subname(subname=output_name_ext_overview, sep=output_name_separator)
        overview_csv_filename.add_datetime(sep=output_name_separator)
        overview_csv_filename.change_filepath(new_filepath=output_csv_location)

        output_csv_filename = utils.FileName(input_csv_filename, colored=colored)
        output_csv_filename.add_subname(subname=output_name_ext_transform, sep=output_name_separator)
        output_csv_filename.add_datetime(sep=output_name_separator)
        output_csv_filename.change_filepath(new_filepath=output_csv_location)
        
        # Output CSV File
        if not csv_stat.empty:
            output_csv_file = utils.generate_outfile_name(input_csv_filename, name_extension=output_name_ext_overview, name_sep=output_name_separator, timestamp=output_name_timestamp)
            if output_csv_location:
                output_csv_file = utils.change_filename_location(output_csv_file, output_csv_location)
            utils.csv_save(csv_stat, csv_file=output_csv_file, csv_separator=output_csv_separator, colored=colored)

    # Missing Parameter File
        if scope=='all' or scope=='parameter_file':
            if selection_type == "PARAMETERFILE":
                print()
                if parameter_csv_filename:
                    parameter_csv_file = utils.CSVFile(csv_filename=parameter_csv_filename, sep=parameter_csv_separator,colored=colored)
                    parameter_csv_file.load()

                while not parameter_csv_filename or parameter_csv_file.content.empty:
                    parameter_csv_filename = utils.FileName(colored=colored).ask_input_file("Parameter File with fields to hash/not hash: ")
                    parameter_csv_file = utils.CSVFile(csv_filename=parameter_csv_filename, sep=parameter_csv_separator,colored=colored)
                    parameter_csv_file.load()

                if len(parameter_csv_file.content.columns) == 1:
                    console.print_msg(severity="ERROR", msg=f"CSV File loaded contains only 1 column while 2 columns are required. Verify if CSV Separator '{parameter_csv_separator}' parameter is correct one.")
                    valid=False
                    exit()
                elif len(parameter_csv_file.content.columns) > 2:
                    console.print_msg(severity="WARNING", msg=f"Parameter File contains more than 2 columns. Extra columns will be ignored. Verify if CSV Separator '{parameter_csv_separator}' parameter is correct one.")
                    if utils.Menu(colored=colored).menu_choice_YN("Do you want to process file") == "N":                
                        valid=False
                    else:
                        parameter_csv_file.content = parameter_csv_file.content.iloc[: , :2] # Keep only the 2 first columns (other considered as comment)
                if valid:
                    parameter_csv_file.content.columns = ["Fields", "Transform"]
                    parameter_csv_file.content["Transform"] = parameter_csv_file.content["Transform"].str.upper().str[0]
        
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
    console.clear_screen()
    get_parameters()
    print(console.get_app_banner(selection=banner_selection, banner_lst=banner_lst, appversion=APP_VERSION, creator=DESIGNED_BY))
    if validate_parameters_and_load_files():
        if do_overview:
            print()
            console.print_msg("INFO", "CSV Content Overview")
            input_csv_file.get_stat()
            if not input_csv_file.stat.empty:
                input_csv_file.save_stat(overview_csv_filename.fullpath, csv_separator=output_csv_separator)
        if algorithm is None:
            console.print_msg("WARNING", "Parameter algorithm not specified. Assuming OverviewFile is needed. Skip Anonymization process !")
        else:
            print()
            console.print_msg("INFO", "Hashing CSV Content")
            input_csv_file.content = csv_transform(input_csv_file.content, algorithm, salt)
            if not input_csv_file.content.empty:
                input_csv_file.save_content(output_csv_filename.fullpath, csv_separator=output_csv_separator)
