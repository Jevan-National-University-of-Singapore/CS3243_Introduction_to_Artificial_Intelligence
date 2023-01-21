def recursion(n):
    recursion.counter += 1
    print(recursion.counter)
    if n > 0:
        for i in range(n):
            return recursion(i)

recursion.counter = 0
print(recursion(5))