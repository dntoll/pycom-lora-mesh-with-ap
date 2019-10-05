from unquote import unquote

class HTTPGet:

    def __init__(self):
        self.allThemParts = {}
        self.isFavicon = False;

    def addLine(self, strline):
        if strline.startswith("GET /favicon.ico HTTP/1.1"):
            self.isFavicon = True;
        elif strline.startswith("GET /?"):
            messageEnd = strline.find(" HTTP/1.1")
            allGetStuff = strline[6:messageEnd]; #skip GET /?
            print(allGetStuff)
            parts = allGetStuff.split("&")


            for getVariable in parts:
                firstAndSecond = getVariable.split("=");
                name = unquote(firstAndSecond[0]).decode()
                value = unquote(firstAndSecond[1]).decode()
                self.allThemParts.update( {name : value } )

    def has(self, name):
        return name in self.allThemParts

    def get(self, name):
        return self.allThemParts.get(name)

    def hasFavicon(self):
        return self.isFavicon;
