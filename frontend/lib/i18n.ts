/**
 * Indian language translations for Benefitor AI.
 * Covers the 7 most widely spoken Indian languages + English.
 */

export type LangCode = "en" | "hi" | "bn" | "ta" | "te" | "mr" | "gu" | "pa";

export interface Translations {
  /** Language selector label */
  langLabel: string;
  /** App tagline */
  tagline: string;
  /** Header */
  browseSchemes: string;
  newChat: string;
  live: string;
  /** Welcome screen */
  welcomeCaption: string;
  welcomeHeading: string;
  welcomeSubtext: string;
  tryExample: string;
  /** Chat input */
  inputPlaceholder: string;
  inputHint: string;
  /** Results panel */
  resultsTitle: string;
  resultsEmpty: string;
  resultsEmptySubtext: string;
  statsSchemes: string;
  statsResultsIn: string;
  statsExplain: string;
  eligible: string;
  possiblyEligible: string;
  notEligible: string;
  viewDetails: string;
  docsRequired: string;
  eligibilityScore: string;
  disclaimer: string;
  /** Schemes page */
  schemesHeading: string;
  schemesSubtext: string;
  searchPlaceholder: string;
  allSchemes: string;
  categoryCounts: string;
  highestBenefit: string;
  freeCost: string;
  checkEligibility: string;
  ctaHeading: string;
  ctaSubtext: string;
  noSchemesFound: string;
  clearFilters: string;
  requiredCriteria: string;
  /** Quick examples */
  examples: string[];
}

