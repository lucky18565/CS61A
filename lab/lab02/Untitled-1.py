def f(x):
    if x == 0:
         return "zero"
    elif x > 0:
        return "positive"
    else:
        return ""
print(f(-1))
print(0 or f(1))