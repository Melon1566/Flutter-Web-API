import mysql.connector
import simplejson as json
import datetime as datetime
import requests


accountsEndpoint = "vsbl-prod.cluster-ch0dsenirhlb.us-east-1.rds.amazonaws.com"
readOnly = "vsbl-prod-proxy-read-only.endpoint.proxy-ch0dsenirhlb.us-east-1.rds.amazonaws.com"

masterDB = mysql.connector.connect(
    host=accountsEndpoint,
    user='admin',
    passwd='adminpass',
    database='Accounts'
)

masterCursor = masterDB.cursor()


def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def buildResults(data, rowHeaders):
    results = []

    for row in data:
        results.append(dict(zip(rowHeaders, decodeResults(row))))
    return results


def decodeResults(row):
    newList = []
    for i in list(row):
        if(i != None):

            if(type(i) == bytearray):
                i = i.decode('utf-8')
        newList.append(i)

    return tuple(newList)


def buildSuccessResponse(data):
    response = {"Data": data, "Error": "None"}
    return json.dumps(response, default=defaultconverter)


def buildErrorResponse(error):
    response = {"Data": "None", "Error": error}
    return json.dumps(response)


def getDayofWeekFromInt(day):
    if(day == 1):
        return "Sunday"
    elif(day == 2):
        return "Monday"
    elif(day == 3):
        return "Tuesday"
    elif(day == 4):
        return "Wednesday"
    elif(day == 5):
        return "Thursday"
    elif(day == 6):
        return "Friday"
    elif(day == 7):
        return "Saturday"
    else:
        return "None"


def sendPushNotification(userID, title, body, payload):

    db = mysql.connector.connect(
        host=accountsEndpoint,
        user='admin',
        passwd='adminpass',
        database='Accounts'
    )

    cursor = db.cursor()

    try:
        serverToken = 'AAAA7iJcuMI:APA91bHr_H8f-mH4gdHvnlP02zLNL0kFIQ4Aj8kM-aH7zVszoqJ3xyfupQUT33dwzjq0fht5AcvuxnUe9BmfQ-xD79d_Cegxyjd74iYiq4oTPMjF8IcpYHOG81hgBmP43jeoz881522T'
        print('executing query to fetch push token')
        arguments = (str(userID), )
        print(arguments)
        cursor.execute(
            f"select PushNotificationToken from Users where UserID = {userID}")
        print('executed query for push notification')

        results = cursor.fetchall()
        row_headers = [x[0] for x in cursor.description]
        results = buildResults(data=results, rowHeaders=row_headers)
        print('results: ' + str(results))
        token = results[0]["PushNotificationToken"]

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }
        if(payload != None):
            body = {
                'notification': {'title': f'{title}',
                                 'body': f'{body}',

                                 },
                'to':
                token,
                'data': payload,
                'priority': 'high',
            }
        else:
            body = {
                'notification': {'title': f'{title}',
                                 'body': f'{body}',

                                 },
                'to':
                token,
                'data': {"Type": "Push"},
                'priority': 'high',
            }
        print('sending the push notification')
        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
        print(response.status_code)

        return 1

    except:
        return 0


def getQuarterParameters(date):

    dateObject = datetime.datetime.fromisoformat(str(date))

    startDate = ''
    endDate = ''
    if(dateObject.month >= 1 and dateObject.month <= 3):
        startDate = f'{dateObject.year}-01-01'
        endDate = f'{dateObject.year}-03-31'
    elif (dateObject.month >= 4 and dateObject.month <= 6):
        startDate = f'{dateObject.year}-04-01'
        endDate = f'{dateObject.year}-06-30'
    elif (dateObject.month >= 7 and dateObject.month <= 9):
        startDate = f'{dateObject.year}-07-01'
        endDate = f'{dateObject.year}-09-30'
    elif (dateObject.month >= 10 and dateObject.month <= 12):
        startDate = f'{dateObject.year}-10-01'
        endDate = f'{dateObject.year}-12-31'

    return startDate, endDate
