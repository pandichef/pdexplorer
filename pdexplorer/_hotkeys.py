# https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard #
# https://github.com/moses-palmer/pynput/issues/20#issuecomment-290649632 #


def hotkey_ctrl_f9(fnc):
    """
    compare to these two alternatives:
    1. import keyboard; keyboard.add_hotkey("ctrl+f9", lambda: print("hello"))
    2. import pynput; pynput.keyboard.GlobalHotKeys({"<ctrl>+<f9>": lambda: print("hello")})
    * all methods freeze ipython when input() is used a python command
    * all methods causes issues in ubuntu
    * pynput appear to be faster than the keyboard package, so I used it vs keyboard
    """
    # from pynput import keyboard

    # LEFT_COMBINATION = {keyboard.Key.ctrl_l, keyboard.Key.f9}
    # RIGHT_COMBINATION = {keyboard.Key.ctrl_r, keyboard.Key.f9}

    # key_set = set()

    # def on_press(key):
    #     if key in LEFT_COMBINATION.union(RIGHT_COMBINATION):
    #         key_set.add(key)
    #         if all(k in key_set for k in LEFT_COMBINATION) or all(
    #             k in key_set for k in RIGHT_COMBINATION
    #         ):
    #             fnc()

    # def on_release(key):
    #     try:
    #         key_set.remove(key)
    #     except KeyError:
    #         pass

    # # ...or, in a non-blocking fashion:
    # listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    # listener.start()
    from pynput import keyboard

    LEFT_COMBINATION = {keyboard.Key.ctrl_l, keyboard.Key.f9}
    RIGHT_COMBINATION = {keyboard.Key.ctrl_r, keyboard.Key.f9}

    key_set = set()

    def on_press(key):
        if key in LEFT_COMBINATION.union(RIGHT_COMBINATION):
            key_set.add(key)

            if LEFT_COMBINATION.issubset(key_set) or RIGHT_COMBINATION.issubset(
                key_set
            ):
                fnc()
                key_set.clear()  # Clear the set after calling fnc()

    def on_release(key):
        key_set.discard(
            key
        )  # Remove the key without raising an exception if it doesn't exist

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
