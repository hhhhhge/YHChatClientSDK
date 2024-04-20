import YHlib


@YHlib.message_receive_normal_event
def _(data):
    print(1)


YHlib.run("xxxxx", 58080)
