(define (ascending? s) 
'YOUR-CODE-HERE
    (if (or(null? s) (null? (cdr s)))
        #t
        (if(>= (car(cdr s)) (car s))
        (ascending? (cdr s))
        #f)
    )
)

(define (my-filter pred s) 
'YOUR-CODE-HERE
    (if (null? s)
        nil
        (if (pred (car s))
        (cons (car s) (my-filter pred (cdr s)))
        (my-filter pred (cdr s)))
    )
)
(define (interleave lst1 lst2) 
'YOUR-CODE-HERE
    (if (null? lst2)
        lst1
        (if (null? lst1)
            lst2
            (cons(car lst1)(interleave lst2 (cdr lst1)))
        )
    )
)

(define (no-repeats s) 
'YOUR-CODE-HERE
    (if(null? s)
        nil
        (cons (car s)
        (no-repeats(my-filter(lambda (x) (not(= x (car s)))) (cdr s))))
    )  
)
