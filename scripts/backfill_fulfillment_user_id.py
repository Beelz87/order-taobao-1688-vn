import os
import sys

# Thêm thư mục gốc dự án vào sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.fulfillment import Fulfillment
from app.models.shipment import Shipment

def backfill_fulfillment_user_ids():
    db: Session = SessionLocal()
    try:
        # Tìm tất cả fulfillment chưa có user_id
        fulfillments = db.query(Fulfillment).filter(Fulfillment.user_id == None).all()
        print(f"🔍 Found {len(fulfillments)} fulfillments missing user_id.")

        updated_count = 0
        for fulfillment in fulfillments:
            shipment = db.query(Shipment).filter_by(id=fulfillment.shipment_id).first()
            if shipment and shipment.user_id:
                fulfillment.user_id = shipment.user_id
                db.add(fulfillment)
                updated_count += 1
                print(f"✅ Fulfillment {fulfillment.id} updated with user_id {shipment.user_id}")
            else:
                print(f"⚠️ Fulfillment {fulfillment.id} skipped (no shipment or shipment.user_id found)")

        db.commit()
        print(f"🎉 Done. Total updated fulfillments: {updated_count}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during update: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    backfill_fulfillment_user_ids()
