import sys

class PrePro:
    @staticmethod
    def filter(source):
        lines = source.split('\n')
        filtered_lines = []
        for line in lines:
            if '--' in line:
                parts = line.split('--', 1)
                line = parts[0].rstrip()
            filtered_lines.append(line)
        return '\n'.join(filtered_lines)

class SymbolTable:
    def __init__(self):
        self.table = {}

    def get(self, identifier):
        if identifier in self.table:
            return self.table[identifier][0], self.table[identifier][1]
        else:
            raise ValueError(f"Variable '{identifier}' not defined")

    def set(self, identifier, value, vtype):
        self.table[identifier] = (value, vtype)

    def create(self, identifier):
        self.table[identifier] = (None, None)

class Node:
    def Evaluate(self, symbolTable):
        pass

class BinOp(Node):
    def __init__(self, left, op, right):
        self.children = [left, right]
        self.op = op

    def Evaluate(self, symbolTable):
        left_val, left_type = self.children[0].Evaluate(symbolTable)
        right_val, right_type = self.children[1].Evaluate(symbolTable)
        
        if left_type != right_type:
            raise TypeError(f"Cannot perform operation between {left_type} and {right_type}")
        
        if left_type == 'string' and right_type == 'string':
            if self.op == 'EQUAL':
                return (int(left_val == right_val)), "int"
            elif self.op == 'LESS':
                return (int(left_val < right_val)), "int"
            elif self.op == 'GREATER':
                return (int(left_val > right_val)), "int"
        if self.op == 'PLUS':
            return left_val + right_val, "int"
        elif self.op == 'MINUS':
            return left_val - right_val, "int"
        elif self.op == 'MULT':
            return left_val * right_val, "int"
        elif self.op == 'DIV':
            return left_val // right_val, "int"
        elif self.op == 'AND':
            return int(left_val and right_val), "int"
        elif self.op == 'OR':
            return int(left_val or right_val), 'int'
        elif self.op == 'EQUAL':
            return int(left_val == right_val), "int"
        elif self.op == 'LESS':
            return int(left_val < right_val), "int"
        elif self.op == 'GREATER':
            return int(left_val > right_val), "int"

class UnOp(Node):
    def __init__(self, op, child):
        self.op = op
        self.child = child

    def Evaluate(self, symbolTable):
        child_val, child_type = self.child.Evaluate(symbolTable)
        if child_type != "int":
            raise TypeError("Unary operations can only be applied to integers.")
        if self.op == 'PLUS':
            return +child_val, "int"
        elif self.op == 'MINUS':
            return -child_val, "int"
        elif self.op == 'NOT':
            return (int(not child_val)), "int"

class ReadOp(Node):
    def __init__(self):
        pass

    def Evaluate(self, symbolTable):
        value = input()
        try:
            return (int(value),'int')  # Tentativa de converter para inteiro
        except ValueError:
            return value  # Retorna como string se falhar

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbolTable):
        return (self.value, 'int')

class StringVal(Node):
    def __init__(self, value):
        self.value = value
    
    def Evaluate(self, symbolTable):
        return (self.value,'string')

class Assign(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def Evaluate(self, symbolTable):
        value = self.expression.Evaluate(symbolTable)
        symbolTable.set(self.identifier, value[0], value[1])

class VarVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, symbolTable):
        if isinstance(self.value, int):
            return (self.value, 'int')
        return symbolTable.get(self.value)

class PrintOp(Node):
    def __init__(self, expression):
        self.expression = expression

    def Evaluate(self, symbolTable):
        value = self.expression.Evaluate(symbolTable)
        print(value[0])

class If(Node):
    def __init__(self, children=None):
        if children is not None:
            self.children = children

    def Evaluate(self, symbolTable):
        condition = self.children[0].Evaluate(symbolTable)
        if condition[0]:
            self.children[1].Evaluate(symbolTable)
        elif len(self.children) > 2 and self.children[2]:
            self.children[2].Evaluate(symbolTable)

class Attack(Node):
    def __init__(self, attacker, target):
        self.attacker = attacker
        self.target = target

    def Evaluate(self, symbolTable):
        symbolTable.set(f"{self.attacker}_next_action", f"attack {self.target}", "string")

class Defend(Node):
    def __init__(self, character):
        self.character = character

    def Evaluate(self, symbolTable):
        symbolTable.set(f"{self.character}_next_action", "defend", "string")

class Move(Node):
    def __init__(self, character, direction):
        self.character = character
        self.direction = direction

    def Evaluate(self, symbolTable):
        symbolTable.set(f"{self.character}_next_action", f"move {self.direction}", "string")

