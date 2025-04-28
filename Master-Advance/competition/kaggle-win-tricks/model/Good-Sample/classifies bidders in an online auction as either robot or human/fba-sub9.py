'''
README

https://www.kaggle.com/c/facebook-recruiting-iv-human-or-bot/
This script classifies bidders in an online auction as either robot or human

To run the code 
bids, bot_or_human = load()
X = build_X(bids, bot_or_human)
make(X)
'''


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import sklearn.preprocessing as preprocessing
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, BayesianRidge
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import roc_auc_score


'''
Declare time units
'''
one_day = 4547368124071.8799
startt = 9631916820392676.0
delta = 2.16e10
cutoff = 1.5e8 #cutoff for "small" time scales

'''
How to calculate time units
start and end times for each three-day data segment
-9631916842105263 + 9645558894736842 = 13642052631579  #week 0
-9695580000000000 + 9709222052631578 = 13642052631578  #week 2
-9759243157894736 + 9772885210526315 = 13642052631579  #week 4
gap between end week 0, start week 2: 50021105263158
gap between end week 2, start week 4: 50021105263158

#use linear regression to calculation startt and one_day
from numpy import arange,array,ones,linalg
times = np.array([9631916842105263, 9645558894736842+1, 9695580000000000, 9709222052631578+1, 9759243157894736, 9772885210526315+1])
days = np.array([0, 3, 14, 17, 28, 31]).reshape((-1,1))
from sklearn import linear_model
clf = linear_model.LinearRegression(fit_intercept=True)
clf.fit(days, times)
4547368124071.8799
startt = clf.predict([0])
startt = 9631916820392676.0

'''

#bids, bot_or_human = load()
def load():
	bot_or_human = pd.read_csv('train.csv')
	test = pd.read_csv('test.csv')
	test['outcome'] = -1
	
	
	bids = pd.read_csv('bids.csv')
	bids = bids.sort(['auction', 'time'])
	
	bot_or_human = pd.concat([ bot_or_human, test ])
	
	#strip the last five characters from the address and payment accounts
	bot_or_human.address = bot_or_human.address.apply(address_strip)
	bot_or_human.payment_account = bot_or_human.payment_account.apply(address_strip)
	
	
	'''
	pivot bidder address prefix and bidder payment_account prefix into features
	'''
	bot_or_human['payment_account_prefix_same_as_address_prefix'] = bot_or_human['address']==bot_or_human['payment_account']
	max_relevant = 6
	
	b = bot_or_human[['bidder_id', 'address']].groupby('address').size().reset_index().sort(0, ascending=False)
	b = b.rename(columns = {0:'address_count'})
	#repeat_addresses = b[b.address_count >= max_relevant].address.values
	infrequent_addresses = b[b.address_count >= 2][b.address_count < max_relevant].address.values
	rare_addresses = b[b.address_count < 2].address.values
	bot_or_human['address'].loc[bot_or_human.address.isin(rare_addresses)] = 'rare_address'
	bot_or_human['address'].loc[bot_or_human.address.isin(infrequent_addresses)] = 'infrequent_address'
	#b = bot_or_human[['bidder_id', 'address']].pivot(index='bidder_id',columns='address').fillna(0).reset_index()
	b = pd.get_dummies(bot_or_human[['address']])
	bot_or_human = pd.concat([bot_or_human, b], axis=1)
	
	b = bot_or_human[['bidder_id', 'payment_account']].groupby('payment_account').size().reset_index().sort(0, ascending=False)
	b = b.rename(columns = {0:'payment_account_count'})
	#repeat_payment_accounts = b[b.payment_account_count >= max_relevant].payment_account.values
	infrequent_payment_account = b[b.payment_account_count >= 2][b.payment_account_count < max_relevant].payment_account.values
	rare_payment_account = b[b.payment_account_count < 2].payment_account.values
	bot_or_human['payment_account'].loc[bot_or_human.payment_account.isin(rare_payment_account)] = 'rare_account'
	bot_or_human['payment_account'].loc[bot_or_human.payment_account.isin(infrequent_payment_account)] = 'infrequent_account'	
	#bot_or_human['payment_account'].loc[~bot_or_human.payment_account.isin(repeat_payment_accounts)] = 'only_once'
	b = pd.get_dummies(bot_or_human[['payment_account']])
	bot_or_human = pd.concat([bot_or_human, b], axis=1)

		
	return bids, bot_or_human
	
	
def address_strip(x):
	return x[0:-5]	
	



