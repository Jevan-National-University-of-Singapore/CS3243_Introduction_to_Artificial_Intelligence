test = {1: "gyue",
        2: "rjiowe",
        3: "hjruioawehu",
        4: "jfeio"}

sort_orders = sorted(test.items(), key=lambda x:x[1])

print(type(sort_orders))
