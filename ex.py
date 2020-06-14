import pandas as pd
import numpy as np
import datetime as dt
# import tsmom as tm
import os

# import seaborn as sns
# import matplotlib.pyplot as plt
# plt.style.use('ggplot')
# import cufflinks as cf
from tqdm import tqdm
from tqdm import trange
from time import sleep
import json
import urllib
import requests

def split_uppercase(str):
    x = ''
    i = 0
    for c in str:

        if i == 0:
            x += c
        elif c.isupper() and not str[i-1].isupper():
            x += ' %s' % c
        else:
            x += c
        i += 1
    return x.strip()

class BCOptionScraper():
    def __init__(self, ticker):
        self.ticker = ticker

    def get_expirys(self):
        url = "https://core-api.barchart.com/v1/options/chain?symbol={}\
&fields=strikePrice%2ClastPrice%2CpercentFromLast%2CbidPrice%\
2Cmidpoint%2CaskPrice%2CpriceChange%2CpercentChange%2Cvolatility%\
2Cvolume%2CopenInterest%2CoptionType%2CdaysToExpiration%2CexpirationDate%\
2CsymbolCode%2CsymbolType&groupBy=optionType\
&raw=1&meta=field.shortName%2Cfield.type%2Cfield.description".format(self.ticker)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        js_file = json.loads(resp.read())
        if js_file['meta']:
            if js_file['meta']['expirations']:
                return js_file['meta']['expirations']
            else:
                e = ValueError
                return('No expiration found for {0} due to {1}'.format(self.ticker, e))
        else:
            return('No expiration Data available')

    def get_json_file(self, expiry = None):
        if not expiry:
            expiry = self.get_expirys()[0]
        url = "https://core-api.barchart.com/v1/options/chain?symbol={0}\
&fields=strikePrice%2ClastPrice%2CpercentFromLast%2CbidPrice%\
2Cmidpoint%2CaskPrice%2CpriceChange%2CpercentChange%2Cvolatility%\
2Cvolume%2CopenInterest%2CoptionType%2CdaysToExpiration%2CexpirationDate%\
2CsymbolCode%2CsymbolType&groupBy=optionType&expirationDate={1}\
&raw=1&meta=field.shortName%2Cfield.type%2Cfield.description".format(self.ticker, expiry)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        js_file = json.loads(resp.read())
        return js_file

    def get_df(self, expiry = None, c_or_p = 'c'):
        js_file = self.get_json_file(expiry = expiry)
        call_list_df = []
        put_list_df = []
        if js_file['data']:
            for i in (js_file['data']['Call']):
                call_list_df.append(pd.DataFrame.from_dict(i['raw'], orient= 'index'))
            call_df = (
                pd.concat(call_list_df, axis = 1).T
                .replace('NA', np.nan)
                .apply(pd.to_numeric, errors = 'ignore')
                .assign(expirationDate = lambda x: pd.to_datetime(x.expirationDate))
                .assign(expirationDate = lambda x: x.expirationDate.dt.strftime('%B %d,%Y'))
                .set_index(['expirationDate', 'strikePrice'])
                )

            call_df.columns = [split_uppercase(i).title() for i in call_df.columns]
            call_df.index.names = [split_uppercase(i).title() for i in call_df.index.names]

            for i in (js_file['data']['Put']):
                put_list_df.append(pd.DataFrame.from_dict(i['raw'], orient= 'index'))
            put_df = (
                pd.concat(put_list_df, axis = 1).T
                .replace('NA', np.nan)
                .apply(pd.to_numeric, errors = 'ignore')
                .assign(expirationDate = lambda x: pd.to_datetime(x.expirationDate))
                .assign(expirationDate = lambda x: x.expirationDate.dt.strftime('%B %d,%Y'))
                .set_index(['expirationDate', 'strikePrice'])
                )

            put_df.columns = [split_uppercase(i).title() for i in put_df.columns]
            put_df.index.names = [split_uppercase(i).title() for i in put_df.index.names]
        else:
    #         raise ValueError('No data found for {}'.format(ticker))
            return (ValueError('No data found for {}'.format(self.ticker)))
        if c_or_p == 'c':
            return call_df
        elif c_or_p == 'p':
            return put_df
        elif c_or_p == 'both':
            return (call_df, put_df)

    def get_total_dfs(self):
        """Function to make dataframe from the options data scraped from NASDAQ website
        Params:
            save: (boolean, optional) whether you want to save it or not,default is False
            folder: (str, optional)folder to save in, could be existing folder
            save_format: supported formats are 'xlsx'(default), 'xls', 'csv', 'txt'
        Returns a Dataframe
        """
        expirys = self.get_expirys()
        self.expirys = expirys
        both_dfs = []
        pbar = tqdm(expirys, unit = ' Expiry Dates', total = len(expirys))
    #     pbar.write('{} has {} expiry dates available'.format(ticker, len(expirys)))
        for expiry in pbar:
            pbar.set_description("Scraping {0}'s options data for {1}: ".format(self.ticker, expiry),
                                 refresh = True)
            try:
                calls, puts = self.get_df(expiry = expiry,
                                          c_or_p= 'both'
                                         )
            except ValueError:
                print('Couldnt find data for {} for {}:'.format(self.ticker, expiry))
            mt = pd.DataFrame(np.nan,
                              index = calls.index,
                              columns = [' '])
            both_dfs.append(pd.concat([calls, mt, puts],
                                      keys = ['Call', ' ', 'Put'],
                                      axis = 1)
                           )
            sleep(0.25)
 #       self.list_dfs = both_dfs
        return both_dfs

    def save_to_excel(self, writer, panes = (3,1)):
        list_dfs = self.get_total_dfs()
        if list_dfs:
            for df in list_dfs:
                if isinstance(df, pd.core.frame.DataFrame):
                    if isinstance(df.index, pd.core.indexes.multi.MultiIndex):
                        idx = df.index.get_level_values(0)[0]
                        new_df = df.loc[idx]
                        new_df.to_excel(writer,
                                        freeze_panes = panes,
                                        sheet_name = idx)
                    else:
                        df.to_excel(writer,
                                    freeze_panes = panses,
                                    sheet_name = self.ticker)
                else:
                    return("Only DataFrames can be saved")


    def get_final(self, save = False, folder = None, save_format = 'xlsx', panes = (3,1)):
        if save:
            if folder:
                if type(folder) == str:
                    path = os.path.join(os.getcwd(), folder, self.ticker.upper())
                    if os.path.exists(path):
                        print('Saving data in {}'.format(str(path)))
                        sleep(2)
                        if (save_format == 'xlsx')|(save_format == 'xls'):
                            total_path = os.path.join(path, self.ticker.upper()+ '.' + save_format)
                            total_path = str(total_path)
                            writer = pd.ExcelWriter(total_path, engine = 'xlsxwriter')
                            # final_df.to_excel(writer,
                            #                   sheet_name = self.ticker.upper() + ' OptionChain',
                            #                   freeze_panes = (3,2))
                            self.save_to_excel(writer, panes = panes)
                            writer.close()
                        elif(save_format == 'csv')|(save_format == 'txt'):
                            final_df = pd.concat(self.get_total_dfs(), axis = 0)
                            final_df.to_csv(os.path.join(path, self.ticker.upper()+ '.' + save_format))
                        print('File Saved')
                    elif not os.path.exists(path):
                        print("Path doesn't exist. Creating directory")
                        sleep(2)
                        os.makedirs(path)
                        print('Saving data in {}'.format(str(path)))
                        sleep(2)
                        if (save_format == 'xlsx')|(save_format == 'xls'):
                            total_path = os.path.join(path, self.ticker.upper()+ '.' + save_format)
                            total_path = str(total_path)
                            writer = pd.ExcelWriter(total_path, engine = 'xlsxwriter')
                            # final_df.to_excel(writer,
                            #                   sheet_name = self.ticker.upper() + ' OptionChain',
                            #                   freeze_panes = (3, 2))
                            self.save_to_excel(writer, panes = panes)
                            writer.close()
                        elif(save_format == 'csv')|(save_format == 'txt'):
                            final_df = pd.concat(self.get_total_dfs(), axis = 0)
                            final_df.to_csv(os.path.join(path, self.ticker.upper()+ '.' + save_format))
                        print('File Saved')
                    # return(str(path))
                else:
                    print('Folder name should be string')

            else:
                pass
        else:
            print('\n\n')
            final_df = pd.concat(self.get_total_dfs(), axis=  0)
            print(final_df)