def dt(X, bids):
	bots = X[X.outcome==1].bidder_id.values
	humans = X[X.outcome==0].bidder_id.values

	'''
	auction duration
	check if auctions run longer than three days
	calculate time from bid until time of last bid in the auction
	calculate time from bid until time of first bid in the auction
	'''	
	times = bids.groupby('auction').time.min().reset_index()
	times=times.rename(columns = {'time':'startt'})
	times2 = bids.groupby('auction').time.max().reset_index()
	times2=times2.rename(columns = {'time':'endt'})
	
	times = pd.merge(times, times2, on='auction', how='left')
	times['duration'] = times.endt - times.startt
	times['short'] = 1.0*(times['duration'] < 3.01*one_day)
	
	bids = pd.merge(bids, times[['auction', 'short', 'startt', 'endt']], on='auction', how='left')
	b = bids.groupby('bidder_id').short.mean().reset_index()
	X = pd.merge(X, b, on='bidder_id', how='left')
	
	#time from bid until end of auction
	bids['t_until_end'] = bids.endt - bids.time
	bids['t_since_start'] = bids.time - bids.startt
	
	b = bids.groupby('bidder_id').t_until_end.median().reset_index()
	b=b.rename(columns = {'t_until_end':'t_until_end_median'})
	X = pd.merge(X, b, on='bidder_id', how='left')	

	b = bids.groupby('bidder_id').t_since_start.median().reset_index()
	b=b.rename(columns = {'t_since_start':'t_since_start_median'})
	X = pd.merge(X, b, on='bidder_id', how='left')		


	'''
	Useful plots
	
	test_ids = X[X.outcome==-1].bidder_id.values
	
	bot = bids[bids.bidder_id.isin(bots)][bids.country.isin(['de', 'nl', 'se', 'no', 'cz', 'hu'])].t_until_end
	human = bids[bids.bidder_id.isin(humans)][bids.country.isin(['de', 'nl', 'se', 'no', 'cz', 'hu'])].t_until_end

	bot = bids[bids.bidder_id.isin(bots)][bids.country.isin(['id'])].t_until_end
	human = bids[bids.bidder_id.isin(humans)][bids.country.isin(['id'])].t_until_end

	bot = bids[bids.bidder_id.isin(bots)].t_until_end
	human = bids[bids.bidder_id.isin(humans)].t_until_end
	botp = np.histogram(bot, 800, range=[0,8e13], normed=True)
	humanp = np.histogram(human, 800, range=[0,8e13], normed=True)

	bot = np.mod(bids[bids.bidder_id.isin(bots)].t_until_end.values, 4.55e12)
	human = np.mod(bids[bids.bidder_id.isin(humans)].t_until_end.values, 4.55e12)
			
	botp = np.histogram(bot, 300, range=[0,4.9e12], normed=True)
	humanp = np.histogram(human, 300, range=[0,4.9e12], normed=True)
	
	plt.plot(botp[1][0:-1], botp[0], 'b.-')
	plt.plot(botp[1][0:-1], humanp[0], 'g.-')



	bot = bids[bids.bidder_id.isin(bots)].time
	human = bids[bids.bidder_id.isin(humans)].time
	test = bids[bids.bidder_id.isin(test_ids)].time
		
	bot = bids[bids.bidder_id.isin(bots)][bids.country.isin(['nl'])].time
	human = bids[bids.bidder_id.isin(humans)][bids.country.isin(['nl'])].time	

	bots = ['5354c02817e47f28e60e44a40ca5e48dll4sz']
	humans = ['ff58ffde976a4899dcd89597a7877e18lntgz']
	
	bot = np.mod(bids[bids.bidder_id.isin(bots)].time.values, one_day)
	human = np.mod(bids[bids.bidder_id.isin(humans)].time.values, one_day)
	humanp = np.histogram(human, 48, range=[0, one_day], normed=True)
	botp = np.histogram(bot, 48, range=[0, one_day], normed=True)


	humanp = np.histogram(human, 4000, range=[9.63e15, 9.78e15], normed=True)
	botp = np.histogram(bot, 4000, range=[9.63e15, 9.78e15], normed=True)
	testp = np.histogram(test, 4000, range=[9.63e15, 9.78e15], normed=True)	
		
	humanp = np.histogram(human, 30, range=[9.63e15, 9.9e15], normed=True)
	botp = np.histogram(bot, 30, range=[9.63e15, 9.9e15], normed=True)
	
	
	humanp = np.histogram(human, 1000, range=[9.631e15, 9.645e15], normed=True)
	botp = np.histogram(bot, 1000, range=[9.631e15, 9.645e15], normed=True)
		
	plt.plot(humanp[1][0:-1], testp[0], 'r.-')	
	plt.plot(humanp[1][0:-1], humanp[0], 'g.-')
	plt.plot(humanp[1][0:-1], botp[0], 'b.-')
	plt.ylabel('fraction of bids made between t and t+dt')
	plt.xlabel('time [arbitrary units]')
	plt.legend(['human','bot'], frameon=False)
	plt.title('bids over time')
	plt.show()
	
	dt = humanp[1][1] - humanp[1][0]
	a = np.correlate(humanp[0], humanp[0], mode='full')
	plt.plot(dt*np.array(range(0,len(a)-len(a)/2)), a[len(a)/2:], 'k.-')
	plt.ylabel('autocorrelation')
	plt.xlabel('time')
	plt.title('autocorrelation of bids/unit time histogram')
	
	#sample bids per unit time over an auction
	plt.hist(bids[bids.auction == bids.auction[3]].time.values, bins=200)
	plt.ylabel('bids')
	plt.xlabel('time')
	plt.title('bids during auction')
	'''

	
	'''
	number of bids per hour (n=24), half hour (n=48)
	'''
	times = [72]
	for n in times: 
		print 'hour ', n
		b = np.floor((1.0*n/one_day*np.mod(bids.time-startt-delta, one_day)))
		b.name = 'hour'+str(n)
		bids = pd.concat([bids, b], axis=1)
		b = bids.groupby(['bidder_id', 'hour'+str(n)]).size().reset_index()
		b=b.rename(columns = {0:'bids_in_hour'})
		b=b.pivot('bidder_id', 'hour'+str(n), 'bids_in_hour').fillna(0).reset_index()
		old_names = b.columns.values
		new_names = b.columns.values
		for i in range(1,len(b.columns)):
			new_names[i] = str(int(old_names[i])) + '_hour'+str(n)
		b = b.rename(columns=dict(zip(old_names, new_names)))
		b['max_bids_in_hour'+str(n)] = b.iloc[:, 1:].max(axis=1)
	
		for i in range(n):
			b[str(i)+'_hour'+str(n)] = b[str(i)+'_hour'+str(n)]/b['max_bids_in_hour'+str(n)]
		#b = b.drop('max_bids_in_hour'+str(n), 1)
		X = pd.merge(X, b, on='bidder_id', how='left')
				
	n = times[0]
	X['sleep'] = 0
	step = int(5.5*n/24)
	for i in xrange(n - step):
		X['sleep'] += X.loc[:, str(i)+'_hour'+str(n):str(i+step)+'_hour'+str(n)].sum(axis=1) == 0
	
	X['sleep'] = (X['sleep'] >= 1)	
	
		
	'''
	dt between a user's bid and the previous bid by another user in the same auction
	'''
	for week in [0, 2, 4]:
		b = bids[bids.week==week].sort(['auction', 'time'])[['auction', 'time', 'bidder_id']]
		b['bidder_id_prev'] = pd.Series(np.append([np.nan], b.bidder_id.values[0:-1]), index=b.index)
		b['auction_prev'] = pd.Series(np.append([np.nan], b.auction.values[0:-1]), index=b.index)
		dt = np.append([np.nan], b.time.values[0:-1])
		b['time_prev'] = pd.Series(dt, index=b.index)
		b['dt'] = b['time'] - b['time_prev']
				
		if week==0:
			c = [b[b.bidder_id != b.bidder_id_prev][b.auction == b.auction_prev]]
		else:
			c.append(b[b.bidder_id != b.bidder_id_prev][b.auction == b.auction_prev])

	c = pd.concat(c)	
	d = c.groupby('bidder_id').dt.median().reset_index()
	d = d.rename(columns = {'dt': 'dt_others_median'})
	X = pd.merge(X, d[['bidder_id', 'dt_others_median']], on='bidder_id', how='left')
	#X.loc[:,'dt_others_median'] = X.loc[:,'dt_others_median'].fillna(3.0*one_day)
	
	c['dt_others_lt_cutoff'] = np.nan
	c.loc[c.dt <= cutoff, 'dt_others_lt_cutoff'] = 1.0
	c.loc[c.dt > cutoff, 'dt_others_lt_cutoff'] = 0.0
	
	a= c[['bidder_id', 'dt_others_lt_cutoff']].dropna().groupby('bidder_id').mean().reset_index()
	X = pd.merge(X, a, on='bidder_id', how='left')
	X=X.rename(columns = {'dt_others_lt_cutoff':'f_dt_others_lt_cutoff'})	
	
	#plt.hist(X[X.outcome==0].dt_median.values, bins=100, range=[0, 1e9], normed=True)
	#plt.hist(X[X.outcome==1].dt_median.values, bins=100, range=[0, 1e9], normed=True)
	
		
 			
	#time between bids by same bidder (does not matter if previous bid is in same auction)
	for week in [0, 2, 4]:
		b = bids[bids.week==week].sort(['bidder_id', 'time'])[['bidder_id', 'time']]
		#b['bidder_id_prev'] = np.nan
		#b.bidder_id_prev[1:] = b.bidder_id[0:-1]
		b['bidder_id_prev'] = pd.Series(np.append([np.nan], b.bidder_id.values[0:-1]), index=b.index)
		
		#b['time_prev'] = np.nan
		dt = np.append([np.nan], b.time.values[0:-1])
		b['time_prev'] = pd.Series(dt, index=b.index)
		b['dt'] = b['time'] - b['time_prev']
		
		
		if week==0:
			c = [b[b.bidder_id == b.bidder_id_prev]]
		else:
			c.append(b[b.bidder_id == b.bidder_id_prev])	
	
	c = pd.concat(c)	
	d = c.groupby('bidder_id').dt.median().reset_index()
	d = d.rename(columns = {'dt': 'dt_self_median'})
	X = pd.merge(X, d[['bidder_id', 'dt_self_median']], on='bidder_id', how='left')
	d = c.groupby('bidder_id').dt.min().reset_index()
	d = d.rename(columns = {'dt': 'dt_self_min'})
	X = pd.merge(X, d[['bidder_id', 'dt_self_min']], on='bidder_id', how='left')
	#X.loc[:,'dt_self_median'] = X.loc[:,'dt_self_median'].fillna(3.0*one_day)
	#X.loc[:,'dt_self_min'] = X.loc[:,'dt_self_min'].fillna(3.0*one_day)

	
	'''
	bot_h = np.histogram(bids[bids.bidder_id.isin(bots)].dt.values, bins=100, range=[0, 1e10], normed=True)
	human_h = np.histogram(bids[bids.bidder_id.isin(humans)].dt.values, bins=100, range=[0, 1e10], normed=True)
	plt.plot(bot_h[1][1:], bot_h[0], 'b.-')
	plt.plot(bot_h[1][1:], human_h[0], 'r.-')
	'''	


		
	return X

	
	

