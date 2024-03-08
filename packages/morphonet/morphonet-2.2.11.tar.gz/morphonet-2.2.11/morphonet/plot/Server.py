from threading import Thread
import threading

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from io import BytesIO
from morphonet import tools
from morphonet.tools import _get_param, printv
from traceback import print_exc
# ****************************************************************** MORPHONET SERVER


class _MorphoServer(Thread):
    def __init__(self, ploti, todo, host="", port=9875):
        Thread.__init__(self)
        self.ploti = ploti
        self.todo = todo
        self.host = host
        self.port = port
        self.handler=None
        self.server_address = (self.host, self.port)
        self.server_ready = threading.Event()

    def run(self):  # START FUNCTION
        self.handler = _MorphoSendHandler(self.ploti, self)  if self.todo == "send" else _MorphoRecieveHandler(self.ploti, self)
        self.httpd = HTTPServer(self.server_address, self.handler)
        self.httpd.serve_forever()

    def stop(self):
        self.server_ready.set()
        self.httpd.shutdown()
        self.httpd.server_close()

    def add(self, cmd, obj):
        self.server_ready.wait() #Cannot add any command before unity communication is one
        self.handler.add(cmd,obj)


class _MorphoSendHandler(BaseHTTPRequestHandler):

    def __init__(self, ploti, ms):
        self.ploti = ploti
        self.ms = ms
        self.send_list=[]

    def __call__(self, *args, **kwargs):  # Handle a request
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")  # To accept request from morphonet
        self.end_headers()

    def do_GET(self):  # NOT USED
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self.ms.server_ready.set()  # Recieve something so unity side is ready
        response = BytesIO()
        self._set_headers()
        if len(self.send_list) > 0:
            cmd, obj= self.send_list.pop(0)
            printv(str(len(self.send_list))+" : POST " + cmd,3)
            response.write(bytes(cmd, 'utf-8'))
            response.write(b';')  # ALWAYS ADD A SEPARATOR
            if obj is not None:
                if cmd.find("RAW") == 0 or cmd.find("EX") == 0 or cmd.find("IC") == 0:
                    response.write(obj)
                else:
                    response.write(bytes(obj, 'utf-8'))
            else:
                response.write(bytes("ok", 'utf-8'))
        else:
            response.write(bytes("ok", 'utf-8'))
        self.wfile.write(response.getvalue())

    def log_message(self, format, *args):
        return

    def add(self,cmd,obj):
        if type(obj) == list: obj = str(obj)

        # We first remove previous plot raw
        if cmd.startswith("RAW_"):
            for cmdC,objC in self.send_list:
                if cmdC.startswith("RAW_"):
                    self.send_list.remove([cmdC,objC])

        printv(str(len(self.send_list))+" : ADD " + cmd, 3)

        if cmd is not None:   cmd = cmd.replace(" ", "%20")
        if obj is not None:
            if type(obj) == str:
                obj = obj.replace(" ", "%20")

        self.send_list.append([cmd, obj])

