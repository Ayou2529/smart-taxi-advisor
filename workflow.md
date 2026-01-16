# Workflow การทำงานของระบบ

## System Flow

1. **Start**: คุณกดรันโปรแกรม `python taxi_advisor.py`
2. **Fetch Data**: โปรแกรมวิ่งไปดึงตารางเที่ยวบินจาก AviationStack
3. **Analyze**: นับจำนวน flight ที่จะลงใน 1-2 ชม. ข้างหน้า
   - ถ้า > 20 เที่ยว: 🔥 **หนาแน่นมาก** (High Demand)
   - ถ้า 10-20 เที่ยว: 🟡 **ปานกลาง** (Moderate)
   - ถ้า < 10 เที่ยว: 🟢 **น้อย** (Low)
4. **Notify**: ส่งข้อความสรุปเข้า Line Notify ของคุณ
5. **Traffic Link**: แนบลิงก์ Google Maps แบบเปิด Traffic Layer ให้แฟนกดเช็คได้เลย

## Deployment Options (ทางเลือกรันโปรแกรม)

- **Local PC**: รันมือเอง (เหมาะกับตอนนี้)
- **GitHub Actions**: ตั้งเวลารันเองอัตโนมัติ (แนะนำสำหรับอนาคต)
- **Cloud Server**: เช่าเซิร์ฟเวอร์เปิด 24 ชม. (มีค่าใช้จ่าย)
