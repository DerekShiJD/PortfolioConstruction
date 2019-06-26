import datetime


def generate_period(period_len=36, freq='month', start_date=None, end_date=None):

    if start_date is None and end_date is None:
        period_len += 1     # add one more period
        now_time = datetime.datetime.now()
        time2 = now_time.strftime('%Y-%m-%d')
        if freq == 'week':
            result_date = now_time + datetime.timedelta(weeks=-1 * period_len)
            time1 = result_date.strftime('%Y-%m-%d')
        elif freq == 'month':
            result_date = now_time + datetime.timedelta(days=-1 * int(30.5 * period_len))
            time1 = result_date.strftime('%Y-%m-%d')
        else:
            time1 = 'error'
            time2 = 'error'
            return time1, time2

    elif start_date is not None and end_date is not None:
        # both start date and end date are given
        start_date = datetime.date(start_date[0], start_date[1], start_date[2])
        end_date = datetime.date(end_date[0], end_date[1], end_date[2])
        time2 = end_date.strftime('%Y-%m-%d')

        if freq == 'week':
            start_date = start_date - datetime.timedelta(weeks=1)
            time1 = start_date.strftime('%Y-%m-%d')
        elif freq == 'month':
            start_date = start_date - datetime.timedelta(days=30.5)
            time1 = start_date.strftime('%Y-%m-%d')
        else:
            time1 = 'error'
            return time1, time2

    elif start_date is not None:
        # start date is given
        period_len += 1
        start_date = datetime.date(start_date[0], start_date[1], start_date[2])

        if freq == 'week':
            start_date = start_date - datetime.timedelta(weeks=1)
            time1 = start_date.strftime('%Y-%m-%d')
            end_date = start_date + datetime.timedelta(weeks=period_len)
            time2 = end_date.strftime('%Y-%m-%d')
        elif freq == 'month':
            start_date = start_date - datetime.timedelta(days=30.5)
            time1 = start_date.strftime('%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=30.5 * period_len)
            time2 = end_date.strftime('%Y-%m-%d')
        else:
            time1 = 'error'
            time2 = 'error'
            return time1, time2

    elif end_date is not None:
        # end date is given
        period_len += 1
        end_date = datetime.date(end_date[0], end_date[1], end_date[2])
        time2 = end_date.strftime('%Y-%m-%d')
        if freq == 'week':
            start_date = end_date - datetime.timedelta(weeks=period_len)
            time1 = start_date.strftime('%Y-%m-%d')
        elif freq == 'month':
            start_date = end_date - datetime.timedelta(days=30.5*period_len)
            time1 = start_date.strftime('%Y-%m-%d')
        else:
            time1 = 'error'
            time2 = 'error'
            return time1, time2

    today = datetime.date.today()
    '''
        if start_date > today or end_date > today:
        time1 = 'error'
        time2 = 'error'
    '''

    return time1, time2


if __name__ == '__main__':
    generate_period(period_len=36, freq='week', end_date=[2018, 1, 1])
