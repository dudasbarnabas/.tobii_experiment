import random

blokk = []
isi = ["r", "l"]

rr = 0
rl = 0
lr = 0
ll = 0

list = []
first = random.choice(isi)
list.append(first)
blokk.append(first)
second = random.choice(isi)

out = 8
max_pair = 2

while len(list) < out:
    while list.count("r") < (out/2) and list.count("l") < out/2:
        if first == "r" and second == "r":
            if rr < max_pair:
                rr += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
        elif first == "r" and second == "l":
            if rl < max_pair:
                rl += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
        elif first == "l" and second == "r":
            if lr < max_pair:
                lr += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
        elif first == "l" and second == "l":
            if ll < max_pair:
                ll += 1
                list.append(second)
                first = second
                second = random.choice(isi)
            else:
                second = random.choice(isi)
    else:
        if list.count("r") == (out/2):
            for i in range(out - len(list)):
                list.append("l")
        elif list.count("l") == (out/2):
            for i in range(out - len(list)):
                list.append("r")
    print(list)
print()


rr = rl = lr = ll = 0

# go through consecutive pairs
for a, b in zip(list, list[1:]):
    if a == "r" and b == "r":
        rr += 1
    elif a == "r" and b == "l":
        rl += 1
    elif a == "l" and b == "r":
        lr += 1
    elif a == "l" and b == "l":
        ll += 1

print(rr, rl, lr, ll)

def is_valid_order(order):
    for i, n in enumerate(order):
        if (i < 4 and n >= 6) or (i >= 4 and n <= 6):
            return False
    return True

def generate_numbers():
    while True:
        sum_num = []
        final = []
        for i in range(4):
            sum_num.append(round(random.uniform(2,6),1))
            sum_num.append(round(random.uniform(6,10),1))
        resid = 48-(sum(sum_num))
        plusmin = divmod((resid*10),8)[0]/10
        
        for i in sum_num:
            rounded = round((i+plusmin),1)
            final.append(rounded)
        rest = round(48-sum(final),1)
        order = sorted(final)
        order[0] = round(order[0]+rest, 1)
        order = sorted(order)

        if is_valid_order(order):
            return order  # Return the valid order if it meets the conditions
        else:
            continue 

    
numbers = generate_numbers()

isi_list =[]
z = 0
k = 4
for i, n in enumerate(list):
    if n == "r":
        isi_list[i] = numbers[z]
        z += 1
    else:
        isi_list[i] = numbers[(z+k)]
        k += 1
print(isi_list)