const TRANSLATIONS: Record<LangCode, Translations> = {
  en: {
    langLabel: "English",
    tagline: "Welfare Navigator",
    browseSchemes: "Browse Schemes",
    newChat: "New Chat",
    live: "Live",
    welcomeCaption: "AI-Powered · Free · Confidential",
    welcomeHeading: "Tell me about your situation",
    welcomeSubtext:
      "I'll find government welfare schemes you may be eligible for — in your language.",
    tryExample: "Try an example",
    inputPlaceholder: "Describe your situation… (press Enter to send)",
    inputHint: "Shift+Enter for new line · Your data is not stored",
    resultsTitle: "Scheme Matches",
    resultsEmpty: "Results appear here",
    resultsEmptySubtext:
      "Start a conversation on the left to check your eligibility for welfare schemes",
    statsSchemes: "Schemes",
    statsResultsIn: "Results in",
    statsExplain: "Explainability",
    eligible: "Likely Eligible",
    possiblyEligible: "Possibly Eligible",
    notEligible: "Not Eligible",
    viewDetails: "View details",
    docsRequired: "documents required",
    eligibilityScore: "Eligibility score",
    disclaimer:
      "Recommendations are informational only. Final eligibility is decided by the relevant government authority.",
    schemesHeading: "Government Welfare Schemes",
    schemesSubtext:
      "Browse all covered schemes, check eligibility criteria, and find the documents you need.",
    searchPlaceholder: "Search schemes, ministries…",
    allSchemes: "All Schemes",
    categoryCounts: "Categories",
    highestBenefit: "Highest benefit",
    freeCost: "Free",
    checkEligibility: "Check Eligibility",
    ctaHeading: "Not sure which scheme you qualify for?",
    ctaSubtext:
      "Describe your situation in plain language and get an instant eligibility check.",
    noSchemesFound: "No schemes found",
    clearFilters: "Clear filters",
    requiredCriteria: "required criteria",
    examples: [
      "I am a second-year engineering student from West Bengal. My family income is ₹1.5 lakh per year.",
      "I am a 68-year-old widow from rural Madhya Pradesh living on ₹3,000 per month.",
      "I am a farmer in Punjab with 2 acres of land and a yearly income of ₹80,000.",
      "I belong to SC category, family income is ₹1 lakh. We live in a rented house in Bihar.",
    ],
  },

  hi: {
    langLabel: "हिन्दी",
    tagline: "कल्याण नेविगेटर",
    browseSchemes: "योजनाएं देखें",
    newChat: "नई बातचीत",
    live: "लाइव",
    welcomeCaption: "AI-संचालित · मुफ़्त · गोपनीय",
    welcomeHeading: "अपनी स्थिति बताएं",
    welcomeSubtext:
      "मैं आपके लिए सरकारी योजनाएं खोजूंगा जिनके लिए आप पात्र हो सकते हैं।",
    tryExample: "उदाहरण आज़माएं",
    inputPlaceholder: "अपनी स्थिति बताएं… (भेजने के लिए Enter दबाएं)",
    inputHint: "नई लाइन के लिए Shift+Enter · आपका डेटा सुरक्षित है",
    resultsTitle: "योजना मिलान",
    resultsEmpty: "परिणाम यहाँ दिखेंगे",
    resultsEmptySubtext:
      "बाईं तरफ बातचीत शुरू करें और अपनी पात्रता जांचें",
    statsSchemes: "योजनाएं",
    statsResultsIn: "परिणाम",
    statsExplain: "पारदर्शिता",
    eligible: "संभवतः पात्र",
    possiblyEligible: "शायद पात्र",
    notEligible: "पात्र नहीं",
    viewDetails: "विवरण देखें",
    docsRequired: "दस्तावेज़ आवश्यक",
    eligibilityScore: "पात्रता स्कोर",
    disclaimer:
      "ये सुझाव केवल जानकारी के लिए हैं। अंतिम पात्रता संबंधित सरकारी विभाग तय करेगा।",
    schemesHeading: "सरकारी कल्याण योजनाएं",
    schemesSubtext:
      "सभी योजनाएं देखें, पात्रता जांचें और जरूरी दस्तावेज़ जानें।",
    searchPlaceholder: "योजना या मंत्रालय खोजें…",
    allSchemes: "सभी योजनाएं",
    categoryCounts: "श्रेणियां",
    highestBenefit: "अधिकतम लाभ",
    freeCost: "मुफ़्त",
    checkEligibility: "पात्रता जांचें",
    ctaHeading: "नहीं पता कौन सी योजना मिलेगी?",
    ctaSubtext: "अपनी स्थिति बताएं और तुरंत जानें।",
    noSchemesFound: "कोई योजना नहीं मिली",
    clearFilters: "फ़िल्टर हटाएं",
    requiredCriteria: "जरूरी शर्तें",
    examples: [
      "मैं पश्चिम बंगाल से दूसरे साल का इंजीनियरिंग छात्र हूं। मेरे परिवार की आय ₹1.5 लाख प्रति वर्ष है।",
      "मैं मध्य प्रदेश के गांव से 68 वर्षीय विधवा हूं। ₹3,000 प्रति माह पर जीवन यापन करती हूं।",
      "मैं पंजाब में किसान हूं। 2 एकड़ जमीन है और सालाना आय ₹80,000 है।",
      "मैं SC वर्ग से हूं। परिवार की आय ₹1 लाख है। हम बिहार में किराए के घर में रहते हैं।",
    ],
  },

  bn: {
    langLabel: "বাংলা",
    tagline: "কল্যাণ নেভিগেটর",
    browseSchemes: "প্রকল্প দেখুন",
    newChat: "নতুন কথোপকথন",
    live: "লাইভ",
    welcomeCaption: "AI-চালিত · বিনামূল্যে · গোপনীয়",
    welcomeHeading: "আপনার পরিস্থিতি বলুন",
    welcomeSubtext: "আমি আপনার জন্য সরকারি কল্যাণ প্রকল্প খুঁজে দেব।",
    tryExample: "উদাহরণ দেখুন",
    inputPlaceholder: "আপনার অবস্থা বলুন… (পাঠাতে Enter চাপুন)",
    inputHint: "নতুন লাইনের জন্য Shift+Enter · আপনার তথ্য সুরক্ষিত",
    resultsTitle: "প্রকল্পের মিল",
    resultsEmpty: "ফলাফল এখানে দেখাবে",
    resultsEmptySubtext: "বাম দিকে কথোপকথন শুরু করুন",
    statsSchemes: "প্রকল্প",
    statsResultsIn: "ফলাফল",
    statsExplain: "স্বচ্ছতা",
    eligible: "সম্ভবত যোগ্য",
    possiblyEligible: "হয়তো যোগ্য",
    notEligible: "যোগ্য নন",
    viewDetails: "বিস্তারিত দেখুন",
    docsRequired: "প্রয়োজনীয় কাগজ",
    eligibilityScore: "যোগ্যতার স্কোর",
    disclaimer: "এই সুপারিশগুলি শুধু তথ্যের জন্য। চূড়ান্ত যোগ্যতা সরকার নির্ধারণ করবে।",
    schemesHeading: "সরকারি কল্যাণ প্রকল্প",
    schemesSubtext: "সমস্ত প্রকল্প দেখুন, যোগ্যতা পরীক্ষা করুন।",
    searchPlaceholder: "প্রকল্প বা মন্ত্রণালয় খুঁজুন…",
    allSchemes: "সকল প্রকল্প",
    categoryCounts: "বিভাগ",
    highestBenefit: "সর্বোচ্চ সুবিধা",
    freeCost: "বিনামূল্যে",
    checkEligibility: "যোগ্যতা পরীক্ষা করুন",
    ctaHeading: "কোন প্রকল্পের জন্য যোগ্য জানেন না?",
    ctaSubtext: "আপনার অবস্থা বলুন এবং তাৎক্ষণিক ফলাফল পান।",
    noSchemesFound: "কোনো প্রকল্প পাওয়া যায়নি",
    clearFilters: "ফিল্টার সরান",
    requiredCriteria: "প্রয়োজনীয় মানদণ্ড",
    examples: [
      "আমি পশ্চিমবঙ্গ থেকে দ্বিতীয় বর্ষের ইঞ্জিনিয়ারিং ছাত্র। পরিবারের আয় বছরে ₹১.৫ লাখ।",
      "আমি মধ্যপ্রদেশের গ্রাম থেকে ৬৮ বছর বয়সী বিধবা। মাসে ₹৩,০০০-এ জীবন কাটাই।",
      "আমি পাঞ্জাবের কৃষক। ২ একর জমি আছে, বার্ষিক আয় ₹৮০,০০০।",
      "আমি SC সম্প্রদায়ের। পরিবারের আয় ₹১ লাখ। বিহারে ভাড়া বাড়িতে থাকি।",
    ],
  },

  ta: {
    langLabel: "தமிழ்",
    tagline: "நலன் வழிகாட்டி",
    browseSchemes: "திட்டங்கள் பார்க்க",
    newChat: "புதிய உரையாடல்",
    live: "நேரடி",
    welcomeCaption: "AI-இயக்கம் · இலவசம் · இரகசியம்",
    welcomeHeading: "உங்கள் நிலை சொல்லுங்கள்",
    welcomeSubtext: "நீங்கள் தகுதியான அரசாங்க திட்டங்களை கண்டுபிடிப்பேன்.",
    tryExample: "உதாரணம் பாருங்கள்",
    inputPlaceholder: "உங்கள் நிலை சொல்லுங்கள்… (Enter அழுத்துங்கள்)",
    inputHint: "புதிய வரிக்கு Shift+Enter · தரவு பாதுகாப்பானது",
    resultsTitle: "திட்ட பொருத்தங்கள்",
    resultsEmpty: "முடிவுகள் இங்கே தோன்றும்",
    resultsEmptySubtext: "இடதுபுறம் உரையாடல் தொடங்குங்கள்",
    statsSchemes: "திட்டங்கள்",
    statsResultsIn: "முடிவுகள்",
    statsExplain: "வெளிப்படைத்தன்மை",
    eligible: "தகுதியானவர்",
    possiblyEligible: "சாத்தியம்",
    notEligible: "தகுதியில்லை",
    viewDetails: "விவரங்கள் பாருங்கள்",
    docsRequired: "ஆவணங்கள் தேவை",
    eligibilityScore: "தகுதி மதிப்பெண்",
    disclaimer: "இவை தகவல் மட்டுமே. இறுதி தகுதி அரசு நிர்ணயிக்கும்.",
    schemesHeading: "அரசாங்க நலத் திட்டங்கள்",
    schemesSubtext: "அனைத்து திட்டங்களையும் பாருங்கள், தகுதி சரிபாருங்கள்.",
    searchPlaceholder: "திட்டம் அல்லது அமைச்சகம் தேடுங்கள்…",
    allSchemes: "அனைத்து திட்டங்கள்",
    categoryCounts: "வகைகள்",
    highestBenefit: "அதிக நலன்",
    freeCost: "இலவசம்",
    checkEligibility: "தகுதி சரிபாருங்கள்",
    ctaHeading: "எந்த திட்டம் கிடைக்கும் என்று தெரியாதா?",
    ctaSubtext: "உங்கள் நிலை சொல்லுங்கள், உடனே தெரிந்துகொள்ளுங்கள்.",
    noSchemesFound: "திட்டங்கள் கிடைக்கவில்லை",
    clearFilters: "வடிகட்டிகளை அகற்றுங்கள்",
    requiredCriteria: "தேவையான நிபந்தனைகள்",
    examples: [
      "நான் மேற்கு வங்காளத்திலிருந்து இரண்டாம் ஆண்டு பொறியியல் மாணவன். குடும்ப வருமானம் ₹1.5 லட்சம்.",
      "நான் மத்தியப் பிரதேசத்திலிருந்து 68 வயது விதவை. மாதம் ₹3,000 வருமானம்.",
      "நான் பஞ்சாபில் விவசாயி. 2 ஏக்கர் நிலம். ஆண்டு வருமானம் ₹80,000.",
      "நான் SC சமூகத்தைச் சேர்ந்தவன். குடும்ப வருமானம் ₹1 லட்சம். பீகாரில் வாடகை வீட்டில் இருக்கிறோம்.",
    ],
  },

  te: {
    langLabel: "తెలుగు",
    tagline: "సంక్షేమ నావిగేటర్",
    browseSchemes: "పథకాలు చూడండి",
    newChat: "కొత్త సంభాషణ",
    live: "లైవ్",
    welcomeCaption: "AI-ఆధారిత · ఉచితం · రహస్యం",
    welcomeHeading: "మీ పరిస్థితి చెప్పండి",
    welcomeSubtext: "మీకు అర్హమైన ప్రభుత్వ సంక్షేమ పథకాలను కనుగొంటాను.",
    tryExample: "ఉదాహరణ చూడండి",
    inputPlaceholder: "మీ పరిస్థితి చెప్పండి… (పంపడానికి Enter నొక్కండి)",
    inputHint: "కొత్త వరుసకు Shift+Enter · మీ డేటా సురక్షితం",
    resultsTitle: "పథకాల సరిపోలిక",
    resultsEmpty: "ఫలితాలు ఇక్కడ కనిపిస్తాయి",
    resultsEmptySubtext: "ఎడమ వైపు సంభాషణ ప్రారంభించండి",
    statsSchemes: "పథకాలు",
    statsResultsIn: "ఫలితాలు",
    statsExplain: "పారదర్శకత",
    eligible: "అర్హత ఉంది",
    possiblyEligible: "బహుశా అర్హత",
    notEligible: "అర్హత లేదు",
    viewDetails: "వివరాలు చూడండి",
    docsRequired: "పత్రాలు అవసరం",
    eligibilityScore: "అర్హత స్కోరు",
    disclaimer: "ఇవి సమాచారం మాత్రమే. తుది అర్హత ప్రభుత్వం నిర్ణయిస్తుంది.",
    schemesHeading: "ప్రభుత్వ సంక్షేమ పథకాలు",
    schemesSubtext: "అన్ని పథకాలు చూడండి, అర్హత తనిఖీ చేయండి.",
    searchPlaceholder: "పథకం లేదా మంత్రిత్వ శాఖ వెతకండి…",
    allSchemes: "అన్ని పథకాలు",
    categoryCounts: "వర్గాలు",
    highestBenefit: "గరిష్ఠ లబ్ధి",
    freeCost: "ఉచితం",
    checkEligibility: "అర్హత తనిఖీ చేయండి",
    ctaHeading: "ఏ పథకానికి అర్హత ఉందో తెలియదా?",
    ctaSubtext: "మీ పరిస్థితి చెప్పి తక్షణ ఫలితాలు పొందండి.",
    noSchemesFound: "పథకాలు కనుగొనబడలేదు",
    clearFilters: "ఫిల్టర్లు తొలగించు",
    requiredCriteria: "అవసరమైన ప్రమాణాలు",
    examples: [
      "నేను పశ్చిమ బెంగాల్ నుండి రెండవ సంవత్సరం ఇంజినీరింగ్ విద్యార్థిని. కుటుంబ ఆదాయం ₹1.5 లక్ష.",
      "నేను మధ్యప్రదేశ్ గ్రామం నుండి 68 ఏళ్ల వితంతువు. నెలకు ₹3,000 ఆదాయం.",
      "నేను పంజాబ్‌లో రైతుని. 2 ఎకరాల భూమి ఉంది. వార్షిక ఆదాయం ₹80,000.",
      "నేను SC వర్గానికి చెందినవాడిని. కుటుంబ ఆదాయం ₹1 లక్ష. బీహార్‌లో అద్దె ఇంట్లో ఉంటాం.",
    ],
  },

  mr: {
    langLabel: "मराठी",
    tagline: "कल्याण नेव्हिगेटर",
    browseSchemes: "योजना पहा",
    newChat: "नवीन संभाषण",
    live: "थेट",
    welcomeCaption: "AI-चालित · मोफत · गोपनीय",
    welcomeHeading: "तुमची परिस्थिती सांगा",
    welcomeSubtext: "तुम्हाला पात्र असलेल्या सरकारी कल्याण योजना शोधेन.",
    tryExample: "उदाहरण पहा",
    inputPlaceholder: "तुमची परिस्थिती सांगा… (पाठवण्यासाठी Enter दाबा)",
    inputHint: "नवीन ओळीसाठी Shift+Enter · तुमचा डेटा सुरक्षित",
    resultsTitle: "योजना जुळणी",
    resultsEmpty: "निकाल येथे दिसतील",
    resultsEmptySubtext: "डाव्या बाजूने संभाषण सुरू करा",
    statsSchemes: "योजना",
    statsResultsIn: "निकाल",
    statsExplain: "पारदर्शकता",
    eligible: "पात्र असण्याची शक्यता",
    possiblyEligible: "कदाचित पात्र",
    notEligible: "पात्र नाही",
    viewDetails: "तपशील पहा",
    docsRequired: "कागदपत्रे आवश्यक",
    eligibilityScore: "पात्रता गुण",
    disclaimer: "हे फक्त माहितीसाठी आहे. अंतिम पात्रता सरकार ठरवेल.",
    schemesHeading: "सरकारी कल्याण योजना",
    schemesSubtext: "सर्व योजना पहा, पात्रता तपासा.",
    searchPlaceholder: "योजना किंवा मंत्रालय शोधा…",
    allSchemes: "सर्व योजना",
    categoryCounts: "श्रेण्या",
    highestBenefit: "जास्तीत जास्त लाभ",
    freeCost: "मोफत",
    checkEligibility: "पात्रता तपासा",
    ctaHeading: "कोणत्या योजनेसाठी पात्र आहात हे माहीत नाही?",
    ctaSubtext: "तुमची परिस्थिती सांगा आणि तात्काळ निकाल मिळवा.",
    noSchemesFound: "योजना सापडल्या नाहीत",
    clearFilters: "फिल्टर काढा",
    requiredCriteria: "आवश्यक निकष",
    examples: [
      "मी पश्चिम बंगालमधून दुसऱ्या वर्षाचा अभियांत्रिकी विद्यार्थी आहे. कुटुंबाचे उत्पन्न ₹1.5 लाख प्रतिवर्ष.",
      "मी मध्य प्रदेशातील खेड्यातून 68 वर्षांची विधवा आहे. ₹3,000 प्रति महिना उत्पन्न.",
      "मी पंजाबमधील शेतकरी आहे. 2 एकर जमीन आहे. वार्षिक उत्पन्न ₹80,000.",
      "मी SC प्रवर्गातील आहे. कुटुंबाचे उत्पन्न ₹1 लाख. बिहारमध्ये भाड्याच्या घरात राहतो.",
    ],
  },

  gu: {
    langLabel: "ગુજરાતી",
    tagline: "કલ્યાણ નેવિગેટર",
    browseSchemes: "યોજનાઓ જુઓ",
    newChat: "નવી વાર્તાલાપ",
    live: "લાઇવ",
    welcomeCaption: "AI-સંચાલિત · મફત · ગોપનીય",
    welcomeHeading: "તમારી સ્થિતિ જણાવો",
    welcomeSubtext: "હું તમારા માટે સરકારી કલ્યાણ યોજનાઓ શોધીશ.",
    tryExample: "ઉદાહરણ જુઓ",
    inputPlaceholder: "તમારી સ્થિતિ જણાવો… (Enter દબાવો)",
    inputHint: "નવી લાઇન માટે Shift+Enter · ડેટા સુરક્ષિત",
    resultsTitle: "યોજના મેળ",
    resultsEmpty: "પરિણામ અહીં દેખાશે",
    resultsEmptySubtext: "ડાબી બાજુ વાર્તાલાપ શરૂ કરો",
    statsSchemes: "યોજનાઓ",
    statsResultsIn: "પરિણામ",
    statsExplain: "પારદર્શિતા",
    eligible: "પાત્ર",
    possiblyEligible: "કદાચ પાત્ર",
    notEligible: "પાત્ર નથી",
    viewDetails: "વિગત જુઓ",
    docsRequired: "દસ્તાવેજ જરૂરી",
    eligibilityScore: "પાત્રતા સ્કોર",
    disclaimer: "આ માત્ર માહિતી છે. અંતિમ પાત્રતા સરકાર નક્કી કરશે.",
    schemesHeading: "સરકારી કલ્યાણ યોજનાઓ",
    schemesSubtext: "બધી યોજનાઓ જુઓ, પાત્રતા ચકાસો.",
    searchPlaceholder: "યોજના અથવા મંત્રાલય શોધો…",
    allSchemes: "બધી યોજનાઓ",
    categoryCounts: "શ્રેણીઓ",
    highestBenefit: "સૌથી વધુ લાભ",
    freeCost: "મફત",
    checkEligibility: "પાત્રતા ચકાસો",
    ctaHeading: "કઈ યોજના મળશે ખ્યાલ નથી?",
    ctaSubtext: "તમારી સ્થિતિ જણાવો અને તરત જ જાણો.",
    noSchemesFound: "કોઈ યોજના મળી નહીં",
    clearFilters: "ફિલ્ટર હટાવો",
    requiredCriteria: "જરૂરી માપદંડ",
    examples: [
      "હું પશ્ચિમ બંગાળથી બીજા વર્ષનો એન્જિનિયરિંગ વિદ્યાર્થી છું. ₹1.5 લાખ વાર્ષિક.",
      "હું મધ્યપ્રદેશના ગામડાથી 68 વર્ષની વિધવા છું. ₹3,000 માસિક.",
      "હું પંજાબમાં ખેડૂત છું. 2 એકર જમીન. ₹80,000 વાર્ષિક આવક.",
      "હું SC વર્ગનો છું. ₹1 લાખ પારિવારિક આવક. બિહારમાં ભાડાના ઘરમાં.",
    ],
  },

  pa: {
    langLabel: "ਪੰਜਾਬੀ",
    tagline: "ਭਲਾਈ ਨੈਵੀਗੇਟਰ",
    browseSchemes: "ਯੋਜਨਾਵਾਂ ਵੇਖੋ",
    newChat: "ਨਵੀਂ ਗੱਲਬਾਤ",
    live: "ਲਾਈਵ",
    welcomeCaption: "AI-ਸੰਚਾਲਿਤ · ਮੁਫ਼ਤ · ਗੁਪਤ",
    welcomeHeading: "ਆਪਣੀ ਸਥਿਤੀ ਦੱਸੋ",
    welcomeSubtext: "ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਸਰਕਾਰੀ ਭਲਾਈ ਯੋਜਨਾਵਾਂ ਲੱਭਾਂਗਾ।",
    tryExample: "ਉਦਾਹਰਣ ਵੇਖੋ",
    inputPlaceholder: "ਆਪਣੀ ਸਥਿਤੀ ਦੱਸੋ… (ਭੇਜਣ ਲਈ Enter ਦਬਾਓ)",
    inputHint: "ਨਵੀਂ ਲਾਈਨ ਲਈ Shift+Enter · ਡੇਟਾ ਸੁਰੱਖਿਅਤ",
    resultsTitle: "ਯੋਜਨਾ ਮੇਲ",
    resultsEmpty: "ਨਤੀਜੇ ਇੱਥੇ ਦਿਖਣਗੇ",
    resultsEmptySubtext: "ਖੱਬੇ ਪਾਸੇ ਗੱਲਬਾਤ ਸ਼ੁਰੂ ਕਰੋ",
    statsSchemes: "ਯੋਜਨਾਵਾਂ",
    statsResultsIn: "ਨਤੀਜੇ",
    statsExplain: "ਪਾਰਦਰਸ਼ਤਾ",
    eligible: "ਯੋਗ",
    possiblyEligible: "ਸ਼ਾਇਦ ਯੋਗ",
    notEligible: "ਯੋਗ ਨਹੀਂ",
    viewDetails: "ਵੇਰਵਾ ਵੇਖੋ",
    docsRequired: "ਦਸਤਾਵੇਜ਼ ਲੋੜੀਂਦੇ",
    eligibilityScore: "ਯੋਗਤਾ ਸਕੋਰ",
    disclaimer: "ਇਹ ਸਿਰਫ਼ ਜਾਣਕਾਰੀ ਲਈ ਹੈ। ਅੰਤਿਮ ਯੋਗਤਾ ਸਰਕਾਰ ਤੈਅ ਕਰੇਗੀ।",
    schemesHeading: "ਸਰਕਾਰੀ ਭਲਾਈ ਯੋਜਨਾਵਾਂ",
    schemesSubtext: "ਸਾਰੀਆਂ ਯੋਜਨਾਵਾਂ ਵੇਖੋ, ਯੋਗਤਾ ਜਾਂਚੋ।",
    searchPlaceholder: "ਯੋਜਨਾ ਜਾਂ ਮੰਤਰਾਲਾ ਖੋਜੋ…",
    allSchemes: "ਸਾਰੀਆਂ ਯੋਜਨਾਵਾਂ",
    categoryCounts: "ਸ਼੍ਰੇਣੀਆਂ",
    highestBenefit: "ਵੱਧ ਤੋਂ ਵੱਧ ਲਾਭ",
    freeCost: "ਮੁਫ਼ਤ",
    checkEligibility: "ਯੋਗਤਾ ਜਾਂਚੋ",
    ctaHeading: "ਕਿਹੜੀ ਯੋਜਨਾ ਮਿਲੇਗੀ ਪਤਾ ਨਹੀਂ?",
    ctaSubtext: "ਆਪਣੀ ਸਥਿਤੀ ਦੱਸੋ ਅਤੇ ਤੁਰੰਤ ਜਾਣੋ।",
    noSchemesFound: "ਕੋਈ ਯੋਜਨਾ ਨਹੀਂ ਮਿਲੀ",
    clearFilters: "ਫਿਲਟਰ ਹਟਾਓ",
    requiredCriteria: "ਲੋੜੀਂਦੇ ਮਾਪਦੰਡ",
    examples: [
      "ਮੈਂ ਪੱਛਮੀ ਬੰਗਾਲ ਤੋਂ ਦੂਜੇ ਸਾਲ ਦਾ ਇੰਜੀਨੀਅਰਿੰਗ ਵਿਦਿਆਰਥੀ ਹਾਂ। ₹1.5 ਲੱਖ ਸਾਲਾਨਾ।",
      "ਮੈਂ ਮੱਧ ਪ੍ਰਦੇਸ਼ ਦੇ ਪਿੰਡ ਤੋਂ 68 ਸਾਲਾਂ ਦੀ ਵਿਧਵਾ ਹਾਂ। ₹3,000 ਪ੍ਰਤੀ ਮਹੀਨਾ।",
      "ਮੈਂ ਪੰਜਾਬ ਵਿੱਚ ਕਿਸਾਨ ਹਾਂ। 2 ਏਕੜ ਜ਼ਮੀਨ। ₹80,000 ਸਾਲਾਨਾ।",
      "ਮੈਂ SC ਵਰਗ ਤੋਂ ਹਾਂ। ₹1 ਲੱਖ ਪਰਿਵਾਰਕ ਆਮਦਨ। ਬਿਹਾਰ ਵਿੱਚ ਕਿਰਾਏ ਦੇ ਘਰ ਵਿੱਚ ਰਹਿੰਦੇ ਹਾਂ।",
    ],
  },
};

