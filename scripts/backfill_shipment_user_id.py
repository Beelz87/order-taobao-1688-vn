import os
import sys

# Thêm thư mục gốc dự án vào sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.shipment import Shipment
from app.models.consignment import Consignment

def backfill_shipment_user_ids():
    db: Session = SessionLocal()
    try:
        # Tìm tất cả shipment chưa có user_id
        shipments = db.query(Shipment).filter(Shipment.user_id == None).all()
        print(f"🔍 Found {len(shipments)} shipments missing user_id.")

        updated_count = 0
        for shipment in shipments:
            consignment = db.query(Consignment).filter_by(id=shipment.consignment_id).first()
            if consignment and consignment.user_id:
                shipment.user_id = consignment.user_id
                db.add(shipment)
                updated_count += 1
                print(f"✅ Shipment {shipment.id} updated with user_id {consignment.user_id}")
            else:
                print(f"⚠️ Shipment {shipment.id} skipped (no consignment or user_id found)")

        db.commit()
        print(f"🎉 Done. Total updated shipments: {updated_count}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during update: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    backfill_shipment_user_ids()