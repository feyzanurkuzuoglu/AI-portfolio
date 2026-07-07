import java.util.*;

public class Operation {
    int code;
    String label;
    int time;
    List<Integer> prereq;

    public Operation(int c, String l, int t, List<Integer> p) {
        code = c;
        label = l;
        time = t;
        prereq = p;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Operation)) return false;

        Operation other = (Operation) o;

        return code == other.code &&
                time == other.time &&
                label.equals(other.label) &&
                prereq.equals(other.prereq);
    }
}