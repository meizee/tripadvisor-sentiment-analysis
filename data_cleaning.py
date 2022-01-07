import pandas as pd
import numpy as np
from datetime import datetime

links = ['/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_canggu.csv', 
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_jimbaran.csv', 
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_legian.csv',
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_nusa_dua.csv',
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_payangan.csv',
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_tanjung_benoa.csv',
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_ubud.csv',
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_seminyak.csv',
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_kuta.csv',
         '/content/drive/MyDrive/Scrapping Web Tripadvisor/data_csv/tripadvisor_reviews_sanur.csv'
         ]

count = 0 
for link in links:
  df = pd.read_csv(link)
  df = df.drop(columns="Unnamed: 0")
  df = df.assign(rating_num=df.rating.str[:1])
  df['rating_num'] =  pd.to_numeric(df['rating_num'], errors='coerce')
  df['date'] =  df.date.str[8:]
  df['dates'] = pd.to_datetime(df['date'], format='%B %d, %Y')
  df = df[(df['dates']>"2020-01-01")]
  count += df.shape[0]
  df.reset_index()
  name = '/content/drive/MyDrive/Scrapping Web Tripadvisor/cleaned_data/' + link[78:]
  df.to_csv(name, index=False)

print(count)

