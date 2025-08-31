# การปรับปรุง Crafting Filter - ข้อมูลตลาด POE2

## วันที่ปรับปรุง: 2025-01-27

## สรุปการเปลี่ยนแปลง

### 1. จัดลำดับความสำคัญตามมูลค่า

#### Tier 1: High Value Items (5-20 Exalted) - สีเขียวเข้ม
- **Rings**: Ruby Ring, Amethyst Ring, Topaz Ring, Sapphire Ring, Lazuli Ring, Pearl Ring
- **Belts**: Heavy Belt, Ornate Belt  
- **Amulets**: Stellar Amulet, Jade Choir Amulet
- **Weapons**: Attuned Wand, Siphoning Wand, Gemini Bow

#### Tier 2: Medium Value Items (1-12 Chaos) - สีเขียวอ่อน
- **Armor**: Falconer's Jacket, Vile Robe, Sleek Jacket, Sandsworn Sandals, Vaal Gloves, Vaal Wraps, Kamasan Tiara
- **Weapons**: Spiked Spear, Rattling Sceptre, Forked Spear
- **Accessories**: Breach Ring, Gold Ring

#### Tier 3: Lower Value Items (1-3 Chaos) - สีเหลือง
- Quickslip Shoes, Primed Quiver, Sacred Focus, Seaglass Spear, Dualstring Bow, Chiming Staff, Massive Spear

### 2. สร้างไฟล์ใหม่: mirror_tier.filter

#### Mirror Tier Items (20+ Exalted) - สีแดง
- **Sapphire Ring**: 10ex (stock: 21)
- **Gemini Bow**: 20ex (stock: 27)

#### Divine Tier Items (1 Divine+) - สีทอง
- **Stellar Amulet**: 4x = 1div (stock: 12-31)

### 3. ปรับปรุงการตั้งค่า

#### Item Level Requirements
- **Tier 1**: ItemLevel >= 82 (ไอเทมที่มีมูลค่าสูง)
- **Tier 2**: ItemLevel >= 82 (ไอเทมที่มีมูลค่าปานกลาง)
- **Tier 3**: ItemLevel >= 79 (ไอเทมที่มีมูลค่าต่ำ)

#### Sound Effects
- **Mirror Tier**: เสียง mirror.mp3 (300 volume)
- **High Value**: เสียง unique.mp3 (300 volume)
- **Medium Value**: เสียง base_item.mp3 (200 volume)
- **Low Value**: เสียง currency.mp3 (150 volume)

#### Visual Indicators
- **Mirror Tier**: สีแดง, ขอบขาว, Red Star icon
- **High Value**: สีเขียวเข้ม, ขอบเหลือง, Yellow Star icon
- **Medium Value**: สีเขียวอ่อน, ขอบฟ้า, Orange Diamond icon
- **Low Value**: สีเหลือง, ขอบเหลือง, Yellow Circle icon

## ข้อมูลตลาดที่ใช้

### ไอเทมที่มีมูลค่าสูง (5-20 Exalted)
```
Ruby Ring: 5ex (stock: 18-21)
Amethyst Ring: 5ex (stock: 21)
Topaz Ring: 5ex (stock: 24)
Sapphire Ring: 10ex (stock: 21)
Lazuli Ring: 5ex (stock: 14)
Pearl Ring: 2ex (stock: 35)
Heavy Belt: 5-8ex (stock: 5-59)
Ornate Belt: 5ex (stock: 12)
Gemini Bow: 20ex (stock: 27)
Attuned Wand: 3ex (stock: 200+)
Siphoning Wand: 3ex (stock: 200+)
```

### ไอเทมที่มีมูลค่าปานกลาง (1-12 Chaos)
```
Falconer's Jacket: 5-12c (stock: 24-75)
Vile Robe: 5-10c (stock: 24-37)
Sleek Jacket: 5-10c (stock: 5-20)
Sandsworn Sandals: 5-12c (stock: 13-70)
Vaal Gloves: 8c (stock: 6-36)
Vaal Wraps: 8c (stock: 3)
Spiked Spear: 1-5c (stock: 75+)
Rattling Sceptre: 1-2c (stock: 34)
Breach Ring: 2c (stock: 25)
```

### ไอเทมที่มีมูลค่าต่ำ (1-3 Chaos)
```
Quickslip Shoes: 2-3c (stock: 46)
Primed Quiver: 1c (stock: 20+)
Sacred Focus: 1c (stock: 64)
```

## การใช้งาน

### สำหรับผู้เล่นทั่วไป
- ฟิลเตอร์จะเน้นไอเทมที่มีมูลค่าสูงเป็นพิเศษ
- เสียงและสีจะช่วยให้แยกแยะมูลค่าได้ง่าย
- ไอเทมที่มีมูลค่าต่ำจะแสดงด้วยสีเหลือง

### สำหรับผู้เล่นที่เน้นการทำเงิน
- เน้นไอเทม Tier 1 และ Mirror Tier
- ใช้เสียงเป็นตัวบ่งชี้มูลค่า
- ตรวจสอบ Item Level ก่อนเก็บ

## การปรับแต่งเพิ่มเติม

### เพิ่มไอเทมใหม่
หากต้องการเพิ่มไอเทมใหม่ ให้แก้ไขไฟล์:
- `dzx_filter/filter_group/crafting.filter` สำหรับไอเทมทั่วไป
- `dzx_filter/filter_group/mirror_tier.filter` สำหรับไอเทมที่มีมูลค่าสูงมาก

### ปรับแต่งเสียง
ไฟล์เสียงอยู่ใน `dzx_filter/soundeffect/type-01/`:
- `mirror.mp3` - สำหรับไอเทม Mirror Tier
- `unique.mp3` - สำหรับไอเทมที่มีมูลค่าสูง
- `base_item.mp3` - สำหรับไอเทมที่มีมูลค่าปานกลาง
- `currency.mp3` - สำหรับไอเทมที่มีมูลค่าต่ำ

## การทดสอบ

### วิธีทดสอบฟิลเตอร์
1. รันสคริปต์สร้างฟิลเตอร์: `python script/start_build.py`
2. ตรวจสอบไฟล์ที่สร้างขึ้นในโฟลเดอร์หลัก
3. ทดสอบในเกม Path of Exile 2

### การตรวจสอบ
- ตรวจสอบว่าไอเทมแสดงด้วยสีที่ถูกต้อง
- ตรวจสอบว่าเสียงทำงานถูกต้อง
- ตรวจสอบว่า Item Level requirements ถูกต้อง

## หมายเหตุ

- ข้อมูลตลาดอาจเปลี่ยนแปลงได้ ควรอัปเดตเป็นระยะ
- ราคาและ stock ขึ้นอยู่กับ server และ league
- ฟิลเตอร์นี้เหมาะสำหรับการเล่นใน endgame (AreaLevel >= 65)
- ควรปรับแต่งตามความต้องการของแต่ละคน
