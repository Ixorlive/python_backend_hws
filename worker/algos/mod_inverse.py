def modInverse(val: int, md: int) -> int:
    """
    Compute the modular multiplicative inverse of 'val' modulo 'md'.
    """
    m0 = md
    x0, x1 = 0, 1

    if md == 1:
        return 0

    while val > 1:
        q = val // md
        t = md
        md = val % md
        val = t
        t = x0
        x0 = x1 - q * x0
        x1 = t
    return x1 + m0 if x1 < 0 else x1
