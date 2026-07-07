public class ShellSort {
    public static void sort(int[] A) {
        int n = A.length;
        int h = 1;
        while(h < n/3){
            h = 3*h + 1;
        }
        while(h >= 1){
            for(int i = h; i < n; i++){
                int j = i;
                while(j >= h && less(A[j], A[j-h])){
                    exch(A, j, j-h);
                    j = j - h;
                }
            }
            h = h / 3;
        }
    }

    public static boolean less(int a, int b){
        if (a < b) return true;
        else return false;
    }

    public static void exch(int[] arr, int i, int j){
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
