import csv
import io
from repositories.booking_repository import BookingRepository

class ReportService:
    def bookings_csv(self) -> str:
        rows = BookingRepository().all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Booking ID", "Customer", "Email", "Property", "Check In", "Check Out", "Guests", "Total Price", "Status"])
        for r in rows:
            writer.writerow([r["id"], r["customer_name"], r["customer_email"], r["property_name"], r["check_in"], r["check_out"], r["guests"], r["total_price"], r["status"]])
        return output.getvalue()

    def bookings_txt(self) -> str:
        rows = BookingRepository().all()
        lines = [
            "LAPORAN BOOKING USTAYEASE",
            "=" * 50,
            ""
        ]
        if not rows:
            lines.append("Belum ada data booking.")
        for r in rows:
            lines.extend([
                f"Booking ID : #{r['id']}",
                f"Customer   : {r['customer_name']} ({r['customer_email']})",
                f"Property   : {r['property_name']}",
                f"Tanggal    : {r['check_in']} s/d {r['check_out']}",
                f"Guests     : {r['guests']}",
                f"Total      : Rp {int(r['total_price']):,}".replace(",", "."),
                f"Status     : {r['status']}",
                "-" * 50
            ])
        return "\n".join(lines)

    def receipt_txt(self, booking_id: int) -> str:
        row = BookingRepository().find_detail(booking_id)
        if not row:
            raise ValueError("Booking tidak ditemukan")
        return "\n".join([
            "STRUK / BUKTI PEMESANAN USTAYEASE",
            "=" * 48,
            f"Booking ID       : #{row['id']}",
            f"Customer         : {row['customer_name']}",
            f"Email            : {row['customer_email']}",
            f"No HP            : {row['customer_phone']}",
            f"Property         : {row['property_name']}",
            f"Lokasi           : {row['property_location']}",
            f"Check-in         : {row['check_in']}",
            f"Check-out        : {row['check_out']}",
            f"Guests           : {row['guests']}",
            f"Metode Bayar     : {row.get('payment_method') or '-'}",
            f"Status Pembayaran: {row.get('payment_status') or row['status']}",
            f"Total            : Rp {int(row['total_price']):,}".replace(",", "."),
            "=" * 48,
            "Terima kasih sudah melakukan pemesanan."
        ])
