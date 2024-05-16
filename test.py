from pprint import pprint

from Event import Event
from Message import MessageSegment
import YHChat_send
import YHChat_recv
import YHChat_run

YHChat_run.run(token="1234567890abcdef", port=18888)

YHChat_send.send_message(recv_type="user", recv_id="4503515", message=MessageSegment.text("Hello, World!"))


@YHChat_recv.on_message
def _(message: Event):
    pprint(message.message)
