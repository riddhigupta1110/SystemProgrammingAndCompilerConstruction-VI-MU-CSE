%option noyywrap
%{
#include<stdio.h>
int vowel=0;
int consonant=0;
%}

%%
[aeiouAEIOU] {vowel++;}
[a-zA-Z] {consonant++;}
\n {return 0;}
. ;
%%

int main(){
yylex();
printf("Number of vowels: %d\n", vowel);
printf("Number of consonants: %d\n", consonant);
return 0;
}
