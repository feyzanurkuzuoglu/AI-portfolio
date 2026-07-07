#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <utility>
using namespace std;

class Reader2
{
public:
    static void reader_part2 (Maps *map, const string& file)
    {
        string myText; ifstream MyReadFile(file);
        getline (MyReadFile, myText); std::istringstream ss(myText);
        int number; ss >> number; map->create(number); number = 0;

        while (number < map->getsize())
        {
            getline (MyReadFile, myText); read2(myText, map, number); number += 1;
        }

        while (getline (MyReadFile, myText))
        {
            std::istringstream ss(myText);
            int x, y;   ss >> x;   ss >> y;
            operation(x,y, map->getsize(), map);
        }
    };

private:
    static void read2 (const std::string& line, Maps *map, int row)
    {
        std::istringstream ss(line); int number;
        for (int i = 0; i < map->getsize(); i++) {ss >> number; map->Map[row][i] = number;}
    };

    static void operation (int x, int y, int size, Maps *map)
    {
        int balloon = map->Map[x][y];
        row(x,size,balloon,map);
        column(y,size,balloon,map);
        right_diagonal(x,y,size,balloon,map);
        left_diagonal(x,y,size,balloon,map);
    };

    static void row (int x, int size, int balloon, Maps *map)
    {
        for (int j = 0; j < size; j++)
        {
            if (map->Map[x][j] == balloon) {map->Map[x][j] = 0; map->result += balloon;}
        }
    };

    static void column (int y, int size, int balloon, Maps *map)
    {
        for (int i = 0; i < size; i++) {
            if (map->Map[i][y] == balloon) {map->Map[i][y] = 0; map->result += balloon;}
        }
    };

    static void right_diagonal (int x, int y, int size, int balloon, Maps *map)
    {
        if (x >= y) {x -= y; y = 0;} else {y -= x; x = 0;}
        while (y < size && x < size)
        {
            if (map->Map[x][y] == balloon) {map->Map[x][y] = 0; map->result += balloon;} x++; y++;
        }
    };

    static void left_diagonal (int x, int y, int size, int balloon, Maps *map)
    {
        if (x + y < size) { y += x; x = 0;} else {x -= size - 1 - y; y = size - 1;}
        while (y >= 0 && x < size)
        {
            if (map->Map[x][y] == balloon) {map->Map[x][y] = 0; map->result += balloon;} x++; y--;
        }
    };
};