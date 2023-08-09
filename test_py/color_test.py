# import os
e = '\033[0m'
color_str = '\033[0m'
color_str2 = '\033[10m'
color_str3 = '\033[100m'
color_list = []
for i in range(10):
    trans_color_str = color_str[0:2] + str(i) + color_str[3:]
    color_list.append(trans_color_str)
for i in range(10,100):
    s = int(i % 10)
    d = int(i / 10)
    trans_color_str = color_str2[0:2] + str(d) + str(s) + color_str2[4:]
    color_list.append(trans_color_str)
for i in range(10):
    trans_color_str = color_str3[0:4] + str(i) + 'm'
    color_list.append(trans_color_str)
print(color_list)
i = 0
# os.system("cls")
for lst in color_list:
    i += 1
    print(lst+'color'+lst[2:4]+e, end='\t')
    if i % 10 == 0:
        print('')


# print('----------------')
# m = '\033[38;2;'
# p = 0
# i = 0
# j = 0
# k = 0
# for i in range(256):
#     for j in range(256):
#         for k in range(256):
#             p +=1
#             op = m+str(i)+';'+str(j)+';'+str(k)+'m'
#             print(op+f'color{i};{j};{k} \033[m',end='')
#             if p % 10 == 0:
#                 print('')

