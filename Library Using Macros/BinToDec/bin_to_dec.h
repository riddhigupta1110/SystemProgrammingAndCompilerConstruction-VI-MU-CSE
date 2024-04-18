#define binToDec(binary)\
	while(binary!=0){\
		temp = binary % 10;\
		dec = dec + (temp * pos);\
		pos = pos * 2;\
		binary = binary / 10;\
	}\
	printf("Decimal equivalent = %d\n", dec);
	
#define decToBin(decimal)\
	while(decimal!=0){\
		temp = decimal%2;\
		bin = bin + (temp*pos);\
		decimal = decimal/2;\
		pos = pos*10;\
	}\
	printf("Binary equivalent = %d\n", bin);
	
