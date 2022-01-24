/**
 * @file chips.C
 * @author Phillip Davis and Logan Richardson
 * @brief  muffin and cookie counting is buggie but the code that determines whether the last chip standing is blue or red 
 * should stand up to scrutiny
 * @version 0.1
 * @date 2022-01-24
 * 
 * @copyright Copyright (c) 2022
 * 
 */

*/

#include <iostream>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "chips.h"

using namespace std;

void chips(int red, int blue)
{

	static int r = 0;
	static int b = 0;
	static int most_cookies = INT_MIN;
	static int most_muffins = INT_MIN;
	static int cookies = 0;
	static int muffins = 0;


	if (red == 0 and blue == 1){
		b++;
		cookies, muffins = 0, 0;
		cout << "Found a blue" << endl;
		return;
	}
	
	if (red == 1 and blue == 0){
		cookies, muffins = 0, 0;
		fprintf(stderr, "Whoopsy, we found a red");
		exit(1);
	}	

	// check for same-color
	if (red > 1){ // two reds
		chips(red - 1, blue);
		if ((++cookies) > most_cookies) {
			most_cookies = cookies; 	
			cout << "Most cookies found is " << most_cookies << endl;
		}
	}

	if (blue > 1){ // two blues
		chips(red + 1, blue - 2);
		if ((++cookies) > most_cookies){
			most_muffins = muffins;
			cout << "Most muffins found is " << most_muffins << endl;
		} 	
	}

	// check for one of each
	if (red >= 1 and blue >= 1){
		chips(red - 1, blue);
		if ((++muffins) > most_muffins) most_muffins = muffins;
	}

}

int main()
{

	chips(14, 15);

}

