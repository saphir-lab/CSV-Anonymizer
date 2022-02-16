# CSV Anonymizer

## Introduction

A common problematic encountered by Data Scientists is to have data containing personally identifiable information (PII) such as email addresses, customer IDs or phone numbers.
A simple solution is to remove these fields before sharing the data. However, analysis may rely on having the PII data. For example, in e-Commerce context, customer IDs are necessary to know how many customers bought which product.
Instead of removing PII data, you can **anonymize** the PII by using hashing technique.

**CSV Anonymizer** provides capacity to anonymize all or **part** of your data using different hash functions.

### Hashing

- Hashing is the transformation of a string of characters into a **fixed-length** value or key that represents the original string.

- A hash function is any function that can be used to map data of arbitrary size to fixed-size values.

- Some Hash functions families:

  - **MD5** (Message Digest 5): is pretty obsolete now, and isn't collision resistant
  - **SHA-1** (Secure Hash Algorithm 1): considered less secure since 2005
  - **SHA-2** (Secure Hash Algorithm 2): family of 4 hash functions; SHA-224, SHA-256, SHA-384 and SHA-512
  - **SHA-3 (Secure Hash Algorithm 3): family of 4 hash functions; SHA3-224, SHA3-256, SHA3-384, SHA3-512
  - **BLAKE2** : faster than SHA-1, SHA-2, SHA-3, and even MD5. More secure than SHA-2, similar to that of SHA-3: immunity to length extension, indifferentiability from a random oracle, etc. It is suited for use on modern CPUs that support parallel computing on multicore systems.

>**Note**: *BLAKE2S is the default/recommended hash function used by this script as it is fast and generate a 256 bits hash value.
>You can use other algorithms that will generate hash values with more digits (up to 512), meanwhile take also in consideration that this can have a big impact on the final size of you CSV file, mainly if you have a lot of rows and/or columns to anonymize.*

## Other usage

If the context of your analysis you need to perform some data quality verification, it starts to be difficult to achieve it for PII elements that have been hashed.
In order to do a minimal verification base on the length of the value, extra option have been added to this script in order to:

- Generate a second file (overview) with some statistics related to orignal data. This include  following statistics **for each column** present in the CSV FIle:
  - Number of values provided (in order to see column with missing values).
  - Number of **unique** values.
  - The minimum length of value
  - The maximum length of value
  - The number of different lengths found.
- Transform original value to the text length

>**Note**: *parameter 'length' is presented in this script as part of the hash algorithms even if, conceptually, this is not a hash function.*

## Configuration

This script accept parameters that you have to specify in a file named '**setting.yaml**' and located on the same directory as the script.

This parameter file contains 5 sections :

- Console: Control the look and feel related to the script execution.
- Source: CSV File to be transformed.
- Output: The location and nomenclature of CSV Tranformed by this anonymization.
- Transform: Scope of the transformation (all columns, all except some columns, only some columns) and how to transform (which hash function).
- SelectionParameters: to precise the list of fields from your source file you want to anonymize or exclude from the anonymization process.

>**Note**: *setting.yaml file contains comments. See sample setting file for more information.*

## Prerequisites

- Use Python 3.x
- Install required python modules using command line (from this directory):
  - `pip install -r requirements.txt`

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
