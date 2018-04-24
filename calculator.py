isOperator = lambda operator : operator in '+-/*'

def do_operation(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    raise ValueError('Mini Dundo')

def evaluate_postfix(expression):
    operators = expression.split(' ')
    stack = []
    for operator in operators:
        if isOperator(operator):
            if len(stack) < 2:
                raise ValueError('Dundo')
            num2 = stack.pop()
            num1 = stack.pop()
            stack.append(do_operation(num1, num2, operator))
        else:
            try:
                stack.append(int(operator))
            except:
                raise ValueError('Super Dundo')
    return stack.pop()

print("Enter an expression")
expression = input()
print(evaluate_postfix(expression))