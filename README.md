# PastPortAPI - Standalone

##### URl Directory:
- '/api/locations' --------- Returns all stored locations
- '/api/locations/last' ---- Returns last stored location
- '/api/now' -------------- Stores and returns current barge location


##### Config Structure:

{
    "ENV":null,
    "DEBUG":true,
    "TESTING":false,
    "LOGGING":true,
    "RESTFUL_JSON":{
        "separators": [", ",": "],
        "indent":2
    },
    "SCHEDULER_DELAY_TIME":600,
    "WEB":{
        "URL":(...),
        "UID":(...),
        "PWD":(...),
        "CONNECTION":{
            "MAX_RETRIES":1,
            "BACKOFF_FACTOR":0.5,
            "BACKOFF_MAX":1,
            "STATUS_FORCELIST":[
                408,409,429,500,502,503,504
            ]
        }
    },
    "DB":{
        "DRIVER":"{SQL Server}",
        "SERVER":"127.0.0.1",
        "DATABASE":(...),
        "UID":(...),
        "PWD":(...)
    },
    "ERR":{
        "MAIL_HOST":[(...),(...)],
        "FROM_ADDR":(...),
        "TO_ADDRS":(...),
        "SUBJECT_DEFAULT":(...)
    }
}