class Statements(Node):
    def __init__(self):
        self.children = []

    def Evaluate(self, symbolTable):
        for child in self.children:
            if child:
                child.Evaluate(symbolTable)

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.selectNext()

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] in ' \t':
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF', '')
        else:
            if self.source[self.position] == '"':
                start = self.position
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] != '"':
                    self.position += 1
                if self.position >= len(self.source):
                    raise Exception('String opened but not closed')
                self.position += 1
                self.next = Token('STRING', self.source[start + 1:self.position - 1])
                return
            elif self.source[self.position].isdigit():
                num = ''
                while self.source[self.position].isdigit():
                    num += self.source[self.position]
                    self.position += 1
                self.next = Token('NUMBER', int(num))
                return
            elif self.source[self.position].isalpha() or self.source[self.position] == '_':
                ident = ''
                while self.source[self.position].isalnum() or self.source[self.position] == '_':
                    ident += self.source[self.position]
                    self.position += 1
                if ident == 'print':
                    self.next = Token('PRINT', ident)                
                elif ident == 'then':
                    self.next = Token('THEN', ident)
                elif ident == 'end':
                    self.next = Token('END', ident)
                elif ident == 'if':
                    self.next = Token('IF', ident)
                elif ident == 'else':
                    self.next = Token('ELSE', ident)
                elif ident == 'attack':
                    self.next = Token('ATTACK', ident)
                elif ident == 'defend':
                    self.next = Token('DEFEND', ident)
                elif ident == 'move':
                    self.next = Token('MOVE', ident)
                elif ident == 'char_a' or ident == 'char_b':
                    self.next = Token('CHARACTER', ident)
                else:
                    self.next = Token('IDENTIFIER', ident)
            elif self.source[self.position] == '=':
                self.next = Token('ASSIGN', '=')
                self.position += 1
                return
            elif self.source[self.position] == '<':
                self.next = Token('LT', '<')
                self.position += 1
                return
            elif self.source[self.position] == '>':
                self.next = Token('GT', '>')
                self.position += 1
                return
            elif self.source[self.position] == '+':
                self.next = Token('PLUS', '+')
                self.position += 1
                return
            elif self.source[self.position] == '-':
                self.next = Token('MINUS', '-')
                self.position += 1
                return
            elif self.source[self.position] == '*':
                self.next = Token('MULT', '*')
                self.position += 1
                return
            elif self.source[self.position] == '/':
                self.next = Token('DIV', '/')
                self.position += 1
                return
            elif self.source[self.position] == '(':
                self.next = Token('LPAREN', '(')
                self.position += 1
                return
            elif self.source[self.position] == ')':
                self.next = Token('RPAREN', ')')
                self.position += 1
                return
            elif self.source[self.position] == '\n':
                self.next = Token('NEWLINE', '\n')
                self.position += 1
                return
            else:
                raise ValueError(f"Unknown character: {self.source[self.position]}")

