import goto


def test_jump_back():
    @goto.goto
    def factorial(n):
        total = 1
        factorial.label("loop")
        total *= n
        n -= 1
        if n > 0:
            factorial.goto("loop")
        return total

    assert factorial(5) == 120


def test_jump_forward():
    @goto.goto
    def jmp():
        x = 0
        jmp.goto("end")
        x = 1
        jmp.label("end")
        return x

    assert jmp() == 0
