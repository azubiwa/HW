#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def read_devide(line, index):
    token = {'type': 'DEVIDE'}
    return token, index + 1

def read_open_parenthesis(line, index):
    token = {'type': 'OPEN_PAREN'}
    return token, index + 1

def read_close_parenthesis(line, index):
    token = {'type': 'CLOSE_PAREN'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_devide(line, index)
        elif line[index] == '(':
            (token, index) = read_open_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_close_parenthesis(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate_times_and_devide(tokens):
    return_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'TIMES':
            last_num = return_tokens.pop(-1)['number']
            number = last_num * tokens[index+1]['number']
            token = {'type': 'NUMBER', 'number': number}
            index += 1
        elif tokens[index]['type'] == 'DEVIDE':
            last_num = return_tokens.pop(-1)['number']
            number = last_num / tokens[index+1]['number']
            token = {'type': 'NUMBER', 'number': number}
            index += 1
        else:
            token = tokens[index]
        return_tokens.append(token)
        index += 1
    return return_tokens


def evaluate_parenthesis(tokens, index):
    return_tokens = []
    index -= 1
    while tokens[index]['type'] != 'OPEN_PAREN':
        return_tokens.insert(0, tokens[index])
        index -= 1
    return return_tokens


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens = evaluate_times_and_devide(tokens)
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
        index += 1
    return answer


def syntax(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index - 1]['type'] == 'NUMBER' and tokens[index]['type'] == 'NUMBER':
            print('Invalid syntax: consecutive numbers')
            exit(1)
        if tokens[index - 1]['type'] != 'NUMBER' and tokens[index - 1]['type'] != 'NUMBER':
            print('Invalid syntax: consecutive operators')
            exit(1)
        # かっこの不正を追加したい
        index += 1


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("2*3")
    test("3/4")
    test("2+3*4+5")
    test("1.0+2.0*3.5/4-2.1")
    # test("(1+2)*(4-3)")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)