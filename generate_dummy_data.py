"""
Tao bo DUMMY DATA dau vao (~80 cong ty SEA) cho he thong scoring Vela.
Phu day du cac kich ban thuc te de kiem thu pipeline. Seed co dinh -> tai lap duoc.
Xuat ra: vela_companies_input.csv
"""
import csv, random

random.seed(42)
CURRENT_YEAR = 2026

COUNTRIES = ["Vietnam","Vietnam","Vietnam","Singapore","Indonesia","Thailand","Philippines","Malaysia"]

# (vertical, mo ta mission-critical, co phai VMS vertical khong)
VERTICALS = [
    ("Healthcare", "Phan mem quan ly benh an va lich hen, dung hang ngay trong van hanh phong kham", True),
    ("Logistics", "Phan mem dieu phoi xe va theo doi don hang cho cong ty logistics", True),
    ("Education", "Phan mem quan ly truong hoc, cot loi cho van hanh dao tao", True),
    ("Agriculture", "Phan mem quan ly chuoi cung ung nong san cho doanh nghiep", True),
    ("Construction", "Phan mem quan ly du an xay dung va tien do cong trinh", True),
    ("Accounting", "Phan mem ke toan va quan ly tai chinh doanh nghiep", True),
    ("Insurance", "Phan mem quan ly hop dong bao hiem cho dai ly", True),
    ("Legal", "Phan mem quan ly ho so va vu viec cho cong ty luat", True),
    ("Real Estate", "Phan mem quan ly bat dong san va giao dich cho moi gioi", True),
    ("Pharma Distribution", "Phan mem quan ly kho va phan phoi cho chuoi nha thuoc", True),
    ("Manufacturing", "Phan mem quan ly san xuat va ton kho cho nha may", True),
    ("F&B", "Phan mem quan ly chuoi nha hang va dat ban", True),
    ("Government", "Phan mem quan ly thu tuc hanh chinh cho co quan nha nuoc", True),
    ("Dental", "Phan mem quan ly phong kham nha khoa, dung trong van hanh hang ngay", True),
    ("HR Tech", "Phan mem quan ly nhan su va tinh luong cho doanh nghiep", True),
    ("Horizontal utility", "Tien ich nho ho tro cong viec, khach hay dung kem Excel", False),
    ("Consumer", "App tien ich cho nguoi tieu dung ca nhan", False),
]

FOUNDER_DEEP = ["Cuu bac si 15 nam roi lap cong ty", "12 nam trong nganh truoc khi lap cong ty",
                "Cuu giam doc van hanh nganh, 10 nam kinh nghiem", "Chuyen gia nganh hon 8 nam"]
PRICING = ["subscription","subscription","hybrid","one_time","freemium"]
CONC = ["low","low","med","high",None]
AGES = ["senior","mid","young"]

def maybe(val, p_missing):
    """Tra ve None voi xac suat p_missing -> mo phong data thieu."""
    return None if random.random() < p_missing else val

rows = []
idx = 0

def add(scenario, n, **opts):
    """Sinh n cong ty theo mot kich ban, voi cac tham so xac suat thieu data."""
    global idx
    for _ in range(n):
        idx += 1
        country = opts.get("country") or random.choice(COUNTRIES)
        vert, desc, is_vms = random.choice(opts.get("vert_pool", VERTICALS))
        name = f"{vert.split()[0]}{random.choice(['Soft','Sys','Pro','Hub','Core','Flow','One','Plus'])}{idx:02d}"
        founded = opts["founded"]()
        rev_reg = None
        # Cong ty VN co the co registry revenue (hard data)
        if country == "Vietnam" and random.random() < opts.get("p_registry", 0.4):
            rev_reg = random.choice([1_800_000, 2_100_000, 2_400_000, 3_000_000, 900_000])
        rows.append({
            "name": name,
            "country": country,
            "is_software": opts.get("is_software", True),
            "is_b2b": opts.get("is_b2b", True),
            "founded_year": founded,
            "product_desc": desc,
            "vertical": vert,
            "num_competitors": random.choice([2,3,4,5,8,12,20,40]),
            "customer_count": maybe(random.choice([30,55,80,120,150,200]), opts.get("m_cust",0.1)),
            "revenue_concentration": maybe(random.choice(CONC[:4]), opts.get("m_conc",0.2)),
            "founder_background": maybe(random.choice(FOUNDER_DEEP), opts.get("m_founder",0.15)),
            "employee_count": maybe(random.choice([8,15,22,30,45,70,110]), opts.get("m_emp",0.15)),
            "registry_revenue": rev_reg,
            "pricing_model": maybe(random.choice(PRICING), opts.get("m_price",0.1)),
            "g2_long_tenure": maybe(random.choice([True,True,False]), opts.get("m_sticky",0.2)),
            "recent_funding": maybe(random.choice([False,False,True]), opts.get("m_fund",0.15)),
            "founder_age_signal": maybe(random.choice(AGES), opts.get("m_age",0.15)),
        })