def n_bids(X, bids):
	a = bids.groupby(['bidder_id', 'auction']).size().reset_index()
	a=a.rename(columns = {0:'bids_per_auction'})
	b = a.groupby('bidder_id').bids_per_auction.median().reset_index()
	b=b.rename(columns = {'bids_per_auction':'bids_per_auction_median'})
	X = pd.merge(X, b, on='bidder_id', how='left')
	
	b = a.groupby('bidder_id').mean().reset_index()
	b=b.rename(columns = {'bids_per_auction':'bids_per_auction_mean'})
	X = pd.merge(X, b, on='bidder_id', how='left')	
	
	b = bids.groupby('bidder_id').size().reset_index()
	b=b.rename(columns = {0:'n_bids'})
	X = pd.merge(X, b, on='bidder_id', how='left')	
		
	return X


def enumerate(x):
	x['bid_order'] = 1.0*np.arange(len(x))/len(x)
	return x
  
  
def fac_div_fac(x,y):

	if x == 0:
		x = 1
	if y == 0:
		y = 1
			
	if x > y:
		return np.sum( np.log(1.0*np.array(range(int(y+1),int(x+1))) ) )
	if y > x:
		return -np.sum( np.log(1.0*np.array(range(int(x+1),int(y+1))) ) )
	return 0.0
		
  
def balance(x):
#	x['balance'] = np.std(x)/np.sqrt(np.mean(x))
	
	x0 = int(np.floor(np.sum(x)/len(x)))
	base = x0*np.ones(len(x))
	base[0:int(np.sum(x)-x0*len(x))] = x0+1
	
	b = 0.0
	for i in xrange(len(x)):
		#print base[i], x[i]
		b += fac_div_fac(base[i], x[i])
	
	#print b
	x['balance'] = b
	
	return x  




