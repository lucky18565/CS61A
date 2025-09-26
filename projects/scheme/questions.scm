(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Problem 15
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 15
  (define (helper s idx)
    (if (null? s)
        '()
        (cons (list idx (car s))
              (helper (cdr s) (+ idx 1)))))
  (helper s 0)
  )
  ; END PROBLEM 15

;; Problem 16

;; Merge two lists S1 and S2 according to ORDERED? and return
;; the merged lists.
(define (merge ordered? s1 s2)
  ; BEGIN PROBLEM 16
  (cond ((and (null? s1) (null? s2))nil)
        ((null? s1) s2)
        ((null? s2) s1)
        ((ordered? (car s1)(car s2))
         (cons (car s1) (merge ordered? (cdr s1) s2)))
        ((ordered? (car s2)(car s1))
         (cons (car s2) (merge ordered? s1 (cdr s2))))
        (else ((cons (car s1) (merge ordered? (cdr s1) s2))))
    )
  )
  ; END PROBLEM 16

;; Optional Problem 2

;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN OPTIONAL PROBLEM 2
          expr
         ; END OPTIONAL PROBLEM 2
         )
        ((quoted? expr)
         ; BEGIN OPTIONAL PROBLEM 2
         (quote expr)
         ; END OPTIONAL PROBLEM 2
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
           (cons form (cons params body)))
           ; END OPTIONAL PROBLEM 2
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
           (let (zipped (zip values))
                (params (car zipped))
                (vals   (cadr zipped)))
                (list (list 'lambda (params body)) vals))
           ; END OPTIONAL PROBLEM 2
           ))
        (else
         ; BEGIN OPTIONAL PROBLEM 2
         (map let-to-lambda expr)
         ; END OPTIONAL PROBLEM 2
         )

; Some utility functions that you may find useful to implement for let-to-lambda

;; Utility function for let-to-lambda
(define (zip pairs)
  (if (or (null? pairs) (null? (car pairs)))
      nil
      (cons (map car pairs)
            (zip (map cdr pairs)))))
;; 这样 zip 就能处理每个子列表有任意多个元素的情况
