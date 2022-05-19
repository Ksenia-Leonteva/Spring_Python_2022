#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# O(NlogN)
class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        nums = []
        for i in range(len(numbers)):
            nums.append(numbers[i])
            
        numbers.sort()  


        for i in range(len(numbers)):
            m = 0
            a = 0
            b = len(numbers)
            f = 0
            c = target - numbers[i]
            
            while (a <= b):
                m = (a + b) // 2
                if c < numbers[m]:
                    b = m - 1
                if c >= numbers[m]:
                    a = m + 1
                if (c == numbers[m]) and (m != i):
                    j = m
                    f = -2
                    break
                if m >= len(numbers) - 1:
                    f = -1
                    break

            if f == -2:
                a = numbers[i]
                b = numbers[j]
                break
                
        c = nums.index(a)
        nums = nums[::-1]
        d = len(nums) - nums.index(b) - 1
        if c > d:
            return(d, c)
        if c < d:
            return(c, d)

