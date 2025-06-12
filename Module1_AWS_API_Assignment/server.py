from flask import Flask, make_response
import time
import platform

app = Flask("Hello World")


@app.route("/hello")
def hello_world():
    return "Hello, World!"

@app.route("/hello/json")
def hello_world_json():
    resp = make_response({"message": "Hello World"})
    resp.status_code=200
    return resp

@app.route("/status")
def status():
    uptime_seconds = time.monotonic()
    system_info = platform.uname()
    resp=make_response({
        "Uptime":uptime_seconds,
        "Status":{
            "System":system_info.system,
            "Node name":system_info.node,
            "Release":system_info.release,
            "Version":system_info.version,
            "Machine":system_info.machine,
            "Processor":system_info.processor
        }    
    })
    resp.status_code=200
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
#Run executes on port 5000
#flask --app server run
#takes port config
#python server.py