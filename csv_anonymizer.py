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

###########
# Functions
###########
     
def csv_transform(df, algorithm="blake2s", salt="", info=True):
    (fields_to_transform, fields_to_keep, fields_missing) = get_field_selection(df, info=info)
    if not fields_to_transform:
        console.print_msg(severity="ERROR", msg=f"No field to transform found in input file. No Output will be generated.")
        return pd.DataFrame()
    else:
        col_order = []
        csv_transformed = pd.DataFrame()
        csv_transformed = input_csv_file.hash_content(fields_to_transform=fields_to_transform, algorithm=algorithm, salt=salt, display_salt=info)
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

def generate_filename(filename, filepath, subname, sep="_", timestamp=True, colored=True):
    newfilename = utils.FileName(filename, colored=colored)
    newfilename.add_subname(subname=subname, sep=sep)
    if timestamp:
        newfilename.add_datetime(sep=sep)
    newfilename.change_filepath(new_filepath=filepath)
    return newfilename

def get_chunk_iterator(csv_file):
    return csv_file.get_chunk_iterator(chunksize=chunk_size)

def get_field_selection(df, info=True):
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
    if info:
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
    global input_csv_filename, input_csv_separator, chunk_size         # Source Parameters
    global output_csv_location, output_csv_separator, do_overview # Output Parameters
    global output_name_separator, output_name_timestamp # Output FileName Parameters
    global algorithm, salt, keep_original_values, keep_column_name, selection_type, chunk_output # Transform Parameters
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
    chunk_size = settings.get("Source", {}).get("ChunkSize", 10000)

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
    chunk_output = settings.get("Transform", {}).get("ChunkOutput", True)
    selection_type = settings.get("Transform", {}).get("Selection","ALL")
    selection_type = "" if selection_type is None else selection_type.upper()

    include_list = settings.get("SelectionParameters", {}).get("InclusionList", [])
    exclude_list = settings.get("SelectionParameters", {}).get("ExclusionList", [])
    parameter_csv_filename = settings.get("SelectionParameters", {}).get("ParameterFile", {}).get("CSVFile", None)
    parameter_csv_separator = settings.get("SelectionParameters", {}).get("ParameterFile", {}).get("CSVSeparator", input_csv_separator)

    # Forced Parameters:
    output_name_ext_transform = "hashed"
    output_name_ext_overview = "overview"
    if algorithm:
        column_extension = "_" + algorithm

def validate_parameters():
    valid = True

    global input_csv_filename, input_csv_file, chunk_size
    global parameter_csv_filename, parameter_csv_file
    global output_name_ext_transform, output_name_ext_overview, keep_column_name, column_extension
    global output_csv_separator, output_name_timestamp, parameter_csv_separator
    global output_csv_location, output_csv_filename, overview_csv_filename
    global do_overview, algorithm, chunk_output

    if not output_csv_separator:
        output_csv_separator = input_csv_separator

    if not parameter_csv_separator:
        parameter_csv_separator = input_csv_separator

