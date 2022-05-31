import argparse
import pandas as pd
import matplotlib.pyplot as plt


def get_data_frame(file_name) -> pd.DataFrame:
    df = pd.read_csv(file_name, sep=',')  # , index_col=1)
    df.index = pd.to_datetime(df['tv']*1000000000)
    return df


def decorate_delta_t(df) -> pd.DataFrame:
    delta_t_list = []
    last_ts = 0
    for row in df.itertuples(index=True, name='Pandas'):
        delta_t_list.append(row.tv - last_ts)
        last_ts = row.tv
    df['delta_t'] = delta_t_list
    df['delta_t'].iloc[0] = 0
    df['delta_t'] = df['delta_t'] / 3600
    return df


def make_hist(df):
    ax = df.hist(column='delta_t', bins=10)
    ax = ax[0]
    for x in ax:
        x.set_xlabel('Delta t [h]')
        x.set_ylabel('Number of events')
    plt.savefig(f'{args.output}/hist.png')
    plt.show()


def make_plot(df, col_list):
    df.plot(y=col_list)
    plt.savefig(f'{args.output}/{col_list[0]}.png')
    plt.show()


def main(args):
    df = get_data_frame(args.input)
    df = decorate_delta_t(df)
    print(f'df=\n{df}')
    make_plot(df, ['center', 'low', 'high'])
    make_plot(df, ['delta_t'])
    make_hist(df)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/csv_file.csv", help="name of input file")
    parser.add_argument("--output", type=str, default="data/plots/", help="name of output folder")
    args = parser.parse_args()
    main(args)
