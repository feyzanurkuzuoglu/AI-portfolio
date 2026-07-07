public class RadixSort {
    public static int[] sort(int[] A, int d) {
        for(int pos = 1; pos <= d; pos++){
            A = countingSort(A, pos);
        }
        return A;
    }

    public static int[] countingSort(int[] A, int pos){
        int[] count = new int[10];
        int[] output = new int[A.length];
        int size = A.length;
        for(int i = 0; i < size; i++){
            int digit = getDigit(A[i], pos);
            count[digit] = count[digit] + 1;
        }
        for(int i = 1; i < 10; i++){
            count[i] = count[i] + count[i - 1];
        }
        for(int i = size - 1; i >= 0; i--){
            int digit = getDigit(A[i], pos);
            count[digit] = count[digit] - 1;
            output[count[digit]] = A[i];
        }
        return output;
    }

    private static int getDigit(int value, int pos) {
        return (int) (Math.abs(value) / Math.pow(10, pos - 1)) % 10;
    }
}