# --- Cac kich ban (tong ~80) ---
# 1) Ung vien Tier A: du data, vertical manh, lau nam
add("A", 14, founded=lambda: random.randint(2005,2014),
    vert_pool=VERTICALS[:15], m_cust=0.05, m_conc=0.05, m_founder=0.05,
    m_emp=0.05, m_price=0.05, m_sticky=0.05, m_fund=0.05, m_age=0.05, p_registry=0.6)

# 2) B-ready: du data, chi so vua phai
add("Bready", 18, founded=lambda: random.randint(2013,2019),
    vert_pool=VERTICALS[:15], m_cust=0.1, m_conc=0.1, m_founder=0.1,
    m_emp=0.1, m_price=0.1, m_sticky=0.1, m_fund=0.1, m_age=0.1)

# 3) B-enrich (edge case VN): thieu nhieu nhung la VN -> registry tra duoc
add("Benrich_VN", 14, founded=lambda: random.choice([None, None, 2010, 2012]),
    country="Vietnam", vert_pool=VERTICALS[:15], m_cust=0.6, m_conc=0.6,
    m_founder=0.6, m_emp=0.7, m_price=0.2, m_sticky=0.2, m_fund=0.6, m_age=0.5, p_registry=0.2)

# 4) B-enrich FLAG: thieu cai kho tra (churn/pricing), non-VN
add("Benrich_flag", 10, founded=lambda: random.randint(2008,2015),
    country=random.choice(["Thailand","Singapore","Malaysia"]), vert_pool=VERTICALS[:15],
    m_cust=0.1, m_conc=0.1, m_founder=0.1, m_emp=0.1,
    m_price=0.8, m_sticky=0.9, m_fund=0.8, m_age=0.7)

# 5) C - B2C (bi loai tang 1)
add("C_b2c", 8, founded=lambda: random.randint(2015,2023),
    is_b2b=False, vert_pool=[VERTICALS[16]], m_cust=0.5)

# 6) C - qua tre (<5 nam)
add("C_young", 6, founded=lambda: random.randint(2022,2024),
    vert_pool=VERTICALS[:15], m_cust=0.2)

# 7) C - non-software
add("C_nonsw", 4, founded=lambda: random.randint(2008,2018),
    is_software=False, vert_pool=VERTICALS[:8])

# 8) C - gac lai (thieu nhieu + nho)
add("C_parked", 6, founded=lambda: random.randint(2018,2021),
    vert_pool=[VERTICALS[15]], m_cust=0.7, m_conc=0.7, m_founder=0.7,
    m_emp=0.0, m_price=0.7, m_sticky=0.8, m_fund=0.7, m_age=0.7)

# Ghi CSV
cols = ["name","country","is_software","is_b2b","founded_year","product_desc","vertical",
        "num_competitors","customer_count","revenue_concentration","founder_background",
        "employee_count","registry_revenue","pricing_model","g2_long_tenure",
        "recent_funding","founder_age_signal"]

with open("vela_companies_input.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r[k] is None else r[k]) for k in cols})

print(f"Da tao {len(rows)} cong ty -> vela_companies_input.csv")
# Thong ke nhanh
from collections import Counter
print("Phan bo quoc gia:", dict(Counter(r["country"] for r in rows)))
