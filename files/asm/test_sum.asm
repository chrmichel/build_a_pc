/* program that sums up all numbers from 1
up to R0 into R1*/

# puts 46 into R0 first
@46
D=A
@R0
M=D
(LOOP)
@i
DM=M+1
@R1
M=D+M
@R0
D=M-D # D is n-i
@LOOP
D;JGT # jump if n-i>0 <=> i<n