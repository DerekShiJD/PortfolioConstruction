import numpy as np
import pprint

def generate_id(mode, num):

    black_list = ['FLR', 'AVGO', 'VAR']

    if mode == 0:
        # main mode
        all_companies = np.load('functions/SP500/SP500Companies.npy')
        all_list = all_companies[:, 0]
        np.random.shuffle(all_list)
        all_list = all_list[0:num]
        company_list = all_list.tolist()

        for name in black_list:
            if name in company_list:
                company_list.remove(name)

        return company_list
    elif mode == 1:
        company_list = ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
        return company_list
    else:
        # test mode
        company_list = ['MMM', 'ADBE', 'BDX', 'CVX']
        return company_list


if __name__ == '__main__':
    black_list = ['FLR', 'AVGO']
    all_companies = np.load('SP500/SP500Companies.npy')
    all_list = all_companies[:, 0]
    np.random.shuffle(all_list)
    all_list = all_list[0:10]
    # company_list = all_list.tolist()
    company_list = ['MMM', 'AAA', 'FLR', 'AVGO']

    for name in black_list:
        if name in company_list:
            company_list.remove(name)

    a = 1

