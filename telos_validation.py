import argparse
import logging
import csv
import time
from time import sleep
from TelosNetInfo import telosnetinfo

#Args
parser = argparse.ArgumentParser(description='Validate tlos genesis snapshot')

parser.add_argument("snapshot_file", type=str, help="Snapshot file")
#parser.add_argument("accounts_column_number", type=int, help="Accounts column number")

parser.add_argument("-a", "--accounts_column_number", type=int, help="Account column number", required=True)
parser.add_argument("-o", "--owner_key_column_number", type=int, help="Owner column number")
parser.add_argument("-b", "--balance_column_number",  type=int, help="Balance column number")
parser.add_argument("-n", "--node", type=str, help="Node url")
parser.add_argument("-v", "--verbose",  action="store_true", help="Verbose output")

args = parser.parse_args()

if args.node is not None:
    mainnet = telosnetinfo(args.node)

else:
    mainnet = telosnetinfo('https://api.theteloscope.io')


input_file = args.snapshot_file
acc_col = args.accounts_column_number

total_balance_csv = 0
total_balance_chain = 0

options = list('00')

if args.owner_key_column_number is not None:
    own_col = args.owner_key_column_number
    options[0] = '1'
if args.balance_column_number is not None:
    bal_col = args.balance_column_number
    options[1] = '1'

options = "".join(options)

#Initalize logger
logging.basicConfig(filename=input_file+'.log', filemode='a', format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().setLevel(logging.INFO)
logging.warning("Execution started")


#Process snapshot
with open(input_file) as csv_file:

    #Open csv and set delimiter
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    #Set start time
    start_time = time.time()

    #Iterate all rows on csv
    for row in csv_reader:

        #Print columns names
        if line_count == 0:
            print(f'Column names: {", ".join(row)}')
            line_count += 1

        else:

            #Only account columns
            if options == '00':
                if not mainnet.account_exists(row[acc_col]):
                    logging.error("ERROR account %s  doesn't exists, line number %s" % (row[acc_col], line_count))
                    print("ERROR account %s doesn't found" % (row[acc_col]))

            #Extra balance option passed
            elif options == '01':
                balance = mainnet.get_total_balance(row[acc_col])
                total_balance_chain += float(balance)
                total_balance_csv += float(row[bal_col])

                # Check if balance exists
                if balance is None:
                    logging.error("ERROR no balance on %s line number %s" % (row[acc_col], line_count))
                    print("ERROR no balance on", row[acc_col])

                # Check balance mismatch
                elif round(balance, 4) != float(row[bal_col]):
                    logging.warning("WARNING MISMATCH account: %s balances: %s %s, line %s" % (
                        row[acc_col], float(row[bal_col]), balance, line_count))
                    print("MISMATCH", row[acc_col], float(row[bal_col]), balance)

                # Check if balance is over 40k
                elif round(balance) > 40000.0:
                    logging.warning("ERROR OVER 40K account: %s balances: %s %s, line %s" % (
                        row[acc_col], float(row[bal_col]), balance, line_count))
                    print("OVER 40k", row[acc_col], float(row[bal_col]), balance)


            # Extra owner key option passed
            elif options == '10':

                if mainnet.account_owner_key(row[acc_col]) != row[own_col]:
                    logging.error("ERROR owner's key doesn't match on %s line number %s" % (row[acc_col], line_count))
                    print("ERROR owner's key doesn't match on", row[acc_col])


            #Extra owner key and balance passed
            elif options == '11':

                # Get balance and owner keys from mainnet
                result = mainnet.get_balance_and_owner_key(row[acc_col])
                balance = result[0]
                owner_key = result[1]
                total_balance_chain += float(balance)
                total_balance_csv += float(row[bal_col])

                # Check if owner's key match
                if owner_key != row[own_col]:
                    logging.error("ERROR owner's key doesn't match on %s line number %s" % (row[acc_col], line_count))
                    print("ERROR owner's key doesn't match on", row[acc_col])

                # Check if balance exists
                if balance is None:
                    logging.error("ERROR no balance on %s line number %s" % (row[acc_col], line_count))
                    print("ERROR no balance on", row[acc_col])

                # Check balance mismatch
                elif round(balance, 4) != float(row[bal_col]):
                    logging.warning("WARNING MISMATCH account: %s balances: %s %s, line %s" % (
                        row[acc_col], float(row[bal_col]), balance, line_count))
                    print("MISMATCH", row[acc_col], float(row[bal_col]), balance)

                # Check if balance is over 40k
                elif round(balance) > 40000.0:
                    logging.warning("ERROR OVER 40K account: %s balances: %s %s, line %s" % (
                        row[acc_col], float(row[bal_col]), balance, line_count))
                    print("OVER 40k", row[acc_col], float(row[bal_col]), balance)

            line_count += 1

        #Trace
        if ((line_count % 100) == 0) and args.verbose:
            print("--- %s seconds ---" % (time.time() - start_time))
            print(line_count)
            sleep(0.1)

        #Loggger trace
        if (line_count % 1000) == 0:
            logging.info("--- %s seconds ---, row number %s" % (time.time() - start_time, line_count))

    #CSV processed
    print(f'Processed {line_count} lines.')
    if (options == '11' or options == '01'):
    	print('Total balance on chain: %s' % round(total_balance_chain,4))
    	print('Total balance on CSV:   %s' % round(total_balance_csv,4))
    	logging.info('Total balance on chain: %s' % round(total_balance_chain,4))
    	logging.info('Total balance on CSV:   %s' % round(total_balance_csv,4))

    logging.warning("Execution finished")