class Parser:
    @staticmethod
    def parseProgram(tokenizer):
        root = Statements()
        while tokenizer.next.type != 'EOF':
            if tokenizer.next.type == 'NEWLINE':
                tokenizer.selectNext()
            else:
                root.children.append(Parser.parseStatement(tokenizer))
        return root

    @staticmethod
    def parseStatement(tokenizer):
        if tokenizer.next.type == 'PRINT':
            tokenizer.selectNext()
            if tokenizer.next.type != 'LPAREN':
                raise SyntaxError("Expected '(' after 'print'")
            tokenizer.selectNext()
            expr = Parser.parseExpression(tokenizer)
            if tokenizer.next.type != 'RPAREN':
                raise SyntaxError("Expected ')' to close 'print'")
            tokenizer.selectNext()
            return PrintOp(expr)
        elif tokenizer.next.type == 'IF':
            tokenizer.selectNext()
            condition = Parser.parseBoolExpression(tokenizer)
            if tokenizer.next.type != 'THEN':
                raise SyntaxError("Expected 'then' after condition in if")
            tokenizer.selectNext()
            if tokenizer.next.type != 'NEWLINE':
                raise SyntaxError("Expected new line after 'then'")
            tokenizer.selectNext()
            then_body = Statements()
            else_body = None
            while tokenizer.next.type not in ['ELSE', 'END', 'EOF']:
                if tokenizer.next.type == 'NEWLINE':
                    tokenizer.selectNext()
                else:
                    then_body.children.append(Parser.parseStatement(tokenizer))
            if tokenizer.next.type == 'ELSE':
                tokenizer.selectNext()
                if tokenizer.next.type != 'NEWLINE':
                    raise SyntaxError("Expected new line after 'else'")
                tokenizer.selectNext()
                else_body = Statements()
                while tokenizer.next.type not in ['END', 'EOF']:
                    if tokenizer.next.type == 'NEWLINE':
                        tokenizer.selectNext()
                    else:
                        else_body.children.append(Parser.parseStatement(tokenizer))
            if tokenizer.next.type != 'END':
                raise SyntaxError("Expected 'end' to close 'if'")
            tokenizer.selectNext()
            if tokenizer.next.type != 'NEWLINE':
                raise SyntaxError("Expected new line after 'end'")
            tokenizer.selectNext()
            return If([condition, then_body, else_body])
        elif tokenizer.next.type == 'NEWLINE':
            tokenizer.selectNext()
            return None
        elif tokenizer.next.type == 'ATTACK':
            tokenizer.selectNext()
            if tokenizer.next.type != 'CHARACTER':
                raise SyntaxError("Expected character after 'attack'")
            attacker = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type != 'CHARACTER':
                raise SyntaxError("Expected character after attacker")
            target = tokenizer.next.value
            tokenizer.selectNext()
            return Attack(attacker, target)
        elif tokenizer.next.type == 'DEFEND':
            tokenizer.selectNext()
            if tokenizer.next.type != 'CHARACTER':
                raise SyntaxError("Expected character after 'defend'")
            character = tokenizer.next.value
            tokenizer.selectNext()
            return Defend(character)
        elif tokenizer.next.type == 'MOVE':
            tokenizer.selectNext()
            if tokenizer.next.type != 'CHARACTER':
                raise SyntaxError("Expected character after 'move'")
            character = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type not in ['up', 'down', 'right', 'left']:
                raise SyntaxError("Expected direction after character")
            direction = tokenizer.next.value
            tokenizer.selectNext()
            return Move(character, direction)
        elif tokenizer.next.type == 'CHARACTER':
            character = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type != 'ASSIGN':
                raise SyntaxError("Expected '=' after character")
            tokenizer.selectNext()
            expr = Parser.parseExpression(tokenizer)
            return Assign(character, expr)
        elif tokenizer.next.type == 'NEWLINE':
            tokenizer.selectNext()
            return None
        else:
            print(tokenizer.next.type, tokenizer.next.value)
            raise SyntaxError("Statement expected")

    @staticmethod
    def parseBoolExpression(tokenizer):
        result = Parser.parseBoolTerm(tokenizer)
        while tokenizer.next.type in ['OR']:
            if tokenizer.next.type == 'OR':
                tokenizer.selectNext()
                next_result = Parser.parseBoolTerm(tokenizer)
                result = BinOp(result, 'OR', next_result)
        return result
    
    @staticmethod
    def parseBoolTerm(tokenizer):
        result = Parser.parseRelExpression(tokenizer)
        while tokenizer.next.type in ['AND']:
            if tokenizer.next.type == 'AND':
                tokenizer.selectNext()
                next_result = Parser.parseRelExpression(tokenizer)
                result = BinOp(result, 'AND', next_result)
        return result
    
    @staticmethod
    def parseRelExpression(tokenizer):
        result = Parser.parseExpression(tokenizer)
        while tokenizer.next.type in ['EQ', 'LT', 'GT']:
            if tokenizer.next.type == 'EQ':
                tokenizer.selectNext()
                next_result = Parser.parseExpression(tokenizer)
                result = BinOp(result, 'EQUAL', next_result)
            elif tokenizer.next.type == 'LT':
                tokenizer.selectNext()
                next_result = Parser.parseExpression(tokenizer)
                result = BinOp(result, 'LESS', next_result)
            elif tokenizer.next.type == 'GT':
                tokenizer.selectNext()
                next_result = Parser.parseExpression(tokenizer)
                result = BinOp(result, 'GREATER', next_result)
        return result

    @staticmethod
    def parseExpression(tokenizer):
        result = Parser.parseTerm(tokenizer)
        while tokenizer.next.type in ['PLUS', 'MINUS']:
            if tokenizer.next.type == 'PLUS':
                tokenizer.selectNext()
                next_result = Parser.parseTerm(tokenizer)
                result = BinOp(result, 'PLUS', next_result)
            elif tokenizer.next.type == 'MINUS':
                tokenizer.selectNext()
                next_result = Parser.parseTerm(tokenizer)
                result = BinOp(result, 'MINUS', next_result)
        return result

    @staticmethod
    def parseTerm(tokenizer):
        result = Parser.parseFactor(tokenizer)
        while tokenizer.next.type in ['MULT', 'DIV']:
            if tokenizer.next.type == 'MULT':
                tokenizer.selectNext()
                next_result = Parser.parseFactor(tokenizer)
                result = BinOp(result, 'MULT', next_result)
            elif tokenizer.next.type == 'DIV':
                tokenizer.selectNext()
                next_result = Parser.parseFactor(tokenizer)
                result = BinOp(result, 'DIV', next_result)
        return result

    @staticmethod
    def parseFactor(tokenizer):
        if tokenizer.next.type == 'NUMBER':
            val = IntVal(tokenizer.next.value)
            tokenizer.selectNext()
            return val
        elif tokenizer.next.type == 'STRING':
            val = StringVal(tokenizer.next.value)
            tokenizer.selectNext()
            return val
        elif tokenizer.next.type == 'IDENTIFIER':
            var_name = tokenizer.next.value
            tokenizer.selectNext()
            return VarVal(var_name)
        elif tokenizer.next.type == 'LPAREN':
            tokenizer.selectNext()
            expr = Parser.parseExpression(tokenizer)
            if tokenizer.next.type != 'RPAREN':
                raise SyntaxError("Expected ')' after expression")
            tokenizer.selectNext()
            return expr
        else:
            raise SyntaxError("Factor expected")

    @staticmethod
    def run(source):
        source = PrePro.filter(source)
        tokenizer = Tokenizer(source)
        ast = Parser.parseProgram(tokenizer)
        symbolTable = SymbolTable()
        # Initialize character variables
        symbolTable.create("char_a_life")
        symbolTable.set("char_a_life", 100, "int")
        symbolTable.create("char_b_life")
        symbolTable.set("char_b_life", 100, "int")
        symbolTable.create("char_a_action")
        symbolTable.set("char_a_action", None, "string")
        symbolTable.create("char_b_action")
        symbolTable.set("char_b_action", None, "string")
        symbolTable.create("char_a_next_action")
        symbolTable.set("char_a_next_action", None, "string")
        symbolTable.create("char_b_next_action")
        symbolTable.set("char_b_next_action", None, "string")
        symbolTable.create("time")
        symbolTable.set("time", 0, "int")
        
        while symbolTable.get("time")[0] < 300:
            # Define next actions
            tokenizer = Tokenizer(source)
            ast.Evaluate(symbolTable)
            symbolTable.set("char_a_action", symbolTable.get("char_a_next_action")[0], "string")
            symbolTable.set("char_b_action", symbolTable.get("char_b_next_action")[0], "string")

            # Process actions
            char_a_action = symbolTable.get("char_a_action")[0]
            char_b_action = symbolTable.get("char_b_action")[0]

            if char_a_action == None:
                char_a_action = ""
            if char_b_action == None:
                char_b_action = ""
            if char_a_action == "defend" and char_b_action.startswith("attack"):
                symbolTable.set("char_a_life", symbolTable.get("char_a_life")[0], "int")
            elif char_b_action == "defend" and char_a_action.startswith("attack"):
                symbolTable.set("char_b_life", symbolTable.get("char_b_life")[0], "int")
            elif char_a_action == "move up" or char_a_action == "move down" or char_a_action == "move right" or char_a_action == "move left":
                pass
            elif char_b_action == "move up" or char_b_action == "move down" or char_b_action == "move right" or char_b_action == "move left":
                pass
            elif char_a_action.startswith("attack") and not char_b_action == "defend":
                symbolTable.set("char_b_life", symbolTable.get("char_b_life")[0] - 5, "int")
            elif char_b_action.startswith("attack") and not char_a_action == "defend":
                symbolTable.set("char_a_life", symbolTable.get("char_a_life")[0] - 5, "int")

            symbolTable.set("time", symbolTable.get("time")[0] + 1, "int")
            if symbolTable.get("char_a_life")[0] <= 0 or symbolTable.get("char_b_life")[0] <= 0:
                break
        
        # Print the result
        char_a_life = symbolTable.get("char_a_life")[0]
        char_b_life = symbolTable.get("char_b_life")[0]
        time = symbolTable.get("time")[0]

        if time == 300:
            if char_a_life > char_b_life and char_b_life > 0:
                print(f"Char A wins! Remaining char_a life: {char_a_life}.Remaining char_b life: {char_b_life}. Time: {time}s")
            elif char_b_life > char_a_life and char_a_life > 0:
                print(f"Char B wins! Remaining char_a life: {char_a_life}. Remaining char_b life: {char_b_life}. Time: {time}s")
            else:
                print(f"Draw! Both characters have {char_a_life} life remaining. Time: {time}s")
        else:
            if char_a_life > char_b_life:
                print(f"Char A wins! Remaining life: {char_a_life}. Time: {time}s")
            elif char_b_life > char_a_life:
                print(f"Char B wins! Remaining life: {char_b_life}. Time: {time}s")
            else:
                print(f"Draw! Both characters have {char_a_life} life remaining. Time: {time}s")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python script.py <file.txt>\n")
        sys.exit(1)
    
    filepath = sys.argv[1]
    with open(filepath, 'r') as file:
        code = file.read()

    Parser.run(code)
