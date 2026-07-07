import org.knowm.xchart.*;
import org.knowm.xchart.style.Styler;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;

public class Main {
    public static void main(String args[]) throws IOException {

        int[] inputAxis = {500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 250000};


        double[][] yAxisRandom = new double[5][10];
        double[][] yAxisSorted = new double[5][10];
        double[][] yAxisReverse = new double[5][10];



        for (int i = 0; i < inputAxis.length; i++) {
            int n = inputAxis[i];
            int[] randomData = readVolumeData("all_stocks_5yr.csv", n);
            int[] sortedData = randomData.clone();
            Arrays.sort(sortedData);
            int[] reverseData = new int[n];
            for (int j = 0; j < n; j++) {
                reverseData[j] = sortedData[n - 1 - j];
            }


            yAxisRandom[0][i] = measureAvgTime("QuickSort", randomData);
            yAxisRandom[1][i] = measureAvgTime("InsertionSort", randomData);
            yAxisRandom[2][i] = measureAvgTime("MergeSort", randomData);
            yAxisRandom[3][i] = measureAvgTime("ShellSort", randomData);
            yAxisRandom[4][i] = measureAvgTime("RadixSort", randomData);

            yAxisSorted[0][i] = measureAvgTime("QuickSort", sortedData);
            yAxisSorted[1][i] = measureAvgTime("InsertionSort", sortedData);
            yAxisSorted[2][i] = measureAvgTime("MergeSort", sortedData);
            yAxisSorted[3][i] = measureAvgTime("ShellSort", sortedData);
            yAxisSorted[4][i] = measureAvgTime("RadixSort", sortedData);

            yAxisReverse[0][i] = measureAvgTime("QuickSort", reverseData);
            yAxisReverse[1][i] = measureAvgTime("InsertionSort", reverseData);
            yAxisReverse[2][i] = measureAvgTime("MergeSort", reverseData);
            yAxisReverse[3][i] = measureAvgTime("ShellSort", reverseData);
            yAxisReverse[4][i] = measureAvgTime("RadixSort", reverseData);

            System.out.println(" for n = " + n + " completed.");
        }


        showAndSaveChart("Random Data Performance", inputAxis, yAxisRandom);
        showAndSaveChart("Sorted Data Performance", inputAxis, yAxisSorted);
        showAndSaveChart("Reverse Data Performance", inputAxis, yAxisReverse);


        // comparison of Shell Sort and Insertion Sort
        double[][] yAxisRandom2 = new double[2][10];

        yAxisRandom2[0] = yAxisRandom[3];
        yAxisRandom2[1] = yAxisRandom[1];

        showAndSave2Chart("Comparison of Shell Sort and Insertion Sort", inputAxis, yAxisRandom2);
    }

    public static int[] readVolumeData(String path, int n) {
        int[] data = new int[n];
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            br.readLine();
            for (int i = 0; i < n; i++) {
                String line = br.readLine();
                if (line == null) break;
                String[] columns = line.split(",");
                data[i] = Integer.parseInt(columns[5]);
            }
        } catch (IOException e) {
            System.err.println("Errorr: " + e.getMessage());
        }
        return data;
    }

    public static double measureAvgTime(String algoName, int[] data) {
        long totalNanoTime = 0;
        int k = 10;

        for (int i = 0; i < k; i++) {
            int[] copy = data.clone();
            long start = System.nanoTime();


            switch (algoName) {
                case "QuickSort": QuickSort.sort(copy, 0, copy.length - 1); break;
                case "InsertionSort": InsertionSort.sort(copy); break;
                case "MergeSort": MergeSort.sort(copy); break;
                case "ShellSort": ShellSort.sort(copy); break;
                case "RadixSort": RadixSort.sort(copy, 10); break;
            }

            long end = System.nanoTime();
            totalNanoTime += (end - start);
        }
        double averageMs = (totalNanoTime / (double) k) / 1_000_000.0;


        System.out.printf("%s average time: %.4f ms\n", algoName, averageMs);

        return averageMs;
    }

    public static void showAndSaveChart(String title, int[] xAxis, double[][] yAxis) throws IOException {
        // Create Chart
        XYChart chart = new XYChartBuilder().width(800).height(600).title(title)
                .yAxisTitle("Time (ms)").xAxisTitle("Input Size (n)").build();

        // Convert x axis to double[]
        double[] doubleX = Arrays.stream(xAxis).asDoubleStream().toArray();

        // Customize Chart
        chart.getStyler().setLegendPosition(Styler.LegendPosition.InsideNE);
        chart.getStyler().setDefaultSeriesRenderStyle(XYSeries.XYSeriesRenderStyle.Line);

        // Add a plot for a sorting algorithm
        chart.addSeries("Quick Sort", doubleX, yAxis[0]);
        chart.addSeries("Insertion Sort", doubleX, yAxis[1]);
        chart.addSeries("Merge Sort", doubleX, yAxis[2]);
        chart.addSeries("Shell Sort", doubleX, yAxis[3]);
        chart.addSeries("Radix Sort", doubleX, yAxis[4]);

        // Save the chart as PNG
        BitmapEncoder.saveBitmap(chart, title + ".png", BitmapEncoder.BitmapFormat.PNG);
        // Show the chart
        new SwingWrapper(chart).displayChart();
    }

    public static void showAndSave2Chart(String title, int[] xAxis, double[][] yAxis) throws IOException {
        // Create Chart
        XYChart chart = new XYChartBuilder().width(800).height(600).title(title)
                .yAxisTitle("Time in Milliseconds").xAxisTitle("Input Size").build();

        // Convert x axis to double[]
        double[] doubleX = Arrays.stream(xAxis).asDoubleStream().toArray();

        // Customize Chart
        chart.getStyler().setLegendPosition(Styler.LegendPosition.InsideNE);
        chart.getStyler().setDefaultSeriesRenderStyle(XYSeries.XYSeriesRenderStyle.Line);

        // Add a plot for a sorting algorithm
        chart.addSeries("Shell Sort", doubleX, yAxis[0]);
        chart.addSeries("Insertion Sort", doubleX, yAxis[1]);

        // Save the chart as PNG
        BitmapEncoder.saveBitmap(chart, title + ".png", BitmapEncoder.BitmapFormat.PNG);

        // Show the chart
        new SwingWrapper(chart).displayChart();


    }
}