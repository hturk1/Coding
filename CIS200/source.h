#include <iostream>

#ifndef SOURCE
#define SOURCE

using namespace std; 

const int MAX_ROWS = 3; 
const int MAX_COLUMNS = 2; 

int howManyEven(int arrIntValues[][MAX_COLUMNS])
{

int count = 0;

for(int i = 0; i < MAX_ROWS ; i++)
{

    for(int j = 0; j < MAX_COLUMNS; j++)
    {

    if(arrIntValues[i][j] % 2 == 0)
    {

    count += 1;

    }

    }

}

return count;

}

void printArray (int arrIntValues[][MAX_COLUMNS])
{

cout << "The array of numbers: " << endl;

    for (int i = 0; i < MAX_ROWS; i++ )
    {

        for(int j = 0; j < MAX_COLUMNS; j++)
        {

        cout << arrIntValues[i][j] << " ";

        }

cout << endl;

}

}

#endif
