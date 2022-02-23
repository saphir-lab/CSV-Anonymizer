### Import standard modules
import datetime
import json
import os
from pathlib import Path
import sys

### Import external modules
import pandas as pd
import yaml

### Import personal modules
from utils.layout import *

def ask_file(question="File name: ", colored=True):
    """Loop requesting user for a file name until this one is found/exists

    Returns:
        str: a file name with appropriate path format
    """
    msg=""
    file_in = ""
    while not file_in:
        if msg:
            print_msg("ERROR", msg=msg, colored=colored)
        file_in = Path(input(question).strip('"'))
        if not file_in.exists() or not file_in.is_file():
            msg = "File Specified doesn't exists. Please specify full path"
            file_in=""
    return file_in

def change_filename_location(file_in, target_location):
    """Change the location of a <file_in> using <target_location>

    Args:
        file_in (str): a file name (with path)
        target_location (str): a path (directory name only)

    Returns:
        [str]: <target_location>/<filename>
    """
    (file_location, file_name) = os.path.split(file_in)
    file_out = target_location + os.path.sep + file_name
    return file_out

def csv_load(csv_file, csv_separator=";", colored=True):
    """[Load and return a CSV file content as a pandas dataframe]

    Returns:
        [DataFrame]: [DataFrame with CSV File content]
    """
    df=pd.DataFrame()
    try:
        df = pd.read_csv(csv_file, delimiter=csv_separator, low_memory=False, dtype=str)  # Force all columns as string
    # except FileNotFoundError:
    #     print("- File not found.")
    # except pd.errors.EmptyDataError:
    #     print("- No data")
    # except pd.errors.ParserError:
    #     print("- Parsing error (check file and or separator character)")
    except:
        print_msg("ERROR", f"{sys.exc_info()[0]}: Fail to load CSV file '{csv_file}'", colored=colored)
    else:
        (nb_rows, nb_columns) = df.shape
        print_msg("SUCCESS", f"Successfully load CSV file '{csv_file}'")
        print(f"- File contains {nb_columns} columns and {nb_rows} lines")
    return df

def csv_save(df, csv_file, csv_separator=";", colored=True):
    """[Save a pandas dataframe as CSV File]

    Returns:
        [Boolean]: True when successfully saved. False otherwise
    """
    status=True
    try:
        df.to_csv(csv_file, encoding="UTF-8", index=False, sep=csv_separator)
    except:
        print_msg("ERROR", f"{sys.exc_info()[0]}: Fail to save CSV file '{csv_file}'", colored=colored)
    else:
        print_msg("SUCCESS", f"Successfully save CSV file '{csv_file}'", colored=colored)

    return status

def generate_outfile_name(file_in, name_extension, name_sep="_", timestamp=True):
    """Add a timestamp in the name of an existing file name

    Args:
        file_in (str): a file name (with path)
        name_extension (str) [Optional]: 

    Returns:
        [str]: <file_in>_<name_extension>_timestamp
    """
    (file_name, file_ext) = os.path.splitext(file_in)
    end_name = ""
    if name_extension:
        end_name += name_sep + name_extension
    if timestamp:
        # end_name += name_sep + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        dt = datetime.datetime.now()
        end_name += name_sep + dt.strftime('%Y%m%d') + name_sep + dt.strftime('%H%M%S') 
    file_out = file_name + end_name + file_ext
    return file_out

def get_file_type(filename):
    """Retrieve the file extension from a filename (part after last DOT)

    Args:
        filename (file): A File name with full path

    Returns:
        String: Characters after last dot in a file path usually last 3 or 4 characters)
    """
    filetype=""
    # try:
    #     filetype = os.path(filename).suffix
    # except:
    #      filetype=""
    try:
        filetype = os.path.splitext(filename)[1].lower()
    except:
        filetype=""
    return filetype

def get_settings(filename):
    """Return a Dictionnary from Json or Yaml file

    Args:
        filename (file): File Name containing settings. Supported foramt : Json or Yaml

    Returns:
        Dictionnary: [A Dictionnary build from Json/YAML]
    """
    custom_settings = {}
    filetype = get_file_type(filename)
    if filetype == ".json":
        try:
            with open(filename) as config_file:
                custom_settings = json.load(config_file)
        except:
            print_msg("ERROR",f"Setting File '{filename}' not found.")
    elif filetype == ".yaml" or filetype == ".yml" :
        try:
            with open(filename) as config_file:
                custom_settings = yaml.safe_load(config_file)
        except:
            print_msg("ERROR",f"Setting File '{filename}' not found.")
    else:
        pass
    return custom_settings