# etfs = ['IVV', 'VOO', 'IWM', 'IJR', 'VB', 'XLE', 'XLY']

def main():
    flag = 0
    print("Module to get Barchart options data.\n\nLet's start with inputting the tickers.")
    etf_list = [x.upper() for x in input().split()]
    save_opt = input('Do you want to save File? [y/n]:  ')
    if save_opt == 'y':
        save = True
        folder_opt = input("What is the folder name you want to save the files in?\nIf you are running this file\
on desktop and want to save it on a relative drectory\nfor example Desktop/Options/Optionchain,\
type Options/Optionchain\n\n\n")
        folder = str(folder_opt)
        format_opt = input('What format do you want to save the file in?\nAvailable options are "xlsx",\
"xls","csv", "txt": ')
        save_format = format_opt
        flag = 1

    elif save_opt == 'n':
        save = False
        folder = None
        save_format = 'xlsx'
        flag = 1
    else:
        return('Please choose from y or n')

    if (save_format == 'xlsx')|(save_format == 'xls')|(save_format == 'csv')|(save_format == 'txt'):
        pass
    else:
        return('File extension not supported, Please try again')

    if flag == 1:
        counter = 0
        counter_size = []
        for i in (etf_list):
            scraper = BCOptionScraper(i)
            size = len(scraper.get_expirys())
            counter+= size
            counter_size.append(size)

        pbar = tqdm(total = counter, unit = 'Ticker')
        for i, j  in zip(etf_list, counter_size):
            scraper = BCOptionScraper(i)
            data = scraper.get_final(save = save, folder = folder, save_format = save_format, panes = (3,1))
            pbar.update(j)
            sleep(2)
        # print(type(save), type(folder), type(save_format))
    elif flag == 0:
        return('Input error, check inputs and try again.')
if __name__ == '__main__':
    main()
