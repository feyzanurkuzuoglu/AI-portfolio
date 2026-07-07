#include <fstream>
#include <string>
#include <sstream>
#include "Map.h"
#include "Reader1.h"
#include "Reader2.h"
using namespace std;

void print_array(Maps map, int size, const string& start, const string& file)
{
    ofstream  MyFile; MyFile.open (file, ofstream::app);
    MyFile << start << "\n";

    for (int i = 0; i < size; i++)
    {
        for (int m = 0; m < size; m++) {MyFile << map.Map[i][m] << " ";} MyFile << "\n";
    }

    if (start == "PART 1:") {MyFile << "\n";} else {MyFile << "Final Point: " << map.result << "p" ;}

    MyFile.close();
}

int main(int argc, char *argv[])
{
    Maps map1; Reader1::reader_part1(&map1, argv[1]);
    print_array(map1, map1.getsize(), "PART 1:",argv[3]);

    Maps map2; Reader2::reader_part2(&map2, argv[2]);
    print_array(map2, map2.getsize(), "PART 2:", argv[3]);

    return 0;
}