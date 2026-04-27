# This approach is by iteration
def binary_search(n, items):
    left = 0
    right = len(n)
    
    while right > left:
        middle = (left + right) // 2
        if nums[middle] > items:
            right = middle
        elif nums[middle] < items:
            left = middle + 1
        else: 
            return middle
    return None