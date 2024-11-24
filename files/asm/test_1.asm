# bootstrap
@256
D=A
@SP
M=D
# push constant 5
@5
D=A
@SP
AM=M+1
A=A-1
M=D
# push constant 12
@12
D=A
@SP
AM=M+1
A=A-1
M=D
# add
@SP
AM=M-1
D=M
A=A-1
M=D+M
# push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D
# eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@EQ_LBL_1
D;JEQ
@SP
A=M-1
M=0
(EQ_LBL_1)
# if-goto
@SP
AM=M-1
D=M
@CORRECT
D;JNE
# push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
(CORRECT)
# push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D