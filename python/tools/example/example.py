def parse(it):
    result = []
    while True:
        try:
            tk = next(it)
        except StopIteration:
            break

        if tk == '}':
            break
        val = next(it)
        if val == '{':
            result.append((tk,parse(it)))
        else:
            result.append((tk, val))

    return result
with open('C:\\scripts\\python27\\coffe_test\\cifar10_quick.prototxt') as f:
    s = f.read()
prototxt_name = re.findall(r'^name:\s+\"(\w+)\"',s)
#pprint.pprint(prototxt_name)
print(prototxt_name)
