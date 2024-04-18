%option noyywrap
%{
#include<stdio.h>
int uCount = 0;
%}

%% 
[a-z]*[A-Z]+[a-z]* {uCount++; printf("\nUppercase :%s",yytext);}
\n {return 0;}
. ;
%%

int main(){
    yylex();
    printf("\nCount of uppercase words: %d", uCount);
    return 0;
}