export const LANGUAGES: { code: LangCode; nativeName: string; flag: string }[] = [
  { code: "en", nativeName: "English", flag: "🇬🇧" },
  { code: "hi", nativeName: "हिन्दी", flag: "🇮🇳" },
  { code: "bn", nativeName: "বাংলা", flag: "🇮🇳" },
  { code: "ta", nativeName: "தமிழ்", flag: "🇮🇳" },
  { code: "te", nativeName: "తెలుగు", flag: "🇮🇳" },
  { code: "mr", nativeName: "मराठी", flag: "🇮🇳" },
  { code: "gu", nativeName: "ગુજરાતી", flag: "🇮🇳" },
  { code: "pa", nativeName: "ਪੰਜਾਬੀ", flag: "🇮🇳" },
];

export interface ExtraTranslations {
  back: string;
  visitOfficialPortal: string;
  overview: string;
  aiAnalysis: string;
  criteriaYouMeet: string;
  infoNeeded: string;
  required: string;
  bonus: string;
  documentsRequired: string;
  apply: string;
  hideProfile: string;
  showExtractedProfile: string;
  extractedProfile: string;
  fields: string;
  noSchemesMatchFilter: string;
  govtOfIndia: string;
  costToApply: string;
  catFarmer: string;
  catHousing: string;
  catHealthcare: string;
  catPension: string;
  catEducation: string;
  age: string;
  state: string;
  district: string;
  occupation: string;
  annual_income: string;
  category: string;
  student_status: string;
  farmer_status: string;
  housing_status: string;
  land_ownership: string;
  disability_status: string;
  senior_citizen_status: string;
  gender: string;
  bpl_card: string;
  yes: string;
  no: string;
}