class _MorphoRecieveHandler(BaseHTTPRequestHandler):

    def __init__(self, ploti, ms):
        self.ploti = ploti
        self.ms = ms

    def __call__(self, *args, **kwargs):  # Handle a request
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")  # To accept request from morphonet
        self.end_headers()

    def do_GET(self):  # NOT USED
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self._set_headers()
        response = BytesIO()  # Read
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        command = self.rfile.read(content_length)
        action = _get_param(command, "action")
        current_time = int(_get_param(command, "time"))
        seg_channel = 0
        if _get_param(command, "seg_channel") is not None and _get_param(command, "seg_channel") != "":
            seg_channel = int(_get_param(command, "seg_channel"))  #TODO CHANGE IN UNITY
        objects = _get_param(command, "objects").split(";")
        printv("action is "+action+ " at "+str(current_time),3)

        #RECUPERER MESH DEFORMATION
        mesh_deform=_get_param(command, "mesh_deform").split(";")

        #Get transforms for copy past
        transforms = _get_param(command,"copy_objects").split(";")
        self.ploti.set_current_time(current_time)
        self.ploti.current_segmented_channel=seg_channel #Set default Channel
        if action == "showraw":
            self.ploti.current_raw_channel = int(objects[0])
            self.ploti.show_raw = True
            self.ploti.plot_raw(current_time)
        elif action == "hideraw":
            self.ploti.show_raw = False
        elif action == "upload":
            self.ploti.upload(objects[0], 2)
        elif action == "cancel":
            self.ploti.cancel()
        elif action=="exit":
            self.ploti.quit_and_exit()
        elif action=="restart":
            self.ploti.restart_plot()
        elif action=="leave":   #this one has to be i a thread : we cannot shutdown a server while it is used for a request
            t2 = threading.Thread(target=self.ploti.quit)
            t2.start()
        elif action == "get_info_field":
            self.ploti.get_property_field(_get_param(command, "info"))
        elif action == "reload_infos":
            self.ploti.reload_properties()
        elif action == "create_curation":
            self.ploti.annotate(_get_param(command, "info"), _get_param(command, "objects"),
                                   _get_param(command, "value"), _get_param(command, "date"))
        elif action == "delete_curation":
            self.ploti.delete_annotation(_get_param(command, "info"), _get_param(command, "objects"),
                                          _get_param(command, "value"), date=_get_param(command, "date"))
        elif action == "delete_curation_value":
            self.ploti.delete_annotation(_get_param(command, "info"), _get_param(command, "objects"),
                                                      _get_param(command, "value"))
        elif action == "create_info_unity":
            self.ploti.create_property_from_unity(_get_param(command, "name"), _get_param(command, "datatype"),
                                              _get_param(command, "infos"),_get_param(command,"file"))
        elif action == "delete_info_unity":
            self.ploti.delete_property_from_unity(_get_param(command, "info"))
        elif action == "delete_selection":
            self.ploti.delete_label_from_unity(_get_param(command, "info"), _get_param(command, "selection"))
        elif action == "get_information_full":
            self.ploti.get_property_field(objects[0])
        elif action == "recompute":
            self.ploti.recompute_data()
        elif action == "get_sk_information":
            name=objects[0]
            if name.startswith("SK"):name=name[2:]
            name=name.replace("-","_")
            self.ploti.get_regionprop(name)
        else:
            actions = unquote(str(command.decode('utf-8'))).split("&")
            for plug in self.ploti.plugins:
                if plug._cmd() == action:
                    printv("Found Plugin "+plug._cmd(),2)
                    ifo = 0
                    for tf in plug.inputfields:
                        plug._set_inputfield(tf, actions[4 + ifo][actions[4 + ifo].index("=") + 1:])
                        ifo += 1

                    for dd in plug.dropdowns:
                        plug._set_dropdown(dd, actions[4 + ifo][actions[4 + ifo].index("=") + 1:])
                        ifo += 1
                    for cd in plug.coordinates:
                        plug._set_coordinates(cd, actions[4 + ifo][actions[4 + ifo].index("=") + 1:])
                        ifo += 1
                    for cb in plug.toggles:
                        plug._set_toggle(cb,actions[4 + ifo][actions[4 + ifo].index("=") + 1:].lower() in ["true","True","1"])
                        ifo += 1

                    if tools.verbose<=1:
                        step_before_execution = self.ploti.dataset.step
                        try: #Exectue the coordinate with exception ...
                            if plug._cmd()=="Deform : Apply a manual deformation on the selected object":
                                plug.process(current_time, self.ploti.dataset, objects,mesh_deform)
                            elif plug._cmd()=="Copy Paste":
                                plug.process(current_time,self.ploti.dataset,objects,transforms)
                            else:
                                plug.process(current_time, self.ploti.dataset, objects)
                        except Exception as e:
                            printv("the plugin had an error ",0)
                            print_exc()
                            if step_before_execution!=self.ploti.dataset.step:
                                printv("cancel last step "+str(self.ploti.dataset.step),1)
                                self.ploti.dataset.cancel()
                    else: #DEV MODE EXCUDE THE PLUGIN WITHOUT CATCHIG THE ERROR
                        if plug._cmd() == "Deform : Apply a manual deformation on the selected object":
                            plug.process(current_time, self.ploti.dataset, objects, mesh_deform)
                        elif plug._cmd() == "Copy Paste":
                            plug.process(current_time, self.ploti.dataset, objects, transforms)
                        else:
                            plug.process(current_time, self.ploti.dataset, objects)


        response.write(bytes("DONE", 'utf-8'))
        self.wfile.write(response.getvalue())

    def log_message(self, format, *args):
        return
