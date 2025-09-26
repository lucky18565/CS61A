(define (over-or-under num1 num2) 
  'YOUR-CODE-HERE
  (cond ((< num1 num2) -1)
        ((= num1 num2) 0)
        ((> num1 num2) 1))
)        
(define (make-adder num) 
'YOUR-CODE-HERE
  (define(add inc) (+ num inc))
  add
)

(define (composed f g) 
'YOUR-CODE-HERE
  (define(call x) (f (g x)))
  call
)

(define (repeat f n) 
'YOUR-CODE-HERE
  (define(call_two x) 
  (if (= n 1)
      (f x)
      ((composed f (repeat f (- n 1))) x)))
  call_two
  )
(define (repeat f n)
  (if (= n 1)
      f
      (lambda (x) ((composed f (repeat f (- n 1))) x))))


(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b) 
'YOUR-CODE-HERE
  (if (zero? b)
      a
      (gcd b (modulo a b)))
)
