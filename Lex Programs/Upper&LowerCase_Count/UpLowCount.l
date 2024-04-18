%option noyywrap
%{
#include<stdio.h>
int uCount = 0;
int lCount = 0;
%}

%% 
[a-z]*[A-Z]+[a-z]* {uCount++; printf("\nUppercase :%s",yytext);}
[a-z]* {lCount++;}
\n {return 0;}
. ;
%%

int main(){
    yylex();
    printf("\nCount of uppercase words: %d", uCount);
    printf("\nCount of lowercase words: %d", lCount);
    return 0;
}

