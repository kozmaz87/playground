from time import time


def main():
    current_time = time()
    from importhax.magic import tf
    print('magic: {}'.format(time() - current_time))

    print(tf.CriticalSection)


def main2():
    current_time = time()
    from importhax.without import tf
    print('without: {}'.format(time() - current_time))

    print(tf.CriticalSection)


if __name__ == '__main__':
    main()
