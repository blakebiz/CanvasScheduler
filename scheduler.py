from canvasapi import Canvas
import datetime
import googCalendar
import Keys

def getEvents():
    courseNums = Keys.getCourses()
    API_URL, API_KEY = Keys.getAPIinfo()

    canvas = Canvas(API_URL, API_KEY)

    events = canvas.get_upcoming_events()
    assignments = []
    for event in events:
        try:
            due_date = datetime.datetime.strptime(event['assignment']['due_at'],"%Y-%m-%dT%H:%M:%SZ") - datetime.timedelta(hours=5)
        except KeyError:
            print("error adding:", event)
        else:
            # if due_date.hour > 18:
            #     due_date.replace(hour=18)

            try:
                label = courseNums[str(event['assignment']['course_id'])]
            except KeyError:
                label = str(event['assignment']['course_id'])

            assignment = [label, event['title'], due_date]
            assignments.append(assignment)

    return assignments


def main():
    assignments = getEvents()
    descs = grabDescriptions()
    for assignment in assignments:
        startTime = (assignment[2] - datetime.timedelta(hours=1)).isoformat()
        endTime = assignment[2].isoformat()
        googEvent = [assignment[0]+' hw', startTime, endTime, assignment[1]]

        if googEvent[3] in descs:
            print('already made:', googEvent[3])
        else:
            googCalendar.createEvent(googEvent[0], googEvent[1], googEvent[2], description=googEvent[3])

def grabDescriptions():
    events = googCalendar.getEvents()
    descs = []
    for event in events:
        try:
            if event['description'] != 'description' and 'confidentiality notice' not in event['description'].lower():
                descs.append(event['description'])
        except KeyError:
            pass
    return descs

if __name__ == '__main__':
    main()