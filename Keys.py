import json

def getAPIinfo():
    try:
        with open('schedulerAPIinfo.json', 'r') as file:
            info = json.load(file)

    except:
        info = askInfo()
        with open('schedulerAPIinfo.json', 'w') as file:
            json.dump(info, file)
    return info[0], info[1]


def getCourses():
    try:
        with open('courseInfo.json', 'r') as file:
            courses = json.load(file)
    except:
        courses = getCourseNums()
        with open('courseInfo.json', 'w') as file:
            json.dump(courses, file)
    return courses

def askInfo():
    urlGot = False
    while not urlGot:
        print('Please input the base url of your canvas website. You can find this by opening Canvas and looking at the url.')
        print('for example, uncw\'s base url is: https://uncw.instructure.com')
        url = input('\nInput school url: ').strip(' ')
        if 'https://' not in url and 'http://' not in url:
            print('\nError, please input the full url including https, try again\n')
        else:
            urlGot = True

    print('Please input the api key for your canvas account. You can find this by opening Canvas,')
    print('then going to account --> settings --> Approved Integrations')
    print('Once there, click new access token and it will generate an api key for you, copy and paste that below')
    key = input('\nApi Key: ').strip(' ')

    return [url, key]

def getCourseNums():
    print('To label your assignments, please input a short 10 or less character title of your course.')
    print('For example, CSC 331. Then, seperated by a ", " input the corresponding course id for the course.')
    print('To find a courses id go to that course on canvas and you\'ll see it in the url it\'s a 5 digit number')
    print('\nAn example of a proper input is as follows: "CSC 331, 12345"')
    print('When done entering courses simply type "done" and hit enter')
    print('\nWARNING any courses you don\'t enter now will simply appear as their course id on your calendar.')

    gettingNums = True
    courses = dict()
    while gettingNums:
        inpt = input('\nPlease input a course and id: ').strip(' ')
        if inpt.lower() == 'done':
            gettingNums = False
        else:
            if ', ' not in inpt:
                print('\nError, invalid input\n')
            else:
                inpt = inpt.split(', ')
                courses[inpt[1]] = inpt[0]
    return courses