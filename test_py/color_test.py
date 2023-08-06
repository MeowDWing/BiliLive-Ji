e = '\033[0m'
color_str = '\033[0m'
color_str2 = '\033[10m'
color_list = []
for i in range(10):
    trans_color_str = color_str[0:2] + str(i) + color_str[3:]
    color_list.append(trans_color_str)
for i in range(10,100):
    s = int(i % 10)
    d = int(i / 10)
    trans_color_str = color_str2[0:2] + str(d) + str(s) + color_str2[4:]
    color_list.append(trans_color_str)
print(color_list)
i = 0
for lst in color_list:
    i += 1
    print(lst+'color'+lst[2:4]+e, end='\t')
    if i % 10 == 0:
        print('')
