from sqlalchemy import desc, asc, func
from datetime import datetime
from application.metrics_model import Metrics
from application import db


def get_result(fields, operation, date_from, date_to, group_by, sort_by, direction, channel, os, country):
    selected_fields_tmp = select_fields(fields)

    if operation and operation == 'sum':
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
    label_fields = [str(field_label).replace('Metrics.', '').replace('(', '_').replace(')', '').lower() for field_label
                    in
                    selected_fields]
    for res in query.all():
        results.append(dict(zip(label_fields, list(res))))
    return {'results': results}


def select_fields(fields):
    if not fields:
        return [Metrics.impressions, Metrics.clicks, Metrics.installs, Metrics.spend, Metrics.revenue]
    selected_fields = []
    missing_fields = []
    for field in list(set(fields.split(','))):
        if field == 'impressions':
            selected_fields.append(Metrics.impressions)
        elif field == 'clicks':
            selected_fields.append(Metrics.clicks)
        elif field == 'installs':
            selected_fields.append(Metrics.installs)
        elif field == 'spend':
            selected_fields.append(Metrics.spend)
        elif field == 'revenue':
            selected_fields.append(Metrics.revenue)
        elif field == 'cpi':
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
        if field == 'date':
            selected_fields.append(Metrics.date)
        elif field == 'channel':
            selected_fields.append(Metrics.channel)
        elif field == 'country':
            selected_fields.append(Metrics.country)
        elif field == 'os':
            selected_fields.append(Metrics.os)
        else:
            missing_fields.append(field)
    if len(missing_fields) > 0:
        raise ValueError('Cannot group by with the fields %s' % ', '.join(missing_fields))
    return selected_fields


def get_sort_by_field(sort_by):
    if not sort_by:
        return None
    if sort_by == 'date':
        return Metrics.date
    elif sort_by == 'channel':
        return Metrics.channel
    elif sort_by == 'country':
        return Metrics.country
    elif sort_by == 'os':
        return Metrics.os
    elif sort_by == 'revenue':
        return Metrics.revenue
    elif sort_by == 'spend':
        return Metrics.spend
    elif sort_by == 'installs':
        return Metrics.installs
    elif sort_by == 'clicks':
        return Metrics.clicks
    elif sort_by == 'impressions':
        return Metrics.impressions
    elif sort_by == 'cpi':
        return Metrics.cpi
    else:
        raise ValueError('%s in not a known field ' % sort_by)


def get_direction_order_function(direction):
    if direction == 'desc':
        direction_func = desc
    else:
        direction_func = asc
    return direction_func
