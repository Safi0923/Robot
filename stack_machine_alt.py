#!/usr/bin/env python3
from enum import IntEnum, Enum
from typing import List, Tuple, Union
from ctypes import c_ubyte

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1
    STOPPED = 0
    ERROR = -1

class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack = []
        
    def is_empty(self):
        stack=self.stack
        if len(stack)==0:
            raise RangeError("Stack is empty. Ending the execution")
        
    def execute(self, code_word):
        stack=self.stack
        if code_word==Instruction.STP.value:
            return SMState.STOPPED
        elif code_word==Instruction.DUP.value:
            self.is_empty()
            operand_popped=stack.pop()
            stack.append(operand_popped)
            stack.append(operand_popped)
            return SMState.RUNNING
        elif code_word==Instruction.DEL.value:
            self.is_empty()
            stack.pop()
            return SMState.RUNNING
        elif code_word==Instruction.SWP.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            stack.append(operand1_popped)
            stack.append(operand2_popped)
            return SMState.RUNNING
        elif code_word==Instruction.ADD.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_sum=operand1_popped.value+operand2_popped.value
                if operand_sum>255:
                    self.overflow=True
                else:
                    self.overflow=False
                print ("Overflow is",self.overflow)
                stack.append(c_ubyte(operand_sum))           
                return SMState.RUNNING
        elif code_word==Instruction.SUB.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_sub=operand2_popped.value-operand1_popped.value
                if operand_sub<0:
                    self.overflow=True
                else:
                    self.overflow=False
                print ("Overflow is",self.overflow)
                stack.append(c_ubyte(operand_sub))
                return SMState.RUNNING
        elif code_word==Instruction.MUL.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_mul=operand1_popped.value * operand2_popped.value
                if operand_mul>255:
                    self.overflow=True
                else:
                    self.overflow=False
                print ("Overflow is",self.overflow)
                stack.append(c_ubyte(operand_mul))
                return SMState.RUNNING
        elif code_word==Instruction.DIV.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                if operand1_popped==0:
                    raise ZeroDivisionError("Cannot divide by zero")
                else:
                    operand_div=operand2_popped.value // operand1_popped.value
                    self.overflow=False
                    print ("Overflow is",self.overflow) 
                    stack.append(c_ubyte(operand_div))
                    return SMState.RUNNING
        elif code_word==Instruction.EXP.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_exp=operand2_popped.value ** operand1_popped.value
                if operand_exp>255:
                    self.overflow=True
                else:
                    self.overflow=False
                print ("Overflow is",self.overflow)
                stack.append(c_ubyte(operand_exp))
                return SMState.RUNNING
        elif code_word==Instruction.MOD.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_mod=operand2_popped.value % operand1_popped.value
                self.overflow=False
                print ("Overflow is",self.overflow) 
                stack.append(c_ubyte(operand_mod))
                return SMState.RUNNING
        elif code_word==Instruction.SHL.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_shl=operand2_popped.value << operand1_popped.value
                if operand_shl>255:
                    self.overflow=True
                else:
                        self.overflow=False
                print ("Overflow is",self.overflow) 
                stack.append(c_ubyte(operand_shl))
                return SMState.RUNNING
        elif code_word==Instruction.SHR.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_shr=operand2_popped.value >> operand1_popped.value
                self.overflow=False
                print ("Overflow is",self.overflow) 
                stack.append(c_ubyte(operand_shr))
                return SMState.RUNNING
        elif code_word==Instruction.HEX.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            operand1=str(operand1_popped.value) \
            if isinstance(operand1_popped, c_ubyte) else operand1_popped
            operand2=str(operand2_popped.value) \
            if isinstance(operand2_popped, c_ubyte) else operand2_popped
            operands= operand1 + operand2
            try:
                operand_hex = int(operands, 16)
            except ValueError:
                raise HexConversionError(f"Failed to convert '{operands}' to hexadecimal")
            if operand_hex<255:
                self.overflow=False
                print ("Overflow is",self.overflow) 
                stack.append(c_ubyte(operand_hex))
                return SMState.RUNNING
            else:
                raise HexConversionError(f"Failed to convert '{operands}' to hexadecimal")
        elif code_word==Instruction.FAC.value:
            self.is_empty()
            operand_popped=stack.pop()
            if type(operand_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_fact = 1
                for i in range(1, operand_popped.value + 1):
                    operand_fact *= i
                if operand_fact>255:
                    self.overflow=True
                else:
                    self.overflow=False
                print ("Overflow is",self.overflow)
                stack.append(c_ubyte(operand_fact))
                return SMState.RUNNING
        elif code_word==Instruction.NOT.value:
            self.is_empty()
            operand_popped=stack.pop()
            if type(operand_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand_popped_binary=bin(operand_popped.value)[2:]
                operand_popped_binary= list(operand_popped_binary.zfill(8))
                operand_not_binary=''.join('0' if bit == '1' else '1' for bit in operand_popped_binary)
                operand_not=int(operand_not_binary,2)
                self.overflow=False
                print ("Overflow is",self.overflow) 
                stack.append(c_ubyte(operand_not))
                return SMState.RUNNING
        elif code_word==Instruction.XOR.value:
            self.is_empty()
            operand1_popped=stack.pop()
            self.is_empty()
            operand2_popped=stack.pop()
            if type(operand1_popped)!=c_ubyte or type(operand2_popped)!=c_ubyte:
                    raise ValueError("Value error occured")
            else:
                operand1_binary=bin(operand1_popped.value)[2:]
                operand2_binary=bin(operand2_popped.value)[2:]
                length=max(len(operand1_binary), len(operand2_binary))
                operand1_binary_str=operand1_binary.zfill(length)
                operand2_binary_str=operand2_binary.zfill(length)
                operand_xor_binary=''.join ('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(operand1_binary_str, operand2_binary_str))
                operand_xor=int(operand_xor_binary,2)
                self.overflow=False
                print ("Overflow is",self.overflow) 
                stack.append(c_ubyte(operand_xor))
                return SMState.RUNNING
    
    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute
        Returns:
            SMState: Current state of the stack machine
        """
        stack=self.stack
        if code_word[:2]==(0,0):
            string = ''.join(map(str, list(code_word[2:6])))
            number = int(string, 2)
            stack.append(c_ubyte(number))
            return SMState.RUNNING
        elif code_word[:2]==(1,0) or code_word[:2]==(1,1):
            if code_word!= Character.SPEAK.value:
                if code_word == Character.NOP1.value:
                    return SMState.RUNNING
                elif code_word == Character.NOP2.value:
                    return SMState.RUNNING
                elif code_word == Character.NOP3.value:
                    return SMState.RUNNING
                elif code_word == Character.NOP4.value:
                    return SMState.RUNNING
                elif code_word == Character.WHITESPACE.value:
                    stack.append(" ")
                    return SMState.RUNNING
                elif code_word == Character.A.value:
                    stack.append("A")
                    return SMState.RUNNING
                elif code_word == Character.B.value:
                    stack.append("B")
                    return SMState.RUNNING
                elif code_word == Character.C.value:
                    stack.append("C")
                    return SMState.RUNNING
                elif code_word == Character.D.value:
                    stack.append("D")
                    return SMState.RUNNING
                elif code_word == Character.E.value:
                    stack.append("E")
                    return SMState.RUNNING
                elif code_word == Character.F.value:
                    stack.append("F")
                    return SMState.RUNNING
                elif code_word == Character.G.value:
                    stack.append("G")
                    return SMState.RUNNING
                elif code_word == Character.H.value:
                    stack.append("H")
                    return SMState.RUNNING
                elif code_word == Character.I.value:
                    stack.append("I")
                    return SMState.RUNNING
                elif code_word == Character.J.value:
                    stack.append("J")
                    return SMState.RUNNING
                elif code_word == Character.K.value:
                    stack.append("K")
                    return SMState.RUNNING
                elif code_word == Character.L.value:
                    stack.append("L")
                    return SMState.RUNNING
                elif code_word == Character.M.value:
                    stack.append("M")
                    return SMState.RUNNING
                elif code_word == Character.N.value:
                    stack.append("N")
                    return SMState.RUNNING
                elif code_word == Character.O.value:
                    stack.append("O")
                    return SMState.RUNNING
                elif code_word == Character.P.value:
                    stack.append("P")
                    return SMState.RUNNING
                elif code_word == Character.Q.value:
                    stack.append("Q")
                    return SMState.RUNNING
                elif code_word == Character.R.value:
                    stack.append("R")
                    return SMState.RUNNING
                elif code_word == Character.S.value:
                    stack.append("S")
                    return SMState.RUNNING
                elif code_word == Character.T.value:
                    stack.append("T")
                    return SMState.RUNNING
                elif code_word == Character.U.value:
                    stack.append("U")
                    return SMState.RUNNING
                elif code_word == Character.V.value:
                    stack.append("V")
                    return SMState.RUNNING
                elif code_word == Character.W.value:
                    stack.append("W")
                    return SMState.RUNNING
                elif code_word == Character.X.value:
                    stack.append("X")
                    return SMState.RUNNING
                elif code_word == Character.Y.value:
                    stack.append("Y")
                    return SMState.RUNNING
                elif code_word == Character.Z.value:
                    stack.append("Z")
                    return SMState.RUNNING
            elif code_word==Character.SPEAK.value:
                self.is_empty()
                l=stack.pop()
                speak_output=""
                for i in range(0,l.value):
                    self.is_empty()
                    popped_value=stack.pop()
                    popped_value_str=str(popped_value.value) \
                    if isinstance(popped_value, c_ubyte) else popped_value
                    speak_output+=popped_value_str
                print (speak_output)
                return SMState.RUNNING
        elif code_word[:2]==(0,1):
            return(self.execute(code_word))

    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack.

        Returns:
            union: Can be tuple, str or None
        """
        stack=self.stack
        if len(stack)!=0:
            if type(stack[len(stack)-1])==c_ubyte:
                temp=bin(stack[len(stack)-1].value)[2:]
                value = list(temp.zfill(8))
                int_values = [int(bit) for bit in value]
                return tuple(int_values)
            elif type(stack[len(stack)-1])==str:
                return stack[len(stack)-1]
        else:
                return None

class Instruction(Enum):
    STP = (0, 1, 0, 0, 0, 0)
    DUP = (0, 1, 0, 0, 0, 1)
    DEL = (0, 1, 0, 0, 1, 0)
    SWP = (0, 1, 0, 0, 1, 1)
    ADD = (0, 1, 0, 1, 0, 0)
    SUB = (0, 1, 0, 1, 0, 1)
    MUL = (0, 1, 0, 1, 1, 0)
    DIV = (0, 1, 0, 1, 1, 1)
    EXP = (0, 1, 1, 0, 0, 0)
    MOD = (0, 1, 1, 0, 0, 1)
    SHL = (0, 1, 1, 0, 1, 0)
    SHR = (0, 1, 1, 0, 1, 1)
    HEX = (0, 1, 1, 1, 0, 0)
    FAC = (0, 1, 1, 1, 0, 1)
    NOT = (0, 1, 1, 1, 1, 0)
    XOR = (0, 1, 1, 1, 1, 1)

class Character(Enum):
    NOP1 = (1, 0, 0, 0, 0, 0)
    SPEAK = (1, 0, 0, 0, 0, 1)
    WHITESPACE = (1, 0, 0, 0, 1, 0)
    NOP2 = (1, 0, 0, 0, 1, 1)
    A = (1, 0, 0, 1, 0, 0)
    B = (1, 0, 0, 1, 0, 1)
    C = (1, 0, 0, 1, 1, 0)
    D = (1, 0, 0, 1, 1, 1)
    E = (1, 0, 1, 0, 0, 0)
    F = (1, 0, 1, 0, 0, 1)
    G = (1, 0, 1, 0, 1, 0)
    H = (1, 0, 1, 0, 1, 1)
    I = (1, 0, 1, 1, 0, 0)
    J = (1, 0, 1, 1, 0, 1)
    K = (1, 0, 1, 1, 1, 0)
    L = (1, 0, 1, 1, 1, 1)
    M = (1, 1, 0, 0, 0, 0)
    N = (1, 1, 0, 0, 0, 1)
    O = (1, 1, 0, 0, 1, 0)
    P = (1, 1, 0, 0, 1, 1)
    Q = (1, 1, 0, 1, 0, 0)
    R = (1, 1, 0, 1, 0, 1)
    S = (1, 1, 0, 1, 1, 0)
    T = (1, 1, 0, 1, 1, 1)
    U = (1, 1, 1, 0, 0, 0)
    V = (1, 1, 1, 0, 0, 1)
    W = (1, 1, 1, 0, 1, 0)
    X = (1, 1, 1, 0, 1, 1)
    Y = (1, 1, 1, 1, 0, 0)
    Z = (1, 1, 1, 1, 0, 1)
    NOP3 = (1, 1, 1, 1, 1, 0)
    NOP4 = (1, 1, 1, 1, 1, 1)

class RangeError(Exception):
    pass

class HexConversionError(Exception):
    pass