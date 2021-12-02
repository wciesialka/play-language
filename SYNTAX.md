# Syntax

The following are valid tokens:

| Symbol | Name | Effect |
| ------ | ---- |------ |
| int | Push | Push int onto stack. |
| . | Pop | Pop from top of stack. |
| , | Non-Op | Do nothing. |
| : | Peek | Peek at top of stack without popping it. |
| c | Char | Peek at top of stack as a character representation. |
| e | Empty | Empty the stack.
| ? | Clone | Push the value on top of stack onto stack. |
| + | Add | Pop two numbers from stack and push sum onto stack. |
| - | Subtract | Pop two numbers from stack and push difference onto stack. |
| * | Multiply | Pop two numbers from stack and push product onto stack. |
| / | Divide | Pop two numbers from stack and push (floor) quotient onto stack. |
| & | And | Pop two numbers from stack and push result of binary and onto stack. |
| \| | Or | Pop two numbers from stack and push result of binary or onto stack. |
| ! | Not | Pop from the stack. If the value is greater than 0, push 0. Otherwise, push 1. |
| ~ | Negate | Pop from the stack and push the negative value onto the stack. |
| \( | If | If the top number is 1, continue. Otherwise, pass. |
| \) | End If | End If block. |

Examples can be found in [examples/](examples/)