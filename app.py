from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/customers", methods=["POST"])
def createCustomer():
    return jsonify({
        "status": 201,
        "data": {
            "message": "createCustomer stub"
        },
        "error": None
    }), 201

@app.route("/customers", methods=["GET"])
def listCustomers():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listCustomers stub"
        },
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["GET"])
def showCustomer(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showCustomer stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["PUT"])
def updateCustomer(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "updateCustomer stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/customers/<id>", methods=["DELETE"])
def deleteCustomer(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deleteCustomer stub",
            "id": id
        },
        "error": None
    }), 200

@app.route("/laundry-orders", methods=["POST"])
def createLaundryOrder():
    return jsonify({
        "status": 201,
        "data": {
            "message": "createLaundryOrder stub"
        },
        "error": None
    }), 201


@app.route("/laundry-orders", methods=["GET"])
def listLaundryOrders():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listLaundryOrders stub"
        },
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["GET"])
def showLaundryOrder(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showLaundryOrder stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["PUT"])
def updateLaundryOrder(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "updateLaundryOrder stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/laundry-orders/<id>", methods=["DELETE"])
def deleteLaundryOrder(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deleteLaundryOrder stub",
            "id": id
        },
        "error": None
    }), 200

@app.route("/pickup-schedules", methods=["POST"])
def createPickupSchedule():
    return jsonify({
        "status": 201,
        "data": {
            "message": "createPickupSchedule stub"
        },
        "error": None
    }), 201


@app.route("/pickup-schedules", methods=["GET"])
def listPickupSchedules():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listPickupSchedules stub"
        },
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["GET"])
def showPickupSchedule(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showPickupSchedule stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["PUT"])
def updatePickupSchedule(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "updatePickupSchedule stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/pickup-schedules/<id>", methods=["DELETE"])
def deletePickupSchedule(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deletePickupSchedule stub",
            "id": id
        },
        "error": None
    }), 200
@app.route("/delivery-records", methods=["POST"])
def createDeliveryRecord():
    return jsonify({
        "status": 201,
        "data": {
            "message": "createDeliveryRecord stub"
        },
        "error": None
    }), 201


@app.route("/delivery-records", methods=["GET"])
def listDeliveryRecords():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listDeliveryRecords stub"
        },
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["GET"])
def showDeliveryRecord(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showDeliveryRecord stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["PUT"])
def updateDeliveryRecord(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "updateDeliveryRecord stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/delivery-records/<id>", methods=["DELETE"])
def deleteDeliveryRecord(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deleteDeliveryRecord stub",
            "id": id
        },
        "error": None
    }), 200

@app.route("/payments", methods=["POST"])
def createPayment():
    return jsonify({
        "status": 201,
        "data": {
            "message": "createPayment stub"
        },
        "error": None
    }), 201


@app.route("/payments", methods=["GET"])
def listPayments():
    return jsonify({
        "status": 200,
        "data": {
            "message": "listPayments stub"
        },
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["GET"])
def showPayment(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "showPayment stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["PUT"])
def updatePayment(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "updatePayment stub",
            "id": id
        },
        "error": None
    }), 200


@app.route("/payments/<id>", methods=["DELETE"])
def deletePayment(id):
    return jsonify({
        "status": 200,
        "data": {
            "message": "deletePayment stub",
            "id": id
        },
        "error": None
    }), 200

if __name__ == "__main__":
    app.run(debug=True)