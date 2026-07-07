import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.*;

public class SpaceportTransitNetwork {

    double shuttleSpeed;
    final double walkSpeed = 1000 / 6.0;

    Station start, end;
    List<ShuttleCorridor> corridors;

    String content;

    int getInt(String v) {
        Pattern p = Pattern.compile(v + "\\s*=\\s*([0-9]+)");
        Matcher m = p.matcher(content);
        m.find();
        return Integer.parseInt(m.group(1));
    }

    double getDouble(String v) {
        // TODO: Regex for double
        Pattern p = Pattern.compile(v + "\\s*=\\s*(-?[0-9]*\\.?[0-9]+)");
        Matcher m = p.matcher(content);
        if (m.find()) {
            return Double.parseDouble(m.group(1));
        }
        return 0.0;
    }

    Point getPoint(String v) {
        // TODO: Regex for point (x,y)
        Pattern p = Pattern.compile(v + "\\s*=\\s*\\(\\s*(-?[0-9]+)\\s*,\\s*(-?[0-9]+)\\s*\\)");
        Matcher m = p.matcher(content);
        if (m.find()) {
            int x = Integer.parseInt(m.group(1));
            int y = Integer.parseInt(m.group(2));
            return new Point(x, y);
        }
        return null;
    }

    List<ShuttleCorridor> parseCorridors() {
        List<ShuttleCorridor> list = new ArrayList<>();
        // TODO: Parse corridor names and stations

        List<String> names = new ArrayList<>();
        Matcher nameMatcher = Pattern.compile("corridor_name\\s*=\\s*\"([^\"]+)\"").matcher(content);
        while (nameMatcher.find()) {
            names.add(nameMatcher.group(1));
        }

        List<String> stationsStrings = new ArrayList<>();
        Matcher stMatcher = Pattern.compile("corridor_stations\\s*=\\s*((?:\\s*\\(\\s*-?[0-9]+\\s*,\\s*-?[0-9]+\\s*\\))+)").matcher(content);
        while (stMatcher.find()) {
            stationsStrings.add(stMatcher.group(1));
        }


        int count = Math.min(names.size(), stationsStrings.size());
        for (int i = 0; i < count; i++) {
            String name = names.get(i);
            String stStr = stationsStrings.get(i);

            List<Station> stationsList = new ArrayList<>();
            Matcher pointMatcher = Pattern.compile("\\(\\s*(-?[0-9]+)\\s*,\\s*(-?[0-9]+)\\s*\\)").matcher(stStr);

            int index = 1;
            while (pointMatcher.find()) {
                int x = Integer.parseInt(pointMatcher.group(1));
                int y = Integer.parseInt(pointMatcher.group(2));
                stationsList.add(new Station(new Point(x, y), name + " Station " + index));
                index++;
            }
            if (!stationsList.isEmpty()) {
                list.add(new ShuttleCorridor(name, stationsList));
            }
        }

        return list;
    }

    void readInput(String f) {
        // TODO: Read file and initialize variables
        try {
            content = new String(Files.readAllBytes(Paths.get(f)));

            getInt("num_shuttle_corridors");
            //shuttleSpeed = getDouble("average_shuttle_speed");

            shuttleSpeed = (getDouble("average_shuttle_speed") * 1000.0) / 60.0;

            start = new Station(getPoint("origin_point"), "Origin Point");
            end = new Station(getPoint("destination_point"), "Destination Point");

            corridors = parseCorridors();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}