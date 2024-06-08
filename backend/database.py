from pymongo import MongoClient
import datetime
import os

client = MongoClient(os.environ.get("DATABASE_URI")).attendance_system


def convert(attendee):
    attendee["_id"] = str(attendee["_id"])
    return attendee


def add_fields(attendee):
    attendee["time"] = None
    attendee["attended"] = False
    return attendee


def open_day():
    if day := client.attendance.find_one({"day": str(datetime.datetime.now().date())}):
        day["_id"] = str(day["_id"])
        day["attendees"] = list(map(convert, day["attendees"]))
        return day
    else:
        students = list(client.students.find())
        attendance = {
            "day": str(datetime.datetime.now().date()),
            "attendees": list(map(add_fields, students)),
        }
        client.attendance.insert_one(attendance)
        day = client.attendance.find_one({"day": str(datetime.datetime.now().date())})
        day["_id"] = str(day["_id"])
        day["attendees"] = list(map(convert, day["attendees"]))
        return day


def add_new(name, regnumber):
    # check if user already exists
    if client.students.find_one({"reg": regnumber.upper()}):
        return False
    students = client.attendance.find_one({"day": str(datetime.datetime.now().date())})[
        "attendees"
    ]
    new = {"name": name, "reg": regnumber.upper()}
    insert_res = client.students.insert_one(new)
    new["time"] = None
    new["attended"] = False
    students.append(new)
    client.attendance.update_one(
        {"day": str(datetime.datetime.now().date())}, {"$set": {"attendees": students}}
    )
    return insert_res


def get_today():
    day = client.attendance.find_one({"day": str(datetime.datetime.now().date())})
    day["_id"] = str(day["_id"])
    day["attendees"] = list(map(convert, day["attendees"]))
    return day


def get_time_stamps():
    time_stamps = client.attendance.find({}, {"_id": 0, "attendees": 0})
    return list(time_stamps)


def check_attendance(regnumber):
    # inner helper function for ticking attendance
    def tick_attendance(attendee):
        if attendee["reg"] == regnumber and not attendee.get("attended"):
            attendee["time"] = str(datetime.datetime.now().time())
            attendee["attended"] = True
            return attendee
        return attendee

    today_attendees = client.attendance.find_one(
        {"day": str(datetime.datetime.now().date())}
    )["attendees"]

    client.attendance.update_one(
        {"day": str(datetime.datetime.now().date())},
        {"$set": {"attendees": list(map(tick_attendance, today_attendees))}},
    )
    day = client.attendance.find_one({"day": str(datetime.datetime.now().date())})
    day["_id"] = str(day["_id"])
    day["attendees"] = list(map(convert, day["attendees"]))
    return day


def get_attendance(day):
    if day := client.attendance.find_one({"day": day}):
        day["_id"] = str(day["_id"])
        day["attendees"] = list(map(convert, day["attendees"]))
        return day
    return None


def delete_from_attendance(day, regnumber):
    def remove_from_attendance(attendee):
        attendee["attended"] = (
            False if attendee["regnumber"] == regnumber else attendee["attended"]
        )
        return attendee

    if attendees := client.attendance.find_one({"day": day})["attendees"]:
        updated_attendance = client.attendance.update_one(
            {"day": day},
            {"$set": {"attendees": list(map(remove_from_attendance, attendees))}},
        )
        return updated_attendance
    return None
