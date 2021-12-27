import datetime

def time_in_range(start, end, current):
    return start <= current <= end

start = datetime.time(21, 56, 0)
end = datetime.time(22, 0, 0)
current = datetime.datetime.now().time()

print(time_in_range(start, end, current))