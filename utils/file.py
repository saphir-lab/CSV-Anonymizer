### Import standard modules
from cmath import nan
import datetime
import hashlib
import json
import os
import sys

### Import external modules
import pandas as pd
import yaml

### Import personal modules
from utils.console import Console

### Retrieve filename and filename elements (path, name, extension, etc.)
class FileName():
    def __init__(self, fullpath="", colored=True):
        self.fullpath=fullpath
        self.fullpath_noextension=""
        self.filepath=""
        self.filename=""
        self.filename_noextension=""
        self.fileextension=""
        if fullpath:
            self.set_filename_elements(fullpath)
        self.console = Console(colored)

    def ask_input_file(self, question="File name: "):
        """Loop requesting user for a file name until this one is found/exists

        Returns:
            str: a file name with appropriate path format
        """
        msg=""
        file_in = ""
        while not file_in:
            if msg:
                self.console.print_msg("ERROR", msg)
            file_in = input(question).strip('"')
            if not os.path.isfile(file_in):
                msg = "File Specified doesn't exists. Please specify full path"
                file_in=""
        self.set_filename_elements(file_in)
        return file_in

    def print_filename_details(self):
        print()
        print("- fullpath: " + self.fullpath)
        print("- fullpath no extension: " + self.fullpath_noextension)
        print("- filepath: " + self.filepath)
        print("- filename: " + self.filename)
        print("- filename no extension: " + self.filename_noextension)
        print("- file extension: " + self.fileextension)

    def set_filename_elements(self, fullpath):
        self.fullpath = fullpath
        try:
            self.filepath = os.path.dirname(self.fullpath)
            self.filename = os.path.basename(self.fullpath)
            self.filename_noextension, self.fileextension = os.path.splitext(self.filename)
            if self.filepath:
                self.fullpath_noextension = self.filepath + os.path.sep + self.filename_noextension
            else:
                self.fullpath_noextension = self.filename_noextension
        except Exception as e:
            self.console.print_msg("ERROR", f"{str(e)}")

### Transform filename
    def change_filepath(self, new_filepath):
        """Change the location of current filename with new_filepath>
        """
        if new_filepath:
            new_fullpath = new_filepath + os.path.sep + self.filename
        else:
            new_fullpath = self.filename
        self.set_filename_elements(new_fullpath)
        return new_fullpath
 
    def add_subname(self, subname, sep="_"):
        """Add free text at the end of the filename using an optional text separator (default separator "_")
        """
        new_fullpath = self.fullpath_noextension + sep + subname + self.fileextension
        self.set_filename_elements(new_fullpath)
        return new_fullpath

    def add_dayonly(self, sep="_"):
        """Add date (YYMMDD) at the end of the filename using an optional text separator (default separator "_")
        """
        dt = datetime.datetime.now()      
        new_fullpath = self.fullpath_noextension + sep + dt.strftime('%Y%m%d') + self.fileextension
        self.set_filename_elements(new_fullpath)
        return new_fullpath

    def add_datetime(self, sep="_"):
        """Add timestamp (YYMMDD HHMMSS) at the end of the filename using an optional text separator (default separator "_")
        """
        dt = datetime.datetime.now()      
        new_fullpath = self.fullpath_noextension + sep + dt.strftime('%Y%m%d') + sep + dt.strftime('%H%M%S') + self.fileextension
        self.set_filename_elements(new_fullpath)
        return new_fullpath

### Read & write CSV File using Pandas dataframes
class CSVFile():
    def __init__(self, csv_filename="", sep=";", colored=True):
        self.filename = csv_filename
        self.separator = sep
        self.console = Console(colored)
        self.content = pd.DataFrame()
        self.stat = pd.DataFrame()

        self.VALID_HASHING = ["blake2s", "blake2b", "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_224", "sha3_256", "sha3_384", "sha3_512"]
        self.VALID_ALGORITHM = ["index", "length"] + self.VALID_HASHING

    def get_stat(self):
        """Return a DataFrame with various info on every columns from a source dataframe

        Args:
            df (DataFrame): Source DataFrame to Analyze

        Returns:
            DataFrame: A dataFrame with some statistics on each columns
        """
        self.stat = pd.DataFrame()
        if not self.content.empty:
            self.stat["column_name"]=list(self.content.columns)
            self.stat["nb_value"] = list(self.content.count())
            self.stat["nb_unique_value"] = list(self.content.nunique())
            
            df_len = self.content.applymap(lambda x: len(x), na_action="ignore")
            self.stat["min_length"]  = list(df_len.min())
            self.stat["max_length"] = list(df_len.max())
            self.stat["nb_unique_length"] = list(df_len.nunique())
            self.stat[["min_length", "max_length"]] = self.stat[["min_length", "max_length"]].fillna("0").astype(int)   ## Necessary step as numeric column with NaN value are considered as float
        return self.stat

    def load(self):
        """[Load and return a CSV file content as a pandas dataframe]

        Returns:
            [DataFrame]: [DataFrame with CSV File content]
        """
        try:
