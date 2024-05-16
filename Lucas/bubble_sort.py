def bubble_sort(nums):
    list_len = len(nums)
    sorted = False

    while not sorted:
        sorted = True
        for i in range(0, list_len - 1):
            if nums[i] > nums[i+1]:
                sorted = False
                nums[i], nums[i+1] = nums[i+1], nums[i]

    return nums
    
nums = [3,2,5,2,5,6,62,2,6,7,7,3,2,22,6]
print(bubble_sort(nums))