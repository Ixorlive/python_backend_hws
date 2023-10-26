from tasks import fft, fft_inverse, mod_inverse


def simple_test():
    arr = [1, 2, 3, 4, 5, 6, 7, 8]
    result = fft.delay(arr)
    rev = fft_inverse.delay(result.get())
    assert rev.get() == arr

    assert mod_inverse.delay(5, 7).get() == 3  # 5 * 3 % 7 == 1


if __name__ == "__main__":
    simple_test()
