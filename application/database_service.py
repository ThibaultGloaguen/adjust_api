from sqlalchemy import desc, asc, func
from datetime import datetime
from application.metrics_model import Metrics
from application import db

SUM = 'sum'
OS = 'os'
COUNTRY = 'country'
CHANNEL = 'channel'
DATE = 'date'
CPI = 'cpi'
REVENUE = 'revenue'
SPEND = 'spend'
INSTALLS = 'installs'
CLICKS = 'clicks'
IMPRESSIONS = 'impressions'


def get_result(fields, operation, date_from, date_to, group_by, sort_by, direction, channel, os, country):
    selected_fields_tmp = select_fields(fields)

    if operation and operation == SUM:
        selected_fields = [func.sum(field) for field in selected_fields_tmp]
    else:
        selected_fields = selected_fields_tmp

    selected_group_by_fields = select_group_by_fields(group_by)

    if selected_group_by_fields:
        # if there is group by fields then we add thoses fields to the SELECT fields
        selected_fields.extend(selected_group_by_fields)

    query = db.session.query(*selected_fields)

    if selected_group_by_fields:
        query = query.group_by(*selected_group_by_fields)

    if date_from:
        query = query.filter(Metrics.date >= datetime.strptime(date_from, '%d.%m.%Y'))
    if date_to:
        query = query.filter(Metrics.date <= datetime.strptime(date_to, '%d.%m.%Y'))

    if channel:
        value = list(set(channel.split(',')))
        query = query.filter(Metrics.channel.in_(value))
    if os:
        value = list(set(os.split(',')))
        query = query.filter(Metrics.os.in_(value))
    if country:
        value = list(set(country.split(',')))
        query = query.filter(Metrics.country.in_(value))

    sort_by_field = get_sort_by_field(sort_by)
    if sort_by_field:
        direction_func = get_direction_order_function(direction)
        query = query.order_by(direction_func(sort_by_field))

    results = []
    label_fields = get_label_fields(selected_fields)
    for res in query.all():
        results.append(dict(zip(label_fields, list(res))))
    return {'results': results}


def get_label_fields(selected_fields):
    return [str(field_label).replace('Metrics.', '').replace('(', '_').replace(')', '').lower() for field_label
            in
            selected_fields]


def select_fields(fields):
    if not fields:
        return [Metrics.impressions, Metrics.clicks, Metrics.installs, Metrics.spend, Metrics.revenue]
    selected_fields = []
    missing_fields = []
    for field in list(set(fields.split(','))):
        if field == IMPRESSIONS:
            selected_fields.append(Metrics.impressions)
        elif field == CLICKS:
            selected_fields.append(Metrics.clicks)
        elif field == INSTALLS:
            selected_fields.append(Metrics.installs)
        elif field == SPEND:
            selected_fields.append(Metrics.spend)
        elif field == REVENUE:
            selected_fields.append(Metrics.revenue)
        elif field == CPI:
            selected_fields.append(Metrics.cpi)
        else:
            missing_fields.append(field)
    if len(missing_fields) > 0:
        raise ValueError('Cannot select the fields %s' % ', '.join(missing_fields))
    return selected_fields


def select_group_by_fields(fields):
    if not fields:
        return None
    missing_fields = []
    selected_fields = []
    for field in list(set(fields.split(','))):
        if field == DATE:
            selected_fields.append(Metrics.date)
        elif field == CHANNEL:
            selected_fields.append(Metrics.channel)
        elif field == COUNTRY:
            selected_fields.append(Metrics.country)
        elif field == OS:
            selected_fields.append(Metrics.os)
        else:
            missing_fields.append(field)
    if len(missing_fields) > 0:
        raise ValueError('Cannot group by with the fields %s' % ', '.join(missing_fields))
    return selected_fields


def get_sort_by_field(sort_by):
    if not sort_by:
        return None
    if sort_by == DATE:
        return Metrics.date
    elif sort_by == CHANNEL:
        return Metrics.channel
    elif sort_by == COUNTRY:
        return Metrics.country
    elif sort_by == OS:
        return Metrics.os
    elif sort_by == REVENUE:
        return Metrics.revenue
    elif sort_by == SPEND:
        return Metrics.spend
    elif sort_by == INSTALLS:
        return Metrics.installs
    elif sort_by == CLICKS:
        return Metrics.clicks
    elif sort_by == IMPRESSIONS:
        return Metrics.impressions
    elif sort_by == CPI:
        return Metrics.cpi
    else:
        raise ValueError('%s in not a known field ' % sort_by)


def get_direction_order_function(direction):
    if direction == 'desc':
        direction_func = desc
    else:
        direction_func = asc
    return direction_func