const EXTRA_TRANSLATIONS: Record<LangCode, ExtraTranslations> = {
  en: {
    back: "Back",
    visitOfficialPortal: "Visit Official Portal",
    overview: "Overview",
    aiAnalysis: "AI Analysis",
    criteriaYouMeet: "Criteria you meet",
    infoNeeded: "Information needed",
    required: "Required",
    bonus: "Bonus",
    documentsRequired: "Documents Required",
    apply: "Apply",
    hideProfile: "Hide profile",
    showExtractedProfile: "Show extracted profile",
    extractedProfile: "Extracted Profile",
    fields: "fields",
    noSchemesMatchFilter: "No schemes match this filter",
    govtOfIndia: "Government of India · Welfare Schemes",
    costToApply: "Cost to apply",
    catFarmer: "Farmer Support",
    catHousing: "Housing",
    catHealthcare: "Healthcare",
    catPension: "Pension",
    catEducation: "Education",
    age: "Age",
    state: "State",
    district: "District",
    occupation: "Occupation",
    annual_income: "Annual Income",
    category: "Category",
    student_status: "Student",
    farmer_status: "Farmer",
    housing_status: "Housing",
    land_ownership: "Owns Land",
    disability_status: "Disability",
    senior_citizen_status: "Senior Citizen",
    gender: "Gender",
    bpl_card: "BPL Card",
    yes: "Yes",
    no: "No"
  },
  hi: {
    back: "वापस",
    visitOfficialPortal: "आधिकारिक पोर्टल पर जाएं",
    overview: "विवरण",
    aiAnalysis: "AI विश्लेषण",
    criteriaYouMeet: "शर्ते जो आप पूरी करते हैं",
    infoNeeded: "आवश्यक जानकारी",
    required: "अनिवार्य",
    bonus: "अतिरिक्त",
    documentsRequired: "आवश्यक दस्तावेज",
    apply: "आवेदन करें",
    hideProfile: "प्रोफ़ाइल छिपाएं",
    showExtractedProfile: "प्रोफ़ाइल दिखाएं",
    extractedProfile: "आपकी प्रोफ़ाइल",
    fields: "विवरण",
    noSchemesMatchFilter: "इस फ़िल्टर से मेल खाती कोई योजना नहीं है",
    govtOfIndia: "भारत सरकार · कल्याणकारी योजनाएं",
    costToApply: "आवेदन शुल्क",
    catFarmer: "किसान सहायता",
    catHousing: "आवास",
    catHealthcare: "स्वास्थ्य सेवा",
    catPension: "पेंशन",
    catEducation: "शिक्षा",
    age: "आयु",
    state: "राज्य",
    district: "जिला",
    occupation: "व्यवसाय",
    annual_income: "वार्षिक आय",
    category: "वर्ग",
    student_status: "छात्र",
    farmer_status: "किसान",
    housing_status: "आवास की स्थिति",
    land_ownership: "भूमि स्वामित्व",
    disability_status: "विकलांगता",
    senior_citizen_status: "वरिष्ठ नागरिक",
    gender: "लिंग",
    bpl_card: "बीपीएल कार्ड",
    yes: "हाँ",
    no: "नहीं"
  },
  bn: {
    back: "ফিরে যান",
    visitOfficialPortal: "অফিসিয়াল পোর্টালে যান",
    overview: "সংক্ষিপ্ত বিবরণ",
    aiAnalysis: "AI বিশ্লেষণ",
    criteriaYouMeet: "যোগ্যতা যা আপনি পূরণ করেন",
    infoNeeded: "প্রয়োজনীয় তথ্য",
    required: "প্রয়োজনীয়",
    bonus: "অতিরিক্ত",
    documentsRequired: "প্রয়োজনীয় নথিপত্র",
    apply: "আবেদন করুন",
    hideProfile: "প্রোফাইল লুকান",
    showExtractedProfile: "প্রোফাইল দেখান",
    extractedProfile: "আপনার প্রোফাইল",
    fields: "তথ্য",
    noSchemesMatchFilter: "এই ফিল্টারের সাথে কোনো প্রকল্প মেলেনি",
    govtOfIndia: "ভারত সরকার · কল্যাণমূলক প্রকল্প",
    costToApply: "আবেদন ফি",
    catFarmer: "কৃষক সহায়তা",
    catHousing: "আবাসন",
    catHealthcare: "স্বাস্থ্য পরিষেবা",
    catPension: "পেনশন",
    catEducation: "শিক্ষা",
    age: "বয়স",
    state: "রাজ্য",
    district: "জেলা",
    occupation: "পেশা",
    annual_income: "বার্ষিক আয়",
    category: "বিভাগ",
    student_status: "ছাত্র",
    farmer_status: "কৃষক",
    housing_status: "আবাসন অবস্থা",
    land_ownership: "জমির মালিকানা",
    disability_status: "প্রতিবন্ধী",
    senior_citizen_status: "প্রবীণ নাগরিক",
    gender: "লিঙ্গ",
    bpl_card: "বিপিএল কার্ড",
    yes: "হ্যাঁ",
    no: "না"
  },
  ta: {
    back: "திரும்பிச் செல்",
    visitOfficialPortal: "அதிகாரப்பூர்வ வலைத்தளத்திற்குச் செல்லவும்",
    overview: "கண்ணோட்டம்",
    aiAnalysis: "AI பகுப்பாய்வு",
    criteriaYouMeet: "நீங்கள் பூர்த்தி செய்யும் நிபந்தனைகள்",
    infoNeeded: "தேவைப்படும் தகவல்",
    required: "தேவையானது",
    bonus: "கூடுதல்",
    documentsRequired: "தேவையான ஆவணங்கள்",
    apply: "விண்ணப்பிக்கவும்",
    hideProfile: "விவரங்களை மறைக்கவும்",
    showExtractedProfile: "விவரங்களைக் காட்டுக",
    extractedProfile: "உங்கள் சுயவிவரம்",
    fields: "விவரங்கள்",
    noSchemesMatchFilter: "இந்த வடிகட்டிக்கு ஏற்ற திட்டங்கள் இல்லை",
    govtOfIndia: "இந்திய அரசு · நலத்திட்டங்கள்",
    costToApply: "விண்ணப்பக் கட்டணம்",
    catFarmer: "விவசாயி ஆதரவு",
    catHousing: "வீட்டுவசதி",
    catHealthcare: "சுகாதாரம்",
    catPension: "ஓய்வூதியம்",
    catEducation: "கல்வி",
    age: "வயது",
    state: "மாநிலம்",
    district: "மாவட்டம்",
    occupation: "தொழில்",
    annual_income: "ஆண்டு வருமானம்",
    category: "பிரிவு",
    student_status: "மாணவர்",
    farmer_status: "விவசாயி",
    housing_status: "வீட்டு வசதி",
    land_ownership: "நில உரிமை",
    disability_status: "மாற்றுத்திறனாளி",
    senior_citizen_status: "முதியவர்",
    gender: "பாலினம்",
    bpl_card: "வறுமைக்கோட்டு அட்டை",
    yes: "ஆம்",
    no: "இல்லை"
  },
  te: {
    back: "వెనుకకు",
    visitOfficialPortal: "అధికారిక పోర్టల్ సందర్శించండి",
    overview: "అవలోకనం",
    aiAnalysis: "AI విశ్లేషణ",
    criteriaYouMeet: "మీరు పూర్తి చేసిన అర్హతలు",
    infoNeeded: "కావలసిన సమాచారం",
    required: "తప్పనిసరి",
    bonus: "అదనం",
    documentsRequired: "కావలసిన పత్రాలు",
    apply: "దరఖాస్తు చేసుకోండి",
    hideProfile: "ప్రొఫైల్ దాచండి",
    showExtractedProfile: "ప్రొఫైల్ చూపించు",
    extractedProfile: "మీ ప్రొఫైల్",
    fields: "వివరాలు",
    noSchemesMatchFilter: "ఈ ఫిల్టర్‌కు సరిపోయే పథకాలు లేవు",
    govtOfIndia: "భారత ప్రభుత్వం · సంక్షేమ పథకాలు",
    costToApply: "దరఖాస్తు రుసుము",
    catFarmer: "రైతు సహాయం",
    catHousing: "గృహనిర్మాణం",
    catHealthcare: "ఆరోగ్యం",
    catPension: "పెన్షన్",
    catEducation: "విద్య",
    age: "వయస్సు",
    state: "రాష్ట్రం",
    district: "జిల్లా",
    occupation: "ఉపాధి",
    annual_income: "వార్షిక ఆదాయం",
    category: "వర్గం",
    student_status: "విద్యార్థి",
    farmer_status: "రైతు",
    housing_status: "గృహ స్థితి",
    land_ownership: "భూమి యాజమాన్యం",
    disability_status: "వికలాంగత్వం",
    senior_citizen_status: "వృద్ధులు",
    gender: "లింగం",
    bpl_card: "బిపిఎల్ కార్డ్",
    yes: "అవును",
    no: "కాదు"
  },
  mr: {
    back: "मागे",
    visitOfficialPortal: "अधिकृत पोर्टलला भेट द्या",
    overview: "आढावा",
    aiAnalysis: "AI विश्लेषण",
    criteriaYouMeet: "अटी ज्या तुम्ही पूर्ण करता",
    infoNeeded: "आवश्यक माहिती",
    required: "आवश्यक",
    bonus: "अतिरिक्त",
    documentsRequired: "आवश्यक कागदपत्रे",
    apply: "अर्ज करा",
    hideProfile: "प्रोफाइल लपवा",
    showExtractedProfile: "प्रोफाइल दाखवा",
    extractedProfile: "आपली प्रोफाइल",
    fields: "माहिती",
    noSchemesMatchFilter: "या फिल्टरशी जुळणारी कोणतीही योजना नाही",
    govtOfIndia: "भारत सरकार · कल्याणकारी योजना",
    costToApply: "अर्ज शुल्क",
    catFarmer: "शेतकरी मदत",
    catHousing: "गृहनिर्माण",
    catHealthcare: "आरोग्य सेवा",
    catPension: "पेन्शन",
    catEducation: "शिक्षण",
    age: "वय",
    state: "राज्य",
    district: "जिल्हा",
    occupation: "व्यवसाय",
    annual_income: "वार्षिक उत्पन्न",
    category: "प्रवर्ग",
    student_status: "विद्यार्थी",
    farmer_status: "शेतकरी",
    housing_status: "घराची स्थिती",
    land_ownership: "जमीन मालकी",
    disability_status: "अपंगत्व",
    senior_citizen_status: "वरिष्ठ नागरिक",
    gender: "लिंग",
    bpl_card: "बीपीएल कार्ड",
    yes: "होय",
    no: "नाही"
  },
  gu: {
    back: "પાછા",
    visitOfficialPortal: "સત્તાવાર પોર્ટલની મુલાકાત લો",
    overview: "ઝાંખી",
    aiAnalysis: "AI વિશ્લેષણ",
    criteriaYouMeet: "શરતો જે તમે પૂર્ણ કરો છો",
    infoNeeded: "જરૂરી માહિતી",
    required: "જરૂરી",
    bonus: "વધારાનું",
    documentsRequired: "જરૂરી દસ્તાવેજો",
    apply: "અરજી કરો",
    hideProfile: "પ્રોફાઇલ છુપાવો",
    showExtractedProfile: "પ્રોફાઇલ બતાવો",
    extractedProfile: "તમારી પ્રોફાઇલ",
    fields: "માહિતી",
    noSchemesMatchFilter: "આ ફિલ્ટર સાથે કોઈ યોજના મેળ ખાતી નથી",
    govtOfIndia: "ભારત સરકાર · કલ્યાણકારી યોજનાઓ",
    costToApply: "અરજી ફી",
    catFarmer: "ખેડૂત સહાય",
    catHousing: "આવાસ",
    catHealthcare: "આરોગ્ય સંભાળ",
    catPension: "પેન્શન",
    catEducation: "શિક્ષણ",
    age: "ઉંમર",
    state: "રાજ્ય",
    district: "જિલ્લો",
    occupation: "વ્યવસાય",
    annual_income: "વાર્ષિક આવક",
    category: "કેટેગરી",
    student_status: "વિદ્યાર્થી",
    farmer_status: "ખેડૂત",
    housing_status: "આવાસની સ્થિતિ",
    land_ownership: "જમીન માલિકી",
    disability_status: "વિકલાંગતા",
    senior_citizen_status: "વરિષ્ઠ નાગરিক",
    gender: "લિંગ",
    bpl_card: "બીપીએલ કાર્ડ",
    yes: "હા",
    no: "ના"
  },
  pa: {
    back: "ਵਾਪਸ",
    visitOfficialPortal: "ਅਧਿਕਾਰਤ ਪੋਰਟਲ 'ਤੇ ਜਾਓ",
    overview: "ਸੰਖੇਪ",
    aiAnalysis: "AI ਵਿਸ਼ਲੇਸ਼ਣ",
    criteriaYouMeet: "ਸ਼ਰਤਾਂ ਜੋ ਤੁਸੀਂ ਪੂਰੀਆਂ ਕਰਦੇ ਹੋ",
    infoNeeded: "ਲੋੜੀਂਦੀ ਜਾਣਕਾਰੀ",
    required: "ਲਾਜ਼ਮੀ",
    bonus: "ਵਾਧੂ",
    documentsRequired: "ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼",
    apply: "ਅਪਲਾਈ ਕਰੋ",
    hideProfile: "ਪ੍ਰੋਫਾਈਲ ਛੁਪਾਓ",
    showExtractedProfile: "ਪ੍ਰੋਫਾਈਲ ਵੇਖੋ",
    extractedProfile: "ਤੁਹਾਡੀ ਪ੍ਰੋਫਾਈਲ",
    fields: "ਵੇਰਵੇ",
    noSchemesMatchFilter: "ਇਸ ਫਿਲਟਰ ਨਾਲ ਮੇਲ ਖਾਂਦੀ ਕੋਈ ਯੋਜਨਾ ਨਹੀਂ ਹੈ",
    govtOfIndia: "ਭਾਰਤ ਸਰਕਾਰ · ਭਲਾਈ ਯੋਜਨਾਵਾਂ",
    costToApply: "ਅਪਲਾਈ ਫੀਸ",
    catFarmer: "ਕਿਸਾਨ ਸਹਾਇਤਾ",
    catHousing: "ਮਕਾਨ",
    catHealthcare: "ਸਿਹਤ ਸੇਵਾ",
    catPension: "ਪੈਨਸ਼ਨ",
    catEducation: "ਸਿੱਖਿਆ",
    age: "ਉਮਰ",
    state: "ਰਾਜ",
    district: "ਜ਼ਿਲ੍ਹਾ",
    occupation: "ਕਿੱਤਾ",
    annual_income: "ਸਾਲਾਨਾ ਕਮਾਈ",
    category: "ਸ਼੍ਰੇਣੀ",
    student_status: "ਵਿਦਿਆਰਥੀ",
    farmer_status: "ਕਿਸਾਨ",
    housing_status: "ਮਕਾਨ ਦੀ ਸਥਿਤੀ",
    land_ownership: "ਜ਼ਮੀਨ ਦੀ ਮਾਲਕੀ",
    disability_status: "ਅਪਾਹਜਤਾ",
    senior_citizen_status: "ਸੀਨੀਅਰ ਸਿਟੀਜ਼ਨ",
    gender: "ਲਿੰਗ",
    bpl_card: "ਬੀਪੀਐਲ ਕਾਰਡ",
    yes: "ਹਾਂ",
    no: "ਨਹੀਂ"
  }
};

export function t(lang: LangCode): Translations {
  return TRANSLATIONS[lang] ?? TRANSLATIONS.en;
}

export function tExtra(lang: LangCode): ExtraTranslations {
  return EXTRA_TRANSLATIONS[lang] ?? EXTRA_TRANSLATIONS.en;
}

export default TRANSLATIONS;
