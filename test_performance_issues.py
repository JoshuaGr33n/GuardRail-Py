"""
Test file with intentional performance issues for GuardRail-Py to detect.

This file contains common performance anti-patterns that junior developers
often write. As a Lead Engineer, I've mentored developers to fix these issues.
"""

# ============================================================================
# ISSUE 1: O(n²) Nested Loops
# ============================================================================

def find_duplicates_naive(items):
    """Naive O(n²) approach to find duplicates."""
    duplicates = []
    
    # NESTED LOOP: O(n²) complexity
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                duplicates.append((i, j))
    
    return duplicates


def matrix_multiplication_naive(a, b):
    """Naive matrix multiplication with triple nested loops."""
    result = []
    
    # TRIPLE NESTED: O(n³) complexity!
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            sum_val = 0
            for k in range(len(b)):
                sum_val += a[i][k] * b[k][j]
            row.append(sum_val)
        result.append(row)
    
    return result


# ============================================================================
# ISSUE 2: Inefficient String Operations
# ============================================================================

def build_csv_string(data):
    """Build CSV string inefficiently."""
    csv = "id,name,value\\n"  # Header
    
    # STRING CONCATENATION IN LOOP: O(n²) for strings
    for row in data:
        csv += f"{row['id']},{row['name']},{row['value']}\\n"
    
    return csv


def create_html_list(items):
    """Create HTML list inefficiently."""
    html = "<ul>\\n"
    
    for item in items:
        # More string concatenation in loop
        html += f"  <li>{item}</li>\\n"
    
    html += "</ul>"
    return html


# ============================================================================
# ISSUE 3: Inefficient List Operations
# ============================================================================

def filter_admins(users):
    """Filter admin users inefficiently."""
    admins = []
    
    # LIST.APPEND() IN LOOP: Could use list comprehension
    for user in users:
        if user.get('role') == 'admin':
            admins.append(user)
    
    return admins


def flatten_list_naive(list_of_lists):
    """Flatten list inefficiently."""
    flat = []
    
    # NESTED LOOP WITH APPEND
    for sublist in list_of_lists:
        for item in sublist:
            flat.append(item)
    
    return flat


# ============================================================================
# ISSUE 4: Unnecessary Repeated Computations
# ============================================================================

def calculate_statistics(numbers):
    """Calculate statistics with repeated computations."""
    stats = {}
    
    # LENGTH COMPUTED MULTIPLE TIMES
    stats['count'] = len(numbers)
    
    total = 0
    for num in numbers:
        total += num
    stats['mean'] = total / len(numbers)  # len() called again
    
    # Could pre-compute len_numbers = len(numbers)
    return stats


# ============================================================================
# OPTIMIZED VERSIONS (For comparison)
# ============================================================================

def find_duplicates_optimized(items):
    """Optimized O(n) approach using dictionary."""
    seen = {}
    duplicates = []
    
    for i, item in enumerate(items):
        if item in seen:
            duplicates.append((seen[item], i))
        else:
            seen[item] = i
    
    return duplicates


def build_csv_string_optimized(data):
    """Build CSV string efficiently with join."""
    header = "id,name,value"
    rows = []
    
    for row in data:
        rows.append(f"{row['id']},{row['name']},{row['value']}")
    
    return header + "\\n" + "\\n".join(rows)


def filter_admins_optimized(users):
    """Filter admin users with list comprehension."""
    return [user for user in users if user.get('role') == 'admin']


# ============================================================================
# MAIN: Test the functions
# ============================================================================

if __name__ == "__main__":
    print("Testing performance-issue functions...")
    
    # Test data
    test_items = [1, 2, 3, 1, 4, 2]
    test_data = [
        {"id": 1, "name": "Alice", "value": 100},
        {"id": 2, "name": "Bob", "value": 200},
    ]
    test_users = [
        {"name": "Alice", "role": "admin"},
        {"name": "Bob", "role": "user"},
        {"name": "Charlie", "role": "admin"},
    ]
    
    print(f"Duplicates (naive): {find_duplicates_naive(test_items)}")
    print(f"Duplicates (optimized): {find_duplicates_optimized(test_items)}")
    print(f"Admins (naive): {filter_admins(test_users)}")
    print(f"Admins (optimized): {filter_admins_optimized(test_users)}")
    
    print("\\nThis file contains intentional performance issues for testing.")
    print("GuardRail-Py should detect all the marked issues above.")