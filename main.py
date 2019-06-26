from functions import generate_target_company_id
from functions import generate_period
from functions import download_data
from functions import expected_return
from functions import regression
from functions import covariance_matrix
from functions import estimate_rf_rm
from functions import download_treasury
from functions import portfolio_construction
import sys
import numpy as np


if __name__ == '__main__':
    print('\n\n' + '*'*65)
    print('Portfolio Construction Using Web Crawler and Machine Learning')
    print('*' * 65, '\n\nUser Input')
    # freq = 'week'
    # period_len = 52
    freq = input('Frequency (week/month): ')
    period_len = int(input('Time period: '))
    stock_input = input('Watch list: ')

    print()

    SP500_exp_ret_list = []     # expected rate of return of S&P500 index
    all_exp_ret_list = []       # expected rate of return of all stocks
    beta_list = []              # beta for each stock
    cov_matrix = np.array([])             # covariance matrix between each stock
    company_list = []

    # Step 1: generate target company list
    # company_list = generate_target_company_id.generate_id(1, 5)        # 0: main mode, 1: FAANG, else: test mode
    # company_list = ['FB', 'AAPL', 'AMZN', 'GOOGL']       # FB AAPL AMZN NFLX GOOGL

    temp_name = ''

    for cha in stock_input:
        if cha != ' ':
            temp_name += cha
        else:
            company_list.append(temp_name)
            temp_name = ''
    if temp_name != '':
        company_list.append(temp_name)

    # Step 2: generate period
    time1, time2 = generate_period.generate_period(period_len, freq)

    print('Query Confirmation')
    print('Time period: ' + time1 + ' to ' + time2)
    print('Stocks: ', end='')
    for name in company_list:
        print(name, end='\t')
    print('\n\n' + '='*50 + '\n')


    if time1 == 'error':
        sys.exit('Error: Generate_period')

    # Step 3: download data from Yahoo Finance and USDT
    SP500data, SP500date, all_data, all_date, flag_download = download_data.downloaddata(company_list, time1, time2, freq)
    t_all_data, t_all_date, t_one_rate = download_treasury.download_treasury_yield()

    if not flag_download:
        sys.exit('Error: Download_data')
    else:
        # Step 4: machine learning => expected rate of return (expected_return.py)
        SP500_exp_ret_list, all_exp_ret_list = expected_return.linear_regression(SP500data, all_data, freq, company_list)

        # Step 5: regression => Beta (regression.py)
        beta_list = regression.calculate_beta(SP500data, all_data)

        # Step 6: cov matrix (covariance_matrix.py)
        cov_matrix = covariance_matrix.calculate_cov_matrix(SP500data, all_data)         # np.array

        # Step 7: Estimate Rf, Rm (input: exp_ret, beta; output: averaged Rf and Rm)
        rf = t_one_rate
        rm = SP500_exp_ret_list[0] * 100
        print('Risk free rate: ', round(rf, 2), '%')
        print('Expected market return (S&P500): ', round(rm, 2), '%\n\n\n\nPortfolio Construction:')

        '''
        rf_mean, rm_mean, rf_medium, rm_medium = estimate_rf_rm.rf_rm_estimation(beta_list, all_exp_ret_list)
        rf_ml, rm_ml = estimate_rf_rm.rf_rm_estimation_ml(beta_list, all_exp_ret_list)
        '''
        # rm, rf, beta
        # exp_ret = rf + beta * (rm - rf)
        # cov_mat

        # Step 8: Portfolio construction
        sharpe_max_weights, sd_min_weights = portfolio_construction.port_cons(rf, rm, cov_matrix, beta_list, company_list)
        print('Completed\n\n\n\n')
        a = 1





