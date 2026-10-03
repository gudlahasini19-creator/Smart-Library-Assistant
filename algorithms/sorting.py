"""
Algorithm: Merge Sort
Time Complexity: O(n log n) - Best, Average, and Worst case
Space Complexity: O(n) - Auxiliary space for merging

Purpose:
A classic Divide-and-Conquer sorting algorithm used to rank book recommendations
by composite relationship score, or alphabetically by title/author/category.
"""

def merge_sort(items, key_func=lambda x: x, reverse=False):
    """
    Sorts a list using the manual Merge Sort algorithm.
    
    Parameters:
        items (list): The list of items to sort.
        key_func (callable): Function to extract the comparison key from each element.
        reverse (bool): If True, sorts in descending order (e.g., highest recommendation score first).
        
    Returns:
        list: A new sorted list.
    """
    # Base Case: An array of 0 or 1 element is already sorted
    if len(items) <= 1:
        return list(items)

    # 1. DIVIDE: Find the midpoint and split into two halves
    mid = len(items) // 2
    left_half = merge_sort(items[:mid], key_func=key_func, reverse=reverse)
    right_half = merge_sort(items[mid:], key_func=key_func, reverse=reverse)

    # 2. CONQUER & COMBINE: Merge the two sorted halves
    return _merge(left_half, right_half, key_func=key_func, reverse=reverse)


def _merge(left, right, key_func, reverse):
    """
    Helper function to merge two sorted lists into a single sorted list.
    Time Complexity of merge step: O(n)
    """
    merged = []
    i = 0  # pointer for left list
    j = 0  # pointer for right list

    while i < len(left) and j < len(right):
        left_val = key_func(left[i])
        right_val = key_func(right[j])

        # Compare based on order (ascending vs descending)
        if reverse:
            # Descending order (e.g., higher score first)
            if left_val >= right_val:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        else:
            # Ascending order (e.g., alphabetical A-Z)
            if left_val <= right_val:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

    # Append any remaining elements from left or right halves
    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def sort_books_by(books, criteria="relevance"):
    """
    Sorts a list of book dictionaries based on user-chosen criteria using Merge Sort.
    
    Supported Criteria:
        - 'relevance' (Descending recommendation score)
        - 'title' (Alphabetical A-Z)
        - 'author' (Alphabetical A-Z)
        - 'category' (Alphabetical A-Z)
        - 'year' (Newest first)
    """
    if criteria == "title":
        return merge_sort(books, key_func=lambda b: b["title"].lower(), reverse=False)
    elif criteria == "author":
        return merge_sort(books, key_func=lambda b: b["author"].lower(), reverse=False)
    elif criteria == "category":
        return merge_sort(books, key_func=lambda b: b["category"].lower(), reverse=False)
    elif criteria == "year":
        return merge_sort(books, key_func=lambda b: b.get("year", 0), reverse=True)
    else:
        # Default: relevance score descending
        return merge_sort(books, key_func=lambda b: b.get("score", 0.0), reverse=True)
