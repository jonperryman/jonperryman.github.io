import os
import signal
import sys
import glob
import time
import html
import traceback
import time
from http.server import HTTPServer, CGIHTTPRequestHandler, SimpleHTTPRequestHandler

# os.chdir( os.path.expanduser("~\\Documents\\jon\\ibm-main") )

class ibm_main:

    def markRead(path):
        buildFiles = glob.glob("build_" + path[2] + ".*.show.html")
        for file in buildFiles:
            os.rename(file, file[:-10] + ".hide.html")
        if len(buildFiles) > 0:
            with open("indexhideitems.html", "a", encoding="utf-8") as f:
                f.write("hide thread=/" + path[2] + "/ build=/" + buildFiles[-1].split(".")[-3]  + "/" )

    def terminate():
        self.kill_now = True
        return("Terminating web server")

    def restart():
        print('***** Restarting web server *****')
        os.execv(sys.executable, ['python'] + sys.argv)
        return('***** Restarting web server *****')

    def itemShowRead(path):
        print("item show hide ", "/".join( path ))
        return("item show hide " + "/".join( path ))

    def indexMarkRead(path):
        buildFiles = glob.glob("build_" + path[2] + ".*.show.html")
        for file in buildFiles:
            os.rename(file, file[:-10] + ".hide.html")
        if len(buildFiles) > 0:
            with open("indexhideitems.html", "a", encoding="utf-8") as f:
                f.write("hide thread=/" + path[2] + "/ build=/" + buildFiles[-1].split(".")[-3]  + "/" )
        return("index mark read has completed")
    
    def indexDelete(path):
        print("index delete", "/".join( path ))
        return("index delete " +  "/".join( path ))

    def indexOpen(path):
        with open("thread_" + path[2] + ".html", "r", encoding="utf-8") as f:
            html = "\n".join([

                            "<div id='threadButtonDiv'>",
                            
                            "<button id='ThreadRead' onclick='threadRead(this, \"" + path[2] + "\");'>Read</button>",

                            "<button id='ThreadShow' onclick='threadShow(this, \"" + path[2] + "\");'>Show</button>",

                            "<button id='ThreadDelete' onclick='threadDelete(this, \"" + path[2] + "\");'>Delete</button>",

                            "</div>", 

                            "<button id='threadclosex' class='closex' onclick='threadClose(this, \"" + path[2] + "\");'>X</button>",

                            "<h1 id='thread_" + path[2] + "' class='threadH1'>" + f.read() + "</h1>\n\n"
                            
                        ])
        for file in glob.glob("build_" + path[2] +".*.html"):
            with open(file, "r", encoding="utf-8") as f:
                html += f.read()
        print("index open", "/".join( path ))
        return(html)

    def threadShow(path):
        print("threadShow", "/".join( path ))
        return("threadShow " +  "/".join( path ))

    def threadRead(path):
        buildFiles = glob.glob("build_" + path[2] + ".*.show.html")
        for file in buildFiles:
            os.rename(file, file[:-10] + ".hide.html")
        if len(buildFiles) > 0:
            with open("indexhideitems.html", "a", encoding="utf-8") as f:
                f.write("hide thread=/" + path[2] + "/ build=/" + buildFiles[-1].split(".")[-3]  + "/" )
        return("hide thread has completed")

    def threadDelete(path):
        print("thread delete", "/".join( path ))
        return("thread delete " +  "/".join( path ))

def httpServer():

    def signal_handler(self, signum, frame):
        print("signal ", signum, "has been received")
        self.kill_now = True
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        pids = []
        with open("webserver.pid") as f:
            pids = f.readlines()
    except:
        pass

    pidActive = True
    while pidActive:    
        pidActive = False
        for pid in pids:
            try:
                os.kill(int(pid.strip("\n")), signal.SIGTERM)
                print("terminating webserver pid=", pid)
                pidActive = True
            except OSError:
                pass
        time.sleep(1)
        print("Still waiting for webserver termination")
    
    with open("webserver.pid","w") as f:
        f.write(str(os.getpid()) + "\n")

    class RequestsHandler(CGIHTTPRequestHandler):
        def do_GET(self):
            try:
                path = self.path[1:].split("?")
                if path[0][:9] == "ibm_main/":
                    path = path[0].split("/")
                    results = getattr(globals()["ibm_main"] , path[1] )(path)
                    self.send_response(200) 
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(str.encode(results))
                else:
                    if path[0] == "":
                        if os.path.exists("index.html"):
                            path[0] = "index.html"
                        else:
                            path[0] = "rss_reader.html"
                    work = path[0].split(".")
                    if len(work) == 1:
                        path[0] += ".html"
                        work[1] = "html"
                    elif len(work) > 2:
                        self.send_error(500, "Invalid web address: " + path[0])
                        return
                    type = ["text/html", "text/javascript", "text/css", "image/png", "image/jpeg", "image/gif"][["html", "js", "css", "png", "jpg", "gif"].index(work[1])]
                    if type[:6] == "image/":
                        with open( path[0], "rb" ) as f:
                            data = f.read()
                    else:
                        with open( path[0], "r") as f:
                            data = f.read().encode("utf-8")
                    self.send_response(200)
                    self.send_header('Content-type', type)
                    self.end_headers()
                    self.wfile.write(data)
            except IOError as err:
                self.send_error(404, "Page '%s' not found" % self.path)
            except Exception as err:
                path = self.path
                tracedata = traceback.format_exc()
                msg = f"{path=} unexpected error: {err=}, {type(err)=} \n\n {tracedata=}".replace("\\n","\n")
                self.send_error(500, msg)
                print(msg)
    try:
        # requestsHandler.cgi_directories = ['/cgi-bin']

        print("starting web server port 8000 pid ", os.getpid())

        httpd = HTTPServer(('', 8000), # 'localhost', 8000),             # localhost:8000
                        RequestsHandler)  # CGI support.

        print(f"Running server. Use [ctrl]-c to terminate.")

        httpd.serve_forever()

    except KeyboardInterrupt:
        print(f"\nReceived keyboard interrupt. Shutting down server.")
        httpd.socket.close()

httpServer()

print("http server has terminated")