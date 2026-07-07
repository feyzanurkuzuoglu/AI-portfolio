public class RouteInstruction {
    String a, b; // start-end
    double t; // time
    boolean shuttle; // true if it's a ride on shuttle, false if it's a walk

    public RouteInstruction(String a, String b, double t, boolean s) {
        this.a = a;
        this.b = b;
        this.t = t;
        this.shuttle = s;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof RouteInstruction)) return false;

        RouteInstruction other = (RouteInstruction) o;

        return a.equals(other.a) &&
                b.equals(other.b) &&
                Math.abs(t - other.t) < 1e-6 &&
                shuttle == other.shuttle;
    }

    @Override
    public String toString() {
        return a + " -> " + b + " (" + t + ")";
    }

}