#!/usr/bin/env python3

from hamming_code import HammingCode
from stack_machine import *
from robot import *

jarvis=Robot()
hamming_correction=HammingCode()
operation=StackMachine()

def run():
     start_or_stop=jarvis.start_robot()
     i=0
     while start_or_stop==1:
        while jarvis.read_value()<294:
            i+=1
            if i!=1:
                jarvis.sensor_step(8,1)
                hamming_and_stack()
            else:
                hamming_and_stack()
            jarvis.scroll_step()
        else:
            temp=jarvis.start_robot()
            ev3.Sound.speak("Insert next card and press the touch sensor.")
            while temp!=1:
                temp=jarvis.start_robot()
            run()
     else:
        temp=jarvis.start_robot()
        ev3.Sound.speak("Insert card and press the touch sensor.")
        while temp!=1:
            temp=jarvis.start_robot()
        run()

def read_line():
    sensor_value=[]
    code_word=[]
    for i in range(0,11):
        jarvis.sensor_step(120,0.5)
        time.sleep(0.25)
        value_temp=jarvis.read_value()
        sensor_value.append(value_temp)
    jarvis.sensor_reset()
    for i in sensor_value:
            if i>230:
                code_word.append(0)
            else:
                code_word.append(1)
    return code_word

def hamming_and_stack():
    k=0
    print("--------------------------------------------------------------------------")
    code_word=read_line()
    print("Code word is:", code_word)
    source_code=hamming_correction.decode(tuple(code_word))
    while source_code[0]==None:
        k+=1
        if k>1:
            ev3.Sound.tone([(200, 100, 100), (500, 200)])
            ev3.Sound.speak("Uncorrectable error again. Aborting the program")
            operation.stack=[]
            print("Emptied the stack. Top of stack is", operation.top())
            time.sleep(10)
            run()
        else:
            jarvis.sensor_step(55,0.5)
            ev3.Sound.tone([(200, 100, 100), (500, 200)])
            ev3.Sound.speak("Uncorrectable error. Trying again")
            code_word=read_line()
            print("Rescanned code word is:", code_word)
            source_code=hamming_correction.decode(tuple(code_word))
    print ("Source code is:", source_code)
    try:
        operation.do(tuple(source_code[0]))
    except RangeError as r:
        ev3.Sound.tone([(200, 100, 100), (500, 200)])
        ev3.Sound.speak("Not enough items. Aborting the program.")
        operation.stack=[]
        print("Emptied the stack. Top of stack is", operation.top())
        time.sleep(10)
        run()    
    except ZeroDivisionError as z:
        ev3.Sound.tone([(200, 100, 100), (500, 200)])
        ev3.Sound.speak("Zero Division Error occured. Aborting the program.")
        operation.stack=[]
        print("Emptied the stack. Top of stack is", operation.top())
        time.sleep(10)
        run()        
    except HexConversionError as h:
        ev3.Sound.tone([(200, 100, 100), (500, 200)])
        ev3.Sound.speak("Invalid range for hexadecimal. Aborting the program.")
        operation.stack=[]
        print("Emptied the stack. Top of stack is", operation.top())
        time.sleep(10)
        run()
    except ValueError as v:
        ev3.Sound.tone([(200, 100, 100), (500, 200)])
        ev3.Sound.speak("Value error occured. Aborting the program.")
        operation.stack=[]
        print("Emptied the stack. Top of stack is", operation.top())
        time.sleep(10)
        run()    
    else:
        for instruction in Instruction:
            if instruction.value == tuple(source_code[0]):
                print(f"Instruction: {instruction.name}")
                if tuple(source_code[0])==(0, 1, 0, 0, 0, 0):
                    ev3.Sound.speak("STP detected. Emptying the stack.")
                    operation.stack=[]
                    print("Emptied the stack. Top of stack is", operation.top())
                    time.sleep(10)
                    run()
    print ("Top of stack is", operation.top())

if __name__ == '__main__':
    run()
