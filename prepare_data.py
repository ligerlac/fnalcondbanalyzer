import argparse
import pandas as pd
import glob


def main(args):
    output_file_name = args.input + '/duplicates_removed.csv'
    df_list = []
    for fn in glob.glob(args.input+'/*.csv'):
        df_list.append(pd.read_csv(fn, sep=','))
    df = pd.concat(df_list, axis=0)
    df = df.drop_duplicates(ignore_index=True)
    print(f'saving {len(df)} rows to {output_file_name}...')
    df.to_csv(output_file_name, sep=',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/distcorryz/", help="folder with input files")
    args = parser.parse_args()
    main(args)
