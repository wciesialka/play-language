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
| % | Modulo | Pop two numbers from stack and push result of modulo operation onto stack. |
| & | Bitwise And | Pop two numbers from stack and push result of bitwise and onto stack. |
| \| | Bitwise Or | Pop two numbers from stack and push result of bitwise or onto stack. |
| ! | Not | Pop from the stack. If the value is greater than 0, push 0. Otherwise, push 1. |
| ~ | Negate | Pop from the stack and push the negative value onto the stack. |
| \( | If | If the top number is 1, continue. Otherwise, pass. |
| \) | End If | End If block. |
| \{ | Else | Begin else block. End with \) token. |
| = | Equality | Pop two numbers from the stack. If equal, push 1. Push 0 otherwise. |
| > | Greater Than | Pop two numbers from the stack. If the first number is greater than the second, push 1 onto the stack. Push 0 otherwise. |
| < | Less Than | Pop two numbers from the stack. If the first number is less than the second, push 1 onto the stack. Push 0 otherwise. |
| r | Return | Set return point. |
| j | Jump | Jump to return point. |
| q | Conditional Jump | Jump to return point if the top of the stack is not zero. |
| $ | Save | Save the top of the stack to the register.
| ^ | Load | Push the register to the top of the stack.

You can also enter string mode. While in string mode, you can type characters. Each character will generate a push operation with it's ord value. 
The following tokens are unique to string mode:

| Symbol | Name | Effect |
| ------ | ---- | ------ |
| "      | Quote | Enter/exit string mode. |
| \\     | Escape | Escape the next character (string mode only.) |

Additionally, you can enter comment mode. While in comment mode, nothing you write will generate tokens. Then following tokens are unique to comment mode:

| Symbol | Name | Effect |
| ------ | ---- | ------ |
| #      | Comment | Enter/Exit comment mode. |

Examples can be found in [examples/](examples/)