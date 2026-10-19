def money(cents):
    return f"{cents / 100:.2f}"


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
