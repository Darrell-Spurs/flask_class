ind=0
a=[1,2,3,5,4,5,6,7,5,1,4]

for i in range(a.count(5)+1):
    temp=""
    while ind!=len(a) and a[ind]!=5:
        temp+=(str(a[ind])+" ")
        ind+=1
    else:
        ind+=1
        print(temp)
        continue