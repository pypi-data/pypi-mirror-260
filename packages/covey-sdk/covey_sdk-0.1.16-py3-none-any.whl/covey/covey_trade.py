import os
import json
import time
import asyncio
import eth_keys
import pandas as pd
import requests
from web3 import Web3
from dotenv import load_dotenv
from eth_account import account
from datetime import datetime, timedelta
from web3.middleware import geth_poa_middleware
from alpaca.trading.client import TradingClient

# # covey libraries - internal test
# from utils import get_data, get_output, get_checks
# from covey_pricer import Pricer
# from covey_calendar import CoveyCalendar
# from alpaca.trading.requests import GetAssetsRequest
# from alpaca.trading.enums import AssetClass, AssetExchange

# covey libraries - packaging
from covey import get_data, get_output
from covey.covey_pricer import Pricer
from covey.covey_calendar import CoveyCalendar

class Trade:
    def __init__(self, **kwargs):
        # check if posting only - False by default
        self.posting_only = kwargs.get('posting_only',False)

        # Geth web3 for account stuff
        self.gethWeb3 = Web3(Web3.IPCProvider())

        # get the address
        self.address = kwargs.get('address')

        # VARIABLE : wallet (address) secret key
        self.address_private = kwargs.get('address_private')

        # VARIABLE : polygon url - will eventually replace infura url
        self.polygon_url = kwargs.get('POLYGON_URL', 'https://polygon-rpc.com/')

        # VARIABLE : covey ledger address (polygon)
        self.covey_ledger_polygon_address = kwargs.get('covey_ledger_polygon_address', '0x587Ec5a7a3F2DE881B15776BC7aaD97AA44862Be')

        # VARIABLE : polygon chain id
        self.polygon_chain_id = kwargs.get('polygon_chain_id', 137)

        # set the abi - must pass in the covey ledger file here otherwise will not work
        self.abi = json.load(open(os.path.join(os.path.dirname(__file__),'CoveyLedger.json')))['abi']

        # set the gas station url
        self.gas_station_url = kwargs.get('gas_station_url','https://gasstation.polygon.technology/v2')

        # if posting only, we don't need to get the pricer and get alpaca involved
        if not self.posting_only:

            # set up the empty dataframe that all of the trades from all chains will append to
            self.trades = pd.DataFrame(columns=['address', 'trades', 'entry_date_time'])

            # gather the trades
            #asyncio.run(self.gather_trades())
            self.gather_trades()

            # transform the trades as necessary to perform any clean up, date renaming etc
            self.transform_trades()
            
            # generate price key
            print("Getting price key in the covey trade")
            p = Pricer(start= self.get_min_trade_entry(), symbols=self.get_symbols())
            self.price_key = p.price_key

            # generate trading key with prices
            self.trading_key = self.get_trading_key()
    
    # getter for symbols
    def get_symbols(self):
        if len(self.trades.index) < 1:
            return []
        else:
            return self.trades['symbol'].unique()

    # get minimum start date
    def get_min_trade_entry(self):
        if len(self.trades.index) < 1:
            return datetime(2021,12,31).strftime('%Y-%m-%d')
        else:
            return self.trades['entry_date'].min().strftime('%Y-%m-%d')

    # getter to return the address from child class if needed, or in current class - either works
    def get_address(self):
        print(self.address)

    # The password here MUST match the password you used to generate your accounts, otherwise it will fail
    def get_private_keys(self, password):
        wallets_list = self.gethWeb3.geth.personal.list_wallets()
        for i in wallets_list:
            address = i['accounts'][0].address
            keyfile_path = i['accounts'][0].url.replace("keystore://", "").replace("\\", "/")
            keyfile = open(keyfile_path)
            keyfile_contents = keyfile.read()
            keyfile.close()
            private_key = eth_keys.keys.PrivateKey(account.Account.decrypt(keyfile_contents, password))
            public_key = private_key.public_key
            private_key_str = str(private_key)
            public_key_str = str(public_key)
            print(f'Address: {address} Private Key: {private_key_str}')

    # The password used here must match the password used to generate the address you are feeding into here
    def get_private_key(self, address, password):
        wallets_list = self.gethWeb3.geth.personal.list_wallets()
        keyfile_path = (
            wallets_list[list(i['accounts'][0]['address'].lower() for i in wallets_list).index(address)][
                'url']).replace(
            "keystore://", "").replace("\\", "/")
        keyfile = open(keyfile_path)
        keyfile_contents = keyfile.read()
        keyfile.close()
        private_key = eth_keys.keys.PrivateKey(account.Account.decrypt(keyfile_contents, password))
        public_key = private_key.public_key

        private_key_str = str(private_key)
        public_key_str = str(public_key)
        print(private_key_str)

    # post trades to the polygon chain
    def post_trades_polygon(self,positionString):
        w3 = Web3(Web3.HTTPProvider(self.polygon_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        covey_ledger = w3.eth.contract(address=self.covey_ledger_polygon_address, abi=self.abi)
        my_address = w3.toChecksumAddress(self.address)
        nonce = w3.eth.get_transaction_count(my_address,'pending')
        gas = covey_ledger.functions.createContent(positionString).estimate_gas({'from': my_address, 'nonce': nonce}) 
        gas_price = requests.get(self.gas_station_url).json().get('fast').get('maxFee')
        txn = covey_ledger.functions.createContent(positionString).build_transaction({
            'chainId': int(self.polygon_chain_id),
            'gas': gas,
            'gasPrice': Web3.toWei(str(round(float(gas_price))), 'gwei'),
            'nonce': nonce,
            'from': my_address
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key= self.address_private)
        w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Posted Trade to: {} for positions: {} on polygon'.format(self.address,positionString))

    # output format [('address', 'position string', unix time),('address', 'position string', unix time),...]
    def get_trades_polygon(self):
        w3 = Web3(Web3.HTTPProvider(self.polygon_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        covey_ledger = w3.eth.contract(address=self.covey_ledger_polygon_address, abi=self.abi)
        my_address = w3.toChecksumAddress(self.address)
        result = covey_ledger.functions.getAnalystContent(my_address).call()
        result_df = pd.DataFrame(result, columns=['address', 'trades', 'entry_date_time'])
        result_df.insert(0, 'chain', 'MATIC')
        self.trades = pd.concat([self.trades, result_df])
        return 0

    # gather all the chains into one dataframe - gather is an async term in general
    def gather_trades(self):
        # await asyncio.gather(
        #     # skale test net down on 8/5/2022 so commented out for now
        #     #self.get_trades_skale(),
        #     self.get_trades_polygon()
        #     )
        
        self.get_trades_polygon()

        # check the trades list, if it's blank we need to put in the DUMMY
        if len(self.trades) == 0:
            result_df = pd.DataFrame({'address' : self.address, 
                                        'trades' : 'DUMMY:0', 
                                        'entry_date_time' : time.mktime(datetime.strptime(self.get_min_trade_entry(),'%Y-%m-%d').timetuple())}, index = [0])
            result_df.insert(0, 'chain', 'NONE')
            self.trades = pd.concat([self.trades, result_df])

      



    # add BLANK ticker, 0 Target Position for wallets with no activity
    def cleanup_trade_cells(self,s):
        return s if len(s) > 0 else 'BLANK:0'

    # check if string is numeric : https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    def is_number_repl_isdigit(self,s):
        """ Returns True is string is a number. """
        try:
            return s.lstrip("-").replace('.', '', 1).isdigit()
        except AttributeError:
            return False
    
    # grab the alpaca universe - this will be used in the transform trade function
    def get_alpaca_universe(self):
        # initialized trading client
        b = TradingClient(api_key = os.environ.get('APCA_API_KEY_ID'), secret_key = os.environ.get('APCA_API_SECRET_KEY'))
        # get the 'list' of assets
        # search for crypto assets
        #search_params = GetAssetsRequest(asset_exchange='NYSE')
        #assets = b.get_all_assets(search_params)
        
        asset_list = b.get_all_assets()
        # put the instance dict() into a dataframe
        asset_df = pd.DataFrame([a.dict() for a in asset_list])
        # cleanup
        asset_df['asset_class'] = asset_df['asset_class'].str.replace('AssetClass.','',regex=True)
        asset_df['status'] = asset_df['status'].str.replace('AssetStatus.','',regex=True)
        asset_df['exchange'] = asset_df['exchange'].str.replace('AssetExchange.','', regex=True)
        asset_df['symbol'] = asset_df['symbol'].str.replace('/','', regex=True)
        # filter for tradeable and active assets only
        asset_mask = (asset_df['tradable'] == True) & (asset_df['status'] == 'active')
        # return filtered df
        return asset_df[asset_mask]

    # transformations to the trades data frame including the actual splitting out of the trades lists
    def transform_trades(self):
        # make sure the trades are actually filled first
        if len(self.trades.index) > 0:
            # convert unix time to datetime
            self.trades['entry_date_time'] = pd.to_datetime(self.trades['entry_date_time'], unit='s')
            # split trades column into multiple rows by delimiter, resulting in each row having one ticker : position combo
            self.trades = self.trades.assign(trades=self.trades['trades'].str.split(',')).explode('trades')
            # clean up blank trade cells, empty string
            self.trades['trades'] = self.trades['trades'].apply(lambda x: self.cleanup_trade_cells(x))
            # split trades column into symbol, position columns
            try:
                self.trades[['symbol', 'target_percentage']] = self.trades['trades'].str.split(':', expand=True).iloc[:,
                                                                 0:2]
            except ValueError:
                self.trades[['symbol', 'target_percentage']] = ['BLANK', 0]
            
            # trim the symbol names just in case
            self.trades['symbol'] = self.trades['symbol'].str.strip()

            # clean up the covey-reset, the target_percentage should be numeric
            self.trades['target_percentage'] = self.trades['target_percentage'].apply(
                lambda x: x if self.is_number_repl_isdigit(x) else 0)

            # remove timezone awareness
            self.trades['entry_date_time'] = self.trades['entry_date_time'].dt.tz_localize(None)

            # add date only column for the merge
            self.trades['entry_date'] = pd.to_datetime(self.trades['entry_date_time']).dt.date

            # conversion for merge
            self.trades['entry_date'] = pd.to_datetime(self.trades['entry_date'])


            # grab the prior to 20220301 trades
            prior_2022_trades = pd.read_csv(get_data('polygon_prior_to_20230301.csv'))
            prior_2022_trades = prior_2022_trades[prior_2022_trades['user_wallet'] == self.address].copy(deep=True)
            prior_2022_trades['user_wallet'] = prior_2022_trades['user_wallet'].str.upper()
            prior_2022_trades.drop(columns=['entry_price'],inplace=True)
            prior_2022_trades.rename(columns={'user_wallet':'address','percent':'target_percentage', 'entry_date':'entry_date_time'},inplace=True)
            prior_2022_trades['entry_date'] = pd.to_datetime(prior_2022_trades['entry_date_time']).dt.date
            prior_2022_trades['trades'] = prior_2022_trades['symbol'] + ':' + prior_2022_trades['target_percentage'].astype(str)

            #prior_2022_trades['entry_date_time'] = pd.to_datetime(prior_2022_trades['entry_date']).view('int64')/1000000

            #print(prior_2022_trades)
            prior_2022_trades['entry_date_time'] = pd.to_datetime(prior_2022_trades['entry_date_time'])
            prior_2022_trades['entry_date'] = pd.to_datetime(prior_2022_trades['entry_date'])

            self.trades['target_percentage'] = pd.to_numeric(self.trades['target_percentage'] )

            self.trades = pd.concat([prior_2022_trades,self.trades])

            # sort the trades and set the index
            self.trades.sort_values(by='entry_date_time', ascending=True, inplace=True)

            # set the trade ID - will be in ascending order of entry date time thanks to above line
            self.trades['trade_id'] = [x for x in range(1, len(self.trades.values) + 1)]

            # check for ticker changes
            self.trades = self.check_ticker_change(self.trades)

            # convert usdt (ending) to usd for filtering purposes
            self.trades['symbol'] = self.trades['symbol'].str.replace('USDT$','USD',regex=True)

            # symbols before filter
            pre_filter_symbols = self.get_symbols()

            # filter on universe - don't want any rogue tickers that will adversely affect the pricer file
            self.trades = pd.merge(left=self.trades, right=self.get_alpaca_universe()[['symbol']], how='inner', on='symbol')

            # symbols after filter
            post_filter_symbols = self.get_symbols()

            # convert usd back to usdt for pricing purposes
            self.trades['symbol'] = self.trades['symbol'].str.replace('USD$','USDT',regex=True)

            # symbols filtered out
            print(f"{list(set(pre_filter_symbols) - set(post_filter_symbols))} were filtered out.")


         

            # print all symbols we've encountered
            #print(f"{list(pre_filter_symbols) + list(post_filter_symbols)} were seen here.")         

        else:
            print("The trades dataframe has not been filled yet")

    # for debugging sets the reference time as of which we look at prices starting from that time
    def set_ref_trade_date_time(self,row):
        date_cols_to_convert = ['entry_date_time', 'date', 'next_market_open_date',
                                'next_market_open', 'next_market_close']
        # adjust it to be the next hour where we will take the VWAP of that hour
        row[date_cols_to_convert] = pd.to_datetime(row[date_cols_to_convert])  # , utc=True)
        trade_date_time_adj = row['entry_date_time'] + timedelta(minutes=61)
        trade_date_time_adj = trade_date_time_adj.replace(minute=0, second=0)

        # trade on holiday or non business day, return the next possible
        if row['date'] != row['next_market_open_date']:
            new_dt = row['next_market_open'] + timedelta(minutes=61)
        # trade during pre-market hours but still on a business day
        elif trade_date_time_adj < row['next_market_open']:
            new_dt = row['next_market_open'] + timedelta(minutes=61)
        # trade during post-market hours but still on a business day
        elif trade_date_time_adj >= row['next_market_close']:
            new_dt = row['next_market_open_t_plus_1']
        else:
            new_dt = trade_date_time_adj

        return new_dt.replace(minute=0, second=0)

    # for updating date time adj based off the prices that we see come in
    def check_max_timestamp(self,row):
        date_cols_to_convert = ['max_time_stamp']

        # adjust it to be the next hour where we will take the VWAP of that hour
        row[date_cols_to_convert] = pd.to_datetime(row[date_cols_to_convert])  # , utc=True)
        trade_date_time_adj = row['entry_date_time'] + timedelta(minutes=61)
        trade_date_time_adj = trade_date_time_adj.replace(minute=0, second=0)

        # price history doesn't go all the way up to the floor timestamp (delayed trade time adj)
        if row['max_time_stamp'] < trade_date_time_adj:
            new_dt = row['max_time_stamp']
        else:
            new_dt = row['market_entry_date_time']

        return new_dt.replace(minute=0, second=0)

    # check for ticker changes, i.e. CREE -> WOLF on 10/1/2021
    def check_ticker_change(self,trading_key):
        ticker_change_df = pd.read_csv(get_data('ticker_changes.csv'))
        df = pd.merge(left = trading_key, right = ticker_change_df, how = 'left', left_on = 'symbol', right_on='symbol')
        df['record_date'] = pd.to_datetime(df['record_date'])
        df['symbol'] = df.apply(lambda x : x['new_symbol'] if x['record_date'] <= x['entry_date_time'] else x['symbol'],
                                axis=1)

        return df

    # adding market entry price to trades
    def get_trading_key(self):
        # columns we care to return 
        columns_to_return = ['trade_id','address','chain','symbol','target_percentage',
                                'entry_date_time','next_market_open', 'market_entry_date_time',
                                'vwap']
        if len(self.trades.index) > 0:
            # copy available trades df
            df = self.trades.copy()

            # for sanity checking
            pre_price_row_count = len(df.index)

            # use the calendar key to get delayed_trade_date (next), and delayed_trade_date_time (next)
            c = CoveyCalendar(start_date = df['entry_date'].min())
            calendar_key = c.set_business_dates()

            # merge trading key with calendar key on date
            df = pd.merge(left= df, right=calendar_key, how='inner', left_on='entry_date', right_on='date')

            # set the reference trade date time - adjusting for pre market and post market trade times
            df['market_entry_date_time'] = df.apply(lambda x: self.set_ref_trade_date_time(x), axis=1)

            # set the reference date - strip timestamp from market entry date time
            df['market_entry_date'] = pd.to_datetime(df['market_entry_date_time']).dt.date

            # conversion for merge
            df['market_entry_date'] = pd.to_datetime(df['market_entry_date'])

            # clean up crypto tokens ending is USDT - legacy as we set it back to USDT in the pricing key at the very end of 
            # get_price_key
            #df['symbol'] = df['symbol'].apply(lambda x: x.replace('USDT', 'USD'))

            df = pd.merge(left=df, right=self.price_key, how='left',
                                   left_on=['symbol', 'market_entry_date'], right_on=['symbol', 'delayed_trade_date'])

            # set max timestamp of prices per trade id, just in case it doesn't show all history between expected open and close times
            # aka RUSL
            df['max_time_stamp'] = df.groupby('trade_id')['timestamp'].transform('max')

            df['market_entry_date_time'] = df.apply(lambda x: self.check_max_timestamp(x), axis=1)

            # fill in the blank timestamps (no prices returned for that ticker/date) so that it won't be filtered out in the next step
            # we want to see the un-priced items
            df['timestamp'].fillna(df['market_entry_date_time'], inplace=True)

            # filter trading key to have trade timestamps fall after the date time adj threshold
            trading_key_mask = (df['timestamp'] >= df['market_entry_date_time'])
            df = df[trading_key_mask]

            # add a ranking to grab the next hours only price
            df['price_rank'] = df.groupby('trade_id')['timestamp'].rank('dense', ascending=True)
            df = df[df['price_rank'] == 1]

            # don't need price rank anymore
            df.drop(columns=['price_rank'], inplace=True)

            df.rename(columns=lambda s: s.replace('_x', ''), inplace=True)

            df = df.loc[:, ~df.columns.str.endswith('_y')]


            # making sure we did not lose any trades in the price merge
            post_price_row_count = len(df.index)

            assert (pre_price_row_count == post_price_row_count)

            df_post_merge_check = self.merger_check(df[columns_to_return])

            # drop trade id
            df_post_merge_check.drop(columns = ['trade_id'], inplace=True)

            # sort the trades and set the index
            df_post_merge_check.sort_values(by='entry_date_time', ascending=True, inplace=True)

            # set the trade ID - will be in ascending order of entry date time thanks to above line
            df_post_merge_check['trade_id'] = [x for x in range(1, len(df_post_merge_check.values) + 1)]

            # set index to trade id
            df_post_merge_check.set_index('trade_id',inplace=True)

            return df_post_merge_check

        else:
            print("The trades data frame has not been filled yet")
            # return empty dataframe
            return pd.DataFrame(columns=columns_to_return, index=[0])
          
    # checking to see if there's any mergers - using a csv as record keeper for that at the moment
    def merger_check(self, trading_key):
        merger_df = pd.read_csv(get_data('mergers.csv'))
        df = trading_key.copy()
        df = pd.merge(left=df, right=merger_df, how = 'left', left_on = 'symbol', right_on='symbol')
        df['is_merger'] = df.apply(lambda x  : 0 if pd.isnull(x['entry_price']) else 1, axis = 1)
        df['symbol_appearance_rank'] = df.groupby('symbol')['trade_id'].rank('dense', ascending=True)
        mergers_only_df = df.loc[(df['is_merger'] == 1) & (df['symbol_appearance_rank'] == 1)]
        mergers_only_df['entry_date_time'] = mergers_only_df['entry_date_time'].dt.normalize()
        mergers_only_df['market_entry_date_time'] = mergers_only_df['market_entry_date_time'] + timedelta(days = 1)
        mergers_only_df['vwap'] = mergers_only_df['entry_price']
        mergers_only_df['target_percentage'] = 0

        # remove tickers from main trading key copy that are mergers and after the first instance
        df = df.loc[~((df['is_merger'] == 1) & (df['symbol_appearance_rank'] > 1))]

        concat_df = pd.concat([df,mergers_only_df[trading_key.columns]])
        concat_df = concat_df[trading_key.columns]

        # re-establish trade id
        concat_df = concat_df.sort_values(by = 'market_entry_date_time', ascending=True)
        concat_df['trade_id'] = [x for x in range(1, len(concat_df.values) + 1)]

        return concat_df

    # export to csv
    def export_to_csv(self, key : str = 'trading'):
        if len(self.trading_key.index) > 0:
            if key == 'trading':
                self.trading_key.to_csv(get_output('trading_key.csv'), index=False)
            elif key == 'price':
                self.price_key.to_csv(get_output('price_key.csv'), index=False)


if __name__ == '__main__':
    # load environment variables (aplaca private and public keys)
    load_dotenv()

    # start the timer
    start_time = time.time()

    # initialize trade data object - all defaults - excpet posting only = True for just posting trades
    t = Trade(address = os.environ.get('WALLET_PUBLIC'),
              address_private = os.environ.get('WALLET_PRIVATE'),
              posting_only=True)

    #requests.get('https://gasstation-mainnet.matic.network/v2').json()
    # post trades
    #t.post_trades_polygon('GOOG:0.25')
    t.get_alpaca_universe()
   

    # log how long it took
    print('---Trades for address {} finished in {} seconds ---'.format(t.address,time.time() - start_time))