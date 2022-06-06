import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os


def get_data_frame(file_name) -> pd.DataFrame:
    df = pd.read_csv(file_name, sep=',')  # , index_col=1)
    #df.index = pd.to_datetime(df['tv']*1000000000)
    return df


def check_channels(df):
    run_numbers = set()
    last_channel = 0
    for row in df.itertuples(index=True, name='Pandas'):
        run_numbers.add(row.tv)
        if not row.channel == last_channel + 1:
            print('Non-successive channels found!')
            print(f'row.channel = {row.channel}, last_channel = {last_channel}')
        last_channel = row.channel
    print(f'run_numbers = {run_numbers}')
    for run_number in run_numbers:
        df_temp = df[df['tv']==run_number]
        print(f'run_number = {run_number}, n = {len(df_temp)}')


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
    df_tot = pd.read_csv('data/distcorryz/run1.csv', sep=',')
    print(f'len(df_tot = {len(df_tot)})')
    df_tot = df_tot.drop_duplicates()
    print(f'len(df_tot = {len(df_tot)})')
#    last_length = 0
#    df_tot = pd.DataFrame()
#    for fn in glob.glob(args.input+'/*.csv'):
#        print(f'fn={fn}')
#        df = pd.read_csv(fn, sep=',')
#        df_tot = pd.concat([df_tot, df], axis=0)
#        df_tot = df_tot.drop_duplicates()
#        if len(df_tot) == last_length:
#            print(f'no new info in {fn}. moving to data/duplicates/ ...')
#            os.rename(fn, fn.replace('data', 'data/duplicates'))

#        print(f'len(df_tot) = {len(df_tot)}')
#        last_length = len(df_tot)
    plt.show()
    sns.pairplot(df_tot)
    plt.savefig('data/pairplot.png')

#    df = get_data_frame(args.input)
#    #df = df[df['tv'] == 5841].drop('tv', axis=1)
#    print(f'df=\n{df}')
#    check_channels(df)
#    plt.show()
#    sns.pairplot(df)
#    plt.savefig('data/pairplot.png')
#    plt.show()
    #make_plot(df, ['center', 'low', 'high'])
    #make_hist(df)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/distcorryz/", help="folder with input files")
    parser.add_argument("--output", type=str, default="data/plots/", help="name of output folder")
    args = parser.parse_args()
    main(args)
