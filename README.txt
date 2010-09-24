This project is an implementation of the metacircular evaluator for scheme in python.
The idea of the project was taken from 'SICP'(Structural Interpretation of Computer Programming) where the Metacircular evaluator for scheme is implemented.
The project evaluates some of the common features of scheme in python and the environement concepts are included.

USING pyscheme_eval:
Execute the python script and you will obtain a prompt as follows:
scheme>>>
Enter the scheme statements at each prompt: For example,
      ( + 4 5 )
      ( define n 6 )
      ( define n 8 )
      ( * n s )
      ( if ( > n s ) ( - n s ) ( - s n ) )
You could also implement functions like :
      ( define ( square ( lambda ( x ) ( * x x ) ) ) ) 
      ( square 5 )

You can also implement recursive functions as follows:
      ( define ( fac ( lambda ( x ) ( if ( = x 1 ) 1 ( * x fac ( - x 1 ) ) ) ) ) )  
This is a function to implement the factorial of a number.
and call the function as follows:
      ( fac 6 )

CTRL-D would cause to exit from the prompt.

