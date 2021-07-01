"""
Human, Driver, Human Driver

Joshua Cheung
2021-06-30

https://www.facebook.com/llamatar/posts/2959761054262301

Human, Driver, Human Driver
What follows is the result of a real conversation had during a car ride. I spent some extra time thinking about it and came up with this.

If you are human, you are "human".
If you drive, you are a "driver".
If you drive a human, you are a "human driver".
If you drive a driver, you are a "driver driver". This can be expanded indefinitely because every "driver^n" for n >= 1 is also a valid driver. 
For example, a "driver driver driver" is someone who drives someone who drives someone who drives. 
In fact, that someone could be the exact same person because you are a driver who drives yourself, making you also a driver driver, and so on.

If you are human and a driver, you are a "human driver".
If you are human and drive a human, you are a "human human driver". 
Note, however, that you cannot be a "human human human driver". 
That would be a human who drives a "human human", and while technically "human human" is the adjective "human" modifying the noun "human", I consider it to be invalid.

If you drive a human human driver, you are a "human human driver driver". 
If you are also human, you are a "human human human driver driver".
The pattern is that one "driver" is necessary for every "human" except one. 
This can be expanded indefinitely because every "human^m driver^n" for 0 <= m <= n+1 and n >= 1 is also a valid driver. 
Additionally, the case where (m,n) = (1,0), "human", is a valid sole human. 
For example, a "human human human human driver driver driver" is a human who drives a "human human human driver driver", 
which we have already previously established is a human who drives a "human human driver", which is a human who drives a human.
When there are more "driver"s than "human"s, it is as the "driver^n" case with some "human"s omitted.

Let's take it one step further.
Just for fun, let's say that you can describe a noun "human" with the entire driver expression. 
That is, you can be a "driver human", which is a human who is a driver, or you can be a "human driver human", which is a human who drives a human. 
However, just as you can't be a "human human human driver", you cannot be a "human human driver human" because that would be a human who drives a "human human". 
In other words, this is just taking the adjective "human" from the left side and putting the noun "human" on the right side. 
As such, we now have every "human^m driver^n human^p" for 0 <= m <= n+1-p, n >= 1, and 0 <= p <= 1 as valid objects, 
in addition to the sole "human" case which can be represented as either (m,n,p) = (1,0,0) or (0,0,1).

Since you can now drive a "human driver human", you can also be a "human driver human driver"...

Aaaand it's at this point that I realized that we've been manually treading through the territory of context-free grammar 
and should use EBNF notation rather than my weird string exponentiation stuff. 
I only had one brief lecture about this a year and a half ago, so this attempt might be totally off, but as far as I can tell, it is consistent.
It turns out that all these shenanigans can be summed up with just 2 definitions. 
Square brackets denote optional expressions, the pipe symbol denotes choice between the expressions on either side, 
and the quotation marks distinguish string characters from referential definitions.

EBNF Description: human
human = ["human"] driver | [driver] "human"
driver = ["human"] [driver] "driver"

TL;DR If you are human and a driver, you are much more than just a human driver!
"""

from functools import cache
from typing import Generator


def generate_human_driver_iterative_dict(max_drivers: int) -> dict[tuple[int, int, int], str]:
    """Returns a dict of (m, n, p) tuples to corresponding human driver strings."""
    return { (m, n, p): generate_human_driver_string(m, n, p) 
        for n in irange(0, max_drivers) # n has no theoretical upper bound, so it is capped by the given value
        for p in (0, 1)
        for m in irange(0, n+1-p)
    }


def generate_human_driver_ebnf_tree(steps: int) -> list:
    """Returns a variable-dimensional list of human driver strings via EBNF rules."""
    return human(steps, 0, 0, 0)


