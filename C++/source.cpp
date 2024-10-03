#include <iostream>
#include "source.h"

using namespace std;

int main ()

{

int arrayIntValues [MAX_ROWS][ MAX_COLUMNS] = { {4 , 2}, {3, 5}, {7, 9} };
int arrayUserValues [MAX_ROWS][ MAX_COLUMNS]; 

printArray(arrayIntValues);

cout << endl;

cout << "Number of even numbers in the array: " << howManyEven(arrayIntValues) << endl;

cout << endl;

char choice; 

do
{
cout << "Would you like to enter a new set of numbers? (y/n)" << endl;
cin >> choice; 
cout << endl;

if (choice != 'n')
{
    cout << "What number would you like to input?" << endl;
    cout << endl;
   
    for (int i = 0; i < MAX_ROWS; i++ )
    {

        for(int j = 0; j < MAX_COLUMNS; j++)
        {

        cin >> arrayUserValues[i][j]; 

        }
    }
    cout << endl;
    printArray(arrayUserValues);

    cout << endl;
    cout << "Number of even numbers in the array: " << howManyEven(arrayUserValues) << endl;
    cout << endl;

}
} while (choice == 'y');

return 0; 

}