%{
#include "parser.tab.h"
%}

DIGIT [0-9]
LETTER [a-zA-Z]
IDENTIFIER {LETTER}({LETTER}|{DIGIT}|_)*
NUMBER {DIGIT}+

%%

"print"         { return PRINT; }
"if"            { return IF; }
"then"          { return THEN; }
"else"          { return ELSE; }
"end"           { return END; }
"attack"        { return ATTACK; }
"defend"        { return DEFEND; }
"move"          { return MOVE; }
"up"            { return UP; }
"down"          { return DOWN; }
"right"         { return RIGHT; }
"left"          { return LEFT; }
"char_a"        { return CHAR_A; }
"char_b"        { return CHAR_B; }
"or"            { return OR; }
"and"           { return AND; }
"=="            { return EQ; }
">"             { return GT; }
"<"             { return LT; }
"+"             { return PLUS; }
"-"             { return MINUS; }
"*"             { return MULT; }
"/"             { return DIV; }
"not"           { return NOT; }
"("             { return LPAREN; }
")"             { return RPAREN; }
","             { return COMMA; }
{NUMBER}        { yylval.num = atoi(yytext); return NUMBER; }
{IDENTIFIER}    { yylval.id = strdup(yytext); return IDENTIFIER; }
"\n"            { return NEWLINE; }
[ \t\r]         { /* skip whitespace */ }
.               { /* ignore any other character */ }

%%

int yywrap() {
    return 1;
}
