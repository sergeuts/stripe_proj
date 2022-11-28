def get_row_value(row, fields):
    res = {}
    # for f in fields:
    #     value = row.__getattribute__(f)
    #     if '.models.' in str(type(value)):
    #         value = value.name
    #     res[f] = value

    for f in fields:
        value = row
        for f in fields:
            ff = f.split('.')
            nesting = len(ff)
            value = row
            for i in range(nesting):
                value = value.__getattribute__(ff[i])
            if '.models.' in str(type(value)):
                value = value.name
            res[f.replace('.', '_') if '.' in f else f] = value
    return res


def get_table_values(table, filter=None, fields=None):
    if filter:
        rr = table.objects.filter(**filter)
    else:
        rr = table.objects.all()
    return [get_row_value(row, fields) for row in rr]