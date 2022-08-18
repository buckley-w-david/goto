from goto import goto

@goto
def loop_sum(limit):
    total = 0
    loop_sum.label("loop")
    total += limit
    limit -= 1
    if limit > 0:
        loop_sum.goto("loop")
    return total

print(loop_sum(5)) # 15

@goto
def jmp():
    jmp.goto("end")
    # There is an optimization that removes all "dead" code after a return
    # This breaks goto functionality, so you would have to do something like this
    if 1 == 1:
        return 0
    jmp.label("end")
    return 1

print(jmp())
