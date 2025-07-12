def factorial(n):
    if n == 1:
        return 1
    
    return n * factorial(n-1)

def sum(n):
    if n == 1:
        return 1
    
    return n + sum(n - 1)

def display_asc(n):
    if n == 0:
        return
    
    display_asc(n - 1)
    print(n)

def display_desc(n):
    if n == 0:
        return
    
    print(n)
    display_desc(n - 1)

def reverse_string(string):
    if len(string) == 0:
        return string
    
    return reverse_string(string[1:]) + string[0]

print(factorial(5))
print(sum(5))
display_asc(5)
display_desc(5)
print(reverse_string("Tryzler"))
