import datetime

DELAY_DAYS = 0


def convert_date_to_datetime_with_delta(dt, delta):
    return convert_date_to_datetime(dt) + datetime.timedelta(hours=delta)
#     dt = convert_date_to_datetime(dt)
#     return datetime.datetime.strptime(dt, '%Y-%m-%d') + datetime.timedelta(hours=delta)

def convert_date_to_datetime(dt):
    return datetime.datetime.strptime(dt, '%Y-%m-%d')
#     return dt.strftime('%Y-%m-%d')

def _get_date_from_timestamp(request, start_date_utc, end_date_utc):

    today = (datetime.datetime.utcnow() - datetime.timedelta(days=DELAY_DAYS)).replace(hour=0,minute=0,second=0)

    if end_date_utc:
        end_date_float = int(end_date_utc) / 1000.0
        end_date = datetime.datetime.fromtimestamp(end_date_float)
        request.session['end_date'] = end_date_float
    else:
        sess_end_date = request.session.get('end_date')
        if sess_end_date:
            end_date = datetime.datetime.fromtimestamp(int(sess_end_date))
        else:
            timestamp = int(today.strftime("%s"))
            end_date = datetime.datetime.fromtimestamp(int(timestamp))

    if start_date_utc:
        start_date_float = int(start_date_utc) / 1000.0
        start_date = datetime.datetime.fromtimestamp(start_date_float)
        request.session['start_date'] = start_date_float

    else:
        sess_start_date = request.session.get('start_date')
        if sess_start_date:
            start_date = datetime.datetime.fromtimestamp(int(sess_start_date))
        else:
            start_date = end_date - datetime.timedelta(days=30)

    return start_date, end_date