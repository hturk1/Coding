#include <iostream>
#include <chrono>
#include <cstdlib>

using namespace std;
using namespace std::chrono;

int main()
{
  
    cout << "Hello World";
    
    int N = 100;
    // This program will create some sequence of random
    // numbers on every program run within range 0 to N-1
    for (int i = 0; i < 5; i++)
    cout << rand() % N << " ";

    return 0;
}