def day(X, bids):
	bots = X[X.outcome==1].bidder_id.values
	humans = X[X.outcome==0].bidder_id.values

	bids['day'] = np.floor((bids['time'] - startt)/one_day)
	
	b = bids.groupby(['bidder_id', 'day']).size().reset_index()
	b = b.rename(columns = {0:'daily_bids'})
	b = b.pivot('bidder_id', 'day', 'daily_bids').fillna(0).reset_index()
	old_names = b.columns.values
	new_names = [b.columns[0]]	
	for i in range(1,len(b.columns)):
		new_names.append( str(int(old_names[i])) + '_day' )
	b = b.rename(columns=dict(zip(old_names, new_names)))	
	
	
	b['monday'] = (b['0_day'] + b['14_day'] + b['28_day']).fillna(0)
	b['tuesday'] = (b['1_day'] + b['15_day'] + b['29_day']).fillna(0)
	b['wednesday'] = (b['2_day'] + b['16_day'] + b['30_day']).fillna(0)
	b['balance'] = b[['monday', 'tuesday', 'wednesday']].apply(balance, axis=1)[['balance']]
	b['balance2'] = b[['0_day', '1_day', '2_day', '14_day', '15_day', '16_day', '28_day', '29_day', '30_day']].apply(balance, axis=1)[['balance']]
	
	X = pd.merge(X, b.loc[:,['bidder_id', 'monday', 'tuesday', 'wednesday', 'balance', 'balance2']], on='bidder_id', how='left')
	X[['monday', 'tuesday', 'wednesday', 'balance']] = X[['monday', 'tuesday', 'wednesday', 'balance']].fillna(0)

	s = X.loc[:, ['monday', 'tuesday', 'wednesday']].max(axis=1)
	X['s_monday'] = X['monday']/s
	X['s_tuesday'] = X['tuesday']/s
	X['s_wednesday'] = X['wednesday']/s
	
	s = X.loc[:, ['monday', 'tuesday', 'wednesday']].sum(axis=1)
	X['f_monday'] = X['monday']/s
	X['f_tuesday'] = X['tuesday']/s
	X['f_wednesday'] = X['wednesday']/s	
	
# 	nbids = X.loc[:, ['monday', 'tuesday', 'wednesday']].sum(axis=1)
# 	X['bids_week0'] = (b['0_day'] + b['1_day'] + b['2_day']).fillna(0)
# 	X['bids_week2'] = (b['14_day'] + b['15_day'] + b['16_day']).fillna(0)
# 	X['bids_week4'] = (b['28_day'] + b['29_day'] + b['30_day']).fillna(0)
# 	s = X.loc[:, ['bids_week0', 'bids_week2', 'bids_week4']].max(axis=1)
# 	X['s_bids_week0'] = X['bids_week0']/s
# 	X['s_bids_weeek2'] = X['bids_week2']/s
# 	X['s_bids_week4'] = X['bids_week4']/s

	X.drop('balance2', 1, inplace=True)

	return X
	 
	 
	 
	    
def bid_order(X, bids):
	bids = bids.groupby('auction').apply(enumerate)
	
	a = bids.sort('time', ascending=True).groupby('auction', as_index=False).first()
	b = a.groupby('bidder_id').size().reset_index()
	b= b.rename(columns = {0:'num_first_bid'})	
	X = pd.merge(X, b, on='bidder_id', how='left')
	print X.columns
	X['num_first_bid'].fillna(0, inplace=True)
	

	return X




def user_countries_per_auction(X, bids):
	#a = bids.groupby(['auction', 'bidder_id', 'country']).country.count()
	#a = bids.groupby(['auction', 'bidder_id']).country.size()
	#bids[bids.bidder_id=='5c28b04424e96267711d5af2db62e022tp36c'][['auction', 'country']].groupby('auction').size()
	
	
	b = bids[['bidder_id', 'auction', 'country']].groupby(['bidder_id','auction']).country.nunique().reset_index()
	b= b.rename(columns = {'country':'countries_per_bidder_per_auction'})	
	
	c = b.groupby('bidder_id').countries_per_bidder_per_auction.median().reset_index()
	c= c.rename(columns = {'countries_per_bidder_per_auction':'countries_per_bidder_per_auction_median'})
	X = pd.merge(X, c, on='bidder_id', how='left')

	c = b.groupby('bidder_id').countries_per_bidder_per_auction.mean().reset_index()
	c= c.rename(columns = {'countries_per_bidder_per_auction':'countries_per_bidder_per_auction_mean'})
	X = pd.merge(X, c, on='bidder_id', how='left')	
	
	c = b.groupby('bidder_id').countries_per_bidder_per_auction.max().reset_index()
	c= c.rename(columns = {'countries_per_bidder_per_auction':'countries_per_bidder_per_auction_max'})
	X = pd.merge(X, c, on='bidder_id', how='left')		
	
	

	a = bids.groupby(['bidder_id']).country.value_counts().reset_index()
	b = a.groupby(['bidder_id']).agg(lambda x: x.iloc[0]).reset_index()
	b= b.rename(columns = {'level_1':'most_common_country'})
	X = pd.merge(X, b[['bidder_id','most_common_country']], on='bidder_id', how='left')	

	
	b = bids[['bidder_id', 'country']].groupby(['bidder_id', 'country']).size().reset_index()
	b= b.rename(columns = {0:'nbids'})
	c = b.pivot('bidder_id','country').fillna(0).reset_index()
	c.columns = c.columns.get_level_values(1)
	c= c.rename(columns={c.columns[0]:'bidder_id'})
	#fraction of bids in each country (for each user)
	#c.iloc[:,1:] = c.iloc[:,1:].div(c.iloc[:,1:].sum(axis=1), axis=0)
	#number of bids in each country rescaled by the largest number of bids in a country (for each user)
	c.iloc[:,1:] = c.iloc[:,1:].div(c.iloc[:,1:].max(axis=1), axis=0)
	X = pd.merge(X, c, on='bidder_id', how='left')
	

	#b = bids[['bidder_id', 'country']].groupby(['bidder_id', 'country']).country.nunique().reset_index()
	#b = bids[['bidder_id', 'country']].groupby(['bidder_id', 'country']).size().reset_index()
	

	
