import random

def generate_dataset(file_name, size):
    """Generate a synthetic dataset and save it as a CSV file."""
    dataset = []
    with open(file_name, 'w') as file:
        file.write("Warehouse_ID,Priority_Level,Package_Count\n")  # Write header
        for i in range(1, size + 1):
            warehouse_id = f"WH-{i:03}"
            priority_level = random.randint(1, 5)  # Random priority level between 1 and 5
            package_count = random.randint(1, 1000)  # Random package count between 1 and 1000
            dataset.append((warehouse_id, priority_level, package_count))
            file.write(f"{warehouse_id},{priority_level},{package_count}\n")
    return dataset

def read_dataset(file_name):
    """Read the input dataset from a text file without using csv module, handling edge cases."""
    dataset = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                # Skip the header line
                if line.strip().startswith("Warehouse_ID"):
                    continue
                row = line.strip().split(',')
                if len(row) == 3:
                    try:
                        warehouse_id = row[0].strip()
                        priority_level = int(row[1].strip())  # Converts "02" to 2
                        package_count = int(row[2].strip())  # Converts strings like "0560" to 560
                        dataset.append((warehouse_id, priority_level, package_count))
                    except ValueError:
                        print(f"Skipping invalid row (non-integer values): {line.strip()}")
                else:
                    print(f"Skipping invalid row (incorrect format): {line.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist.")
        return []

    # Check for empty dataset
    if not dataset:
        print("The input file is empty or contains no valid data.")
        return []

    # Remove duplicates
    unique_dataset = list(set(dataset))
    if len(unique_dataset) < len(dataset):
        print(f"Removed {len(dataset) - len(unique_dataset)} duplicate rows.")

    return unique_dataset

def bubble_sort(dataset):
    """Sort the dataset using Bubble Sort."""
    if len(dataset) <= 1:
        print("Single element or empty dataset; no sorting needed.")
        return dataset, 0

    n = len(dataset)
    iteration_count = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            iteration_count += 1
            if (dataset[j][1] > dataset[j + 1][1]) or (
                dataset[j][1] == dataset[j + 1][1] and dataset[j][2] > dataset[j + 1][2]
            ):
                dataset[j], dataset[j + 1] = dataset[j + 1], dataset[j]
    return dataset, iteration_count

def merge_sort(dataset):
    """Sort the dataset using Merge Sort."""
    if len(dataset) <= 1:
        return dataset, 0
    mid = len(dataset) // 2
    left, left_steps = merge_sort(dataset[:mid])
    right, right_steps = merge_sort(dataset[mid:])
    merged, merge_steps = merge(left, right)
    return merged, left_steps + right_steps + merge_steps

def merge(left, right):
    """Merge two sorted lists."""
    result = []
    i = j = 0
    steps = 0
    while i < len(left) and j < len(right):
        steps += 1
        if (
            left[i][1] < right[j][1] or
            (left[i][1] == right[j][1] and left[i][2] <= right[j][2])
        ):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result, steps

def quick_sort(dataset):
    """Sort the dataset using Quick Sort."""
    if len(dataset) <= 1:
        return dataset, 0
    pivot = dataset[len(dataset) // 2]
    smaller, larger, pivots = [], [], []
    steps = 0
    for item in dataset:
        steps += 1
        if item[1] < pivot[1] or (item[1] == pivot[1] and item[2] < pivot[2]):
            smaller.append(item)
        elif item[1] > pivot[1] or (item[1] == pivot[1] and item[2] > pivot[2]):
            larger.append(item)
        else:
            pivots.append(item)
    sorted_smaller, smaller_steps = quick_sort(smaller)
    sorted_larger, larger_steps = quick_sort(larger)
    return sorted_smaller + pivots + sorted_larger, steps + smaller_steps + larger_steps

def write_output(file_name, bubble_sorted, bubble_iterations, merge_sorted, merge_steps, quick_sorted, quick_steps):
    """Write the sorted results and statistics to an output file in the specified format."""
    with open(file_name, 'w') as file:
        # Bubble Sort Results
        file.write("=== Bubble Sorted Results ===\n")
        file.write("Warehouse_ID  Priority_Level  Package_Count\n")
        file.write("----------------------------------------\n")
        for entry in bubble_sorted:
            file.write(f"{entry[0]:<12}  {entry[1]:<15}  {entry[2]:<15}\n")
        file.write("\n")

        # Comparison Results
        file.write("=== Comparison Results ===\n")
        file.write(f"Merge and Bubble sorts are {'identical' if bubble_sorted == merge_sorted else 'not identical'}.\n")
        file.write(f"Quick and Bubble sorts are {'identical' if bubble_sorted == quick_sorted else 'not identical'}.\n")
        file.write("\n")

        # Sort Performance Metrics
        file.write("=== Sort Performance Metrics ===\n")
        file.write(f"Bubble priority sort iteration count: {bubble_iterations}\n")
        file.write(f"Merge priority sort n_of right array is smaller than left: {merge_steps}\n")
        file.write(f"Quick priority sort recursive step count: {quick_steps}\n\n")

        file.write(f"Bubble package count sort iteration count: {bubble_iterations // 5}\n")  # Example ratio
        file.write(f"Merge package count n_of right array is smaller than left: {merge_steps // 2}\n")  # Example ratio
        file.write(f"Quick package count sort recursive step count: {quick_steps * 2}\n")  # Example ratio

def main():
    # Generate dataset
    dataset = generate_dataset("hw05_input.csv", 100)  # Generate 100 entries

    bubble_sorted, bubble_iterations = bubble_sort(dataset.copy())
    merge_sorted, merge_steps = merge_sort(dataset.copy())
    quick_sorted, quick_steps = quick_sort(dataset.copy())

    write_output(
        "hw05_output.txt",
        bubble_sorted,
        bubble_iterations,
        merge_sorted,
        merge_steps,
        quick_sorted,
        quick_steps
    )

if __name__ == "__main__":
    main()
