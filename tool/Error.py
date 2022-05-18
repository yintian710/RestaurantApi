class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class SqlColumnError(Exception):
    def __init__(self, column):
        self.message = f'查询表中无{column}列'


if __name__ == '__main__':
    pass