# 	a = bids.groupby(['bidder_id', 'country']).size().reset_index()
# 	a= a.rename(columns = {0:'c_count'})
# 	a.groupby(['bidder_id']).sort('c_count').agg(lambda x: x.iloc[0])
# 	
# 	a = bids.groupby(['bidder_id']).country.apply(mode())	
# 	a= a.rename(columns = {0:'bids_in_country'})
# 	a.groupby(['bidder_id']).agg(lambda x:x.value_counts())
	
	#bids[bids.bidder_id=='0053b78cde37c4384a20d2da9aa4272aym4pb'][bids.auction=='1l3p3'][['time', 'country']]
	
# 	hum = np.histogram(X[X.outcome==0].countries_per_bidder_per_auction_max.values, bins=10, normed=True, range=[0,10])
# 	bot = np.histogram(X[X.outcome==1].countries_per_bidder_per_auction_max.values, bins=10, normed=True, range=[0,10])
# 	plt.plot(hum[1][0:-1], hum[0], 'g.-')
# 	plt.plot(hum[1][0:-1], bot[0], 'b.-')

	return X


	
def log_entropy(x):
	e = np.sum(np.log(np.array(range(1,np.sum(x)))))
	for i in x:
		e -= np.sum(np.log(np.array(range(1,i))))
	
	return e	


#X = urls(X, bids)
def urls(X, bids):
	'''
	number of unique referring urls used by bidder
	unique referring urls / total_bids
	'''
	b = bids.groupby('bidder_id').url.nunique().reset_index().fillna(1)
	b= b.rename(columns = {'url':'n_urls'})
	X = pd.merge(X, b, on='bidder_id', how='left')
	b = bids.groupby(['bidder_id']).url.count().reset_index().fillna(1)
	b= b.rename(columns = {'url':'n_bids_url'})
	X = pd.merge(X, b, on='bidder_id', how='left')
	X['f_urls'] = X['n_urls']/X['n_bids_url']

 	nbids =bids.groupby(['bidder_id']).size().reset_index()
 	nbids= nbids.rename(columns = {0:'nbids'})
 			
	a =bids.groupby(['bidder_id', 'url']).size().reset_index()
	a= a.rename(columns = {0:'url_counts'})
	a['urls_used'] = 1.0
	
	
	a = pd.merge(a, nbids, on='bidder_id', how='left')
	a['f_urls'] = a['url_counts']/a['nbids']
	
	b = a.groupby('url').urls_used.count().reset_index()
 	print 'num urls ', b[b.urls_used > 18].url.values.shape[0]
 	
 	repeat_urls = b[b.urls_used > 18].url.values
 	
 	c = a[a.url.isin(repeat_urls)].pivot('bidder_id','url','f_urls').reset_index()
	X = pd.merge(X, c, on='bidder_id', how='left')
	X.iloc[:, -len(repeat_urls):] = X.iloc[:, -len(repeat_urls):].fillna(0)
 		
	b = bids.groupby(['bidder_id', 'url']).size().reset_index()
	b= b.rename(columns = {0:'url_count'})
	c = b.groupby('bidder_id').url_count.apply(log_entropy).reset_index()
	c= c.rename(columns = {'url_count':'url_entropy'})
	
	X = pd.merge(X, c, on='bidder_id', how='left')	
	
	X['f_urls'].fillna(1.0)
		
	return X
	
	
def merch(X, bids):
	'''
	type of merchandise on first page visited by bidder
	'''
	a = bids.groupby('bidder_id').first().reset_index()
	b = pd.get_dummies(a['merchandise'], columns='merchandise')
	X = pd.concat([X, b], axis=1)
	
	return X
		

	
def ip(X,bids):
	bots = list(X[X.outcome==1].bidder_id.values)
	humans = list(X[X.outcome==0].bidder_id.values)


	
	'''
	IP fingerprint
	uses a clustering algorithm to group bidders which use a similar set of IPs
	it's quite time consuming
	'''
	'''
	nbids = bids.groupby('bidder_id').size().reset_index()
	nbids= nbids.rename(columns = {0:'n_bids'})
	
	b = bids[bids.bidder_id.isin(bots+humans)].groupby('ip').bidder_id.nunique().reset_index()
	ip_many_users = b[b.bidder_id >= 2].ip.values
	c = bids[bids.bidder_id.isin(bots+humans)].loc[bids.ip.isin(ip_many_users), :].groupby(['bidder_id', 'ip']).size().reset_index()
	#c['v'] = 1
	c= c.rename(columns = {0:'counts'})
	c = pd.merge(c, nbids, on='bidder_id', how='left')
	c['f'] = c['counts']/c['n_bids']
	d = c.pivot('bidder_id', 'ip', 'f').reset_index().fillna(0)
	print 'starting clustering'
	brc = MiniBatchKMeans(n_clusters=100, init='k-means++', max_iter=100, batch_size=100, verbose=0, compute_labels=True, random_state=None, tol=0.0, max_no_improvement=10, init_size=None, n_init=3, reassignment_ratio=0.01)
	brc.fit(d.values[:, 1:])

	c = bids.loc[bids.ip.isin(ip_many_users), :].groupby(['bidder_id', 'ip']).size().reset_index()
	c['v'] = 1
	d = c.pivot('bidder_id', 'ip', 'v').reset_index().fillna(0)	
	clusters = brc.predict(d.values[:, 1:])
	print 'done clustering'
	
	e = d[['bidder_id']]
	e['ip_cluster'] = np.nan
	e.loc[:,['ip_cluster']] = pd.Series(clusters, index=e.index)

	
	X= pd.merge(X, e[['bidder_id', 'ip_cluster']], on='bidder_id', how='left')
	X['ip_cluster'].fillna(-1, inplace=True)
	y = pd.get_dummies(X['ip_cluster'])
	print 'ip groupings size ', y.shape[1]
	X = X.join(y)
	X = X.drop('ip_cluster', 1)

	print 'done ip fingerprint'
	'''
	
	

	'''
	ips per auction for each bidder
	'''
	a = bids[['bidder_id', 'auction', 'ip']].groupby(['bidder_id','auction', 'ip']).size().reset_index()
	a= a.rename(columns = {0:'bids_per_auction_per_ip'})
	b = a.groupby(['bidder_id', 'auction']).bids_per_auction_per_ip.apply(log_entropy).reset_index()
	b= b.rename(columns = {'bids_per_auction_per_ip':'bids_per_auction_per_ip_entropy'})	
	c = b.groupby('bidder_id').bids_per_auction_per_ip_entropy.median().reset_index()
	c= c.rename(columns = {'bids_per_auction_per_ip_entropy':'bids_per_auction_per_ip_entropy_median'})
	X = pd.merge(X, c[['bidder_id','bids_per_auction_per_ip_entropy_median' ]], on='bidder_id', how='left')	
	c = b.groupby('bidder_id').bids_per_auction_per_ip_entropy.mean().reset_index()
	c= c.rename(columns = {'bids_per_auction_per_ip_entropy':'bids_per_auction_per_ip_entropy_mean'})
	X = pd.merge(X, c[['bidder_id','bids_per_auction_per_ip_entropy_mean' ]], on='bidder_id', how='left')	
		
	b = bids[['bidder_id', 'auction', 'ip']].groupby(['bidder_id','auction']).ip.nunique().reset_index()
	b= b.rename(columns = {'ip':'ips_per_bidder_per_auction'})	
