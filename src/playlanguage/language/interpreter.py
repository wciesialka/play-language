import playlanguage.language.tokenizer as tokenizer
import playlanguage.language.tokens as tokens
import logging

def interpret(program:str):
    logging.info("Building program.")
    stack = []
    condition = True
    conditional_stack = []
    reader = tokenizer.Tokenizer(stack)
    program = reader.read(program)

    for operation in program:
        if isinstance(operation,tokens.IfToken):
            conditional_stack.append(condition)
            condition = bool(stack[-1])
        elif isinstance(operation,tokens.EndIfToken):
            condition = conditional_stack.pop()
        else:
            if condition:
                value = operation()
                if not value is None:
                    print(value,end="")