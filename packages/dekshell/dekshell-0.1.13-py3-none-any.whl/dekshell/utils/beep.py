def sound_notify(success):
    try:
        from beepy import beep
    except ModuleNotFoundError:
        return
    beep('coin' if success else 'robot_error')
