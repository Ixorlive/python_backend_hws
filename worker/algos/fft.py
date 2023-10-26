from algos.mod_inverse import modInverse


def fft(
    array: list[int],
    invert: bool,
    mod: int = 7340033,
    root: int = 5,
    root_1: int = 4404020,
    root_pw: int = 1 << 20,
) -> list[int]:
    """
    Perform the Fast Fourier Transform (FFT) on the input array 'a' using modular arithmetic.
    If 'invert' is True, perform the inverse FFT.

    Note: The provided default values for mod, root, root_1, and root_pw must be consistent and correct.
    Incorrect values will lead to incorrect results.

    Args:
    - a: The input array.
    - n: Length of the input array (must be a power of 2).
    - invert: If True, compute the inverse FFT.
    - mod: Modulus for the FFT. Default is 7340033.
    - root: Primitive root. Default is 5.
    - root_1: Modular multiplicative inverse of the root. Default is 4404020.
    - root_pw: A power of 2 larger than n, typically used to determine the length of the FFT. Default is 1<<20.

    Modifies:
    - The input array 'a' is modified in-place.
    """
    n = len(array)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j >= bit:
            j -= bit
            bit >>= 1
        j += bit
        if i < j:
            array[i], array[j] = array[j], array[i]

    len_ = 2
    while len_ <= n:
        wlen = root_1 if invert else root
        i = len_
        while i < root_pw:
            wlen = (wlen * wlen) % mod
            i <<= 1
        i = 0
        while i < n:
            w = 1
            for j in range(len_ // 2):
                u, v = array[i + j], (array[i + j + len_ // 2] * w) % mod
                array[i + j] = u + v if u + v < mod else u + v - mod
                array[i + j + len_ // 2] = u - v if u - v >= 0 else u - v + mod
                w = (w * wlen) % mod
            i += len_
        len_ <<= 1

    if invert:
        nrev = modInverse(n, mod)
        for i in range(n):
            array[i] = (array[i] * nrev) % mod

    return array
