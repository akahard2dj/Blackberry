
def row2dict(row, fields: set=set()):
    d = {}
    for column in row.__table__.columns:
        if column.name in fields:
            d[column.name] = str(getattr(row, column.name))
    return d


def rows2dict(rows, fields: set=set()):
    arr = []
    for row in rows:
        arr.append(row2dict(row, fields))
    return arr


class ResponseWrapper:
    @staticmethod
    def ok(message: str='success', data: object=None):
        result = dict()
        result['message'] = message
        result['data'] = data
        return result
