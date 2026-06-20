"""
Schemes knowledge base — 5 MVP welfare schemes with structured eligibility rules.
"""
from models import Scheme, EligibilityRule

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


    # ─── 21. PMFBY (Pradhan Mantri Fasal Bima Yojana) ──────────────────────────
    ]

# Fast lookup map
SCHEMES_BY_ID: dict[str, Scheme] = {s.id: s for s in SCHEMES}