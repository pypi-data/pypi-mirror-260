#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import frida
import argparse
import signal
import struct
import time
import pprint
import os
import socket
import sys
import traceback
import tempfile
import json
import friTap.pcap as pcap
from friTap.__init__ import __version__
from friTap.__init__ import __author__
from friTap.__init__ import debug
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import logging
import click

try:
    import hexdump  # pylint: disable=g-import-not-at-top
except ImportError:
    print("Unable to import hexdump module!")
    pass



keydump_Set = {*()}
traced_Socket_Set = {*()}
traced_scapy_socket_Set = {*()}
filename = ""
keylog_file = ""
tmpdir = ""
pcap_obj = None
script = None
startup = True
frida_agent_script = "_ssl_log.js"

# Names of all supported read functions:
SSL_READ = ["SSL_read", "wolfSSL_read", "readApplicationData", "NSS_read","Full_read"]
# Names of all supported write functions:
SSL_WRITE = ["SSL_write", "wolfSSL_write", "writeApplicationData", "NSS_write","Full_write"]

# here - where we are.
here = os.path.abspath(os.path.dirname(__file__))

# usually not needed - but sometimes the replacements of the script result into minor issues
# than we have to look into generated final frida script we supply
def write_debug_frida_file(debug_script_version):
    debug_script_file = "_ssl_log_debug.js"
    f = open(debug_script_file, 'wt', encoding='utf-8')
    f.write(debug_script_version)
    f.close()
    print(f"[!] written debug version of the frida script: {debug_script_file}")

def cleanup(live=False, socket_trace=False, full_capture=False, debug_output=False, debug=False):
    global pcap_obj
    if live:
        os.unlink(filename)  # Remove file
        os.rmdir(tmpdir)  # Remove directory
    if type(socket_trace) is str:
        print(f"[*] Write traced sockets into {socket_trace}")
        write_socket_trace(socket_trace)
    if socket_trace == True:
        print("[*] Traced sockets")
        print(pcap.PCAP.get_filter_from_traced_sockets(traced_Socket_Set))
    
    if full_capture and len(traced_scapy_socket_Set) > 0:
        if debug_output or debug:
            print("[*] traced sockets: "+str(traced_scapy_socket_Set))

        pcap_obj.create_application_traffic_pcap(traced_scapy_socket_Set)
    elif full_capture and len(traced_scapy_socket_Set) < 1:
        print(f"[-] friTap was unable to indentify the used sockets.\n[-] The resulting PCAP will contain all trafic from the device.")
        
    print("\n\nThx for using friTap\nHave a nice day\n")
    os._exit(0)
    

def pcap_cleanup(is_full_capture, is_mobile, pcap_name):
    if is_full_capture and pcap_obj is not None:
            capture_type = "local"
            pcap_obj.full_capture_thread.join(2.0)
            if pcap_obj.full_capture_thread.is_alive() and is_mobile == False:
                pcap_obj.full_capture_thread.socket.close()
            if pcap_obj.full_capture_thread.mobile_pid != -1:
                capture_type = "mobile"
                pcap_obj.full_capture_thread.mobile_pid.terminate()
                pcap_obj.android_Instance.send_ctrlC_over_adb()
                pcap_obj.android_Instance.pull_pcap_from_device()
            print(f"[*] full {capture_type} capture safed to _{pcap_name}")
            if keylog_file is None:
                print(f"[*] remember that the full capture won't contain any decrypted TLS traffic.")
            else:
                print(f"[*] remember that the full capture won't contain any decrypted TLS traffic. In order to decrypt it use the logged keys from {keylog_file.name}")

  
def get_addr_string(socket_addr,ss_family):
    if ss_family == "AF_INET":
        return  socket.inet_ntop(socket.AF_INET, struct.pack(">I", socket_addr))
    else: # this should only be AF_INET6
        raw_addr = bytes.fromhex(socket_addr)
        return socket.inet_ntop(socket.AF_INET6, struct.pack(">16s", raw_addr))
    

def get_fritap_frida_script(frida_agent_script):
    with open(os.path.join(here, frida_agent_script), encoding='utf8', newline='\n') as f:
            script_string = f.read()
            return script_string
            

