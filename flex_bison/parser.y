%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern FILE *yyin;
extern char *yytext;

void yyerror(const char *s);
int yylex(void);

%}

%union {
    int num;
    char* id;
}

%token <num> NUMBER
%token <id> IDENTIFIER
%token PRINT IF THEN ELSE END ATTACK DEFEND MOVE UP DOWN RIGHT LEFT WAIT CHAR_A CHAR_B OR AND EQ GT LT PLUS MINUS MULT DIV NOT LPAREN RPAREN COMMA NEWLINE

%type <id> BLOCK STATEMENT PRINT_STATEMENT IF_STATEMENT ATTACK_STATEMENT DEFEND_STATEMENT MOVE_STATEMENT BOOL_EXP BOOL_TERM REL_EXP EXPRESSION TERM FACTOR
%type <id> CHARACTER DIRECTION

%%

program:
    BLOCK
    ;

BLOCK:
    STATEMENT NEWLINE BLOCK
    | /* empty */
    ;

STATEMENT:
    PRINT_STATEMENT
    | IF_STATEMENT
    | ATTACK_STATEMENT
    | DEFEND_STATEMENT
    | MOVE_STATEMENT
    ;

PRINT_STATEMENT:
    PRINT LPAREN EXPRESSION RPAREN
    {
        printf("Print: %s\n", $3);
    }
    ;

IF_STATEMENT:
    IF BOOL_EXP THEN NEWLINE BLOCK END NEWLINE
    {
        printf("If: %s then ... end\n", $2);
    }
    | IF BOOL_EXP THEN NEWLINE BLOCK ELSE NEWLINE BLOCK END NEWLINE
    {
        printf("If: %s then ... else ... end\n", $2);
    }
    ;

ATTACK_STATEMENT:
    ATTACK CHARACTER CHARACTER
    {
        printf("Attack: %s attacks %s\n", $2, $3);
    }
    ;

DEFEND_STATEMENT:
    DEFEND CHARACTER
    {
        printf("Defend: %s\n", $2);
    }
    ;

MOVE_STATEMENT:
    MOVE CHARACTER DIRECTION
    {
        printf("Move: %s moves %s\n", $2, $3);
    }
    ;

DIRECTION:
    UP { $$ = strdup("up"); }
    | DOWN { $$ = strdup("down"); }
    | RIGHT { $$ = strdup("right"); }
    | LEFT { $$ = strdup("left"); }
    ;

BOOL_EXP:
    BOOL_TERM
    {
        $$ = $1;
    }
    | BOOL_EXP OR BOOL_TERM
    {
        asprintf(&$$, "%s or %s", $1, $3);
    }
    ;

BOOL_TERM:
    REL_EXP
    {
        $$ = $1;
    }
    | BOOL_TERM AND REL_EXP
    {
        asprintf(&$$, "%s and %s", $1, $3);
    }
    ;

REL_EXP:
    EXPRESSION EQ EXPRESSION
    {
        asprintf(&$$, "%s == %s", $1, $3);
    }
    | EXPRESSION GT EXPRESSION
    {
        asprintf(&$$, "%s > %s", $1, $3);
    }
    | EXPRESSION LT EXPRESSION
    {
        asprintf(&$$, "%s < %s", $1, $3);
    }
    ;

EXPRESSION:
    TERM
    {
        $$ = $1;
    }
    | EXPRESSION PLUS TERM
    {
        asprintf(&$$, "%s + %s", $1, $3);
    }
    | EXPRESSION MINUS TERM
    {
        asprintf(&$$, "%s - %s", $1, $3);
    }
    ;

TERM:
    FACTOR
    {
        $$ = $1;
    }
    | TERM MULT FACTOR
    {
        asprintf(&$$, "%s * %s", $1, $3);
    }
    | TERM DIV FACTOR
    {
        asprintf(&$$, "%s / %s", $1, $3);
    }
    ;

FACTOR:
    NUMBER
    {
        asprintf(&$$, "%d", $1);
    }
    | IDENTIFIER
    {
        $$ = $1;
    }
    | PLUS FACTOR
    {
        asprintf(&$$, "+%s", $2);
    }
    | MINUS FACTOR
    {
        asprintf(&$$, "-%s", $2);
    }
    | NOT FACTOR
    {
        asprintf(&$$, "not %s", $2);
    }
    | LPAREN EXPRESSION RPAREN
    {
        $$ = $2;
    }
    | "read" LPAREN RPAREN
    {
        $$ = strdup("read()");
    }
    ;

CHARACTER:
    CHAR_A { $$ = strdup("char_a"); }
    | CHAR_B { $$ = strdup("char_b"); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            perror(argv[1]);
            return 1;
        }
        yyin = file;
    }

    yyparse();
    return 0;
}
