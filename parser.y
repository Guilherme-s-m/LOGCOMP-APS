%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);

typedef struct {
    int ival;
    char *sval;
} YYSTYPE;

#define YYSTYPE YYSTYPE
%}

%union {
    int ival;
    char *sval;
}

%token <ival> NUMBER
%token <sval> IDENTIFIER CHARACTER
%token PRINT WHILE DO IF THEN ELSE ATTACK DEFEND MOVE
%token UP DOWN RIGHT LEFT READ NOT AND OR EQ GT LT ASSIGN
%token PLUS MINUS MULTIPLY DIVIDE LBRACE RBRACE LPAREN RPAREN LAMBDA SEMICOLON

%type <ival> expression term factor
%type <sval> assignment bool_exp bool_term rel_exp

%%
block: 
    { /* empty block */ }
    | statement_list
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    assignment SEMICOLON
    | loop
    | if_statement
    | LAMBDA
    | print_statement SEMICOLON
    | attack_statement SEMICOLON
    | defend_statement SEMICOLON
    | move_statement SEMICOLON
    ;

assignment:
    CHARACTER IDENTIFIER ASSIGN expression
    ;

print_statement:
    PRINT LPAREN expression RPAREN
    ;

loop:
    WHILE bool_exp DO LBRACE statement_list RBRACE
    ;

if_statement:
    IF bool_exp THEN LBRACE statement_list RBRACE
    | IF bool_exp THEN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
    ;

attack_statement:
    ATTACK CHARACTER CHARACTER CHARACTER
    ;

defend_statement:
    DEFEND CHARACTER
    ;

move_statement:
    MOVE CHARACTER UP
    | MOVE CHARACTER DOWN
    | MOVE CHARACTER RIGHT
    | MOVE CHARACTER LEFT
    ;

bool_exp:
    bool_term
    | bool_exp OR bool_term
    ;

bool_term:
    rel_exp
    | bool_term AND rel_exp
    ;

rel_exp:
    expression
    | expression EQ expression
    | expression GT expression
    | expression LT expression
    | defend_statement
    ;

expression:
    term
    | expression PLUS term
    | expression MINUS term
    ;

term:
    factor
    | term MULTIPLY factor
    | term DIVIDE factor
    ;

factor:
    NUMBER
    | IDENTIFIER
    | PLUS factor
    | MINUS factor
    | NOT factor
    | LPAREN expression RPAREN
    | READ LPAREN RPAREN
    ;

%%
void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}

int main(void) {
    return yyparse();
}
