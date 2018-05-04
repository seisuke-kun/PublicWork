import pandas as pd
import numpy as np
from load_data.data_loader import load_hotel_reserve
customer_tb, hotel_tb, reserve_tb = load_hotel_reserve()


##単純列抽出##

# reserve_tbの配列に文字配列を指定することで、指定した列名の列を抽出
reserve_tb[['reserve_id', 'hotel_id', 'customer_id','reserve_datetime', 'checkin_date', 'checkin_time','checkout_date']]
# loc関数の2次元配列の2次元目に抽出したい列名の配列を指定することで、列を抽出
reserve_tb.loc[:, ['reserve_id', 'hotel_id', 'customer_id','reserve_datetime', 'checkin_date','checkin_time', 'checkout_date']]
# drop関数によって、不要な列を削除
# axisを1にすることによって、列の削除を指定
# inplaceをTrueに指定することによって、reserve_tbの書き換えを指定
reserve_tb.drop(['people_num', 'total_price'], axis=1, inplace=True)#最も負荷が低い


##列条件に沿った行抽出##
#query関数を使うと、可読性高く、1行で表現できる
reserve_tb.query('"2016-10-13" <= checkout_date <= "2016-10-14"')


##ランダムサンプリング##
#割合指定
reserve_tb.sample(frac=0.5)
#件数指定
reserve_tb.sample(n=100)


##公平なサンプリングのために、集約するcolumnsを決め、そこからランダムサンプリングを行う##
# reserve_tb['customer_id'].unique()は、重複を排除したcustomer_idを返す
# sample関数を利用するためにpandas.Series(pandasのリストオブジェクト)に変換
# sample関数によって、顧客IDをサンプリング
target = pd.Series(reserve_tb['customer_id'].unique()).sample(frac=0.5)
# isin関数によって、customer_idがサンプリングした顧客IDのいずれかに一致した行を抽出
reserve_tb[reserve_tb['customer_id'].isin(target)]

