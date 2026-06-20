"""
Schemes knowledge base — 5 MVP welfare schemes with structured eligibility rules.
"""
from models import Scheme, EligibilityRule

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

SCHEMES: list[Scheme] = [

    # ─── 1. PM-KISAN ──────────────────────────────────────────────────────────
    Scheme(
        id="pm-kisan",
        name="PM-KISAN",
        category="farmer",
        summary=(
            "Pradhan Mantri Kisan Samman Nidhi provides ₹6,000 per year income support "
            "in three installments of ₹2,000 each to small and marginal farmer families."
        ),
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a farmer",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="land_ownership",
                operator="is_true",
                value=True,
                label="Must own agricultural land",
                weight=1.5,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=200000,
                label="Annual income should not exceed ₹2 lakh (for marginal farmers)",
                weight=1.0,
                required=False,
            ),
        ],
        documents_required=[
            "Aadhaar Card",
            "Land Records / Khasra-Khatauni",
            "Bank Account details (linked to Aadhaar)",
            "Citizenship Certificate",
        ],
        official_url="https://pmkisan.gov.in",
        benefit_amount="₹6,000 per year",
        ministry="Ministry of Agriculture & Farmers Welfare",
    ),

    # ─── 2. PMAY — Pradhan Mantri Awas Yojana ────────────────────────────────
    Scheme(
        id="pmay",
        name="PMAY (Pradhan Mantri Awas Yojana)",
        category="housing",
        summary=(
            "PMAY provides financial assistance for construction/purchase of affordable houses "
            "to eligible beneficiaries from EWS, LIG, and MIG categories."
        ),
        eligibility_rules=[
            EligibilityRule(
                field="housing_status",
                operator="in",
                value=["kutcha", "rented", "homeless"],
                label="Should not own a pucca house",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=600000,
                label="Annual income must not exceed ₹6 lakh (EWS/LIG category)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=[
            "Aadhaar Card",
            "Income Certificate",
            "Caste Certificate (if applicable)",
            "Bank Account Details",
            "Self-declaration of no pucca house",
        ],
        official_url="https://pmaymis.gov.in",
        benefit_amount="Up to ₹2.5 lakh subsidy",
        ministry="Ministry of Housing and Urban Affairs",
    ),

    # ─── 3. Ayushman Bharat — PMJAY ──────────────────────────────────────────
    Scheme(
        id="ayushman-bharat",
        name="Ayushman Bharat (PM-JAY)",
        category="healthcare",
        summary=(
            "Pradhan Mantri Jan Arogya Yojana provides health insurance coverage of ₹5 lakh "
            "per family per year for secondary and tertiary hospitalisation."
        ),
        eligibility_rules=[
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=500000,
                label="Annual family income should be ₹5 lakh or below",
                weight=1.5,
                required=True,
            ),
            EligibilityRule(
                field="bpl_card",
                operator="is_true",
                value=True,
                label="BPL card holder (preferred, not mandatory if SECC listed)",
                weight=1.0,
                required=False,
            ),
        ],
        documents_required=[
            "Aadhaar Card (any family member)",
            "Ration Card",
            "Income Certificate",
        ],
        official_url="https://pmjay.gov.in",
        benefit_amount="₹5 lakh health coverage per family per year",
        ministry="Ministry of Health and Family Welfare",
    ),

    # ─── 4. NSAP — National Social Assistance Programme ──────────────────────
    Scheme(
        id="nsap",
        name="NSAP (National Social Assistance Programme)",
        category="pension",
        summary=(
            "NSAP provides social security in the form of old age pension, widow pension, "
            "and disability pension to BPL households."
        ),
        eligibility_rules=[
            EligibilityRule(
                field="senior_citizen_status",
                operator="is_true",
                value=True,
                label="Must be a senior citizen (age ≥ 60) OR disabled",
                weight=2.0,
                required=False,
            ),
            EligibilityRule(
                field="disability_status",
                operator="is_true",
                value=True,
                label="Persons with disability also eligible",
                weight=2.0,
                required=False,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=150000,
                label="Must be from a Below Poverty Line (BPL) household",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=[
            "Aadhaar Card",
            "Age Proof (Birth Certificate or Voter ID)",
            "BPL Card / Ration Card",
            "Bank Account Details",
            "Disability Certificate (for disability pension)",
        ],
        official_url="https://nsap.nic.in",
        benefit_amount="₹200–₹500 per month (pension amount varies by state)",
        ministry="Ministry of Rural Development",
    ),

    # ─── 5. National Scholarship Portal (NSP) ────────────────────────────────
    Scheme(
        id="nsp-scholarship",
        name="National Scholarship Portal (NSP)",
        category="education",
        summary=(
            "NSP is a one-stop platform for all government scholarships including "
            "pre-matric, post-matric, and merit-cum-means scholarships for students "
            "from SC/ST/OBC/Minority/General categories."
        ),
        eligibility_rules=[
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be a currently enrolled student",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=250000,
                label="Family annual income must be ₹2.5 lakh or below",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=[
            "Aadhaar Card",
            "Income Certificate (from competent authority)",
            "Caste Certificate (for reserved category scholarships)",
            "Previous Year Marksheet",
            "Bonafide Certificate from Institution",
            "Bank Account Details (student's own account)",
        ],
        official_url="https://scholarships.gov.in",
        benefit_amount="Varies by scholarship — ₹1,200 to ₹20,000+ per year",
        ministry="Ministry of Electronics and Information Technology / Various ministries",
    ),

    # ─── 6. PM-SVANidhi ──────────────────────────────────────────────────────
    Scheme(
        id="pm-svanidhi",
        name="PM-SVANidhi (PM Street Vendor's AtmaNirbhar Nidhi)",
        category="farmer",
        summary="Special micro-credit facility for street vendors to access collateral-free working capital loan up to ₹10,000.",
        eligibility_rules=[
            EligibilityRule(
                field="occupation",
                operator="eq",
                value="self-employed",
                label="Must be self-employed / street vendor",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Voter Identity Card", "Certificate of Vending / Letter of Recommendation"],
        official_url="https://pmsvanidhi.mohua.gov.in",
        benefit_amount="Collateral-free loan up to ₹10,000",
        ministry="Ministry of Housing and Urban Affairs",
    ),

    # ─── 7. PM Ujjwala Yojana (PMUY) ─────────────────────────────────────────
    Scheme(
        id="pmuy",
        name="PM Ujjwala Yojana (PMUY)",
        category="healthcare",
        summary="PMUY aims to safeguard the health of women & children by providing clean cooking fuel (LPG connection) to BPL households.",
        eligibility_rules=[
            EligibilityRule(
                field="gender",
                operator="eq",
                value="female",
                label="Applicant must be a female",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="bpl_card",
                operator="is_true",
                value=True,
                label="Must belong to BPL category",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Ration Card copy", "BPL Certificate / Income Certificate"],
        official_url="https://www.pmuy.gov.in",
        benefit_amount="Free LPG Connection + First Cylinder Subsidy",
        ministry="Ministry of Petroleum and Natural Gas",
    ),

    # ─── 8. PM Mudra Yojana (PMMY) ──────────────────────────────────────────
    Scheme(
        id="pm-mudra",
        name="PM Mudra Yojana (PMMY)",
        category="farmer",
        summary="Provides collateral-free loans up to ₹10 lakh to non-corporate, non-farm small/micro enterprises.",
        eligibility_rules=[
            EligibilityRule(
                field="occupation",
                operator="eq",
                value="self-employed",
                label="Must be self-employed or running a micro-enterprise",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Business Registration Proof", "Bank Statement (Last 6 Months)"],
        official_url="https://www.mudra.org.in",
        benefit_amount="Loan from ₹50,000 up to ₹10 lakh",
        ministry="Ministry of Finance",
    ),

    # ─── 9. PM Vishwakarma ──────────────────────────────────────────────────
    Scheme(
        id="pm-vishwakarma",
        name="PM Vishwakarma",
        category="farmer",
        summary="Support for traditional artisans and craftspeople with skill training, toolkit incentives, and collateral-free credit.",
        eligibility_rules=[
            EligibilityRule(
                field="occupation",
                operator="eq",
                value="self-employed",
                label="Must be a traditional artisan or craftsman",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Caste Certificate (if applicable)", "Artisan Registration Proof"],
        official_url="https://pmvishwakarma.gov.in",
        benefit_amount="Skill training + ₹15,000 toolkit incentive + ₹3 lakh credit support",
        ministry="Ministry of Micro, Small and Medium Enterprises",
    ),

    # ─── 10. Sukanya Samriddhi Yojana (SSY) ─────────────────────────────────
    Scheme(
        id="sukanya-samriddhi",
        name="Sukanya Samriddhi Yojana (SSY)",
        category="education",
        summary="A small deposit savings scheme for a girl child launched as a part of the 'Beti Bachao Beti Padhao' campaign.",
        eligibility_rules=[
            EligibilityRule(
                field="age",
                operator="lte",
                value=10,
                label="Girl child must be below 10 years of age",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="gender",
                operator="eq",
                value="female",
                label="Applicable only for a girl child",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Birth Certificate of Girl Child", "Aadhaar Card of Parent/Guardian", "Address Proof"],
        official_url="https://www.indiapost.gov.in",
        benefit_amount="High-interest savings account (currently 8.2% tax-free)",
        ministry="Ministry of Finance",
    ),

    # ─── 11. Atal Pension Yojana (APY) ───────────────────────────────────────
    Scheme(
        id="apy",
        name="Atal Pension Yojana (APY)",
        category="pension",
        summary="Pension scheme focused on unorganized sector workers, guaranteeing a minimum monthly pension of ₹1,000 to ₹5,000.",
        eligibility_rules=[
            EligibilityRule(
                field="age",
                operator="gte",
                value=18,
                label="Must be at least 18 years old",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=40,
                label="Must be under 40 years old to join",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Savings Bank Account details (with auto-debit facility)"],
        official_url="https://www.npscra.nsdl.co.in",
        benefit_amount="Guaranteed pension of ₹1,000 to ₹5,000 per month after age 60",
        ministry="Ministry of Finance",
    ),

    # ─── 12. PM Jeevan Jyoti Bima Yojana (PMJJBY) ────────────────────────────
    Scheme(
        id="pmjjby",
        name="PM Jeevan Jyoti Bima Yojana (PMJJBY)",
        category="healthcare",
        summary="A one-year life insurance scheme, renewable from year to year, offering life cover for death due to any reason.",
        eligibility_rules=[
            EligibilityRule(
                field="age",
                operator="gte",
                value=18,
                label="Must be at least 18 years old",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=50,
                label="Must be under 50 years old to join",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Consent for auto-debit from bank account"],
        official_url="https://www.jansuraksha.gov.in",
        benefit_amount="₹2 lakh life insurance coverage for ₹436 annual premium",
        ministry="Ministry of Finance",
    ),

    # ─── 13. PM Suraksha Bima Yojana (PMSBY) ─────────────────────────────────
    Scheme(
        id="pmsby",
        name="PM Suraksha Bima Yojana (PMSBY)",
        category="healthcare",
        summary="Accident insurance scheme offering accidental death and disability cover.",
        eligibility_rules=[
            EligibilityRule(
                field="age",
                operator="gte",
                value=18,
                label="Must be at least 18 years old",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=70,
                label="Must be under 70 years old",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Consent for auto-debit from bank account"],
        official_url="https://www.jansuraksha.gov.in",
        benefit_amount="₹2 lakh accidental death / full disability cover for ₹20 annual premium",
        ministry="Ministry of Finance",
    ),

    # ─── 14. Lakhpati Didi ───────────────────────────────────────────────────
    Scheme(
        id="lakhpati-didi",
        name="Lakhpati Didi",
        category="farmer",
        summary="Empowerment scheme targeting women in Self-Help Groups (SHGs) to help them earn a sustainable annual income of ₹1 lakh or more.",
        eligibility_rules=[
            EligibilityRule(
                field="gender",
                operator="eq",
                value="female",
                label="Applicable only to female beneficiaries",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=150000,
                label="Priority for low-income rural households",
                weight=1.0,
                required=False,
            ),
        ],
        documents_required=["Aadhaar Card", "Self-Help Group (SHG) membership proof", "Income Certificate"],
        official_url="https://rural.gov.in",
        benefit_amount="Interest subvention loans + financial literacy and business training support",
        ministry="Ministry of Rural Development",
    ),

    # ─── 15. PM Garib Kalyan Anna Yojana (PMGKAY) ───────────────────────────
    Scheme(
        id="pmgkay",
        name="PM Garib Kalyan Anna Yojana (PMGKAY)",
        category="healthcare",
        summary="Food security welfare scheme providing free food grains to the poorest citizens through Public Distribution System.",
        eligibility_rules=[
            EligibilityRule(
                field="bpl_card",
                operator="is_true",
                value=True,
                label="Must possess a valid BPL card or Priority Household (PHH) card",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Ration Card (BPL/Antyodaya)", "Aadhaar Card"],
        official_url="https://nfsa.gov.in",
        benefit_amount="5 kg free food grains per person per month",
        ministry="Ministry of Consumer Affairs, Food and Public Distribution",
    ),

    # ─── 16. PM Shram Yogi Maan-dhan (PM-SYM) ────────────────────────────────
    Scheme(
        id="pm-sym",
        name="PM Shram Yogi Maan-dhan (PM-SYM)",
        category="pension",
        summary="Voluntary and contributory pension scheme for unorganized workers like home-based workers, street vendors, rickshaw pullers.",
        eligibility_rules=[
            EligibilityRule(
                field="age",
                operator="gte",
                value=18,
                label="Must be between 18 and 40 years of age",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=40,
                label="Must be under 40 years old",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=180000,
                label="Monthly income should be ₹15,000 or below",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Savings Bank Account / Jan Dhan Account with IFSC"],
        official_url="https://maandhan.in",
        benefit_amount="Guaranteed monthly pension of ₹3,000 after age 60",
        ministry="Ministry of Labour and Employment",
    ),

    # ─── 17. Janani Suraksha Yojana (JSY) ────────────────────────────────────
    Scheme(
        id="jsy",
        name="Janani Suraksha Yojana (JSY)",
        category="healthcare",
        summary="Safe motherhood intervention scheme promoting institutional delivery among poor pregnant women.",
        eligibility_rules=[
            EligibilityRule(
                field="gender",
                operator="eq",
                value="female",
                label="Only applicable for pregnant women",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="bpl_card",
                operator="is_true",
                value=True,
                label="Must belong to Below Poverty Line (BPL) household",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "BPL Ration Card copy", "MCP Card (Mother and Child Protection)"],
        official_url="https://nhm.gov.in",
        benefit_amount="Cash assistance of ₹1,000 to ₹1,400 for institutional delivery",
        ministry="Ministry of Health and Family Welfare",
    ),

    # ─── 18. DAY-NRLM (National Rural Livelihoods Mission) ───────────────────
    Scheme(
        id="day-nrlm",
        name="DAY-NRLM (National Rural Livelihoods Mission)",
        category="farmer",
        summary="Promotes rural livelihoods by enabling rural poor households to access self-employment and skilled wage employment opportunities.",
        eligibility_rules=[
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=150000,
                label="Targeted at rural poor households",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "BPL Certificate / SECC list document", "SHG Group Details"],
        official_url="https://aajeevika.gov.in",
        benefit_amount="Revolving fund and capital subsidy support for self-help groups",
        ministry="Ministry of Rural Development",
    ),

    # ─── 19. National Means-cum-Merit Scholarship (NMMSS) ───────────────────
    Scheme(
        id="nmmss",
        name="National Means-cum-Merit Scholarship (NMMSS)",
        category="education",
        summary="Scholarship awarded to meritorious students of economically weaker sections to arrest their drop-out at class VIII.",
        eligibility_rules=[
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be a currently enrolled student in Class IX",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=350000,
                label="Parental income must not exceed ₹3.5 lakh per annum",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Class VIII Marksheet showing at least 55% marks", "Income Certificate"],
        official_url="https://education.gov.in",
        benefit_amount="Scholarship of ₹12,000 per year (₹1,000 per month)",
        ministry="Ministry of Education",
    ),

    # ─── 20. PM-PRANAM ───────────────────────────────────────────────────────
    Scheme(
        id="pm-pranam",
        name="PM-PRANAM",
        category="farmer",
        summary="Program for Restoration, Awareness, Nourishment and Amelioration of Mother Earth to promote balanced use of chemical fertilizers.",
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a practicing farmer",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Land Records / Soil Health Card"],
        official_url="https://fertilizer.aws.nic.in",
        benefit_amount="Subsidy savings allocated for bio-fertilizer infrastructure and organic farming training",
        ministry="Ministry of Chemicals and Fertilizers",
    ),

    # ─── 21. PMFBY (Pradhan Mantri Fasal Bima Yojana) ──────────────────────────
    Scheme(
        id="pmfby",
        name="PMFBY (Pradhan Mantri Fasal Bima Yojana)",
        category="farmer",
        summary="Crop insurance scheme providing financial support to farmers suffering crop loss/damage arising out of unforeseen events.",
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a farmer",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="land_ownership",
                operator="is_true",
                value=True,
                label="Must own or cultivate agricultural land",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Land Records / Cultivation Certificate", "Bank Account Details", "Sowing Certificate"],
        official_url="https://pmfby.gov.in",
        benefit_amount="Insurance coverage for crop loss/damage",
        ministry="Ministry of Agriculture & Farmers Welfare",
    ),

    # ─── 22. Soil Health Card Scheme ─────────────────────────────────────────
    Scheme(
        id="soil-health-card",
        name="Soil Health Card Scheme",
        category="farmer",
        summary="Provides Soil Health Cards with crop-wise nutrient status and recommendations for optimal fertilizer use.",
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a farmer",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="land_ownership",
                operator="is_true",
                value=True,
                label="Must own agricultural land",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Land Records / Soil Sample Details"],
        official_url="https://soilhealth.dac.gov.in",
        benefit_amount="Soil health report and customized fertilizer recommendations",
        ministry="Ministry of Agriculture & Farmers Welfare",
    ),

    # ─── 23. PKVY (Paramparagat Krishi Vikas Yojana) ──────────────────────────
    Scheme(
        id="pkvy",
        name="PKVY (Paramparagat Krishi Vikas Yojana)",
        category="farmer",
        summary="Promotes organic farming through cluster approach and certification, raising farmer incomes and soil health.",
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a farmer",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Land Records", "Organic Certification Proof"],
        official_url="https://dshd.dac.gov.in",
        benefit_amount="₹50,000 per hectare financial assistance for organic farming",
        ministry="Ministry of Agriculture & Farmers Welfare",
    ),

    # ─── 24. PMKSY (Pradhan Mantri Krishi Sinchayee Yojana) ────────────────────
    Scheme(
        id="pmksy",
        name="PMKSY (Pradhan Mantri Krishi Sinchayee Yojana)",
        category="farmer",
        summary="Focuses on end-to-end water conservation, farm-level water management, and micro-irrigation systems.",
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a farmer",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="land_ownership",
                operator="is_true",
                value=True,
                label="Must own agricultural land with water source",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Land Records", "Irrigation System Details / Quotes"],
        official_url="https://pmksy.gov.in",
        benefit_amount="Up to 55% subsidy on micro-irrigation systems (drip/sprinkler)",
        ministry="Ministry of Agriculture & Farmers Welfare",
    ),

    # ─── 25. PM-KMY (Pradhan Mantri Kisan Maan-Dhan Yojana) ────────────────────
    Scheme(
        id="pm-kmy",
        name="PM Kisan Maan-Dhan Yojana (PM-KMY)",
        category="pension",
        summary="Old age pension scheme for all small and marginal farmers providing a minimum assured pension of ₹3,000 per month.",
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a farmer",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="gte",
                value=18,
                label="Age must be at least 18 years",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=40,
                label="Age must be under 40 years to join",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Land Records / Khasra-Khatauni", "Savings Bank Account details (linked to Aadhaar)"],
        official_url="https://maandhan.in",
        benefit_amount="Guaranteed monthly pension of ₹3,000 after age 60",
        ministry="Ministry of Agriculture & Farmers Welfare",
    ),

    # ─── 26. PMVVY (Pradhan Mantri Vaya Vandana Yojana) ───────────────────────
    Scheme(
        id="pmvvy",
        name="PMVVY (Pradhan Mantri Vaya Vandana Yojana)",
        category="pension",
        summary="Pension scheme for senior citizens offering an assured rate of return and old age income security.",
        eligibility_rules=[
            EligibilityRule(
                field="senior_citizen_status",
                operator="is_true",
                value=True,
                label="Must be a senior citizen (age >= 60)",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Age Proof (Birth Certificate or Voter ID)", "Bank Account Details"],
        official_url="https://licindia.in",
        benefit_amount="Guaranteed pension of 7.4% per annum for 10 years",
        ministry="Ministry of Finance",
    ),

    # ─── 27. VPBY (Varishtha Pension Bima Yojana) ─────────────────────────────
    Scheme(
        id="vpby",
        name="VPBY (Varishtha Pension Bima Yojana)",
        category="pension",
        summary="A pension scheme managed by LIC designed to provide social security to the elderly through an immediate annuity.",
        eligibility_rules=[
            EligibilityRule(
                field="senior_citizen_status",
                operator="is_true",
                value=True,
                label="Must be a senior citizen (age >= 60)",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Age Proof", "Bank Account Details"],
        official_url="https://licindia.in",
        benefit_amount="Immediate annuity pension based on deposit amount",
        ministry="Ministry of Finance",
    ),

    # ─── 28. PMBJP (Pradhan Mantri Bhartiya Janaushadhi Pariyojana) ─────────────
    Scheme(
        id="pmbjp",
        name="PMBJP (Pradhan Mantri Bhartiya Janaushadhi Pariyojana)",
        category="healthcare",
        summary="Campaign launched by the Department of Pharmaceuticals to provide quality generic medicines at affordable prices to all.",
        eligibility_rules=[
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=10000000,
                label="Open to all Indian citizens",
                weight=1.0,
                required=False,
            ),
        ],
        documents_required=["Doctor's Prescription (preferred, not mandatory for general purchase)"],
        official_url="http://janaushadhi.gov.in",
        benefit_amount="High-quality generic medicines at 50% to 90% cheaper rates",
        ministry="Ministry of Chemicals and Fertilizers",
    ),

    # ─── 29. PMMVY (Pradhan Mantri Matru Vandana Yojana) ─────────────────────
    Scheme(
        id="pmmvy",
        name="PMMVY (Pradhan Mantri Matru Vandana Yojana)",
        category="healthcare",
        summary="Maternity benefit program providing cash incentives for pregnant and lactating mothers for the first living child.",
        eligibility_rules=[
            EligibilityRule(
                field="gender",
                operator="eq",
                value="female",
                label="Applicant must be a female",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "MCP Card (Mother and Child Protection)", "Bank Account Details", "Husband's Aadhaar Card"],
        official_url="https://wcd.nic.in",
        benefit_amount="Cash incentive of ₹5,000 in three installments",
        ministry="Ministry of Women and Child Development",
    ),

    # ─── 30. ICDS (Integrated Child Development Services) ─────────────────────
    Scheme(
        id="icds",
        name="ICDS (Integrated Child Development Services)",
        category="healthcare",
        summary="Provides food, preschool education, primary healthcare, immunization, health checkup and referral services to children and mothers.",
        eligibility_rules=[
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=150000,
                label="Children below 6 years of age OR pregnant/lactating women",
                weight=1.0,
                required=False,
            ),
        ],
        documents_required=["Aadhaar Card", "Birth Certificate (for children)", "Ration Card"],
        official_url="https://wcd.nic.in",
        benefit_amount="Supplementary nutrition, immunization, and pre-school education",
        ministry="Ministry of Women and Child Development",
    ),

    # ─── 31. PMAY-G (Pradhan Mantri Awas Yojana - Gramin) ──────────────────────
    Scheme(
        id="pmay-g",
        name="PMAY-G (Pradhan Mantri Awas Yojana - Gramin)",
        category="housing",
        summary="Provides financial assistance to rural households for construction of pucca houses with basic amenities.",
        eligibility_rules=[
            EligibilityRule(
                field="housing_status",
                operator="in",
                value=["kutcha", "rented", "homeless"],
                label="Should not own a pucca house",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Income Certificate", "Ration Card / BPL Card", "Bank Account Details", "Self-declaration of no pucca house"],
        official_url="https://pmayg.nic.in",
        benefit_amount="Financial assistance of ₹1.2 lakh (plains) to ₹1.3 lakh (hilly areas)",
        ministry="Ministry of Rural Development",
    ),

    # ─── 32. DDA Housing Scheme ──────────────────────────────────────────────
    Scheme(
        id="dda-housing",
        name="DDA Housing Scheme",
        category="housing",
        summary="Allotment of affordable residential flats across Delhi to various income categories via computerized draws.",
        eligibility_rules=[
            EligibilityRule(
                field="age",
                operator="gte",
                value=18,
                label="Must be at least 18 years old",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "PAN Card", "Income Certificate", "Residential Proof"],
        official_url="https://dda.gov.in",
        benefit_amount="Affordable housing allotment via computerized draw",
        ministry="Ministry of Housing and Urban Affairs / Delhi Development Authority",
    ),

    # ─── 33. PMKVY (Pradhan Mantri Kaushal Vikas Yojana) ─────────────────────
    Scheme(
        id="pmkvy",
        name="PMKVY (Pradhan Mantri Kaushal Vikas Yojana)",
        category="education",
        summary="Skill certification scheme aiming to enable Indian youth to take up industry-relevant skill training.",
        eligibility_rules=[
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Open to youth; student or unemployed status preferred",
                weight=1.0,
                required=False,
            ),
        ],
        documents_required=["Aadhaar Card", "Educational Certificates (if any)", "Bank Account Details"],
        official_url="https://pmkvyofficial.org",
        benefit_amount="Free skill training, assessment, and placement support",
        ministry="Ministry of Skill Development and Entrepreneurship",
    ),

    # ─── 34. DDU-GKY (Deen Dayal Upadhyaya Grameen Kaushalya Yojana) ──────────
    Scheme(
        id="ddu-gky",
        name="DDU-GKY (Deen Dayal Upadhyaya Grameen Kaushalya Yojana)",
        category="education",
        summary="Demand-driven placement-linked skill training initiative targeting rural poor youth.",
        eligibility_rules=[
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=150000,
                label="Must belong to rural poor household (BPL/Ration card)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "BPL/Ration Card", "Age Proof", "Educational Certificates"],
        official_url="https://ddugky.gov.in",
        benefit_amount="Skill training, study materials, and guaranteed job placement",
        ministry="Ministry of Rural Development",
    ),

    # ─── 35. KGBV (Kasturba Gandhi Balika Vidyalaya) ──────────────────────────
    Scheme(
        id="kgbv",
        name="KGBV (Kasturba Gandhi Balika Vidyalaya)",
        category="education",
        summary="Residential upper primary schools for girls belonging to SC, ST, OBC, Minority, and BPL families.",
        eligibility_rules=[
            EligibilityRule(
                field="gender",
                operator="eq",
                value="female",
                label="Applicable only for girls",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be an active student",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Birth Certificate / Age Proof", "Caste Certificate", "BPL Card / Income Certificate"],
        official_url="https://education.gov.in",
        benefit_amount="Free residential elementary and secondary education",
        ministry="Ministry of Education",
    ),

    # ─── 36. PM-POSHAN (Mid-Day Meal Scheme) ──────────────────────────────────
    Scheme(
        id="pm-poshan",
        name="PM-POSHAN (Mid-Day Meal Scheme)",
        category="education",
        summary="Provides hot cooked meals to school children in government and government-aided schools for improved nutrition.",
        eligibility_rules=[
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be a student enrolled in Classes I to VIII",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["School Enrollment Proof (handled by schools)"],
        official_url="https://pmposhan.education.gov.in",
        benefit_amount="Free hot cooked meal every school day",
        ministry="Ministry of Education",
    ),

    # ─── 37. CSSS (Central Sector Scheme of Scholarship) ─────────────────────
    Scheme(
        id="csss-scholarship",
        name="Central Sector Scheme of Scholarship (CSSS)",
        category="education",
        summary="Provides financial assistance to meritorious students from poor families to meet a part of their day-to-day expenses while pursuing higher studies.",
        eligibility_rules=[
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be a currently enrolled student in college/university",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=450000,
                label="Family annual income must be ₹4.5 lakh or below",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Class XII Marksheet", "Income Certificate", "Fee Receipt / College Admission Proof"],
        official_url="https://scholarships.gov.in",
        benefit_amount="₹12,000 per year for graduation, ₹20,000 per year for post-graduation",
        ministry="Ministry of Education",
    ),

    # ─── 38. Stand-Up India Scheme ───────────────────────────────────────────
    Scheme(
        id="standup-india",
        name="Stand-Up India Scheme",
        category="farmer",
        summary="Promotes entrepreneurship among women and SC/ST communities by providing bank loans for greenfield enterprises.",
        eligibility_rules=[
            EligibilityRule(
                field="gender",
                operator="eq",
                value="female",
                label="Must be a female entrepreneur OR SC/ST category applicant",
                weight=2.0,
                required=False,
            ),
        ],
        documents_required=["Aadhaar Card", "Caste Certificate (if applicable)", "Business Plan / Project Report", "PAN Card"],
        official_url="https://www.standupmitra.in",
        benefit_amount="Bank loan between ₹10 lakh and ₹1 crore for starting a business",
        ministry="Ministry of Finance",
    ),

    # ─── 39. PM Garib Kalyan Rojgar Abhiyaan ─────────────────────────────────
    Scheme(
        id="pmgkra",
        name="PM Garib Kalyan Rojgar Abhiyaan",
        category="farmer",
        summary="Massive employment-cum-rural infrastructure creation scheme to empower returnee migrants and rural citizens.",
        eligibility_rules=[
            EligibilityRule(
                field="farmer_status",
                operator="is_true",
                value=True,
                label="Must be a rural worker or returnee migrant",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Ration Card", "Self-declaration of migrant worker status"],
        official_url="https://rural.gov.in",
        benefit_amount="Employment opportunities for 125 days across 25 works",
        ministry="Ministry of Rural Development",
    ),

    # ─── 40. National Family Benefit Scheme (NFBS) ───────────────────────────
    Scheme(
        id="nfbs",
        name="National Family Benefit Scheme (NFBS)",
        category="pension",
        summary="Provides one-time lump sum financial assistance to a BPL household on the death of the primary breadwinner.",
        eligibility_rules=[
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=150000,
                label="Must belong to Below Poverty Line (BPL) household",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Aadhaar Card", "Death Certificate of Breadwinner", "BPL Card / Income Certificate", "Relationship Proof"],
        official_url="https://nsap.nic.in",
        benefit_amount="One-time lump sum assistance of ₹20,000",
        ministry="Ministry of Rural Development",
    ),

    # ─── 41. US Medicaid ─────────────────────────────────────────────────────
    Scheme(
        id="us-medicaid",
        name="Medicaid (US Healthcare)",
        category="healthcare",
        summary="Medicaid provides free or low-cost health coverage to eligible low-income individuals, families, children, pregnant women, the elderly, and people with disabilities.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=40000,
                label="Household annual income should not exceed $40,000 (standard state threshold)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Proof of Income (W-2 / Pay stubs)", "Proof of U.S. Citizenship or Legal Residency", "Government-issued Photo ID"],
        official_url="https://www.medicaid.gov",
        benefit_amount="Free or low-cost comprehensive healthcare coverage",
        ministry="U.S. Department of Health and Human Services",
    ),

    # ─── 42. US SNAP (Food Stamps) ───────────────────────────────────────────
    Scheme(
        id="us-snap",
        name="SNAP (Supplemental Nutrition Assistance Program)",
        category="healthcare",
        summary="SNAP provides food-purchasing assistance to supplement the food budget of needy families so they can purchase healthy food and move towards self-sufficiency.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=30000,
                label="Gross annual household income should be below $30,000 (roughly 130% of the Federal Poverty Level)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Proof of Income", "Proof of Identity", "Utility and Rent bills (to calculate deductions)"],
        official_url="https://www.fns.usda.gov/snap",
        benefit_amount="Monthly balance deposited to Electronic Benefit Transfer (EBT) card",
        ministry="U.S. Department of Agriculture (USDA)",
    ),

    # ─── 43. Federal Pell Grant ──────────────────────────────────────────────
    Scheme(
        id="us-pell-grant",
        name="Federal Pell Grant",
        category="education",
        summary="Federal Pell Grants are direct grants awarded to undergraduate students who display exceptional financial need and have not earned a bachelor's or professional degree.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be an enrolled undergraduate student",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=60000,
                label="Total family annual income must not exceed $60,000",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Free Application for Federal Student Aid (FAFSA) confirmation", "Tax Returns / W-2 forms", "High School Diploma or equivalent"],
        official_url="https://studentaid.gov",
        benefit_amount="Up to $7,395 per academic year for tuition and college expenses",
        ministry="U.S. Department of Education",
    ),

    # ─── 44. Section 8 Housing Voucher ───────────────────────────────────────
    Scheme(
        id="us-section-8",
        name="Section 8 (Housing Choice Voucher Program)",
        category="housing",
        summary="The housing choice voucher program is the federal government's major program for assisting very low-income families, the elderly, and the disabled to afford decent, safe, and sanitary housing.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="housing_status",
                operator="in",
                value=["rented", "homeless"],
                label="Must be a tenant renting or currently homeless",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=45000,
                label="Gross annual household income should be below $45,000 (varies by county, typically below 50% of local median income)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of Income", "Social Security Numbers for all household members", "Rental History and references", "U.S. Citizenship or eligible immigration status"],
        official_url="https://www.hud.gov",
        benefit_amount="Subsidy paid directly to landlord covering a portion of rent",
        ministry="U.S. Department of Housing and Urban Development (HUD)",
    ),

    # ─── 45. Supplemental Security Income (SSI) ──────────────────────────────
    Scheme(
        id="us-ssi",
        name="Supplemental Security Income (SSI)",
        category="pension",
        summary="SSI is a federal program designed to help aged, blind, and disabled people who have little or no income by providing monthly cash support.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=25000,
                label="Gross annual household income must not exceed $25,000",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Proof of Age (Birth certificate)", "Medical records of disability (if under 65)", "Bank statements / Proof of assets"],
        official_url="https://www.ssa.gov",
        benefit_amount="Up to $943 per month for an individual or $1,415 per month for a couple",
        ministry="U.S. Social Security Administration (SSA)",
    ),

    # ─── 46. Children's Health Insurance Program (CHIP) ──────────────────────
    Scheme(
        id="us-chip",
        name="CHIP (Children's Health Insurance Program)",
        category="healthcare",
        summary="CHIP provides low-cost health coverage to children in families that earn too much money to qualify for Medicaid but not enough to buy private insurance.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=18,
                label="Child must be 18 years of age or younger",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=50000,
                label="Household annual income must not exceed $50,000 (varies by state, typically below 200% of FPL)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Child's Birth Certificate", "Proof of Income", "Proof of residency", "Social Security Number (SSN)"],
        official_url="https://www.insurekidsnow.gov",
        benefit_amount="Low-cost comprehensive health and dental insurance for children",
        ministry="U.S. Department of Health and Human Services",
    ),

    # ─── 47. Low Income Home Energy Assistance Program (LIHEAP) ────────────────
    Scheme(
        id="us-liheap",
        name="LIHEAP (Low Income Home Energy Assistance Program)",
        category="housing",
        summary="LIHEAP helps low-income households meet their immediate home energy needs, offering assistance with heating/cooling bills, energy crises, and weatherization repairs.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=30000,
                label="Annual household income must be below $30,000 (standard threshold at 150% of the FPL)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Recent utility bills", "Proof of gross income", "Social Security Numbers", "Proof of home ownership or rent lease"],
        official_url="https://www.acf.hhs.gov/ocs/low-income-home-energy-assistance-program-liheap",
        benefit_amount="Direct financial credit on heating/cooling utility bills or emergency heating repair",
        ministry="U.S. Department of Health and Human Services",
    ),

    # ─── 48. National School Lunch Program (NSLP) ────────────────────────────
    Scheme(
        id="us-nslp",
        name="NSLP (National School Lunch Program)",
        category="education",
        summary="NSLP is a federally assisted meal program operating in public and non-profit private schools, providing nutritionally balanced, low-cost or free lunches to children each school day.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be an enrolled student",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=35000,
                label="Family annual income must not exceed $35,000 for free lunch eligibility",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["School Enrollment details", "Household income self-declaration / application form"],
        official_url="https://www.fns.usda.gov/nslp",
        benefit_amount="Free or reduced-price nutritious school lunches",
        ministry="U.S. Department of Agriculture (USDA)",
    ),

    # ─── 49. Temporary Assistance for Needy Families (TANF) ──────────────────
    Scheme(
        id="us-tanf",
        name="TANF (Temporary Assistance for Needy Families)",
        category="pension",
        summary="TANF provides state-administered cash grants and support services to very low-income families with children to promote job preparation, work, and marriage.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=20000,
                label="Family annual income must not exceed $20,000 (varies by state, set below local thresholds)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of income and employment status", "Social Security Numbers", "Children's birth certificates", "Proof of US citizenship / legal status"],
        official_url="https://www.acf.hhs.gov/ofa/programs/temporary-assistance-needy-families-tanf",
        benefit_amount="Monthly cash assistance + job training and placement support",
        ministry="U.S. Department of Health and Human Services",
    ),

    # ─── 50. Head Start Program ──────────────────────────────────────────────
    Scheme(
        id="us-head-start",
        name="Head Start Program",
        category="education",
        summary="Head Start and Early Head Start provide comprehensive early childhood education, health, nutrition, and parent involvement services to low-income children and their families.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=5,
                label="Child must be 5 years of age or younger",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=30000,
                label="Family annual income must be below $30,000 (federal poverty guidelines limit)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Child's Birth Certificate", "Proof of family income", "Immunization records", "Address proof"],
        official_url="https://eclkc.ohs.acf.hhs.gov",
        benefit_amount="Free comprehensive early childhood education, daycare, and nutritional care",
        ministry="U.S. Department of Health and Human Services",
    ),

    # ─── 51. Federal Work-Study Program ──────────────────────────────────────
    Scheme(
        id="us-work-study",
        name="Federal Work-Study",
        category="education",
        summary="Provides part-time employment opportunities for undergraduate and graduate students with financial need, helping them earn money to offset college costs.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be an enrolled student",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=50000,
                label="Total family annual income must not exceed $50,000",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["FAFSA Submission confirmation", "Financial Aid award letter", "College enrollment proof"],
        official_url="https://studentaid.gov",
        benefit_amount="Part-time campus/community employment earning at least federal minimum wage",
        ministry="U.S. Department of Education",
    ),

    # ─── 52. Social Security Disability Insurance (SSDI) ─────────────────────
    Scheme(
        id="us-ssdi",
        name="Social Security Disability Insurance (SSDI)",
        category="pension",
        summary="SSDI pays monthly benefits to you and certain members of your family if you have a medically determinable disability and worked long enough in social security covered jobs.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="disability_status",
                operator="is_true",
                value=True,
                label="Must have a qualified medical disability status",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=45000,
                label="Annual earned income must be below $45,000 (substantial gainful activity limits)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Detailed medical histories and doctor assessments", "W-2 forms / Tax records"],
        official_url="https://www.ssa.gov/benefits/disability",
        benefit_amount="Monthly cash benefits based on historical earnings",
        ministry="U.S. Social Security Administration (SSA)",
    ),

    # ─── 53. Earned Income Tax Credit (EITC) ─────────────────────────────────
    Scheme(
        id="us-eitc",
        name="Earned Income Tax Credit (EITC)",
        category="pension",
        summary="EITC is a federal tax credit for low- to moderate-income working individuals and couples, particularly those with children, providing a substantial tax refund.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=55000,
                label="Gross annual household income must not exceed $55,000",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Federal Tax Return (Form 1040)", "W-2 forms", "Social Security Numbers for all children claimed"],
        official_url="https://www.irs.gov/eitc",
        benefit_amount="Tax credit refund ranging from $600 to over $7,400 depending on children",
        ministry="Internal Revenue Service (IRS)",
    ),

    # ─── 54. USDA Section 504 Housing Repair Program ─────────────────────────
    Scheme(
        id="us-home-repair",
        name="USDA Section 504 Home Repair Program",
        category="housing",
        summary="Provides loans to very-low-income rural homeowners to repair, improve or modernize their homes, or grants to elderly low-income homeowners to remove safety hazards.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="housing_status",
                operator="eq",
                value="pucca",
                label="Must own and occupy the home in a rural area",
                weight=1.5,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=30000,
                label="Family annual income must not exceed $30,000 (set below 50% of local median income)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of Home Ownership (Title deeds)", "Proof of income", "Quotes/Estimates for repair works", "Residency proof"],
        official_url="https://www.rd.usda.gov",
        benefit_amount="Up to $40,000 low-interest repair loan (1%) or up to $10,000 hazard removal grant for elderly",
        ministry="U.S. Department of Agriculture (USDA) Rural Development",
    ),

    # ─── 55. Medicare (US Senior Healthcare) ─────────────────────────────────
    Scheme(
        id="us-medicare",
        name="Medicare",
        category="healthcare",
        summary="Medicare is the federal health insurance program for people who are 65 or older, certain younger people with disabilities, and people with End-Stage Renal Disease.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="senior_citizen_status",
                operator="is_true",
                value=True,
                label="Must be a senior citizen (65 years of age or older)",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Proof of Age", "Social Security Card", "U.S. Citizenship or Permanent Residency card"],
        official_url="https://www.medicare.gov",
        benefit_amount="Federal hospital (Part A) and medical (Part B) health insurance coverage",
        ministry="U.S. Department of Health and Human Services / Social Security Administration",
    ),

    # ─── 56. WIC (Supplemental Nutrition Program) ───────────────────────────
    Scheme(
        id="us-wic",
        name="WIC (Special Supplemental Nutrition Program)",
        category="healthcare",
        summary="Provides federal grants to states for supplemental foods, health care referrals, and nutrition education for low-income pregnant, breastfeeding, and non-breastfeeding postpartum women, and to infants and children up to age 5.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=45000,
                label="Household annual income must not exceed $45,000 (roughly 185% of Federal Poverty Level)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of identity", "Proof of residency", "Proof of income / Medicaid enrollment card", "Health professional referral form"],
        official_url="https://www.fns.usda.gov/wic",
        benefit_amount="Supplemental food packages (milk, eggs, juice, cereal) + nutrition education",
        ministry="U.S. Department of Agriculture (USDA)",
    ),

    # ─── 57. Lifeline Support Program ────────────────────────────────────────
    Scheme(
        id="us-lifeline",
        name="Lifeline Support for Affordable Communications",
        category="housing",
        summary="Federal Communications Commission (FCC) program that provides a monthly discount on phone or internet service for low-income households.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=25000,
                label="Annual household income must be below $25,000 (under 135% of Federal Poverty Guidelines)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Proof of income or participation in assistance programs (SNAP, Medicaid, SSI)", "Valid ID"],
        official_url="https://www.lifelinesupport.org",
        benefit_amount="Monthly discount of $9.25 on phone/internet or up to $34.25 for Tribal land residents",
        ministry="Federal Communications Commission (FCC)",
    ),

    # ─── 58. LIHWAP (Water Assistance) ───────────────────────────────────────
    Scheme(
        id="us-lihwap",
        name="LIHWAP (Low Income Household Water Assistance Program)",
        category="housing",
        summary="Provides federal grants directly to states and tribes to assist low-income households, particularly those with the lowest incomes, with paying their water and wastewater bills.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=35000,
                label="Household annual income must not exceed $35,000 (typically below 150% of FPL)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Copy of recent water bill showing past-due amount or disconnection threat", "Proof of income", "Government issued ID"],
        official_url="https://www.acf.hhs.gov/ocs/programs/lihwap",
        benefit_amount="Direct payment credit to water/utility vendor to resolve arrears or restore services",
        ministry="U.S. Department of Health and Human Services",
    ),

    # ─── 59. Weatherization Assistance Program (WAP) ─────────────────────────
    Scheme(
        id="us-wap",
        name="Weatherization Assistance Program (WAP)",
        category="housing",
        summary="Reduces energy costs for low-income households, particularly for the elderly, people with disabilities, and families with children, by improving the energy efficiency of their homes.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=40000,
                label="Annual household income must not exceed $40,000 (usually set at 200% of FPL)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of income", "Home ownership title deed or landlord consent form for renters", "Recent utility bills"],
        official_url="https://www.energy.gov/scep/wap",
        benefit_amount="Free energy audit + home insulation, sealing, and energy system upgrades",
        ministry="U.S. Department of Energy",
    ),

    # ─── 60. Child Tax Credit (CTC) ──────────────────────────────────────────
    Scheme(
        id="us-child-tax-credit",
        name="Child Tax Credit (CTC)",
        category="pension",
        summary="A tax credit that helps families with qualifying children under the age of 17 get a tax break or a refund on their federal tax returns.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=150000,
                label="Total family annual income must not exceed $150,000 to receive full credit",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Federal Tax Return (Form 1040)", "Schedule 8812 (Credits for Qualifying Children and Other Dependents)", "Social Security Cards for dependents"],
        official_url="https://www.irs.gov/credits-deductions/individuals/child-tax-credit",
        benefit_amount="Up to $2,000 per qualifying child (partially refundable up to $1,700)",
        ministry="Internal Revenue Service (IRS)",
    ),

    # ─── 61. Child Care Subsidy (CCDF) ───────────────────────────────────────
    Scheme(
        id="us-child-care-subsidy",
        name="Child Care and Development Fund (CCDF) Subsidy",
        category="education",
        summary="A program designed to assist low-income families in obtaining quality child care so they can work, attend school, or participate in job training.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=13,
                label="Qualifying child must be under 13 years of age",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=45000,
                label="Household annual income must not exceed $45,000 (varies by state)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Birth Certificate of Child", "Proof of parent employment/school schedule", "Proof of income", "Residency proof"],
        official_url="https://www.acf.hhs.gov/occ",
        benefit_amount="Voucher or direct payment covering a significant portion of child care fees",
        ministry="U.S. Department of Health and Human Services",
    ),

    # ─── 62. Unemployment Insurance (UI) ─────────────────────────────────────
    Scheme(
        id="us-unemployment-insurance",
        name="Unemployment Insurance (UI)",
        category="pension",
        summary="Provides temporary, partial wage replacement benefits to workers who have lost their jobs through no fault of their own and meet other eligibility criteria.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=80000,
                label="Qualifying earned base income in the state's base period",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Employment history (names/addresses of past employers)", "Recent paystubs", "Direct deposit details"],
        official_url="https://www.dol.gov/general/topic/unemployment-insurance",
        benefit_amount="Weekly financial benefit (typically 50% of prior wage up to state cap) for up to 26 weeks",
        ministry="U.S. Department of Labor (DOL) / State Workforce Agencies",
    ),

    # ─── 63. Veterans Pension Program ────────────────────────────────────────
    Scheme(
        id="us-va-pension",
        name="VA Veterans Pension",
        category="pension",
        summary="A needs-based benefit program for veterans who served during a designated period of wartime, who meet age or disability criteria, and have low net worth/income.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=25000,
                label="Net annual family income must be below the limit set by Congress (typically $25,000 or lower)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["DD Form 214 (Discharge Papers)", "Marriage/Birth certificates for dependents", "Proof of household income and net worth assets", "Medical records of disability if under 65"],
        official_url="https://www.va.gov/pension/veterans-pension-rates",
        benefit_amount="Monthly supplementary cash pension payments based on maximum annual benefit rate",
        ministry="U.S. Department of Veterans Affairs (VA)",
    ),

    # ─── 64. Post-9/11 GI Bill ───────────────────────────────────────────────
    Scheme(
        id="us-gi-bill",
        name="Post-9/11 GI Bill (Education Support)",
        category="education",
        summary="Provides up to 36 months of education benefits for veterans and their service-member family dependents who served on active duty after September 10, 2001.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be enrolled in an approved educational institution",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["DD Form 214", "College admission acceptance letter", "VA Certificate of Eligibility (COE)", "FAFSA / enrollment details"],
        official_url="https://www.va.gov/education/about-gi-bill-benefits/post-9-11",
        benefit_amount="Full tuition & fees (public school rate) + monthly housing allowance + book stipend",
        ministry="U.S. Department of Veterans Affairs (VA)",
    ),

    # ─── 65. VA Disability Compensation ──────────────────────────────────────
    Scheme(
        id="us-va-disability",
        name="VA Disability Compensation",
        category="healthcare",
        summary="A tax-free monetary benefit paid to Veterans with mental or physical disabilities that are the result of an injury or disease incurred or aggravated during active military service.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="disability_status",
                operator="is_true",
                value=True,
                label="Must have a service-connected disability status",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["DD Form 214", "Military medical and service records", "Private medical reports", "VA claim form (Form 21-526EZ)"],
        official_url="https://www.va.gov/disability",
        benefit_amount="Monthly tax-free cash compensation (ranges from $171 to $3,737+ based on rating)",
        ministry="U.S. Department of Veterans Affairs (VA)",
    ),

    # ─── 66. Federal Supplemental Educational Opportunity Grant (FSEOG) ──────
    Scheme(
        id="us-fseog",
        name="Federal Supplemental Educational Opportunity Grant (FSEOG)",
        category="education",
        summary="Federal grants for undergraduate students with exceptional financial need, administered directly by the financial aid office at participating postsecondary schools.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be an enrolled undergraduate student",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=40000,
                label="Family annual income must not exceed $40,000 (priority given to Pell Grant recipients)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Free Application for Federal Student Aid (FAFSA)", "High School transcript", "Financial Aid award package"],
        official_url="https://studentaid.gov/understand-aid/types/grants/fseog",
        benefit_amount="Grants between $100 and $4,000 per academic year",
        ministry="U.S. Department of Education",
    ),

    # ─── 67. Job Corps ───────────────────────────────────────────────────────
    Scheme(
        id="us-job-corps",
        name="Job Corps Program",
        category="education",
        summary="A no-cost education and vocational training program that helps young people learn a career, earn a high school diploma or GED, and find and keep a good job.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="gte",
                value=16,
                label="Must be at least 16 years of age",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="lte",
                value=24,
                label="Must be under 24 years of age",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=25000,
                label="Must meet low-income eligibility requirements",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of income or participation in public assistance", "Age proof (Birth certificate/ID)", "Social Security Card", "School transcript or dropout documentation"],
        official_url="https://www.jobcorps.gov",
        benefit_amount="Free housing, meals, basic medical care, academic education & job skill credentials",
        ministry="U.S. Department of Labor (DOL)",
    ),

    # ─── 68. SCSEP (Senior Community Service Employment) ────────────────────
    Scheme(
        id="us-scsep",
        name="Senior Community Service Employment Program (SCSEP)",
        category="pension",
        summary="A community service and work-based job training program for older, unemployed low-income Americans, helping them transition into unsubsidized employment.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="gte",
                value=55,
                label="Must be 55 years of age or older",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=20000,
                label="Household annual income must not exceed 125% of the Federal Poverty Guidelines",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of age", "Proof of income", "Work history documentation", "U.S. citizenship or legal work authorization status"],
        official_url="https://www.dol.gov/agencies/eta/seniors",
        benefit_amount="Paid part-time training (minimum wage) in community service assignments",
        ministry="U.S. Department of Labor (DOL)",
    ),

    # ─── 69. Ryan White HIV/AIDS Program ─────────────────────────────────────
    Scheme(
        id="us-ryan-white",
        name="Ryan White HIV/AIDS Program",
        category="healthcare",
        summary="Provides medical care, medications, and support services to people living with HIV who are uninsured or underinsured, to improve health outcomes and reduce transmission.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=55000,
                label="Household income threshold (typically under 300% or 400% of FPL depending on state)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Documentation of HIV status", "Proof of residency", "Proof of income / insurance status", "Government photo ID"],
        official_url="https://ryanwhite.hrsa.gov",
        benefit_amount="Free/subsidized HIV primary medical care, prescription drugs (ADAP), and counseling support",
        ministry="U.S. Department of Health and Human Services (HRSA)",
    ),

    # ─── 70. TEFAP (Emergency Food Assistance) ───────────────────────────────
    Scheme(
        id="us-tefap",
        name="TEFAP (The Emergency Food Assistance Program)",
        category="healthcare",
        summary="A federal program that helps supplement the diets of low-income Americans, including elderly people, by providing them with emergency food assistance at no cost.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=35000,
                label="Household annual income must fall below state-designated low-income guidelines",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of residency in the distribution area", "Self-declaration of income eligibility / pay stubs"],
        official_url="https://www.fns.usda.gov/tefap",
        benefit_amount="Nutritious USDA Foods (canned goods, vegetables, protein) distributed via local food banks",
        ministry="U.S. Department of Agriculture (USDA)",
    ),

    # ─── 71. Commodity Supplemental Food Program (CSFP) ─────────────────────
    Scheme(
        id="us-csfp",
        name="CSFP (Commodity Supplemental Food Program for Seniors)",
        category="healthcare",
        summary="Improves the health of low-income persons at least 60 years of age by supplementing their diets with nutritious USDA foods.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="age",
                operator="gte",
                value=60,
                label="Must be 60 years of age or older",
                weight=2.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=25000,
                label="Household income must not exceed 130% of Federal Poverty Guidelines",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of age", "Proof of residency", "Proof of gross household income"],
        official_url="https://www.fns.usda.gov/csfp",
        benefit_amount="Monthly nutritional food package containing fruits, vegetables, grains, cheese, and milk",
        ministry="U.S. Department of Agriculture (USDA)",
    ),

    # ─── 72. Public Service Loan Forgiveness (PSLF) ──────────────────────────
    Scheme(
        id="us-pslf",
        name="Public Service Loan Forgiveness (PSLF)",
        category="education",
        summary="Forgives the remaining balance on Direct Loans after you have made 120 qualifying monthly payments under a qualifying repayment plan while working full-time for a qualifying employer (government or non-profit).",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must have outstanding federal student loans and be in a qualifying repayment plan",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Employment Certification Form (ECF) signed by qualifying employer", "Direct Loan details", "Payment histories"],
        official_url="https://studentaid.gov/manage-loans/forgiveness-cancellation/public-service",
        benefit_amount="Complete forgiveness of remaining federal student loan principal and accrued interest",
        ministry="U.S. Department of Education",
    ),

    # ─── 73. USDA Section 502 Direct Home Loan ───────────────────────────────
    Scheme(
        id="us-section-502",
        name="USDA Section 502 Direct Single Family Housing Loans",
        category="housing",
        summary="Assists low- and very-low-income applicants in obtaining decent, safe, and sanitary housing in eligible rural areas by providing payment assistance (interest subsidy).",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=55000,
                label="Household annual income must be below the local low-income limit (typically $55,000 depending on area)",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Proof of income & tax returns", "Detailed credit report history", "Purchase contract for property in a designated rural area", "U.S. citizenship or legal status"],
        official_url="https://www.rd.usda.gov/programs-services/single-family-housing-programs/single-family-housing-direct-home-loans",
        benefit_amount="Direct mortgage loan with no down payment requirement and interest rate subsidized down to 1%",
        ministry="U.S. Department of Agriculture (USDA) Rural Development",
    ),

    # ─── 74. Segal AmeriCorps Education Award ────────────────────────────────
    Scheme(
        id="us-americorps",
        name="Segal AmeriCorps Education Award",
        category="education",
        summary="An education award earned by members who successfully complete a term of service in an approved AmeriCorps program, used to pay educational expenses or student loans.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="student_status",
                operator="is_true",
                value=True,
                label="Must be enrolled in college or have qualifying outstanding student loans",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Americorps term of service completion certificate", "FAFSA / college billing details or student loan account records"],
        official_url="https://americorps.gov/members-volunteers/segal-americorps-education-award",
        benefit_amount="Financial award matching the maximum value of the Federal Pell Grant (approx. $7,395)",
        ministry="AmeriCorps (Corporation for National and Community Service)",
    ),

    # ─── 75. Disaster Unemployment Assistance (DUA) ──────────────────────────
    Scheme(
        id="us-unemployment-disaster",
        name="Disaster Unemployment Assistance (DUA)",
        category="pension",
        summary="Provides financial assistance to individuals whose employment or self-employment has been lost or interrupted as a direct result of a major disaster declared by the President.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=60000,
                label="Must have lost work directly in the disaster area and be ineligible for regular UI",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Proof of employment/self-employment at the time of the disaster", "Recent tax returns or pay stubs"],
        official_url="https://www.benefits.gov/benefit/597",
        benefit_amount="Weekly financial assistance benefit (equivalent to regular state UI rates) for up to 26 weeks",
        ministry="U.S. Department of Labor (DOL) / Federal Emergency Management Agency (FEMA)",
    ),

    # ─── 76. HRSA Health Center Program ──────────────────────────────────────
    Scheme(
        id="us-hrsa-health",
        name="HRSA Health Center Program Care",
        category="healthcare",
        summary="Provides affordable, high-quality primary health care services to individuals and families regardless of their ability to pay or insurance status, adjusting fees based on income.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Government-issued ID", "Self-declaration of income (for sliding scale fee discounts)"],
        official_url="https://findahealthcenter.hrsa.gov",
        benefit_amount="Comprehensive primary care, dental, mental health, and prescription discounts on a sliding scale",
        ministry="U.S. Department of Health and Human Services (HRSA)",
    ),

    # ─── 77. Residential Clean Energy Tax Credit ────────────────────────────
    Scheme(
        id="us-energy-star",
        name="Residential Clean Energy Tax Credit (Energy Star)",
        category="housing",
        summary="Allows homeowners to claim a federal tax credit for a percentage of the cost of installing residential clean energy property, such as solar panels, wind turbines, and heat pumps.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Federal Tax Return (Form 5695 - Residential Energy Credits)", "Manufacturer's certification statement", "Purchase receipts and invoices"],
        official_url="https://www.energystar.gov/about/federal-tax-credits/residential-clean-energy-tax-credits",
        benefit_amount="Tax credit covering up to 30% of qualified installation costs",
        ministry="U.S. Department of Energy / Internal Revenue Service (IRS)",
    ),

    # ─── 78. FEMA Individuals and Households Program (IHP) ───────────────────
    Scheme(
        id="us-fema-housing",
        name="FEMA Individuals and Households Program (IHP) - Housing Assistance",
        category="housing",
        summary="Provides financial help or direct services to people with housing needs caused by a natural disaster, when they are uninsured or underinsured.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
        ],
        documents_required=["Social Security Number (SSN)", "Proof of ownership or occupancy of the damaged dwelling", "Insurance declaration page", "Detailed disaster damage list"],
        official_url="https://www.fema.gov/assistance/individual/program",
        benefit_amount="Temporary rental assistance, home repair grants, or direct temporary housing units",
        ministry="Federal Emergency Management Agency (FEMA) / Department of Homeland Security",
    ),

    # ─── 79. Indian Housing Block Grant (IHBG) ───────────────────────────────
    Scheme(
        id="us-native-housing",
        name="Indian Housing Block Grant (IHBG) Program",
        category="housing",
        summary="A formula grant program that provides federal funds to Indian tribes or tribally designated housing entities (TDHEs) for affordable housing activities, including housing development and assistance.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="annual_income",
                operator="lte",
                value=60000,
                label="Household income must not exceed 80% of local median income",
                weight=1.5,
                required=True,
            ),
        ],
        documents_required=["Tribal membership card / Certificate of Degree of Indian Blood (CDIB)", "Proof of income", "Housing assessment form"],
        official_url="https://www.hud.gov/program_offices/public_indian_housing/ih/grants/ihbg",
        benefit_amount="Subsidized construction, rehabilitation, or rental housing assistance on tribal lands",
        ministry="U.S. Department of Housing and Urban Development (HUD)",
    ),

    # ─── 80. Vocational Rehabilitation Services ─────────────────────────────
    Scheme(
        id="us-disability-vocational",
        name="State Vocational Rehabilitation Services",
        category="education",
        summary="A state-federal program that helps individuals with physical or mental disabilities prepare for, find, and retain gainful employment.",
        eligibility_rules=[
            EligibilityRule(
                field="state",
                operator="in",
                value=US_STATES,
                label="Must live in the United States",
                weight=1.0,
                required=True,
            ),
            EligibilityRule(
                field="disability_status",
                operator="is_true",
                value=True,
                label="Must have a physical or mental impairment that impedes employment",
                weight=2.0,
                required=True,
            ),
        ],
        documents_required=["Detailed medical/psychological evaluations of disability", "Government-issued ID", "Employment/education history"],
        official_url="https://rsa.ed.gov/about/programs/vocational-rehabilitation-state-grants",
        benefit_amount="Free counseling, job training, assistive technology, and placement assistance services",
        ministry="U.S. Department of Education / Rehabilitation Services Administration (RSA)",
    ),
]

# Fast lookup map
SCHEMES_BY_ID: dict[str, Scheme] = {s.id: s for s in SCHEMES}