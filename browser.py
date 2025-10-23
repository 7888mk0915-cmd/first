import socket
import ssl
import tkinter

tkinter.mainloop()

while True:
    for evt in pendingEvents():
        handleEvent(evt)
    drawScreen()
    
WIDTH, HEIGHT = 800, 600
class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()

ctx = ssl.create_default_context()
s = ctx.wrap_socket(s, server_hostname=host)

class URL:
    def __init__(self, url): # 호스트와 경로 부분
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]
        # / 기준 앞 문자열은 호스트, 뒤 문자열은 경로
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/",1)
        self.path = "/" + url
        
        if self.scheme == "http":
            self.port=80
        elif self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
            self.port = 443
            
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self): # 웹페이지 다운로드
        s = socket.socket(
            family = socket.AF_INET,
            type = socket.SOCK_STREAM,
            proto = socket.IPPROTO_TCP,
            )
        s.connect((self.host, self.port))
        
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        s.send(request.encode("utf8")) # 센더는 서버에 요청을 전송함

        response = s.makefile("r", encoding="utf8", newline="\r\n") # 데이터가 도착할 때마다 수집하는 루프
        
        statusline = response.readline() # 상태 응답 처리?
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {} # 헤더
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        body = response.read()
        s.close()

        return body

def lex(body):
        text = ""
        in_tag = False
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                int_tag = False
            elif not in_tag:
                text += c
        return text

def load(self, url):
        body = url.request()
        show(body)
        self.canvas.create_ractangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text="Hi!")
        for c in text:
            self.canvas.create_text(100, 100, text=c)
        
if __name__ == "__main__":
        import sys
        load(URL(sys.argv[1]))
        tkinter.mainloop()