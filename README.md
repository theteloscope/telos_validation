# Telos Validation

Basic script for Telos validation. The main script reads accounts, balances and/or keys from a snapshot (in CVS format) and tries to match each account against a live full node.

A sample CSV script with some predefined mismatches and unknown accounts is provided for testing. 

## Usage


```
usage: telos_validation.py [-h] -a ACCOUNTS_COLUMN_NUMBER
                           [-o OWNER_KEY_COLUMN_NUMBER]
                           [-b BALANCE_COLUMN_NUMBER] [-n NODE] [-v]
                           snapshot_file
```

For a typical run against a local node:

```
python3 telos_validation.py -n https://api.theteloscope.io -a 2 -o 3 -b 4 -v sample.csv 
```

The script will generate a log file for each CSV processed
