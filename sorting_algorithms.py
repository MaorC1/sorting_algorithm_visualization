
# O(n^2)
def bubble_sort(lst: list, ascending=True):
    for i in range(len(lst) - 1):
        swapped = False
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j] # swap num1 and num2
                swapped = True
        if not swapped: # no more swapping needed, list is ordered
            return lst

print(bubble_sort([3, 2, 88, 4, 2, 5, 9], False))