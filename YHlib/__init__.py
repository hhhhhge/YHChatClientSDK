from . import YHsend
from . import YHrecv

message_receive_normal_event = YHrecv.message_receive_normal_event
message_receive_instruction_event = YHrecv.message_receive_instruction_event
bot_followed_event = YHrecv.bot_followed_event
bot_unfollowed_event = YHrecv.bot_unfollowed_event
group_leave_event = YHrecv.group_leave_event
button_report_inline_event = YHrecv.button_report_inline_event


def set_token(token):
    YHsend.token = token


def run(token, port):
    if token is not None:
        YHsend.token = token
    else:
        raise YHsend.TokenEmptyError("token不能为空")
    YHrecv.run(port)
