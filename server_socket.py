import zmq
import requests
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("A connection with client was successful")
while True:

    # wait for next request from client
    message = socket.recv()
    print("A request from client was successful.")
    # do some work
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": message, "page": "1", "num_pages": "1"}
    headers = {
        "X-RapidAPI-Key": "4167ff9878msh83998ccaf4a3f29p1f360ajsn54b63e763db9",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    results_data = response.json()

    print("Done gathering information, now writing to text file")

    with open('jobs.txt', 'w') as g:
        for item in results_data["data"]:
            g.write(item["employer_name"])
            g.write(item["job_title"])
            g.write(item["job_description"])
            g.write("\n")

        g.close()
    print("Done writing to txt file")
    socket.send_string('jobs.txt')