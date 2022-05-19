#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# O(N)
class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        nums = set(numbers)
        for i in range(len(numbers)):
            if (target - numbers[i] in nums):
                a = numbers[i]
                b = target - numbers[i] 
        m = len(numbers) - numbers[::-1].index(b) - 1
        n = numbers.index(a)
        if n != m:
            return (n, m)
        else:
            for i in range(len(numbers)):
                if (target - numbers[i] in nums):
                    a = numbers[i]
                    b = target - numbers[i] 
                    break
            return (numbers.index(a), len(numbers) - numbers[::-1].index(b) - 1)

