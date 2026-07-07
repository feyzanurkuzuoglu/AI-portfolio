#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;

class Maps
{
public:
    Maps() = default; ~Maps() = default;
    int result = 0; int **Map{}; int getsize() const {return size;}

    void create (const int number)
    {
        this->size = number; Map = new int*[this->size];
        for (int i = 0; i < this->size; i++)
        {
            Map[i] = new int[this->size]; for (int j = 0; j < this->size; j++) {Map[i][j] = 0;}
        }
    }

private:
    int size{};
};