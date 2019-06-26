# Estimate Rf and Rm using Beta and Exp_ret

import numpy as np
from sympy import *
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def rf_rm_estimation(beta_list, all_exp_ret_list):
    rf_list = []
    rm_list = []

    # All stocks
    stock_num = len(all_exp_ret_list)
    for i in range(stock_num):
        for j in range(i+1, stock_num, 1):
            x = Symbol('x')
            y = Symbol('y')

            b1 = beta_list[i]
            b2 = beta_list[j]
            e1 = all_exp_ret_list[i]
            e2 = all_exp_ret_list[j]

            ans = solve([(1-b1)*x+b1*y-e1, (1-b2)*x+b2*y-e2], [x, y])

            rf_list.append(ans[x])
            rm_list.append(ans[y])
            a = 1

    rf_list = np.array(rf_list)
    rm_list = np.array(rm_list)

    rf_medium = np.median(rf_list)
    rm_medium = np.median(rm_list)

    rf_mean = np.mean(rf_list)
    rm_mean = np.mean(rm_list)

    print('*** method 1 (SymPy) ***')
    print('rf_mean: ' + str(rf_mean) + '\nrm_mean: ' + str(rm_mean) + '\nrf_medium: ' + str(
        rf_medium) + '\nrm_medium: ' + str(rm_medium) + '\n' + '-'*15)

    return rf_mean, rm_mean, rf_medium, rm_medium


def rf_rm_estimation_ml(beta_list, all_exp_ret_list):
    x = np.array(beta_list)
    x = x.reshape(x.shape[0], 1)
    y = np.array(all_exp_ret_list)

    model = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=True)
    model.fit(x, y)

    rf = model.intercept_
    rm = model.coef_[0] + rf

    predicted = model.predict(x)
    plt.scatter(x, y, marker='+')
    plt.plot(x, predicted, c='r', linestyle=':')
    plt.xlabel("Beta")
    plt.ylabel("Exp_ret")
    plt.show()

    print('*** method 2 (ML) ***')
    print('rf: ' + str(rf) + 'rm: ' + str(rm) + '\n' + '-'*15)

    return rf, rm


if __name__ == '__main__':
    beta_list = [1.2053291601444025, 1.3501080147885933, 0.6364557608544632, 0.5327826823786834]
    all_exp_ret_list = [0.15469103380879656, 0.3760748002582879, 0.17146566309465605, 0.07901932357627328]
    rf, rm = rf_rm_estimation(beta_list, all_exp_ret_list)
    a = 1