#            self.content = pd.read_csv(self.filename, encoding="UTF-8", delimiter=self.separator, low_memory=False, dtype=str)  # Force all columns as string
#           change encoding in order to solve following error : utf-8' codec can't decode byte 0xae in position xxx: invalid start byte
            self.content = pd.read_csv(self.filename, encoding="unicode_escape", delimiter=self.separator, low_memory=False, dtype=str)  # Force all columns as string
        except Exception as e:
            self.console.print_msg("ERROR", f"Fail to load CSV file '{self.filename}':")
            self.console.print_msg("ERROR", f"{str(e)}")
        else:
            (nb_rows, nb_columns) = self.content.shape
            self.console.print_msg("SUCCESS", f"Successfully load CSV file '{self.filename}'")
            print(f"- File contains {nb_columns} columns and {nb_rows} lines")
        return self.content

    def save_content(self, csv_filename, csv_separator=""):
        """[Save a pandas dataframe as CSV File]

        Returns:
            [Boolean]: True when successfully saved. False otherwise
        """
        if not csv_separator:
            csv_separator = self.separator
        try:
            self.content.to_csv(csv_filename, encoding="UTF-8", index=False, sep=csv_separator)
        except Exception as e:
            self.console.print_msg("ERROR", f"Fail to save CSV file '{csv_filename}':")
            self.console.print_msg("ERROR", f"{str(e)}")
            return False
        else:
            self.console.print_msg("SUCCESS", f"Successfully save CSV file '{csv_filename}'")
            return True
    
    def save_stat(self, csv_filename, csv_separator=""):
        """[Save a pandas statistics dataframe as CSV File]

        Returns:
            [Boolean]: True when successfully saved. False otherwise
        """
        if not csv_separator:
            csv_separator = self.separator
        try:
            self.stat.to_csv(csv_filename, encoding="UTF-8", index=False, sep=csv_separator)
        except Exception as e:
            self.console.print_msg("ERROR", f"Fail to save CSV file '{csv_filename}':")
            self.console.print_msg("ERROR", f"{str(e)}")
            return False
        else:
            self.console.print_msg("SUCCESS", f"Successfully save CSV file '{csv_filename}'")
            return True
    
    def hash_content(self, fields_to_transform, algorithm="blake2s", salt=""):
        df_transformed = pd.DataFrame()
        algorithm_hash = ""
        missing_value = ""
        distinct_values = []
        VALID_HASHING = ["blake2s", "blake2b", "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_224", "sha3_256", "sha3_384", "sha3_512"]

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
                    distinct_value_col=self.content[el].unique()
                    distinct_values = distinct_values + list(set(distinct_value_col).difference(distinct_values))
                algorithm_hash = f"{distinct_values}.index(x)+1"
                missing_value = 0
            else:
                self.console.print_msg("ERROR", f"Unknown Algorithm specified: {algorithm}")
            df_transformed = self.content[fields_to_transform].fillna("").applymap(
                lambda x: 
                    eval(algorithm_hash,{"hashlib":hashlib},{"salt":salt, "x":x}) if not x == "" else missing_value
            )
        return df_transformed
   
### Retrieve Json or Yaml Content
class ParameterFile():
    def __init__(self, filename="", colored=True):
        self.filename = FileName()
        self.parameters={}
        self.console = Console(colored)

        if filename:
            self.filename = FileName(filename)
            self.load()
        
    def load(self):
        """Return a Dictionnary from Json or Yaml file

        Args:
            filename (file): File Name containing settings. Supported format : Json or Yaml

        Returns:
            Dictionnary: [A Dictionnary build from Json/YAML]
        """
        self.parameters = {}
        filetype = self.filename.fileextension.lower()

        supported_filetype = [".json", ".yaml", ".yml"]
        if filetype not in supported_filetype:
            self.console.print_msg("ERROR",f"Parameter file supports following format only: json, yml, yaml.")
        else:
            try:
                if filetype == ".json":
                    with open(self.filename.fullpath) as config_file:
                        self.parameters = json.load(config_file)
                elif filetype == ".yaml" or filetype == ".yml" :
                    with open(self.filename.fullpath) as config_file:
                        self.parameters = yaml.safe_load(config_file)
            except Exception as e:
                self.console.print_msg("ERROR",f"with Parameter File '{self.filename.fullpath}':")
                self.console.print_msg("ERROR",f"{str(e)}")
            else:
                self.console.print_msg("SUCCESS",f"Parameter file '{self.filename.fullpath}' successfuly loaded")

        return self.parameters

