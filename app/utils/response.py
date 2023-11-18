

def bad_response(message):
    return ({"status": 400, "message": message}, 400)

def good_response(data):
    return  ({"status": 200, "data": data}, 200)

def unauthorized():
    return  ({"status": 401, "message": "Unauthorized"}, 401)

def not_found(message = "Not Found!"):
    return  ({"status": 404, "message": message}, 404)

def server_error():
    return  ({"status": 500, "message":  "Server error"}, 500)
