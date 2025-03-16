
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

def selection_sort(lst: list):
    for i in range(len(lst) - 1):
        min_index = i

        for j in range(i + 1, len(lst)): # start from the next index
            if lst[j] < lst[min_index]:
                min_index = j

        lst[i], lst[min_index] = lst[min_index], lst[i] # switch positions with the minimum and current
    return lst
