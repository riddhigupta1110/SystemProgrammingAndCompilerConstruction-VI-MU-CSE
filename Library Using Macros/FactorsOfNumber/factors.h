#define factorsOfNumber(num)\
	printf("Factors of %d are: \n", num);\
	for(i=1; i<=num; i++)\
		if(num%i == 0){\
			printf("%d \n", i);\
		}
