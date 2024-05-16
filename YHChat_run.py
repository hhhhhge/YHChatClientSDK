from YHChat_recv import app
import YHChat_send
import threading


def run(*, token, port=8080):
    YHChat_send.token = token

    def recv_run(port_):
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port_)

    threading.Thread(target=recv_run, args=(port,)).start()
