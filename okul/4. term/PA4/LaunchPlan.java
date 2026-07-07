import java.util.*;

public class LaunchPlan {

    String name;
    List<Operation> ops;

    public LaunchPlan(String n, List<Operation> o) {
        name = n;
        ops = o;
    }

    /**
     * Computes the earliest possible start times for all operations.
     * You should consider dependency constraints between operations.
     */
    public int[] earliest() {
        // TODO: Implement topological sorting + scheduling

        int maxCode = 0;
        for (Operation op : ops) {
            if (op.code > maxCode) {
                maxCode = op.code;
            }
        }

        Map<Integer, Operation> opMap = new HashMap<>();

        // adjacency list
        List<Integer>[] adjList = new ArrayList[maxCode + 1];
        for (int i = 0; i <= maxCode; i++) {
            adjList[i] = new ArrayList<>();
        }

        // edges:  reqCode -> op.code
        for (Operation op : ops) {
            opMap.put(op.code, op);
            for (int reqCode : op.prereq) {
                adjList[reqCode].add(op.code);
            }
        }

        // topological order
        boolean[] visited = new boolean[maxCode + 1];
        Stack<Integer> stack = new Stack<>();

        for (Operation op : ops) {
            if (!visited[op.code]) {
                dfs(op.code, visited, adjList, stack);
            }
        }

        // relaxation
        int[] schedule = new int[maxCode + 1];

        while (!stack.isEmpty()) {
            int u = stack.pop();
            Operation opU = opMap.get(u);

            if (opU != null) {
                int finishTimeU = schedule[u] + opU.time;

                for (int v : adjList[u]) {
                    if (schedule[v] < finishTimeU) {
                        schedule[v] = finishTimeU;
                    }
                }
            }
        }

        return schedule;


        // return null;
    }

    private void dfs(int u, boolean[] visited, List<Integer>[] adjList, Stack<Integer> stack) {
        visited[u] = true;

        for (int v : adjList[u]) {
            if (!visited[v]) {
                dfs(v, visited, adjList, stack);
            }
        }
        // postorder
        stack.push(u);
    }

    /**
     * Computes total time required to complete all operations.
     */
    public int total(int[] schedule) {
        // TODO: Compute maximum finish time

        int maxFinishTime = 0;

        for (Operation op : ops) {
            int currentFinishTime = schedule[op.code] + op.time;
            if (currentFinishTime > maxFinishTime) {
                maxFinishTime = currentFinishTime;
            }
        }

        return maxFinishTime;

        // return 0;
    }

    /**
     * Helper function to print separator line
     */
    public static void printLine(int n) {
        for (int i = 0; i < n; i++) System.out.print("-");
        System.out.println();
    }

    /**
     * Prints the launch plan timeline in required format.
     */
    public void print() {

        int[] schedule = earliest();

        int width = 65;

        printLine(width);
        System.out.println("Launch Plan: " + name);
        printLine(width);

        System.out.printf("%-8s%-35s%-8s%-8s\n", "Code", "Operation", "Begin", "Finish");

        printLine(width);

        // TODO:
        // Print each operation with:
        // code, label, start time, finish time

        for (Operation op : ops) {
            int beginTime = schedule[op.code];
            int finishTime = beginTime + op.time;
            System.out.printf("%-8d%-35s%-8d%-8d\n", op.code, op.label, beginTime, finishTime);
        }

        printLine(width);

        // TODO:
        // Print total duration in format:
        // Launch-ready in X hour(s).

        int totalDuration = total(schedule);
        System.out.println("Launch-ready in " + totalDuration + " hour(s).");

        printLine(width);


    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof LaunchPlan)) return false;

        LaunchPlan other = (LaunchPlan) o;

        return name.equals(other.name) && ops.equals(other.ops);
    }
}