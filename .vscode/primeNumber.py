minNum=int(input("Enter the minimum number: "))
maxNum=int(input("Enter the maximum number: "))
for num in range(minNum,maxNum+1):  
   if num > 1:  
       for i in range(2,num):  
           if (num % i) == 0:  
               break  
       else:  
           print(num)