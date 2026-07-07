public class QuickSort {
    public static void sort(int[] A, int low, int high) {
        int stackSize = high - low + 1;
        int[] stack = new int[stackSize];
        int top = -1;
        top++;
        stack[top] = low;
        top++;
        stack[top] = high;
        while (top >= 0) {
            high = stack[top];
            top--;
            low = stack[top];
            top--;
            int pivot = partition(A, low, high);
            if(pivot - 1 > low){
                top++;
                stack[top] = low;
                top++;
                stack[top] = pivot - 1;
            }
            if(pivot + 1 < high){
                top++;
                stack[top] = pivot + 1;
                top++;
                stack[top] = high;
            }
        }
    }
    public static int partition(int[] A, int low, int high) {
        int pivot = A[high];
        int i = low - 1;
        for(int j = low; j < high; j++){
        if(A[j] <= pivot){
            i++;
            swap(A, i, j);
            }
        }
        swap(A,i+1,high);
        return  i+1;
    }

    public static void swap(int[] arr, int i, int j){
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

}
