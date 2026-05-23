from flask import Blueprint, jsonify, request, Response
from repositories.property_repository import PropertyRepository
from repositories.booking_repository import BookingRepository
from repositories.stats_repository import StatsRepository
from services.booking_service import BookingService
from services.report_service import ReportService
from repositories.system_repository import SystemRepository
from repositories.user_repository import UserRepository

api = Blueprint("api", __name__, url_prefix="/api")

@api.get("/health")
def health():
    return jsonify({"status": "ok", "app": "STAYINOW Backend"})


@api.get("/system/maintenance")
def get_system_maintenance():
    return jsonify(SystemRepository().get_maintenance())

@api.post("/system/maintenance")
def set_system_maintenance():
    payload = request.get_json() or {}
    enabled = bool(payload.get("maintenance"))
    return jsonify(SystemRepository().set_maintenance(enabled))

@api.post("/auth/register")
def register():
    try:
        return jsonify(UserRepository().create_user(request.get_json() or {})), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.post("/auth/login")
def login():
    try:
        payload = request.get_json() or {}
        return jsonify(UserRepository().login(payload.get("email", ""), payload.get("password", "")))
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@api.get("/properties")
def get_properties():
    rows = PropertyRepository().all()
    for row in rows:
        facilities = row.get("facilities") or ""
        row["facilities"] = [x.strip() for x in facilities.split(",") if x.strip()]
    return jsonify(rows)


@api.post("/properties")
def create_property():
    try:
        row = PropertyRepository().create(request.get_json() or {})
        return jsonify(row), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.patch("/properties/<int:property_id>/maintenance")
def update_maintenance(property_id):
    payload = request.get_json() or {}
    status = payload.get("status")
    if status not in ["available", "maintenance"]:
        return jsonify({"error": "Status harus available atau maintenance"}), 400
    try:
        row = PropertyRepository().update_status(property_id, status)
        return jsonify(row)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@api.get("/bookings")
def get_bookings():
    return jsonify(BookingRepository().all())

@api.post("/bookings")
def create_booking():
    try:
        result = BookingService().create_booking(request.get_json() or {})
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.get("/stats")
def stats():
    return jsonify(StatsRepository().dashboard())

@api.get("/reports/bookings.csv")
def bookings_report():
    csv_text = ReportService().bookings_csv()
    return Response(csv_text, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=bookings_report.csv"})

@api.get("/reports/bookings.txt")
def bookings_report_txt():
    txt = ReportService().bookings_txt()
    return Response(txt, mimetype="text/plain", headers={"Content-Disposition": "attachment; filename=bookings_report.txt"})

@api.get("/receipts/<int:booking_id>.txt")
def booking_receipt_txt(booking_id):
    try:
        txt = ReportService().receipt_txt(booking_id)
        return Response(txt, mimetype="text/plain", headers={"Content-Disposition": f"attachment; filename=receipt_booking_{booking_id}.txt"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
