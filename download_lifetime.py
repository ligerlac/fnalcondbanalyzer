from datetime import datetime
import argparse
import requests
import csv


def get_time_stamps(args) -> tuple[int, int]:
    t0 = datetime.strptime(args.begin, '%Y-%m-%d-%H')
    t1 = datetime.strptime(args.end, '%Y-%m-%d-%H')
    return int(datetime.timestamp(t0)), int(datetime.timestamp(t1))


def get_curl_string(t0, t1):
    pre_text = "https://dbdata0vm.fnal.gov:9443/dune_con_prod/app/"
    get_string = f"get?table=pdunesp.lifetime_purmon&type=data&tag=v1.1&t0={t0}&t1={t1}&columns=center,low,high"
    return pre_text + get_string


def write_raw_text_to_csv_file(raw_text, file_name):
    with open(file_name, 'w') as f:
        cw = csv.writer(f, delimiter=',')
        for line in raw_text.splitlines():
            row = line.split(',')
            cw.writerow(row)


def main(args):
    print(f'getting values from pdunesp.lifetime_purmon between {args.begin} and {args.end}')
    t0, t1 = get_time_stamps(args)
    curl_string = get_curl_string(t0, t1)
    print(f'curl string:\n{curl_string}')
    raw_text = requests.get(curl_string).text
    write_raw_text_to_csv_file(raw_text, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="data/lifetime/csv_file.csv", help="name of output file")
    parser.add_argument("--begin", type=str, default='2018-09-14-00', help="date from which data is retreived")
    parser.add_argument("--end", type=str, default='2018-11-12-23', help="date to which data is retreived")
    args = parser.parse_args()
    main(args)

#run 1 from 2018-09-14 to 2018-11-12
