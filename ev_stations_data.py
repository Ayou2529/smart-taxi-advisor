# Bangkok EV Charging Stations Database
# Data compiled from PEA VOLTA, EGAT EleXA, EA Anywhere networks

EV_STATIONS_BANGKOK = [
    # Central Bangkok - Shopping & Entertainment
    {
        "name": "PEA VOLTA - Central World",
        "provider": "PEA VOLTA",
        "location": "ถนนพระราม 1, ปทุมวัน",
        "lat": 13.7467,
        "lng": 100.5392,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2 (43kW)", "DC CCS (50kW)"],
        "open_24h": True,
        "icon": "⚡"
    },
    {
        "name": "EA Anywhere - Siam Paragon",
        "provider": "EA Anywhere",
        "location": "ชั้น B, สยามพารากอน",
        "lat": 13.7467,
        "lng": 100.5343,
        "pricing": {"peak": "8.0 ฿/หน่วย", "off_peak": "6.0 ฿/หน่วย"},
        "charger_types": ["DC Fast (60kW)"],
        "open_24h": False,
        "icon": "⚡"
    },
    {
        "name": "PEA VOLTA - Terminal 21",
        "provider": "PEA VOLTA",
        "location": "ชั้น 5, อโศก",
        "lat": 13.7372,
        "lng": 100.5597,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2", "DC CHAdeMO (50kW)"],
        "open_24h": False,
        "icon": "⚡"
    },
    
    # Airports
    {
        "name": "EGAT EleXA - Suvarnabhumi Airport",
        "provider": "EGAT",
        "location": "ที่จอดรถ P4, สุวรรณภูมิ",
        "lat": 13.6900,
        "lng": 100.7501,
        "pricing": {"peak": "7.5 ฿/หน่วย", "off_peak": "7.5 ฿/หน่วย"},
        "charger_types": ["DC Fast (120kW)", "Ultra Fast (350kW)"],
        "open_24h": True,
        "icon": "⚡"
    },
    {
        "name": "PEA VOLTA - Don Mueang Airport",
        "provider": "PEA VOLTA",
        "location": "ที่จอดรถ P1, ดอนเมือง",
        "lat": 13.9126,
        "lng": 100.6066,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["DC CCS (50kW)"],
        "open_24h": True,
        "icon": "⚡"
    },
    
    # Business Districts
    {
        "name": "EA Anywhere - Sathorn Square",
        "provider": "EA Anywhere",
        "location": "ถนนสาทร, ยานนาวา",
        "lat": 13.7245,
        "lng": 100.5327,
        "pricing": {"peak": "8.0 ฿/หน่วย", "off_peak": "6.0 ฿/หน่วย"},
        "charger_types": ["DC Fast (60kW)"],
        "open_24h": True,
        "icon": "⚡"
    },
    {
        "name": "PEA VOLTA - Silom Complex",
        "provider": "PEA VOLTA",
        "location": "ถนนสีลม, บางรัก",
        "lat": 13.7284,
        "lng": 100.5321,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2", "DC CCS"],
        "open_24h": False,
        "icon": "⚡"
    },
    
    # North Bangkok
    {
        "name": "PEA VOLTA - Future Park Rangsit",
        "provider": "PEA VOLTA",
        "location": "ชั้น G, รังสิต",
        "lat": 13.9814,
        "lng": 100.5924,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["DC CCS (50kW)"],
        "open_24h": False,
        "icon": "⚡"
    },
    {
        "name": "EGAT EleXA - Chatuchak Weekend Market",
        "provider": "EGAT",
        "location": "ใกล้ MRT จตุจักร",
        "lat": 13.7998,
        "lng": 100.5501,
        "pricing": {"peak": "7.5 ฿/หน่วย", "off_peak": "7.5 ฿/หน่วย"},
        "charger_types": ["DC Fast (80kW)"],
        "open_24h": False,
        "icon": "⚡"
    },
    
    # East Bangkok
    {
        "name": "EA Anywhere - Mega Bangna",
        "provider": "EA Anywhere",
        "location": "ชั้น 1, บางนา",
        "lat": 13.6674,
        "lng": 100.6476,
        "pricing": {"peak": "8.0 ฿/หน่วย", "off_peak": "6.0 ฿/หน่วย"},
        "charger_types": ["DC Fast (60kW)", "Ultra Fast (150kW)"],
        "open_24h": False,
        "icon": "⚡"
    },
    {
        "name": "PEA VOLTA - Seacon Square",
        "provider": "PEA VOLTA",
        "location": "ชั้น B, ศรีนครินทร์",
        "lat": 13.6587,
        "lng": 100.6493,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2", "DC CHAdeMO"],
        "open_24h": False,
        "icon": "⚡"
    },
    
    # West Bangkok
    {
        "name": "PEA VOLTA - MBK Center",
        "provider": "PEA VOLTA",
        "location": "ชั้น 7, พญาไท",
        "lat": 13.7444,
        "lng": 100.5304,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2", "DC CCS"],
        "open_24h": False,
        "icon": "⚡"
    },
    {
        "name": "EA Anywhere - The Mall Bangkapi",
        "provider": "EA Anywhere",
        "location": "ชั้น B, บางกะปิ",
        "lat": 13.7726,
        "lng": 100.6443,
        "pricing": {"peak": "8.0 ฿/หน่วย", "off_peak": "6.0 ฿/หน่วย"},
        "charger_types": ["DC Fast (60kW)"],
        "open_24h": False,
        "icon": "⚡"
    },
    
    # South Bangkok
    {
        "name": "EGAT EleXA - Central Rama 2",
        "provider": "EGAT",
        "location": "ชั้น G, พระราม 2",
        "lat": 13.6907,
        "lng": 100.4191,
        "pricing": {"peak": "7.5 ฿/หน่วย", "off_peak": "7.5 ฿/หน่วย"},
        "charger_types": ["DC Fast (100kW)"],
        "open_24h": False,
        "icon": "⚡"
    },
    {
        "name": "PEA VOLTA - Central Rama 3",
        "provider": "PEA VOLTA",
        "location": "ชั้น B, ยานนาวา",
        "lat": 13.6990,
        "lng": 100.5309,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2", "DC CCS"],
        "open_24h": False,
        "icon": "⚡"
    },
    
    # Strategic Locations
    {
        "name": "PEA VOLTA - Headquarters (Ngamwongwan)",
        "provider": "PEA VOLTA",
        "location": "200 ถนนงามวงศ์วาน, จตุจักร",
        "lat": 13.8466,
        "lng": 100.5616,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2", "DC CCS", "DC CHAdeMO"],
        "open_24h": True,
        "icon": "⚡"
    },
    {
        "name": "EA Anywhere - PTT Station (Sukhumvit)",
        "provider": "EA Anywhere",
        "location": "ปั๊ม PTT สุขุมวิท 50",
        "lat": 13.7038,
        "lng": 100.6011,
        "pricing": {"peak": "8.0 ฿/หน่วย", "off_peak": "6.0 ฿/หน่วย"},
        "charger_types": ["DC Fast (80kW)"],
        "open_24h": True,
        "icon": "⚡"
    },
    {
        "name": "EGAT EleXA - Ladprao Intersection",
        "provider": "EGAT",
        "location": "แยกลาดพร้าว-รัชดา",
        "lat": 13.7643,
        "lng": 100.5623,
        "pricing": {"peak": "7.5 ฿/หน่วย", "off_peak": "7.5 ฿/หน่วย"},
        "charger_types": ["DC Fast (120kW)"],
        "open_24h": True,
        "icon": "⚡"
    },
    {
        "name": "PEA VOLTA - Victory Monument",
        "provider": "PEA VOLTA",
        "location": "ใกล้ BTS อนุสาวรีย์ชัยฯ",
        "lat": 13.7637,
        "lng": 100.5374,
        "pricing": {"peak": "7.2 ฿/หน่วย", "off_peak": "5.5 ฿/หน่วย"},
        "charger_types": ["AC Type 2", "DC CCS"],
        "open_24h": False,
        "icon": "⚡"
    },
    {
        "name": "EA Anywhere - Emporium",
        "provider": "EA Anywhere",
        "location": "ชั้น B, สุขุมวิท 24",
        "lat": 13.7310,
        "lng": 100.5691,
        "pricing": {"peak": "8.0 ฿/หน่วย", "off_peak": "6.0 ฿/หน่วย"},
        "charger_types": ["DC Fast (60kW)"],
        "open_24h": False,
        "icon": "⚡"
    }
]