# 	b = pd.merge(b,a, on=['bidder_id', 'auction'], how='left')
# 	b['f_ips_per_bidder_per_auction'] = b['ips_per_bidder_per_auction']/b['bids_per_auction']
	
	c = b.groupby('bidder_id').ips_per_bidder_per_auction.median().reset_index()
	c= c.rename(columns = {'ips_per_bidder_per_auction':'ips_per_bidder_per_auction_median'})
	X = pd.merge(X, c[['bidder_id', 'ips_per_bidder_per_auction_median']], on='bidder_id', how='left')
	c = b.groupby('bidder_id').ips_per_bidder_per_auction.mean().reset_index()
	c= c.rename(columns = {'ips_per_bidder_per_auction':'ips_per_bidder_per_auction_mean'})
	X = pd.merge(X, c[['bidder_id', 'ips_per_bidder_per_auction_mean']], on='bidder_id', how='left')

	'''
	fraction of bids placed by user from IP which is rare
	'''
	#b = bids.groupby(['ip', 'bidder_id']).size().reset_index()
	b = bids.groupby('ip').bidder_id.nunique().reset_index()
	ip_many_users = b[b.bidder_id > 1].ip.values
	#ip_some_users = b[b.bidder_id < 300].ip.values
	#ip_few_users = b[b.bidder_id <= 50].ip.values
	ip_only_one_user = b[b.bidder_id == 1].ip.values
	
	bids['ip2'] = np.nan
	bids.loc[bids.ip.isin(ip_many_users), ['ip2']] = 'many'
	#bids.loc[bids.ip.isin(ip_some_users), ['ip2']] = 'some'
	#bids.loc[bids.ip.isin(ip_few_users), ['ip2']] = 'few'
	bids.loc[bids.ip.isin(ip_only_one_user), ['ip2']] = 'only_one_user'
	
	c = bids.groupby(['bidder_id','ip2']).size().reset_index()
	c = c.rename(columns = {0: 'counts'})
	d = c.pivot('bidder_id', 'ip2', 'counts').reset_index().fillna(0)
	d['ip_only_one_user_counts'] = 1*d['only_one_user']
	d.iloc[:,1:] = d.iloc[:,1:].div(d.iloc[:,1:].sum(axis=1), axis=0)
	X = pd.merge(X, d, on='bidder_id', how='left')
	X.iloc[:, -(d.shape[1]-1):].fillna(0, inplace=True)
	X = X.drop('many', 1)
	#X = X.drop('some', 1)
	#X = X.drop('few', 1)
	print 'finished building ip pivot table', d.shape[1]
	
	
	'''
	does the bidder use a network that has a bot on it? (where the bot is not that bidder)
	what fraction of networks used by the bidder have bots on them? (where the bot is not that bidder)
	'''
	
	bids = pd.merge(bids, X[['bidder_id', 'outcome']], on='bidder_id', how='left')
	bids['outcome'] = 1.0*(bids['outcome'] == 1)
	b = bids.groupby(['ip', 'bidder_id']).outcome.mean().reset_index()
	b.outcome = 1.0*(b.outcome)
	c = b.groupby('ip').outcome.sum().reset_index()		
	c['nbots_on_ip'] = c.outcome
	bids = pd.merge(bids, c[['ip', 'nbots_on_ip']], on='ip', how='left')
	bids['on_ip_that_has_a_bot'] = 1*((bids['nbots_on_ip'] - bids['outcome']) >= 1)
	bids['on_ip_that_has_3bots'] = 1*((bids['nbots_on_ip'] - bids['outcome']) >= 3)
 	bids = bids.drop('outcome', 1)
 	bids = bids.drop('nbots_on_ip', 1)
	
 	b = bids.groupby(['bidder_id', 'ip']).on_ip_that_has_a_bot.mean().reset_index()
 	c = b.groupby('bidder_id').on_ip_that_has_a_bot.mean().reset_index()
	X = pd.merge(X, c[['bidder_id', 'on_ip_that_has_a_bot']], on='bidder_id', how='left')
	X['on_ip_that_has_a_bot_mean'] = X['on_ip_that_has_a_bot'].fillna(0)
	X['on_ip_that_has_a_bot'] = 1*(X['on_ip_that_has_a_bot'].fillna(0) > 0)
	