def write_socket_trace(socket_trace_name):
    with open(socket_trace_name, 'a') as trace_file:
        trace_file.write(pcap.PCAP.get_filter_from_traced_sockets(traced_Socket_Set) + '\n')
        

def temp_fifo():
    global tmpdir
    global filename
    tmpdir = tempfile.mkdtemp()
    filename = os.path.join(tmpdir, 'fritap_sharkfin')  # Temporary filename
    os.mkfifo(filename)  # Create FIFO
    try:
        return filename
    except OSError as e:
        print(f'Failed to create FIFO: {e}')


def ssl_log(app, pcap_name=None, verbose=False, spawn=False, keylog=False, enable_spawn_gating=False, mobile=False, live=False, environment_file=None, debug_mode=False,full_capture=False, socket_trace=False, host=False, offsets=None, debug_output=False, experimental=False, anti_root=False, payload_modification=False,enable_default_fd=False):
    global debug
    debug = debug_mode
    
    def on_detach(reason):
        if reason != "application-requested":
            print(f"\n[*] Target process stopped: {reason}\n")
                    
        pcap_cleanup(full_capture,mobile,pcap_name)
        cleanup(live,socket_trace,full_capture,debug)
        
    

    def on_message(message, data):
        global pcap_obj
        global script
        global startup
        """Callback for errors and messages sent from Frida-injected JavaScript.
        Logs captured packet data received from JavaScript to the console and/or a
        pcap file. See https://www.frida.re/docs/messages/ for more detail on
        Frida's messages.
        Args:
        message: A dictionary containing the message "type" and other fields
            dependent on message type.
        data: The string of captured decrypted data.
        """
            
        if startup and message['payload'] == 'experimental':
            script.post({'type':'experimental', 'payload': experimental})

        if startup and message['payload'] == 'defaultFD':
            script.post({'type':'defaultFD', 'payload': enable_default_fd})
        
        if startup and message['payload'] == 'anti':
            script.post({'type':'antiroot', 'payload': anti_root})
            startup = False
            
        
        
        if message["type"] == "error":
            pprint.pprint(message)
            os.kill(os.getpid(), signal.SIGTERM)
            return
        
        p = message["payload"]
        if not "contentType" in p:
            return
        if p["contentType"] == "console":
            print("[*] " + p["console"])
        if debug_mode or debug_output:
            if p["contentType"] == "console_dev" and p["console_dev"]:
                if len(p["console_dev"]) > 3:
                    print("[***] " + p["console_dev"])
        if verbose:
            if(p["contentType"] == "keylog") and keylog:
                if p["keylog"] not in keydump_Set:
                    print(p["keylog"])
                    keydump_Set.add(p["keylog"])
                    keylog_file.write(p["keylog"] + "\n")
                    keylog_file.flush()    
            elif not data or len(data) == 0:
                return
            else:
                src_addr = get_addr_string(p["src_addr"], p["ss_family"])
                dst_addr = get_addr_string(p["dst_addr"], p["ss_family"])
                
                if socket_trace == False and full_capture  == False:
                    print("SSL Session: " + str(p["ssl_session_id"]))
                if full_capture:
                    scapy_filter = pcap.PCAP.get_bpf_filter(src_addr,dst_addr)
                    traced_scapy_socket_Set.add(scapy_filter)
                if socket_trace:
                    display_filter = pcap.PCAP.get_display_filter(src_addr,dst_addr)
                    traced_Socket_Set.add(display_filter)
                    print("[socket_trace] %s:%d --> %s:%d" % (src_addr, p["src_port"], dst_addr, p["dst_port"]))
                else:
                    print("[%s] %s:%d --> %s:%d" % (p["function"], src_addr, p["src_port"], dst_addr, p["dst_port"]))
                    hexdump.hexdump(data)
                print()
        if pcap_name and p["contentType"] == "datalog" and full_capture == False:
            pcap_obj.log_plaintext_payload(p["ss_family"], p["function"], p["src_addr"],
                     p["src_port"], p["dst_addr"], p["dst_port"], data)
        if live and p["contentType"] == "datalog" and full_capture == False:
            try:
                pcap_obj.log_plaintext_payload(p["ss_family"], p["function"], p["src_addr"],
                         p["src_port"], p["dst_addr"], p["dst_port"], data)
            except (BrokenPipeError, IOError):
                process.detach()
                cleanup(live)

        if keylog and p["contentType"] == "keylog":
            if p["keylog"] not in keydump_Set:
                keylog_file.write(p["keylog"] + "\n")
                keylog_file.flush()
                keydump_Set.add(p["keylog"])
        
        if socket_trace or full_capture:
            if "src_addr" not in p:
                return
            
            src_addr = get_addr_string(p["src_addr"], p["ss_family"])
            dst_addr = get_addr_string(p["dst_addr"], p["ss_family"])
            if socket_trace:
                display_filter = pcap.PCAP.get_display_filter(src_addr,dst_addr)
                traced_Socket_Set.add(display_filter)
            else:
                scapy_filter = pcap.PCAP.get_bpf_filter(src_addr,dst_addr)
                traced_scapy_socket_Set.add(scapy_filter)
            

    def on_child_added(child):
        print(f"[*] Attached to child process with pid {child.pid}")
        instrument(device.attach(child.pid))
        device.resume(child.pid)

    def on_spawn_added(spawn):
        print(
            f"[*] Process spawned with pid {spawn.pid}. Name: {spawn.identifier}")
        instrument(device.attach(spawn.pid))
        device.resume(spawn.pid)
        

    def instrument(process):
        global script
        runtime="qjs"
        debug_port = 1337
        if debug:
            if frida.__version__ < "16":
                process.enable_debugger(debug_port)
            print("\n[!] running in debug mode")
            print(f"[!] Chrome Inspector server listening on port {debug_port}")
            print("[!] Open Chrome with chrome://inspect for debugging\n")
            runtime="v8"
        
        script_string = get_fritap_frida_script(frida_agent_script)
        

        if offsets_data is not None:
            print(f"[*] applying hooks at offset {offsets_data}")
            script_string = script_string.replace('"{OFFSETS}"', offsets_data)
            # might lead to a malformed package in recent frida versions
                    

        script = process.create_script(script_string, runtime=runtime)

        if debug and frida.__version__ >= "16":
            script.enable_debugger(debug_port)
        script.on("message", on_message)
        script.load()
        
        

        
        #script.post({'type':'readmod', 'payload': '0x440x410x53'})
        if payload_modification:
            class ModWatcher(FileSystemEventHandler):
                def __init__(self, process):
                    
                    self.process = process

                def on_any_event(self, event):
                    try:
                        if(event.event_type == "modified" and ("readmod" in event.src_path)):
                            with open("./readmod.bin", "rb") as f:
                                buffer = f.read()
                                script.post({'type':'readmod', 'payload': buffer.hex()})
                        elif(event.event_type == "modified" and ("writemod" in event.src_path)):
                            with open("./writemod.bin", "rb") as f:
                                buffer = f.read()
                                script.post({'type':'writemod', 'payload': buffer.hex()})
                    except RuntimeError as e:
                        print(e)
                
                

            print("Init watcher")
            event_handler = ModWatcher(process)
            
            observer = Observer()
            observer.schedule(event_handler, os.getcwd())
            observer.start()

    # Main code
    global pcap_obj
    global offsets_data
    global frida_agent_script
    global keylog_file
    
    #frida_agent_script = "_ssl_log_legacy.js"
    # derzeit klappt aus irgend einen Grund das kompilieren nicht mehr so richtig bzw. das Interpretieren von 
    # malformed == komische symbole/emojies im code

    if frida.__version__ < "16":
        frida_agent_script = "_ssl_log_legacy.js"

    if mobile:
        device = frida.get_usb_device()
    elif host:
        device = frida.get_device_manager().add_remote_device(host)
    else:
        device = frida.get_local_device()


    if offsets is not None:
        if os.path.exists(offsets):
            file = open(offsets, "r")
            offsets_data = file.read()
            file.close()
        else:
            try:
                json.load(offsets)
                offsets_data = offsets
            except ValueError as e:
                print("Log error, defaulting to auto-detection?")
    else:
        offsets_data = None

    device.on("child_added", on_child_added)
    if enable_spawn_gating:
        device.enable_spawn_gating()
        device.on("spawn_added", on_spawn_added)
    if spawn:
        print("spawning "+ app)
        
        if pcap_name:
            pcap_obj =  pcap.PCAP(pcap_name,SSL_READ,SSL_WRITE,full_capture, mobile,debug_mode)
            
        if mobile or host:
            pid = device.spawn(app)
        else:
            used_env = {}
            if environment_file:
                with open(environment_file) as json_env_file:
                    used_env = json.load(json_env_file)
            pid = device.spawn(app.split(" "),env=used_env)
            device.resume(pid)
            time.sleep(1) # without it Java.perform silently fails
        process = device.attach(pid)
    else:
        if pcap_name:
            pcap_obj =  pcap.PCAP(pcap_name,SSL_READ,SSL_WRITE,full_capture, mobile,debug_mode)
        process = device.attach(int(app) if app.isnumeric() else app)

    if live:
        if pcap_name:
            print("[*] YOU ARE TRYING TO WRITE A PCAP AND HAVING A LIVE VIEW\nTHIS IS NOT SUPPORTED!\nWHEN YOU DO A LIVE VIEW YOU CAN SAFE YOUR CAPUTRE WIHT WIRESHARK.")
        fifo_file = temp_fifo()
        print(f'[*] friTap live view on Wireshark')
        print(f'[*] Created named pipe for Wireshark live view to {fifo_file}')
        print(
            f'[*] Now open this named pipe with Wireshark in another terminal: sudo wireshark -k -i {fifo_file}')
        print(f'[*] friTap will continue after the named pipe is ready....\n')
        pcap_obj =  pcap.PCAP(fifo_file,SSL_READ,SSL_WRITE,full_capture, mobile,debug_mode)
        

    if keylog:
        keylog_file = open(keylog, "w")
    

    instrument(process)

    

    if pcap_name and full_capture:
        print(f'[*] Logging pcap to {pcap_name}')
    if pcap_name and full_capture == False:
        print(f'[*] Logging TLS plaintext as pcap to {pcap_name}')
    if keylog:
        print(f'[*] Logging keylog file to {keylog}')
        
    process.on('detached', on_detach)

    if spawn:
        device.resume(pid)
    try:
        while True:
            time.sleep(1)
        sys.stdin.read()
    except KeyboardInterrupt:
        pass

    process.detach()


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        print("friTap v" + __version__)
        print("by " + __author__)
        print()
        print("Error: " + message)
        print()
        print(self.format_help().replace("usage:", "Usage:"))
        self.exit(0)


