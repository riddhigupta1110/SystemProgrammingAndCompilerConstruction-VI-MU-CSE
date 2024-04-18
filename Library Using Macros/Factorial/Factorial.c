#include <stdio.h>
#include "factorialOfNumber.h"

void main(){
	int num, factNum = 1, i;
	printf("Enter a number to find factorial:");
	scanf("%d", &num);
	factorial(num);
}
