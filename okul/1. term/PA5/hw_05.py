import os
# Custom pseudorandom number generator with a random initial seed
class PRNG:
    def __init__(self, seed=None):
        # Use a truly random seed if no seed is provided
        if seed is None:
            seed = int.from_bytes(os.urandom(4), 'big')  # Generate a random 32-bit integer
        self.state = seed

    def randint(self, low, high):
        # Simple linear congruential generator (LCG)
        self.state = (1103515245 * self.state + 12345) % (2**31)
        return low + (self.state % (high - low + 1))

# Generate logistics dataset
def generate_logistics_dataset(num_warehouses=100, max_packages=1000, seed=None):
    """Generates a logistics dataset with a random or specified seed."""
    prng = PRNG(seed)  # Initialize PRNG with the seed or a random one
    data = []
    for i in range(1, num_warehouses + 1):
        warehouse_id = f"WH-{str(i).zfill(3)}"
        priority_level = prng.randint(1, 5)
        package_count = prng.randint(0, max_packages)
        data.append([warehouse_id, priority_level, package_count])
    return data

# Save dataset to a CSV file
def save_to_csv(data, file_name):
    """Saves the dataset to a CSV file."""
    with open(file_name, "w") as file:
        # Write the header
        file.write("Warehouse_ID,Priority_Level,Package_Count\n")
        # Write each row
        for row in data:
            file.write(",".join(map(str, row)) + "\n")



def bubble_sort(dataset):
    """Sort the dataset using Bubble Sort."""
    if len(dataset) <= 1:
        print("Single element or empty dataset; no sorting needed.")
        return dataset, 0

    n = len(dataset)
    counter = 0
    counterr = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            counter += 1
            if dataset[j][1] > dataset[j + 1][1]:
                dataset[j], dataset[j + 1] = dataset[j + 1], dataset[j]
            elif dataset[j][1] == dataset[j + 1][1]:  # Priority_Level eşit Package_Count karşılaştırma sayacı
                counterr += 1
                if dataset[j][2] > dataset[j + 1][2]:
                    dataset[j], dataset[j + 1] = dataset[j + 1], dataset[j]
    return dataset, counter, counterr

def merge_sort(dataset):
    counterr = 0  # Package_Count karşılaştırmaları için sayaç

    def merge_sort_inner(dataset):
        nonlocal  counterr
        if len(dataset) <= 1:
            return dataset, 0
        mid = len(dataset) // 2
        left, left_steps = merge_sort_inner(dataset[:mid])
        right, right_steps = merge_sort_inner(dataset[mid:])
        merged, merge_steps = merge(left, right)
        return merged, left_steps + right_steps + merge_steps

    def merge(left, right):
        nonlocal counter, counterr
        result = []
        i = j = 0
        merge_counter = 0
        while i < len(left) and j < len(right):
            merge_counter += 1
            if left[i][1] < right[j][1]:
                result.append(left[i])
                i += 1
            elif left[i][1] > right[j][1]:
                result.append(right[j])
                j += 1
            else:  # Priority_Level eşit, Package_Count karşılaştırması
                counterr += 1
                if left[i][2] <= right[j][2]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result, merge_counter

    sorted_dataset, counter = merge_sort_inner(dataset)
    return sorted_dataset, counter, counterr