def main():

    parser = ArgParser(
        add_help=False,
        description="Decrypts and logs an executables or mobile applications SSL/TLS traffic.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
        epilog=r"""
Examples:
  %(prog)s -m -p ssl.pcap com.example.app
  %(prog)s -m --pcap log.pcap --verbose com.example.app
  %(prog)s -m -k keys.log -v -s com.example.app
  %(prog)s --pcap log.pcap "$(which curl) https://www.google.com"
  %(prog)s -H --pcap log.pcap 192.168.0.1:1234 com.example.app
  %(prog)s -m -p log.pcap --enable_spawn_gating -v -do --full_capture -k keys.log com.example.app
  %(prog)s -m -p log.pcap --enable_spawn_gating -v -do --anti_root --full_capture -k keys.log com.example.app
""")

    args = parser.add_argument_group("Arguments")
    args.add_argument("-m", "--mobile", required=False, action="store_const",
                      const=True, default=False, help="Attach to a process on android or iOS")
    args.add_argument("-H", "--host", metavar="<ip:port>", required=False,
                      help="Attach to a process on remote frida device")
    args.add_argument("-d", "--debug", required=False, action="store_const", const=True,
                      help="Set friTap into debug mode this include debug output as well as a listening Chrome Inspector server for remote debugging.")
    args.add_argument("-do", "--debugoutput", required=False, action="store_const", const=True,
                      help="Activate the debug output only.")
    args.add_argument("-ar", "--anti_root", required=False, action="store_const",
                      const=True, help="Activate anti root hooks for Android")
    args.add_argument("-ed", "--enable_default_fd", required=False, action="store_const",
                      const=True, help="Activate the fallback socket information (127.0.0.1:1234-127.0.0.1:2345) whenever the file descriptor (FD) of the socket cannot be determined")
    args.add_argument("-f", "--full_capture", required=False, action="store_const", const=True, default=False,
                      help="Do a full packet capture instead of logging only the decrypted TLS payload. Set pcap name with -p <PCAP name>")
    args.add_argument("-k", "--keylog", metavar="<path>", required=False,
                      help="Log the keys used for tls traffic")
    args.add_argument("-l", "--live", required=False, action="store_const", const=True,
                      help="Creates a named pipe /tmp/sharkfin which can be read by Wireshark during the capturing process")
    args.add_argument("-p ", "--pcap", metavar="<path>", required=False,
                      help="Name of PCAP file to write")
    args.add_argument("-s", "--spawn", required=False, action="store_const", const=True,
                      help="Spawn the executable/app instead of attaching to a running process")
    args.add_argument("-sot", "--socket_tracing", metavar="<path>", required=False, nargs='?', const=True,
                      help="Traces all socket of the target application and provide a prepared wireshark display filter. If pathname is set, it will write the socket trace into a file-")
    args.add_argument("-env","--environment", metavar="<env.json>", required=False,
                      help="Provide the environment necessary for spawning as an JSON file. For instance: {\"ENV_VAR_NAME\": \"ENV_VAR_VALUE\" }")
    args.add_argument("-v", "--verbose", required=False, action="store_const",
                      const=True, help="Show verbose output")
    args.add_argument('--version', action='version',version='friTap v{version}'.format(version=__version__))
    args.add_argument("--enable_spawn_gating", required=False, action="store_const", const=True,
                      help="Catch newly spawned processes. ATTENTION: These could be unrelated to the current process!")
    args.add_argument("exec", metavar="<executable/app name/pid>",
                      help="executable/app whose SSL calls to log")
    args.add_argument("--offsets", required=False, metavar="<offsets.json>",
                      help="Provide custom offsets for all hooked functions inside a JSON file or a json string containing all offsets. For more details see our example json (offsets_example.json)")
    args.add_argument("--payload_modification", required=False, action="store_const", const=True, default=False,
                      help="Capability to alter the decrypted payload. Be careful here, because this can crash the application.")                  
    args.add_argument("-exp","--experimental", required=False, action="store_const", const=True, default=False,
                      help="Activates all existing experimental feature (see documentation for more information)")
    parsed = parser.parse_args()

    
    if parsed.full_capture and parsed.pcap is None:
        parser.error("--full_capture requires -p to set the pcap name")
        exit(2)

    if parsed.full_capture and parsed.keylog is None:
        print("[*] Are you sure you want to proceed without recording the key material (-k <keys.log>)?\n[*] Without the key material, you have a complete network record, but no way to view the contents of the TLS traffic.")
        print("[*] Do you want to proceed without recording keys? : <press any key to proceed or Strg+C to abort>")
        input()


   
    
    try:
        print("Start logging")
        print("Press Ctrl+C to stop logging")
        ssl_log(parsed.exec, parsed.pcap, parsed.verbose,
                parsed.spawn, parsed.keylog, parsed.enable_spawn_gating, parsed.mobile, parsed.live, parsed.environment, parsed.debug, parsed.full_capture, parsed.socket_tracing, parsed.host, parsed.offsets, parsed.debugoutput,parsed.experimental, parsed.anti_root, parsed.payload_modification, parsed.enable_default_fd)

       
    except Exception as ar:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()
        
        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)
        
        # Format stacktrace
        stack_trace = list()
        
        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        
        if parsed.debug or parsed.debugoutput:
            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %stack_trace)


        if "unable to connect to remote frida-server: closed" in str(ar):
            print("\n[-] frida-server is not running in remote device. Please run frida-server and rerun")
            
        print(f"\n[-] Unknown error: {ex_value}")
        
        cleanup(parsed.live,parsed.socket_tracing,parsed.full_capture,parsed.debug,parsed.debugoutput)    
        os._exit(2)

    finally:
        pcap_cleanup(parsed.full_capture,parsed.mobile,parsed.pcap)
        cleanup(parsed.live,parsed.socket_tracing,parsed.full_capture,parsed.debug)
        

if __name__ == "__main__":
    main()