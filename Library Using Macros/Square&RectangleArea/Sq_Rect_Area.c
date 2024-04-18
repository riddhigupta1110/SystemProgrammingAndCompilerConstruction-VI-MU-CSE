#include <stdio.h>
#include "sq_rect_area.h"

void main(){
	int side, l, b;
	printf("Enter side of square:");
	scanf("%d", &side);
	printf("Area of square: %d \n", squareArea(side));
	
	printf("Enter length and breadth of rectangle:");
	scanf("%d %d", &l, &b);
	printf("Area of rectangle: %d \n", rectArea(l, b));
}
