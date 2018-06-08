import datetime

with open('input.in') as ii:
    tm = datetime.datetime.strptime(str(ii.readline()), '%Y-%m-%d %H:%M:%S.%f')
    #tm = ii.readline()
    print(type(tm))
    print(tm)