@cache
def human(steps: int, m: int, n: int, p: int) -> list or tuple[int, int, int]:
    """Implementation of EBNF definition: human = ['human'] driver | [driver] 'human'"""
    if(steps == 0): return (m, n, p)

    return [driver(steps-1, m, n, p)    # <driver>
        , driver(steps-1, m+1, n, p)    # 'human' <driver>
        , (m, n, p+1)                   # 'human'
        , driver(steps-1, m, n, p+1)    # <driver> 'human'
    ]


@cache
def driver(steps: int, m: int, n: int, p: int) -> list or tuple[int, int, int]:
    """Implementation of EBNF definition: driver = ['human'] [driver] 'driver'"""
    if(steps == 0): return (m, n, p)

    return [(m, n+1, p)                 # 'driver'    
        , driver(steps-1, m, n+1, p)    # <driver> 'driver'
        , (m+1, n+1, p)                 # 'human' 'driver'
        , driver(steps-1, m+1, n+1, p)  # 'human' <driver> 'driver'
    ]


def generate_human_driver_string(m: int, n: int, p: int) -> str:
    """Returns a string of m human, n driver, and p human."""
    return ' '.join(['human' for _ in range(m)] 
                    + ['driver' for _ in range(n)] 
                    + ['human' for _ in range(p)]
    )


def print_dict(dict_to_print: dict) -> None:
    """Prints each key-value pair of the given dict."""
    for k, v in sorted(dict_to_print.items()):
        print(f'{k}: {v}')


def print_set(set_to_print: set) -> None:
    """Prints each (m, n, p) tuple and the corresponding human driver string."""
    for element in sorted(set_to_print):
        print(f'{element}: {generate_human_driver_string(element[0], element[1], element[2])}')


def get_unique_elements(tree: list) -> set:
    """Returns a set with the elements of tree."""
    element_set = set()
    flatten_tree(element_set, tree)
    return element_set


def flatten_tree(element_set: set, tree: list) -> None:
    """Recursively flattens the variable-dimensional tree into a 1D set."""
    if(type(tree) == tuple):
        element_set.add(tree)
    else:
        for element in tree:
            flatten_tree(element_set, element)


def irange(start: int, stop: int, step: int = 1) -> Generator:
    """Returns a range generator with inclusive endpoint."""
    return range(start, stop+1, step)


if __name__ == '__main__':
    max_drivers = 3
    
    # get user input for max_drivers
    try:
        user_input = int(input('Please input the max number of drivers (anything greater than 20 will take a while to run): '))

        if(user_input < 0):
            raise ValueError
        elif(user_input > 20):
            print("You've been warned... Press Ctrl+C to quit while the program is still running.")

        max_drivers = user_input
    except ValueError:
        print('Invalid input. Defaulting to max_drivers=3')
    print()

    # generate a list of human driver strings based on iteration and transform it into a set 
    human_driver_iterative_dict = generate_human_driver_iterative_dict(max_drivers)
    dict_set = set(human_driver_iterative_dict.keys())
    dict_set.remove((0,0,0))    # special case: empty string
    dict_set.remove((1,0,0))    # special case: "human"

    # generate a tree of human driver strings based on EBNF rules and transform it into a set 
    human_driver_ebnf_tree = generate_human_driver_ebnf_tree(max_drivers+2)
    element_set = get_unique_elements(human_driver_ebnf_tree)
    max_drivers_set = {element for element in element_set if element[1] <= max_drivers} # filter out elements with more drivers than max_drivers
    
    print(f'human_driver_iterative_dict: {max_drivers=}')
    print_dict(human_driver_iterative_dict)
    print()

    # determine if the two sets of human driver strings have any differences
    diff = dict_set ^ max_drivers_set
    if(len(diff) == 0 or max_drivers == 0):
        print('no differences between iterative version and EBNF version except the special cases (0, 0, 0) and (1, 0, 0)')
    else:
        print('human_driver_ebnf_tree')
        print_set(max_drivers_set)
        print()
        
        print('diff')
        print(sorted(diff))
    print()

    

    