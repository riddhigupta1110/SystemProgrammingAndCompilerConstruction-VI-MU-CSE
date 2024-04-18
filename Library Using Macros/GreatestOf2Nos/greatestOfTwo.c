#include <stdio.h>
#include "greatest.h"

void main(){
	int num1, num2;
	printf("Enter two numbers: ");
	scanf("%d %d", &num1, &num2);
	
	largerNumber(num1, num2);
}
