from numpy import random

ct =0
rndG = random
for i in range(100):
    value = rndG.random()
    print(value)
    if value < float(0/10):
        ct += 1
        print("Saturated")
    else:
        print("Ok")

print(ct)