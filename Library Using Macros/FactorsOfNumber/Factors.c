#include<stdio.h>
#include "factors.h"

void main(){
	int num, i;
	printf("Enter a number to find its factors: ");
	scanf("%d", &num);
	factorsOfNumber(num);
}
