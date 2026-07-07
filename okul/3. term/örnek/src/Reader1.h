#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <utility>
#include <vector>
using namespace std;

class Reader1
{
public:
    static void reader_part1 (Maps *map, const string& file)
    {
        string myText; ifstream MyReadFile(file);
        getline (MyReadFile, myText); std::istringstream ss(myText);
        int number; ss >> number; map->create(number);

        while (getline (MyReadFile, myText)) {read1(myText, map);}

        MyReadFile.close();
    };

private:
    struct address {int x,y;};

    static void read1 (const std::string& line, Maps *map)
    {
        std::istringstream ss(line);
        int number,x,y; ss >> number; ss >> x; ss >> y;
        map->Map[x][y] = number;
        vector<address> addresses;

        while (true)
        {
            searching(map, map->Map[x][y], x, y, &addresses, true, true, true, true);
            if (addresses.size() > 1) {bomb(map, x, y, &addresses); addresses.clear();} else {break;}
        }
    };

    static void searching (Maps *map, int balloon, int x, int y, vector<address> *addresses, bool r, bool l, bool u, bool d)
    {
        if (r) {right(map, balloon, x, y, addresses);}
        if (l) {left(map, balloon, x, y, addresses);}
        if (u) {up(map, balloon, x, y, addresses);}
        if (d) {down(map, balloon, x, y, addresses);}
    };

    static void right (Maps *map, int balloon, int x, int y, vector<address> *addresses)
    {
        if (position_check(map->getsize(), x, y+1) && map->Map[x][y+1] == balloon)
        {
            addresses->push_back({x, y+1});
            searching(map, balloon, x, y+1, addresses, true, false, true, true);
        }
    };

    static void left (Maps *map, int balloon, int x, int y, vector<address> *addresses)
    {
        if (position_check(map->getsize(), x, y-1) && map->Map[x][y-1] == balloon)
        {
            addresses->push_back({x, y-1});
            searching(map, balloon, x, y-1, addresses, false, true, true, true);
        }
    };

    static void up (Maps *map, int balloon, int x, int y, vector<address> *addresses)
    {
        if (position_check(map->getsize(), x-1, y) && map->Map[x-1][y] == balloon)
        {
            addresses->push_back({x-1, y});
            searching(map, balloon, x-1, y, addresses, true, true, true, false);
        }
    };

    static void down (Maps *map, int balloon, int x, int y, vector<address> *addresses)
    {
        if (position_check(map->getsize(), x+1, y) && map->Map[x+1][y] == balloon)
        {
            addresses->push_back({x+1, y});
            searching(map, balloon, x+1, y, addresses, true, true, false, true);
        }
    };

    static bool position_check (int size, int x, int y)
    {
        if (x < 0 || y < 0 || x >= size || y >= size) {return false;} return true;
    };

    static void bomb (Maps *map, int x, int y, vector<address> *addresses)
    {
        for (address p : *addresses) {map->Map[p.x][p.y] = 0;} map->Map[x][y] += 1;
    }
};