def quick_sort(dataset):
    counterr = 0  # Package_Count karşılaştırmalarını saymak için sayaç
    """Sort the dataset using Quick Sort and count Priority_Level and Package_Count comparisons."""

    def quick_sort_inner(dataset):
        nonlocal counterr
        if len(dataset) <= 1:
            return dataset, 0
        pivot = dataset[len(dataset) // 2]
        smaller, larger, pivots = [], [], []
        counter = 0
        for item in dataset:
            counter += 1
            if item[1] < pivot[1]:
                smaller.append(item)
            elif item[1] > pivot[1]:
                larger.append(item)
            else:  # Priority_Level eşit, Package_Count karşılaştırması
                counterr += 1
                if item[2] < pivot[2]:
                    smaller.append(item)
                elif item[2] > pivot[2]:
                    larger.append(item)
                else:
                    pivots.append(item)
        sorted_smaller, smaller_steps = quick_sort_inner(smaller)
        sorted_larger, larger_steps = quick_sort_inner(larger)
        return sorted_smaller + pivots + sorted_larger, counter + smaller_steps + larger_steps

    sorted_dataset, total_counter = quick_sort_inner(dataset)
    return sorted_dataset, total_counter, counterr


def two_level_sorting(sorting, dataset):
    if sorting == bubble_sort:
        sort, pl_iterations,  pc_iterations = bubble_sort(dataset.copy())
    if sorting == merge_sort:
        sort, pl_iterations,  pc_iterations  = merge_sort(dataset.copy())
    if sorting == quick_sort:
        sort, pl_iterations,  pc_iterations = quick_sort(dataset.copy())
    return sort, pl_iterations, pc_iterations


def write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
):
    """Write sorted results and comparisons to the output file."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write("=== Bubble Sorted Results ===\n")
        # file.write(bubble_sorted.to_string() + "\n\n")
        file.write("Warehouse_ID  Priority_Level  Package_Count\n")
        file.write("-" * 40 + "\n")
        for row in bubble_sorted:
            file.write(f"{row[0]:<12}  {row[1]:<14}  {row[2]:<13}\n")
        file.write("\n")
        file.write("=== Comparison Results ===\n")
        if merge_check:
            file.write("Merge and Bubble sorts are identical.\n")
        else:
            file.write("Merge and Bubble sorts differ.\n")

        if quick_check:
            file.write("Quick and Bubble sorts are identical.\n")
        else:
            file.write("Quick and Bubble sorts differ.\n")

        file.write("\n=== Sort Performance Metrics ===\n")
        file.write(f"Bubble priority sort iteration count: {bubble_sort_pl_iterations}\n")
        file.write(f"Merge priority sort n_of right array is smaller than left: {merge_sort_pl_counter}\n")
        file.write(f"Quick priority sort recursive step count: {quick_sort_pl_counter}\n\n")

        file.write(f"Bubble package count sort iteration count: {bubble_sort_pc_iterations}\n")
        file.write(f"Merge package count n_of right array is smaller than left: {merge_sort_pc_counter}\n")
        file.write(f"Quick package count sort recursive step count: {quick_sort_pc_counter}\n")

    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    # File paths and dataset size
    # Specify paths for input and output files

    INPUT_FILE = "hw05_input.csv"  # Input file should be in the same folder as the script
    OUTPUT_FILE = "hw05_output.txt"  # Output file will be saved in the same folder

    SIZE = 10  # Number of warehouses in the dataset

    # Generate the dataset
    dataset = generate_logistics_dataset(SIZE,
                                         max_packages=100)  # Generate a dataset with SIZE warehouses and max_packages packages

    # Save the generated dataset to the input file
    save_to_csv(dataset, INPUT_FILE)
    ###############################################################################################################
    # Perform sorting and counting operations
    # Sort using Bubble Sort and count iterations for Priority Level (_pl_) and Package Count (_pc_)
    bubble_sorted, bubble_sort_pl_iterations, bubble_sort_pc_iterations = two_level_sorting(bubble_sort, dataset)

    # Sort using Merge Sort and count recursive steps for Priority Level and Package Count
    merge_sorted, merge_sort_pl_counter, merge_sort_pc_counter = two_level_sorting(merge_sort, dataset)

    # Sort using Quick Sort and count recursive steps for Priority Level and Package Count
    quick_sorted, quick_sort_pl_counter, quick_sort_pc_counter = two_level_sorting(quick_sort, dataset)
    ###############################################################################################################

    # Comparisons
    # Check if Merge Sort results match Bubble Sort results
    merge_check = merge_sorted == bubble_sorted

    # Check if Quick Sort results match Bubble Sort results
    quick_check = quick_sorted == bubble_sorted

    # Write results and metrics to the output file
    write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
    )


