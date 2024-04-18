#include<stdio.h>
#include "bin_to_dec.h"

void main(){
	int binary, dec = 0, temp, pos = 1;
	int decimal, bin = 0;
	printf("Enter a binary number: ");
	scanf("%d", &binary);
	binToDec(binary);
	
	pos = 1;
	printf("Enter a decimal number: ");
	scanf("%d", &decimal);
	decToBin(decimal);
	
}
