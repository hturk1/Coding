#include <iostream>
#include <iomanip>

using namespace std; 

const int NUM_DEPTS = 2;
const int NUM_STORES = 2;
const int NUM_MONTHS = 12;

void printMonthlySales(float storeMonthlySales [NUM_STORES][NUM_MONTHS][NUM_DEPTS], int month)
{

cout << "Sales for month #" << month << ":" << endl;
cout << endl;
cout << "       " << "   Dept#1 "  << "Dept#2 " << "Store Total" << endl;

float storeSales;
float deptSales;
float overallSales = 0.0;
    
    for (int store = 0; store < NUM_STORES; ++store) 
    {
        float storeSales = 0.0;
        cout << "Store#" << store + 1 << "   ";

        for (int dept = 0; dept < NUM_DEPTS; ++dept)
        {
            float deptSales = 0.0;
            for (int months = 0; months < NUM_MONTHS; ++months)
            {
            if (months == month - 1)
            {
                cout << storeMonthlySales[store][months][dept] << "    "; 
                deptSales += storeMonthlySales[store][months][dept];
                storeSales += storeMonthlySales[store][months][dept];
            }

            }
        }


        cout << storeSales << endl;
    }

    cout << "DeptTotal ";
    for (int dept = 0; dept < NUM_DEPTS; ++dept) 
    {
        float deptSales = 0.0;
        for (int store = 0; store < NUM_STORES; ++store) 
        {
            
            for (int months = 0; months < NUM_MONTHS; ++months) 
            {
                
                if (months == month - 1) 
                {
                    
                    deptSales += storeMonthlySales[store][months][dept];
                }
            }
        }

        cout << deptSales << "    ";
    }

    for (int store = 0; store < NUM_STORES; ++store) 
    {
        for (int dept = 0; dept < NUM_DEPTS; ++dept) 
        {
            for (int months = 0; months < NUM_MONTHS; ++months) 
            {
                
                if (months == month - 1)
                {
                    
                    overallSales += storeMonthlySales[store][months][dept];
                }
            }
        }
    }

    cout << overallSales << endl;
}


int main ()
{

float storeMonthlySales[NUM_STORES][NUM_MONTHS][NUM_DEPTS] =

{ 
{{1.1, 1.2}, {1.3, 1.4}, {1.5, 1.6}, {1.7, 1.8}, {1.9, 2.0}, {2.1, 2.2},
{2.1, 2.2}, {2.3, 2.4}, {2.5, 2.6}, {2.7, 2.8}, {2.9, 3.0}, {3.1, 3.2}},

{{3.1, 3.2}, {3.3, 3.4}, {3.5, 3.6}, {3.7, 3.8}, {3.9, 4.0}, {4.1, 4.2},
{2.1, 2.2}, {2.3, 2.4}, {2.5, 2.6}, {2.7, 2.8}, {2.9, 3.0}, {3.1, 3.2}}
};

char choice;
int month; 

do
{
    cout << "Would you like to print out the values for a certain month? (y/n)" << endl;
    cin >> choice;

    if (choice!= 'n')
{
    cout << endl; 
    cout << "Which month? (1-12 or 0 to exit)" << endl;
    cin >> month; 
    cout << endl;

    if (month == 0)
    {
        break;
    }
    else if (month >= 0 && month <= 12)
    {
        printMonthlySales(storeMonthlySales, month); 
        cout << endl;
    }
    else 
    {
        cout << "Not a valid input" << endl; 
    }
}

}while (choice == 'y');

    return 0; 
}