from datetime import datetime
import argparse
import requests
import csv

#s = "https://dbdata0vm.fnal.gov:9443/dune_con_prod/app/get?table=pdunesp.lifetime_purmon&type=data&tag=v1.1&t0=1539711086&t1=1539883886&columns=center,low,high"
#s = "https://dbdata0vm.fnal.gov:9443/dune_con_prod/app/get?table=pdunesp.distcorryz&t=5841&columns=y,dy,z,dz,corr,corr_err&type=data"


def get_curl_string(table_name, t0, t1):
    print(f'getting values from {table_name} between {datetime.fromtimestamp(t0)} and {datetime.fromtimestamp(t1)}')
    pre_text = "https://dbdata0vm.fnal.gov:9443/dune_con_prod/app/"
    get_string = f"get?table={table_name}&type=data&tag=v1.1&t0={t0}&t1={t1}&columns=center,low,high"
    s = pre_text + get_string
    print(f'curl string:\n{s}')
    return s


def write_raw_text_to_csv_file(raw_text, file_name):
    with open(file_name, 'w') as f:
        cw = csv.writer(f, delimiter=',')
        for line in raw_text.splitlines():
            row = line.split(',')
            cw.writerow(row)


def main(args):
    curl_string = get_curl_string(args.tablename, args.begin, args.end)
    raw_text = requests.get(curl_string).text
    write_raw_text_to_csv_file(raw_text, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="data/csv_file.csv", help="name of output file")
    parser.add_argument("--tablename", type=str, default="pdunesp.lifetime_purmon", help="name of table in db")
    parser.add_argument("--begin", type=int, default=1539711086, help="time stamp from which data is retreived")
    parser.add_argument("--end", type=int, default=1539883886, help="time stamp to which data is retreived")
    args = parser.parse_args()
    main(args)
