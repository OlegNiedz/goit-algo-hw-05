from functools import reduce
from typing import Callable
import re
def generator_numbers(text: str):
    numbers=map(float,filter(lambda x: re.match(r"\d+[\.,]{0,1}\d+.",x),text.split(" ")))
    for number in numbers:
        yield number

def sum_profit(text: str, func: Callable):
    return reduce(lambda x,y:x+y ,func(text))

def main():
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    print(f'{text} =>')
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")

if __name__=="__main__":
    main()
    
