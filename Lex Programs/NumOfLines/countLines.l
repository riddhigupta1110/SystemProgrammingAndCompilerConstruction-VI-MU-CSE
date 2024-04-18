%option noyywrap
%{
#include<stdio.h>
int lineCount=0;
%}

%%
\n {lineCount++;}//increase count of line
"null" {return 0;}
. ;//ignore other characters
%%

int main(){
yylex();
printf("Number of lines: %d", lineCount);
return 0;
}


