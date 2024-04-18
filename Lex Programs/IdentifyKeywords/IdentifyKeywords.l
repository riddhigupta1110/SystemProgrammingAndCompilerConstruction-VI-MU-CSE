%{
#include<stdio.h>
#include<string.h>

char keywords[50][20];
int count = 0;

void add_keyword(const char *keyword){
	for(int i=0;i<count;i++){
		if(strcmp(keywords[i],keyword) == 0){
			return;
		}
	}
	strcpy(keywords[count],keyword);
	count++;
}
%}

%%
"if"	{add_keyword(yytext);}
"else"	{add_keyword(yytext);}
"while" {add_keyword(yytext);}
"do" 	{add_keyword(yytext);}
"switch" {add_keyword(yytext);}
"for"	{add_keyword(yytext);}
"case"	{add_keyword(yytext);}
"break"	{add_keyword(yytext);}
"continue"	{add_keyword(yytext);}
"int"	{add_keyword(yytext);}
"float"	{add_keyword(yytext);}
"double"	{add_keyword(yytext);}
"string"	{add_keyword(yytext);}
"void"	{add_keyword(yytext);}
\n ;
"null" {return 0;}
. ;
%%

int yywrap(void){
return 1;
}

int main(){
yylex();
printf("Keywords:\n");
for (int i = 0; i < count; i++) {
        printf("%d-%s\n",i, keywords[i]);
}
return 0;
}
