%{
#include "parser.tab.h"
%}

DIGIT [0-9]
LETTER [a-zA-Z]
IDENTIFIER ({LETTER}({LETTER}|{DIGIT}|_)*)
NUMBER {DIGIT}+
CHARACTER "char_a"|"char_b"

%%
"print"                 { return PRINT; }
"while"                 { return WHILE; }
"do"                    { return DO; }
"if"                    { return IF; }
"then"                  { return THEN; }
"else"                  { return ELSE; }
"attack"                { return ATTACK; }
"defend"                { return DEFEND; }
"move"                  { return MOVE; }
"up"                    { return UP; }
"down"                  { return DOWN; }
"right"                 { return RIGHT; }
"left"                  { return LEFT; }
"read"                  { return READ; }
"not"                   { return NOT; }
"and"                   { return AND; }
"or"                    { return OR; }
"=="                    { return EQ; }
">"                     { return GT; }
"<"                     { return LT; }
"{"                     { return LBRACE; }
"}"                     { return RBRACE; }
"("                     { return LPAREN; }
")"                     { return RPAREN; }
"="                     { return ASSIGN; }
"+"                     { return PLUS; }
"-"                     { return MINUS; }
"*"                     { return MULTIPLY; }
"/"                     { return DIVIDE; }
"λ"                     { return LAMBDA; }
";"                     { return SEMICOLON; }
{NUMBER}                { yylval.ival = atoi(yytext); return NUMBER; }
{CHARACTER}             { yylval.sval = strdup(yytext); return CHARACTER; }
{IDENTIFIER}            { yylval.sval = strdup(yytext); return IDENTIFIER; }

[ \t\n\r]+              { /* Ignore whitespace */ }
.                       { return yytext[0]; }

%%
