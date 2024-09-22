from flask import Flask, request, jsonify
from DTOs.Device import *
from DTOs.Lecture import *
import uuid

app = Flask(__name__)

devices = {}
lectures = {}

#/GetCode?deviceId=12345678&lectureId=1234567&threadCount=10&currentSearchValue=0
@app.route('/GetCode', methods=['POST'])
def get_code():
    device_id = request.args.get("deviceId")
    lecture_id = request.args.get("lectureId")
    thread_count = int(request.args.get("threadCount", 1))
    current_search_value = int(request.args.get("currentSearchValue", 0))

    # Check if the lecture already exists
    if lecture_id in lectures:
        lecture = lectures[lecture_id]
        if lecture.foundCode != -1:
            return jsonify({
                "status": 200,
                "FoundCode": lecture.foundCode
            })
        
        # Update lecture's current search value if the incoming value is higher
        if lecture.currentSearchValue < current_search_value:
            lecture.currentSearchValue = current_search_value
    else:
        # Create a new lecture if it doesn't exist
        lecture = Lecture(lecture_id, current_search_value)
        lectures[lecture_id] = lecture

    # Update or create the device in the dictionary
    if device_id in devices:
        device = devices[device_id]
        device.lectureId = lecture_id
        device.threadCount = thread_count
    else:
        device = Device(
            deviceId=device_id,
            lectureId=lecture_id,
            threadCount=thread_count,
            currentSearchValue=current_search_value,
        )
        devices[device_id] = device

    # Calculate total thread count and the starting search value
    total_threads = get_total_thread_count(lecture_id)
    start_search_value = get_start_search_value(device_id, lecture_id, total_threads)

    return jsonify({
        "status": 200,
        "FoundCode": -1,
        "SearchGap": total_threads,
        "CurrentSearchValue": start_search_value,
    })

def get_start_search_value(device_id, lecture_id, total_threads):
    devs = get_devices_by_lecture(lecture_id)
    lecture = lectures[lecture_id]
    start_thread_offset = 0

    for dev in devs:
        if dev.deviceId == device_id:
            return max(0, lecture.currentSearchValue - total_threads + start_thread_offset)
        start_thread_offset += dev.threadCount

    return 0


def get_total_thread_count(lecture_id):
    lecture_devices = get_devices_by_lecture(lecture_id)
    return sum(dev.threadCount for dev in lecture_devices)

def get_devices_by_lecture(lecture_id):
    return [device for device in devices.values() if device.lectureId == lecture_id]

# /FoundCode?=deviceId=12345678&lectureId=1234567&foundCode=123456
@app.route('/FoundCode', methods=['POST'])
def FoundCode():
    device_id = request.args.get("deviceId")
    lecture_id = request.args.get("lectureId")
    lecture_code = request.args.get("foundCode")

    if has_device_been_searching(device_id, lecture_id):
        lectures[lecture_id].foundCode = lecture_code
        return jsonify({
            "status": 200,
            "FoundCode": lecture_code
        })

    return jsonify({
        "status": 401,
        "message": "You are not authorized"
    })

def has_device_been_searching(deviceId, lectureId):
    return any(device.deviceId == deviceId for device in get_devices_by_lecture(lectureId))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7153)

