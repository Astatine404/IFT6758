# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, NavigableString
import requests


class Prog1:

	def q1(self, url = 'https://raw.githubusercontent.com/ift-6758/files/main/ufo-table.html'):
		"""
		Your solution / Votre solution
		"""
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		rows = list(soup.find_all('tbody')[0].children)
		n_columns = len([el for el in list(rows[1].children) if not isinstance(el, NavigableString)]) - 1
		df = pd.DataFrame(columns=[i for i in range(n_columns)])
		i, j = 0, 0
		for row in rows[2:]:
			if isinstance(row, NavigableString):
				continue
			j = 0
			for item in list(row.children)[2:]:
				if isinstance(item, NavigableString):
					continue
				df.loc[i, j] = item.get_text()
				j += 1
			i += 1
		return df

	def q2(self, csv_file='https://raw.githubusercontent.com/ift-6758/files/main/ufo-table.csv', column_name='state'):
		"""
		Your solution / Votre solution
		"""
		df = pd.read_csv(csv_file)
		count = df[df[column_name].isna()].shape[0]
		df[column_name] = df[column_name].replace(to_replace=np.nan, value="unknown")

		return df, count

	def q3(self, df):
		df_out = df[df['comments'].str.contains("light") & (df['state'] != "unknown") & (df['city'] != "unknown") & (df['shape'] != "unknown") & (df['duration_seconds'] >= 400)]
		df_out = df_out.sort_values(by=['duration_seconds'], ascending=False)
		df_out['ind'] = range(0, 2 * df_out.shape[0], 2)
		df_out = df_out.set_index('ind')

		return df_out

	def q4(self, df):
		datetime_df = pd.to_datetime(df['sighted_timestamp'], format='%m/%d/%Y %H:%M')
		df['month'] = datetime_df.dt.strftime('%b').str.lower()
		df['day_of_week'] = datetime_df.apply(lambda x: (x.dayofweek + 1) % 7)

		return df

	def q5(self, df):
		df = df.groupby(['month', 'state'], sort=False).mean()[['duration_seconds']].reset_index()
		df = df.rename(columns={'duration_seconds': 'mean_duration_seconds'})

		return df

	def q6(self, df):
		df = df.groupby(['month', 'state']).count().reset_index().loc[:, ['month', 'state', 'city']].rename({'city': 'count'}, axis=1)
		df = df.pivot(index='state', columns='month')

		return df