#  	b = bids.groupby(['bidder_id', 'ip']).on_ip_that_has_3bots.mean().reset_index()
#  	c = b.groupby('bidder_id').on_ip_that_has_3bots.mean().reset_index()	
#  	X = pd.merge(X, c[['bidder_id', 'on_ip_that_has_3bots']], on='bidder_id', how='left')
# 	X['on_ip_that_has_3bots_mean'] = X['on_ip_that_has_3bots'].fillna(0)
# 	X['on_ip_that_has_3bots'] = 1*(X['on_ip_that_has_3bots'].fillna(0) > 0)
	
	'''
	IP entropy
	'''
	b = bids.groupby(['bidder_id', 'ip']).size().reset_index()
	b= b.rename(columns = {0:'ip_count'})
	c = b.groupby('bidder_id').ip_count.apply(log_entropy).reset_index()
	c= c.rename(columns = {'ip_count':'ip_entropy'})
	X = pd.merge(X, c, on='bidder_id', how='left')
	


	'''
	time between subsequent bids on different IPs for each user
	'''
	for week in [0, 2, 4]:
		b = bids[bids.week==week].sort(['bidder_id', 'time'])[['bidder_id', 'time', 'ip']]
		b['bidder_id_prev'] = pd.Series(np.append([np.nan], b.bidder_id.values[0:-1]), index=b.index)
		b['ip_prev'] = pd.Series(np.append([np.nan], b.ip.values[0:-1]), index=b.index)
		dt = np.append([np.nan], b.time.values[0:-1])
		b['time_prev'] = pd.Series(dt, index=b.index)
		b['dt'] = b['time'] - b['time_prev']
				
		if week==0:
			c = [b[b.bidder_id == b.bidder_id_prev][b.ip != b.ip_prev]]
		else:
			c.append(b[b.bidder_id == b.bidder_id_prev][b.ip != b.ip_prev])

	c = pd.concat(c)	
	d = c.groupby('bidder_id').dt.median().reset_index()
	d = d.rename(columns = {'dt': 'dt_change_ip_median'})
	X = pd.merge(X, d[['bidder_id', 'dt_change_ip_median']], on='bidder_id', how='left')
	
	
	'''
	time between bids on the same IP for each user
	'''
	for week in [0, 2, 4]:
		b = bids[bids.week==week].sort(['bidder_id', 'time'])[['bidder_id', 'time', 'ip']]
		b['bidder_id_prev'] = pd.Series(np.append([np.nan], b.bidder_id.values[0:-1]), index=b.index)
		b['ip_prev'] = pd.Series(np.append([np.nan], b.ip.values[0:-1]), index=b.index)
		dt = np.append([np.nan], b.time.values[0:-1])
		b['time_prev'] = pd.Series(dt, index=b.index)
		b['dt'] = b['time'] - b['time_prev']
				
		if week==0:
			c = [b[b.bidder_id == b.bidder_id_prev][b.ip == b.ip_prev]]
		else:
			c.append(b[b.bidder_id == b.bidder_id_prev][b.ip == b.ip_prev])

	c = pd.concat(c)	
	d = c.groupby('bidder_id').dt.median().reset_index()
	d = d.rename(columns = {'dt': 'dt_same_ip_median'})
	X = pd.merge(X, d[['bidder_id', 'dt_same_ip_median']], on='bidder_id', how='left')
	


	
	#X['dt_change_ip-dt_same_ip'] = X['dt_change_ip_median'] - X['dt_same_ip_median']
	#X.loc[:,'dt_change_ip_median'] = X.loc[:,'dt_change_ip_median'].fillna(30.0*one_day)
	#X.loc[:,'dt_same_ip_median'] = X.loc[:,'dt_same_ip_median'].fillna(30.0*one_day)
	#X.loc[:,'dt_change_ip-dt_same_ip'] = X.loc[:,'dt_change_ip-dt_same_ip'].fillna(30.0*one_day)
	
 	X['dt_change_ip_median'].fillna(-1, inplace=True)
 	X['dt_same_ip_median'].fillna(-1, inplace=True)
# 	X['dt_change_ip-dt_same_ip'].fillna(-31*one_day, inplace=True)
	
	
	'''
	giant pivot table of overlapping IPs
	'''
	'''
	q = bids[bids.bidder_id.isin(bots+humans)].groupby('ip').bidder_id.nunique().reset_index()
	ip_many_users = q[q.bidder_id >= 3].ip.values
	
	b = bids.groupby(['ip','bidder_id',]).size().reset_index()
	b = b[b.ip.isin(ip_many_users)]
	b = b.rename(columns = {0:'count'})
	b.drop('count', 1, inplace=True)

	b2 = bids[bids.bidder_id.isin(bots+humans)].groupby(['ip','bidder_id',]).size().reset_index()
	b2 = b2[b2.ip.isin(ip_many_users)]
	b2 = b2.rename(columns = {0:'count'})
	b2.drop('count', 1, inplace=True)	
	
	b2 = b2.rename(columns = {'bidder_id':'bidder_id2'})
	b2['v'] = 1
	c = pd.merge(b,b2, on='ip', how='left')
	d = c.pivot_table(index='bidder_id', columns='bidder_id2', values='v')
	d = d.reset_index().fillna(0)
	X = pd.merge(X, d, on='bidder_id', how='left')
	X.iloc[:, -d.shape[1]-1:].fillna(0, inplace=True)
	print 'finished cluster fingerprint'
	'''

	
	return X
	
	
	
	
