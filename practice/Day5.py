import random

checkout = ''

for i in range(4):
    current = random.randrange(0, 4)
    if i != current:
        temp = chr(random.randint(65, 90))
    else:
        temp = random.randint(0, 9)
    checkout += str(temp)

print(checkout)
