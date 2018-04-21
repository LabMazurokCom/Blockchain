Exchange = ['binance','bitstamp','cex','exmousd', 'exmousdt', 'gdax','kucoin']
import numpy as np
from script import run_script
from time import sleep, time
import pandas as pd
import plotly.offline as pl
import plotly.graph_objs as go
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
pl.init_notebook_mode(connected=True)

for i in range(7):
    files = [Exchange[i]+'_exp_ask.csv', Exchange[i]+'_frac_ask.csv', Exchange[i]+'_fracas_ask.csv']
    for f in files:
        with open('f', 'w'):
            pass
for i in range(7):
    files = [Exchange[i]+'_exp_bid.csv', Exchange[i]+'_frac_bid.csv', Exchange[i]+'_fracas_bid.csv']
    for f in files:
        with open('f', 'w'):
            pass
for s in range(2):
    try:
        run_script()
        for i in range(1):
            ask = pd.read_csv('ask.csv', header=None)
            ask.columns=['price','btc','exchange','currency']
            bid = pd.read_csv('bid.csv', header=None)
            bid.columns=['price','btc','exchange','currency']
            ask['volume'] = ask['price']*ask['btc']/1000
            bid['volume'] = bid['price']*bid['btc']/1000
            bid['cum'] = bid['volume'] # Фактически нужет только 1ый элемент
            ask['cum'] = ask['volume']
            ask_cex = ask[ask.exchange==Exchange[i]].copy()
            bid_cex = bid[bid.exchange==Exchange[i]].copy()
            bid_cex.reset_index(drop=True, inplace=True)
            ask_cex.reset_index(drop=True, inplace=True)
            num_order_ask=len(ask_cex.cum)
            num_order_bid=len(bid_cex.cum)
            for j in range(1, num_order_bid):
                 bid_cex.cum[j] = bid_cex.cum[j-1] + bid_cex.volume[j]
            for j in range(1, num_order_ask):
                 ask_cex.cum[j] = ask_cex.cum[j-1] + ask_cex.volume[j]
            y = ask_cex['cum'].values
            ybid = bid_cex['cum'].values
            x = ask_cex['price'].values
            xbid = bid_cex['price'].values
            Vask = y[num_order_ask-1]
            Vbid = ybid[num_order_bid-1]
            Pask = np.sum(x*ask_cex['volume'].values)/np.sum(ask_cex['volume'].values)
            Pbid = np.sum(xbid*bid_cex['volume'].values)/np.sum(bid_cex['volume'].values)
            K0 = np.log(Vask/y[0]-1)/(Pask-x[0])
            K0bid = np.log(Vbid/ybid[0]-1)/(xbid[0]-Pbid)
            B = 2*y[0]*(Pask-x[0])/(Vask-2*y[0])
            Bbid = 2*ybid[0]*(xbid[0]-Pbid)/(Vbid-2*ybid[0])
            def funexp(startexp):
                V = startexp[0]
                P = startexp[1]
                K = startexp[2]
                return np.sum((y-V/((np.exp(-K*(x-P))+1)))**2)
            def funexp_bid(startexp_bid):
                V = startexp_bid[0]
                P = startexp_bid[1]
                K = startexp_bid[2]
                return np.sum((ybid-V/((np.exp(K*(xbid-P))+1)))**2)
            def funfrac_bid(startfrac_bid):
                V = startfrac_bid[0]
                P = startfrac_bid[1]
                A = startfrac_bid[2]
                B = startfrac_bid[3]
                return np.sum((ybid-V/2*((P-xbid+A)/(np.abs(P-xbid)+B)+1))**2)
            def funfrac(startfrac):
                V = startfrac[0]
                P = startfrac[1]
                A = startfrac[2]
                B = startfrac[3]
                return np.sum((y-V/2*((x-P+A)/(np.abs(x-P)+B)+1))**2)
            def funfracas(startfracas):
                V = startfracas[0]
                P = startfracas[1]
                B = startfracas[2]
                return np.sum((y-V/2*((x-P)/(np.abs(x-P)+B)+1))**2)
            def funfracas_bid(startfracas_bid):
                V = startfracas_bid[0]
                P = startfracas_bid[1]
                B = startfracas_bid[2]
                return np.sum((ybid-V/2*((P-xbid)/(np.abs(P-xbid)+B)+1))**2)
            def funexppredict(startexp,x):
                V = startexp[0]
                P = startexp[1]
                K = startexp[2] 
                return V/((np.exp(-K*(x-P))+1))
            def funexppredict_bid(startexp_bid,xbid):
                V = startexp_bid[0]
                P = startexp_bid[1]
                K = startexp_bid[2] 
                return V/((np.exp(K*(xbid-P))+1))
            def funfracpredict(startfrac,x):
                V = startfrac[0]
                P = startfrac[1]
                A = startfrac[2]
                B = startfrac[3]
                return V/2*((x-P+A)/(np.abs(x-P)+B)+1)
            def funfracpredict_bid(startfrac_bid,xbid):
                V = startfrac_bid[0]
                P = startfrac_bid[1]
                A = startfrac_bid[2]
                B = startfrac_bid[3]
                return V/2*((P-xbid+A)/(np.abs(P-xbid)+B)+1)
            def funfracaspredict(startfracas,x):
                V = startfracas[0]
                P = startfracas[1]
                B = startfracas[2]
                return V/2*((x-P)/(np.abs(x-P)+B)+1)
            def funfracaspredict_bid(startfracas_bid,xbid):
                V = startfracas_bid[0]
                P = startfracas_bid[1]
                B = startfracas_bid[2]
                return V/2*((P-xbid)/(np.abs(P-xbid)+B)+1)
            startexp = [Vask, Pask, K0]
            startexp_bid = [Vbid, Pbid, K0bid]
            startfrac = [Vask, Pask, 0, B]
            startfrac_bid = [Vbid, Pbid, 0, Bbid]
            startfracas = [Vask, Pask, B]
            startfracas_bid = [Vbid, Pbid, Bbid]
            resexp = minimize(funexp, startexp)
            pexp = resexp.x
            resfrac = minimize(funfrac, startfrac)
            pfrac = resfrac.x
            resfracas = minimize(funfracas, startfracas)
            pfracas = resfracas.x
            resexp_bid = minimize(funexp_bid, startexp_bid)
            pexp_bid = resexp_bid.x
            resfrac_bid = minimize(funfrac_bid, startfrac_bid)
            pfrac_bid = resfrac_bid.x
            resfracas_bid = minimize(funfracas_bid, startfracas_bid)
            pfracas_bid = resfracas_bid.x
            V = pexp[0]
            P = pexp[1]
            K = pexp[2] 
            rest_exp = np.sum(np.abs(y-V/(np.exp(-K*(x-P))+1))/y)/num_order_ask*100
            V = pexp_bid[0]
            P = pexp_bid[1]
            K = pexp_bid[2] 
            rest_exp_bid = np.sum(np.abs(ybid-V/(np.exp(K*(xbid-P))+1))/ybid)/num_order_bid*100
            V = pfrac_bid[0]
            P = pfrac_bid[1]
            A = pfrac_bid[2]
            B = pfrac_bid[3]
            rest_frac_bid = np.sum(np.abs(ybid-V/2*((P-xbid+A)/(np.abs(P-xbid)+B)+1))/ybid)/num_order_bid*100
            V = pfracas_bid[0]
            P = pfracas_bid[1]
            B = pfracas_bid[2]
            rest_fracas_bid = np.sum(np.abs(ybid-V/2*((P-xbid)/(np.abs(P-xbid)+B)+1))/ybid)/num_order_bid*100
            #
            pexp=np.append(pexp, rest_exp)
            pexp=np.append(pexp, time())
            pfrac=np.append(pfrac, rest_frac)
            pfrac=np.append(pfrac, time())
            pfracas=np.append(pfracas, rest_fracas)
            pfracas=np.append(pfracas, time())
            coeff_exp_file = Exchange[i]+'_exp_ask.csv'
            coeff_frac_file = Exchange[i]+'_frac_ask.csv'
            coeff_fracas_file = Exchange[i]+'_fracas_ask.csv'
            DFpexp = pd.DataFrame(pexp).T
            DFfrac = pd.DataFrame(pfrac).T
            DFfracas = pd.DataFrame(pfracas).T
            DFpexp.to_csv(coeff_exp_file, mode='a', header=None, index=False)
            DFfrac.to_csv(coeff_frac_file, mode='a', header=None, index=False)
            DFfracas.to_csv(coeff_fracas_file, mode='a', header=None, index=False)
            #
            pexp_bid=np.append(pexp_bid, rest_exp_bid)
            pexp_bid=np.append(pexp_bid, time())
            pfrac_bid=np.append(pfrac_bid, rest_frac_bid)
            pfrac_bid=np.append(pfrac_bid, time())
            pfracas_bid=np.append(pfracas_bid, rest_fracas_bid)
            pfracas_bid=np.append(pfracas_bid, time())
            coeff_exp_file_bid = Exchange[i]+'_exp_bid.csv'
            coeff_frac_file_bid = Exchange[i]+'_frac_bid.csv'
            coeff_fracas_file_bid = Exchange[i]+'_fracas_bid.csv'
            DFpexpbid = pd.DataFrame(pexp_bid).T
            DFfracbid = pd.DataFrame(pfrac_bid).T
            DFfracasbid = pd.DataFrame(pfracas_bid).T
            DFpexpbid.to_csv(coeff_exp_file_bid, mode='a', header=None, index=False)
            DFfracbid.to_csv(coeff_frac_file_bid, mode='a', header=None, index=False)
            DFfracasbid.to_csv(coeff_fracas_file_bid, mode='a', header=None, index=False)
            #sleep(5)
    except:
        pass