# Format problem with some parameter value
    if algorithm not in VALID_ALGORITHM and algorithm is not None:
        console.print_msg(severity="ERROR", msg=f"Invalid algorithm specified: '{algorithm}'.\nPossible values are: {VALID_ALGORITHM}")
        valid = False

    if any(invalid_char in output_name_separator for invalid_char in INVALID_SEPARATOR):
        console.print_msg(severity="ERROR", msg=f"Invalid character as FileNameSeparator ({output_name_separator}).\nProhibited characters are: {INVALID_SEPARATOR}")
        valid = False

    if valid:
    # Missing Input CSV File
        print()
        if input_csv_filename:
            input_csv_file = utils.CSVFile(csv_filename=input_csv_filename, sep=input_csv_separator,colored=colored)
            input_csv_file.load_sample()
        while not input_csv_filename or input_csv_file.content.empty:
            input_csv_filename = utils.FileName(colored=colored).ask_input_file("CSV File to transform: ")
            input_csv_file = utils.CSVFile(csv_filename=input_csv_filename, sep=input_csv_separator,colored=colored)
            input_csv_file.load_sample()
        if len(input_csv_file.content.columns) == 1:
            console.print_msg(severity="WARNING", msg=f"CSV File loaded contains only 1 column. Verify if CSV Separator '{input_csv_separator}' parameter is correct one.")
            if utils.Menu(colored=colored).menu_choice_YN("Do you want to process file") == "N":                
                exit()
    # Set same location for output files as input file in case not specified 
        if output_csv_location is None:
            output_csv_location=utils.FileName(input_csv_filename).filepath
        
    # Set same location for output files as input file in case not specified 
        overview_csv_filename = generate_filename(filename=input_csv_filename,
                                filepath=output_csv_location,
                                subname=output_name_ext_overview + output_name_separator + "chunk0",
                                sep=output_name_separator,
                                timestamp=output_name_timestamp,
                                colored=True,
                                )

        output_csv_filename = generate_filename(filename=input_csv_filename,
                                filepath=output_csv_location,
                                subname=output_name_ext_transform,
                                sep=output_name_separator,
                                timestamp=output_name_timestamp,
                                colored=True,
                                )

    # Missing Parameter File
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
        if keep_original_values and keep_column_name:
            keep_column_name = False    # Force to change column name for transformed columns
            console.print_msg(severity="INFO", msg=f"keep_original_values=true => set keep_column_name=false")

        # We have to generate multiple chunk file if algorithm index
        if algorithm=="index" and not chunk_output:
            chunk_output = True
            console.print_msg(severity="INFO", msg=f"algorithm='index' => set chunk_output=true")

        if  do_overview and not chunk_output:
            console.print_msg(severity="INFO", msg=f"Note that Overiew file is chunked by default. This generate statistics PER CHUNK.")
    
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
    if validate_parameters():
        df_iterator = get_chunk_iterator(input_csv_file)
        for i, input_csv_file.content in enumerate(df_iterator):
            print(f'\n--- Chunk {i+1}: lines {i*chunk_size+1}-{i*chunk_size + input_csv_file.content.shape[0]}')
            
            display_info = i == 0                               # Display info & add header only for the first chunk
            if not chunk_output and i>0:
                mode = "a"
                display_header=False 
            else:
                mode = "w"     # Set writing mode to append after first chunk
                display_header=True

            if do_overview:
                console.print_msg("INFO", "CSV Content Overview")
                input_csv_file.get_stat()
                if not input_csv_file.stat.empty:
                    overview_csv_filename = generate_filename(filename=input_csv_filename,
                        filepath=output_csv_location,
                        subname=f"{output_name_ext_overview}{output_name_separator}chunk{i+1}",
                        sep=output_name_separator,
                        timestamp=output_name_timestamp,
                        colored=True,
                        )
                    input_csv_file.save_stat(overview_csv_filename.fullpath, csv_separator=output_csv_separator)
            if algorithm is None:
                console.print_msg("WARNING", "Parameter algorithm not specified. Assuming OverviewFile is needed. Skip Anonymization process !")
            else:
                console.print_msg("INFO", "Hashing CSV Content")
                input_csv_file.content = csv_transform(input_csv_file.content, algorithm, salt, info=display_info)
                if not input_csv_file.content.empty:
                    if chunk_output:
                        output_csv_filename = generate_filename(filename=input_csv_filename,
                                                filepath=output_csv_location,
                                                subname=f"{output_name_ext_transform}{output_name_separator}chunk{i+1}",
                                                sep=output_name_separator,
                                                timestamp=output_name_timestamp,
                                                colored=True,
                                                )
                    input_csv_file.save_content(output_csv_filename.fullpath, csv_separator=output_csv_separator, header=display_header, mode=mode)
