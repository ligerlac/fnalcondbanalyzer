import argparse
import requests
import csv


def get_curl_string(table_name, run_number):
    pre_text = "https://dbdata0vm.fnal.gov:9443/dune_con_prod/app/"
    get_string = f"get?table=pdunesp.{table_name}&t={run_number}&type=data"
    if table_name == 'distcorryz':
        get_string += f"&columns=y,dy,z,dz,corr,corr_err"
    elif table_name == 'distcorrx':
        get_string += f"&columns=x,dx,shape,shape_err"
    elif table_name == 'distcorrnorm':
        get_string += f"&columns=norm,norm_err"
    return pre_text + get_string


def write_raw_text_to_csv_file(raw_text, file_name):
    if raw_text == '':
        print(f'no data was downloaded. skipping output {file_name}...')
        return 0
    print(f'write_raw_text_to_csv_file(file_name={file_name})')
    with open(file_name, 'w') as f:
        cw = csv.writer(f, delimiter=',')
        for line in raw_text.splitlines():
            row = line.split(',')
            cw.writerow(row)


def main(args):
    for run_number in range(args.begin, args.end):
        curl_string = get_curl_string(args.tablename, run_number)
        print(f'curl string:\n{curl_string}')
        raw_text = requests.get(curl_string).text
        write_raw_text_to_csv_file(raw_text, f'data/{args.tablename}/{run_number}.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="data/csv_file.csv", help="name of output file")
    parser.add_argument("--tablename", type=str, default="distcorryz", help="name of table in db (omitting 'pdunesp.')")
    parser.add_argument("--begin", type=int, default=4300, help="run number from which data is retreived")
    parser.add_argument("--end", type=int, default=5856, help="run number to which data is retreived")
    args = parser.parse_args()
    main(args)

#run 1 from 4300 to 5856
