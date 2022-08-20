import goto


def test_jump_back():
    @goto.goto
    def loop_sum(limit):
        total = 0
        loop_sum.label("loop")
        total += limit
        limit -= 1
        if limit > 0:
            loop_sum.goto("loop")
        return total

    assert loop_sum(5) == 15


def test_jump_forward():
    @goto.goto
    def jmp():
        x = 0
        jmp.goto("end")
        x = 1
        jmp.label("end")
        return x

    assert jmp() == 0
