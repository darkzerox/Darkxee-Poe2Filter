# DZX Filter POE2 - TFT Market Data Update (2024)

## การอัปเดต Filter Groups ตามข้อมูล TFT

### ไฟล์ที่อัปเดต:

1. **crafting.filter** - รวมข้อมูล TFT ทั้งหมดไว้ในไฟล์เดียว
   - Tier 1: Divine+ Value Items (8x = 1div) - Dark Green
   - Tier 2: High Value Items (15-30 Exalted) - Bright Green  
   - Tier 3: Medium Value Items (2-3 Exalted) - Light Green
   - Tier 4: Lower Value Items (1-2 Exalted) - Yellow
   - Tier 5: Chaos Value Items (1-5 Chaos) - Orange
   - Tier 6: Low Value Items (1 Chaos) - Red

### ไฟล์ที่ลบออก:

2. **divine_tier.filter** - รวมเข้าใน crafting.filter
3. **high_value_weapons.filter** - รวมเข้าใน crafting.filter
4. **high_value_armor.filter** - รวมเข้าใน crafting.filter

### ไฟล์ที่กลับไปเป็นแบบเดิม:

5. **ring.filter** - Legacy Rules Only (Breach Rings)
6. **belts.filter** - Legacy Rules Only
7. **amulets.filter** - Legacy Rules Only

### ข้อมูล TFT ที่ใช้ใน crafting.filter:

- **Forked Spear**: 8x = 1div, 1 = 15-30ex
- **Heavy Belt**: 8ex each, 2-3ex each
- **Sapphire Ring**: 7ex each
- **Ruby Ring, Amethyst Ring, Topaz Ring, Lazuli Ring**: 2-3ex each
- **Stellar Amulet**: 3ex each
- **Attuned Wand, Siphoning Wand, Acrid Wand**: 3ex each
- **Gold Ring, Iron Ring**: 1-2ex each
- **Armor pieces**: 1-5c each
- **Weapons**: 1-5c each

### การจัดกลุ่มตามราคา:

1. **Divine Tier** (Dark Green): 8x = 1div
2. **High Value** (Bright Green): 15-30ex each
3. **Medium Value** (Light Green): 2-8ex each
4. **Lower Value** (Yellow): 1-2ex each
5. **Chaos Value** (Orange): 1-5c each
6. **Low Value** (Red): 1c each

### เสียงและเอฟเฟกต์:

- **Divine Tier**: divine.mp3, Yellow Star, Volume 300
- **High Value**: unique.mp3, Yellow Star, Volume 300
- **Medium Value**: base_item.mp3, Orange Diamond, Volume 200
- **Lower Value**: currency.mp3, Yellow Circle, Volume 150
- **Chaos Value**: salvage.mp3, Orange Circle, Volume 100
- **Low Value**: salvage.mp3, Red Circle, Volume 50

### การตั้งค่า:

- **ItemLevel**: >= 82 สำหรับ items ราคาสูง, >= 79 สำหรับ items ราคาต่ำ
- **AreaLevel**: >= 65 สำหรับทุก items
- **Rarity**: Normal Magic สำหรับ crafting items
- **Font Size**: 35-42 ตามความสำคัญ

การอัปเดตนี้รวมข้อมูล TFT ทั้งหมดไว้ในไฟล์ crafting.filter ไฟล์เดียว เพื่อให้ง่ายต่อการจัดการและอัปเดต