#X = build_X(bids, bot_or_human) 	
def build_X(bids, bot_or_human):
	X = bot_or_human
	X = X.drop('payment_account', 1)
	X = X.drop('address', 1)

	bids['day'] = (np.floor((bids['time'] - startt)/one_day))
	bids['week'] = (np.floor(bids['day']/7.0))
		
	#print bids.bidder_id[0]
	print 'starting ips'
	X = ip(X, bids)		
	print 'starting bid order'
	X = bid_order(X, bids)
	print 'starting dt'
	X = dt(X, bids)				
	print 'startin day'
	X = day(X, bids)
	print 'starting n_bids'
	X = n_bids(X, bids)
	print 'starting urls'
	X = urls(X, bids)
	#print 'starting bid order'
	#X = bid_order(X, bids)
	print 'starting countries'
	X = user_countries_per_auction(X, bids)
	print 'starting merch'
	X = merch(X, bids)		
	

	return X




def mean_over_cols(x):
	s = np.sum(x)
	x['f_bids_first_third'] = x[0]/s
	x['f_bids_second_third'] = x[1]/s
	x['f_bids_third_third'] = x[2]/s
	return x
	





def make(X):
	output = X[X.outcome==-1]['bidder_id'].reset_index()
	print X.shape
	X.drop(X[X.outcome >=0][X.n_bids.isnull()].index, inplace=True)
	print X.shape
	
	#X = X.sort(['n_bids', 'dt_others_median'])
	X = X.sort(['dt_others_median'])
	#X = X.sort(['on_ip_that_has_a_bot_mean', 'dt_others_median'])
	X = X.fillna(method='pad')
#  	X = X.sort(['on_ip_that_has_a_bot_mean'])
#  	X = X.fillna(method='pad')
	X = X.fillna(method='backfill')
	X.sort_index(inplace=True)
	X = X.fillna(0)
	
	X = X.drop('most_common_country', 1)
	X = X.drop('bidder_id', 1)
		
	#clf0 = GradientBoostingClassifier(n_estimators=100, learning_rate=0.01, max_depth=4, min_samples_split=2)
	#clf0 = RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_split=2, random_state=0) 
	
	#clf = SGDClassifier(loss="modified_huber", penalty="elasticnet", n_iter=20000, class_weight='auto', alpha=0.1, epsilon=0.01)
	#clf = SVC(C=1.0, class_weight='auto', probability=True, kernel='rbf', gamma=0.0, tol=1e-1)
	#clf = AdaBoostClassifier(n_estimators=3000)
	#clf = GradientBoostingClassifier(n_estimators=3000, learning_rate=0.01, max_depth=None, min_samples_leaf=1)
	#clf = ExtraTreesClassifier(n_estimators=3000, max_depth=None, min_samples_leaf=1, random_state=0)
	
	#clf = RandomForestClassifier(n_estimators=2500, max_depth=None, min_samples_leaf=1, random_state=0, criterion='entropy') 
	clf = []
	nclf = 5
	for i in xrange(nclf):
		clf.append(RandomForestClassifier(n_estimators=800, max_depth=None, min_samples_leaf=1, random_state=i, criterion='entropy') )

	scores = []
	scores0 = []
	
	Yb = X['outcome'].values
	Xb = 1.0*X.drop('outcome', 1)
	
	columns = Xb.columns
	Xb = preprocessing.normalize(Xb.values, axis=0)
	first_test_item = X[X.outcome>=0].shape[0]
	
	
	X_test = Xb[first_test_item:, :]
	print 'X_test shape ', X_test.shape
	Y = Yb[0:first_test_item]
	X = Xb[0:first_test_item, :]
	
	
	n = int(0.8*X.shape[0])
	all = range(X.shape[0])
					
	for i in range(100):
		
		np.random.shuffle(all)
		train = all[0:n]
		valid = all[n:]

		X_train = Xb[train, :]
		X_valid = Xb[valid, :]
		Y_train = Yb[train]
		Y_valid = Yb[valid]
		


  		X_train2 = X_train
  		X_valid2 = X_valid
  		
  		print '--- ', i
  		pred_valid = np.zeros(X_valid2.shape[0])
		for j in range(nclf):
			clf[j].fit(X_train2, Y_train) #, sample_weight=(0.95*Y_train+0.05)
			#pred_train = clf.predict_proba(X_train2) 
			#print pred_train[[21,50,51, 100, 101, 102, 103]]
			#print Y_train.shape, pred_train.shape
			#print roc_auc_score(Y_train, pred_train[:,1])
			a = clf[j].predict_proba(X_valid2)[:,1]
			pred_valid += a
			print roc_auc_score(Y_valid, a)
		pred_valid = 1.0*pred_valid/nclf	
		
		s = roc_auc_score(Y_valid, pred_valid)
		print s
		scores.append(s)
		

		
	print np.mean(scores), 2.0*np.std(scores)	
	#print np.max(clf.feature_importances_), np.argmax(clf.feature_importances_)
	#for i in range(20):
	#	print columns[i], clf.feature_importances_[i]
	
 	v = np.argsort(clf[0].feature_importances_)[::-1]
 	for i in range(40):
 		print columns[v[i]], clf[0].feature_importances_[v[i]]

	if len(scores) == 100:
		print np.sort(np.array(scores))[10]
		print np.sort(np.array(scores))[25]
		print np.sort(np.array(scores))[50]

	
	print 'making test predictions'
	
	X_train = X
	Y_train = Y

	
	pred_test = np.zeros(X_test.shape[0])
	for j in range(nclf):
		clf[j].fit(X_train, Y_train) #, sample_weight=(0.95*Y_train+0.05)
		a = clf[j].predict_proba(X_test)[:,1]
		pred_test += a
		
	pred_test = 1.0*pred_test/nclf
			

	
	#output probability that bidder is a robot
	
	print pred_test.shape, 
	output['prediction'] = pd.Series(pred_test, index=output.index)
	output.drop('index', 1)
	
	output.to_csv('fba_sub9.csv', sep=',', index=False, header=True, columns=['bidder_id', 'prediction'])
	
	
	

	return scores
