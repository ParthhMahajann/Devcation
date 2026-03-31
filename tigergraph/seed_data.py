"""
MedGraph AI v2.0 — Seed Data Script
Populates all 13 vertex types and key relationships with realistic medical data.

Run:
  TG_PASSWORD=yourpassword python tigergraph/seed_data.py

Sources: OMIM, DrugBank, SIDER, KEGG, WHO ICD-10 (public knowledge only)
"""
import os
import sys
import pyTigerGraph as tg

# ─── Config ──────────────────────────────────────────────────────────────────
HOST     = os.getenv("TG_HOST",     "http://127.0.0.1")
SECRET   = os.getenv("TG_SECRET",   "")
USERNAME = os.getenv("TG_USERNAME", "tigergraph")
PASSWORD = os.getenv("TG_PASSWORD", "tigergraph")
GRAPH    = os.getenv("TG_GRAPHNAME","MedGraph")


def connect():
    print(f"Connecting to {HOST} …")
    conn = tg.TigerGraphConnection(
        host=HOST, graphname=GRAPH,
        gsPort=os.getenv("TG_GS_PORT", "14240"),
        restppPort=os.getenv("TG_RESTPP_PORT", "9000"),
        username=USERNAME, password=PASSWORD,
    )
    if SECRET:
        try:
            token = conn.getToken(SECRET)
            print(f"  Token: {str(token)[:30]}…")
        except Exception as e:
            print(f"  Warning (token): {e}")
    else:
        try:
            secret = conn.createSecret()
            token  = conn.getToken(secret)
            print(f"  Token obtained via new secret.")
        except Exception as e:
            print(f"  Warning (token): {e}")
    return conn


def uv(conn, vtype, vid, attrs):
    """Upsert a single vertex."""
    conn.upsertVertex(vtype, vid, attributes=attrs)


def ue(conn, src_type, src_id, etype, tgt_type, tgt_id, attrs=None):
    """Upsert a single edge."""
    conn.upsertEdge(src_type, src_id, etype, tgt_type, tgt_id,
                    attributes=attrs or {})


# ════════════════════════════════════════════════════════════════════════════════
# VERTEX DATA
# ════════════════════════════════════════════════════════════════════════════════

def seed_body_systems(conn):
    print("  Seeding BodySystem …")
    systems = [
        ("BS001","Cardiovascular",   "Heart, blood vessels, circulatory system"),
        ("BS002","Respiratory",      "Lungs, airways, breathing"),
        ("BS003","Neurological",     "Brain, spinal cord, peripheral nerves"),
        ("BS004","Gastrointestinal", "Stomach, intestines, digestive organs"),
        ("BS005","Endocrine",        "Hormonal glands: pancreas, thyroid, adrenal"),
        ("BS006","Musculoskeletal",  "Bones, joints, muscles, connective tissue"),
        ("BS007","Hematologic",      "Blood, bone marrow, immune cells"),
        ("BS008","Renal",            "Kidneys, urinary tract"),
        ("BS009","Dermatological",   "Skin, hair, nails"),
        ("BS010","Reproductive",     "Reproductive organs"),
        ("BS011","Ophthalmological", "Eyes, vision"),
        ("BS012","Hepatic",          "Liver, biliary system"),
        ("BS013","General/Systemic", "Whole-body or multi-system effects"),
    ]
    for sid, name, desc in systems:
        uv(conn, "BodySystem", sid, {"name": name, "description": desc})
    print(f"    {len(systems)} body systems seeded.")


def seed_drug_classes(conn):
    print("  Seeding DrugClass …")
    classes = [
        ("DC001","NSAID",              "COX inhibition","Reduce prostaglandin synthesis"),
        ("DC002","ACE Inhibitor",      "ACE enzyme block","Block conversion of angiotensin I→II"),
        ("DC003","Beta Blocker",       "Beta-adrenergic blockade","Block epinephrine on beta receptors"),
        ("DC004","Statin",             "HMG-CoA reductase inhibition","Block cholesterol synthesis in liver"),
        ("DC005","Anticoagulant",      "Coagulation factor inhibition","Prevent blood clot formation"),
        ("DC006","Biguanide",          "AMPK activation / hepatic glucose output reduction","Lower blood glucose in T2DM"),
        ("DC007","Loop Diuretic",      "Na-K-2Cl transporter inhibition","Increase urine output"),
        ("DC008","Calcium Channel Blocker","L-type calcium channel block","Vasodilation and reduced cardiac work"),
        ("DC009","Proton Pump Inhibitor","H+/K+-ATPase inhibition","Reduce gastric acid secretion"),
        ("DC010","Beta-2 Agonist",     "Beta-2 receptor activation","Bronchodilation"),
        ("DC011","Antiplatelet",       "COX-1 / P2Y12 inhibition","Prevent platelet aggregation"),
        ("DC012","Factor Xa Inhibitor","Factor Xa inhibition","Direct oral anticoagulant"),
        ("DC013","AChE Inhibitor",     "Acetylcholinesterase inhibition","Increase acetylcholine in synapses"),
        ("DC014","Anthracycline",      "DNA intercalation / topoisomerase II","Cytotoxic chemotherapy"),
        ("DC015","SERM",               "Selective estrogen receptor modulation","Antagonist in breast tissue"),
    ]
    for cid, name, mech, desc in classes:
        uv(conn, "DrugClass", cid, {"name": name, "mechanism": mech, "description": desc})
    print(f"    {len(classes)} drug classes seeded.")


def seed_pathways(conn):
    print("  Seeding Pathway …")
    pathways = [
        ("PW001","Renin-Angiotensin-Aldosterone System","signaling","Blood pressure regulation via angiotensin","hsa04614","R-HSA-2022377"),
        ("PW002","HMG-CoA Reductase / Cholesterol Synthesis","metabolic","Cholesterol biosynthesis pathway","hsa00100","R-HSA-191273"),
        ("PW003","Arachidonic Acid / COX Pathway","signaling","Prostaglandin and thromboxane synthesis","hsa00590","R-HSA-2142753"),
        ("PW004","Insulin Signaling Pathway","signaling","Glucose uptake and glycogen synthesis","hsa04910","R-HSA-74752"),
        ("PW005","Coagulation Cascade","metabolic","Blood clotting factor activation","hsa04610","R-HSA-140877"),
        ("PW006","Beta-Adrenergic Signaling","signaling","cAMP-mediated cardiac and bronchial effects","hsa04022","R-HSA-418555"),
        ("PW007","AMPK Signaling Pathway","signaling","Energy sensing and glucose metabolism","hsa04152","R-HSA-380972"),
        ("PW008","p53 Tumor Suppressor","regulatory","DNA damage response and apoptosis","hsa04115","R-HSA-5633007"),
        ("PW009","HER2 / ErbB Signaling","signaling","Cell proliferation in breast cancer","hsa04012","R-HSA-1227990"),
        ("PW010","TGF-Beta Signaling","signaling","Fibrosis and immune regulation","hsa04350","R-HSA-170834"),
    ]
    for pid, name, ptype, desc, kegg, reactome in pathways:
        uv(conn, "Pathway", pid, {"name": name, "pathway_type": ptype,
                                   "description": desc, "kegg_id": kegg, "reactome_id": reactome})
    print(f"    {len(pathways)} pathways seeded.")


def seed_genes(conn):
    print("  Seeding Gene …")
    genes = [
        ("G001","Angiotensin Converting Enzyme","ACE","17q23.3","protein_coding",
         "Converts angiotensin I to angiotensin II; regulates blood pressure","MIM:106180","P12821"),
        ("G002","Proprotein Convertase Subtilisin/Kexin 9","PCSK9","1p32.3","protein_coding",
         "Degrades LDL receptors; raises LDL cholesterol","MIM:607786","Q8NBP7"),
        ("G003","Cytochrome P450 2D6","CYP2D6","22q13.2","protein_coding",
         "Metabolises ~25% of all drugs including metoprolol, clopidogrel","MIM:124030","P10635"),
        ("G004","Cytochrome P450 3A4","CYP3A4","7q22.1","protein_coding",
         "Metabolises ~50% of all drugs including atorvastatin, amlodipine","MIM:124010","P08684"),
        ("G005","BRCA1 DNA Repair Associated","BRCA1","17q21.31","protein_coding",
         "Tumour suppressor; DNA repair; breast and ovarian cancer risk","MIM:113705","P38398"),
        ("G006","Apolipoprotein E","APOE","19q13.32","protein_coding",
         "Lipid transport; APOE4 allele increases Alzheimer's and CVD risk","MIM:107741","P02649"),
        ("G007","Transcription Factor 7 Like 2","TCF7L2","10q25.2","protein_coding",
         "Regulates insulin secretion; strongest T2DM GWAS locus","MIM:602228","Q9NQB0"),
        ("G008","Coagulation Factor II (Prothrombin)","F2","11p11.2","protein_coding",
         "G20210A variant increases VTE risk; warfarin target","MIM:176930","P00734"),
        ("G009","Vitamin K Epoxide Reductase Complex Subunit 1","VKORC1","16p11.2","protein_coding",
         "Warfarin target gene; VKORC1 variants affect warfarin sensitivity","MIM:608547","Q9BQB6"),
        ("G010","Erb-B2 Receptor Tyrosine Kinase 2","ERBB2","17q12","protein_coding",
         "HER2 amplification in ~20% of breast cancers; targeted by trastuzumab","MIM:164870","P04626"),
        ("G011","Tumor Protein p53","TP53","17p13.1","protein_coding",
         "Master tumour suppressor; mutated in ~50% of all cancers","MIM:191170","P04637"),
        ("G012","Vascular Endothelial Growth Factor A","VEGFA","6p21.1","protein_coding",
         "Promotes angiogenesis; elevated in tumours and heart failure","MIM:192240","P15692"),
    ]
    for gid, name, sym, chrom, gtype, func, omim, uniprot in genes:
        uv(conn, "Gene", gid, {
            "name": name, "symbol": sym, "chromosome": chrom, "gene_type": gtype,
            "function_desc": func, "omim_id": omim, "uniprot_id": uniprot,
        })
    print(f"    {len(genes)} genes seeded.")


def seed_biomarkers(conn):
    print("  Seeding Biomarker …")
    bms = [
        ("BM001","HbA1c","%",4.0,5.6,"lab"),
        ("BM002","LDL Cholesterol","mg/dL",0.0,100.0,"lab"),
        ("BM003","INR (International Normalised Ratio)","ratio",0.8,1.2,"lab"),
        ("BM004","Troponin I","ng/mL",0.0,0.04,"lab"),
        ("BM005","Serum Creatinine","mg/dL",0.6,1.2,"lab"),
        ("BM006","TSH (Thyroid Stimulating Hormone)","mIU/L",0.4,4.0,"lab"),
        ("BM007","PSA (Prostate Specific Antigen)","ng/mL",0.0,4.0,"lab"),
        ("BM008","CRP (C-Reactive Protein)","mg/L",0.0,1.0,"lab"),
        ("BM009","eGFR","mL/min/1.73m2",60.0,120.0,"lab"),
        ("BM010","Systolic Blood Pressure","mmHg",90.0,120.0,"clinical"),
        ("BM011","NT-proBNP","pg/mL",0.0,125.0,"lab"),
        ("BM012","ALT (Alanine Aminotransferase)","U/L",7.0,56.0,"lab"),
        ("BM013","Fasting Blood Glucose","mg/dL",70.0,100.0,"lab"),
        ("BM014","Total Cholesterol","mg/dL",0.0,200.0,"lab"),
        ("BM015","eGFR (CKD Staging)","mL/min/1.73m2",60.0,120.0,"lab"),
    ]
    for bid, name, unit, lo, hi, btype in bms:
        uv(conn, "Biomarker", bid, {
            "name": name, "unit": unit, "normal_range_low": lo,
            "normal_range_high": hi, "biomarker_type": btype,
        })
    print(f"    {len(bms)} biomarkers seeded.")


def seed_risk_factors(conn):
    print("  Seeding RiskFactor …")
    rfs = [
        ("RF001","Smoking","lifestyle",True,"Current or former smoking significantly increases CVD, COPD, and cancer risk"),
        ("RF002","Obesity (BMI > 30)","lifestyle",True,"Excess adipose tissue drives insulin resistance, hypertension, and joint stress"),
        ("RF003","Sedentary Lifestyle","lifestyle",True,"Physical inactivity increases T2DM, CVD, and obesity risk"),
        ("RF004","High Sodium Diet","lifestyle",True,"Excess sodium intake elevates blood pressure"),
        ("RF005","Family History of CVD","genetic",False,"First-degree relative with premature CVD doubles personal risk"),
        ("RF006","Age > 65","demographic",False,"Ageing increases risk of all chronic diseases"),
        ("RF007","Uncontrolled Diabetes","clinical",True,"Poorly managed glucose accelerates vascular and neurological damage"),
        ("RF008","Hypertension","clinical",True,"Elevated BP is a major risk factor for stroke, MI, and renal failure"),
        ("RF009","Alcohol Abuse","lifestyle",True,"Chronic heavy drinking damages liver, heart, and neurological function"),
        ("RF010","Air Pollution Exposure","environmental",False,"Particulate matter drives respiratory and cardiovascular disease"),
        ("RF011","Hyperlipidemia","clinical",True,"Elevated LDL accelerates atherosclerosis"),
        ("RF012","Family History of Cancer","genetic",False,"BRCA/TP53 germline variants increase cancer risk"),
        ("RF013","Chronic Inflammation","clinical",True,"Persistent CRP elevation correlates with CVD and cancer risk"),
        ("RF014","Chronic Kidney Disease","clinical",True,"CKD is an independent CVD risk amplifier"),
        ("RF015","Post-Menopausal (Female)","demographic",False,"Loss of oestrogen increases CVD and osteoporosis risk"),
    ]
    for rid, name, cat, mod, desc in rfs:
        uv(conn, "RiskFactor", rid, {
            "name": name, "category": cat, "modifiable": mod, "description": desc,
        })
    print(f"    {len(rfs)} risk factors seeded.")


def seed_medical_tests(conn):
    print("  Seeding MedicalTest …")
    tests = [
        ("MT001","Complete Blood Count (CBC)","blood","Measures RBC, WBC, platelets, haemoglobin",25.0,4,False),
        ("MT002","Echocardiogram","imaging","Ultrasound of heart structure and function",500.0,24,False),
        ("MT003","HbA1c Blood Test","blood","3-month average blood glucose indicator",30.0,1,False),
        ("MT004","Coronary Angiography","imaging","X-ray of coronary arteries with contrast dye",3500.0,2,True),
        ("MT005","MRI Brain","imaging","Structural MRI for stroke, tumour, Alzheimer's",1200.0,24,False),
        ("MT006","Chest X-Ray","imaging","First-line chest investigation for COPD, pneumonia, cancer",80.0,2,False),
        ("MT007","Spirometry","functional","Lung function test for COPD and asthma",150.0,1,False),
        ("MT008","Liver Biopsy","biopsy","Tissue sampling for NAFLD/cirrhosis grading",2000.0,48,True),
        ("MT009","Electrocardiogram (ECG)","functional","Electrical activity of the heart",50.0,1,False),
        ("MT010","Oral Glucose Tolerance Test","blood","Diagnoses T2DM and pre-diabetes",40.0,4,False),
        ("MT011","Renal Ultrasound","imaging","Kidney size and structure assessment",350.0,4,False),
        ("MT012","INR / PT Test","blood","Monitors warfarin anticoagulation",20.0,2,False),
        ("MT013","Lipid Panel","blood","Total cholesterol, LDL, HDL, triglycerides",35.0,2,False),
        ("MT014","Troponin Assay","blood","Diagnoses acute myocardial infarction",60.0,1,False),
        ("MT015","CT Chest (HRCT)","imaging","High-resolution lung imaging for COPD/cancer staging",800.0,4,False),
    ]
    for tid, name, ttype, desc, cost, hrs, inv in tests:
        uv(conn, "MedicalTest", tid, {
            "name": name, "test_type": ttype, "description": desc,
            "cost_usd": cost, "turnaround_hours": hrs, "is_invasive": inv,
        })
    print(f"    {len(tests)} medical tests seeded.")


def seed_procedures(conn):
    print("  Seeding Procedure …")
    procs = [
        ("PR001","Coronary Artery Bypass Graft (CABG)","surgical","Open-heart surgery to bypass blocked coronary arteries","33510",6.0,True),
        ("PR002","Percutaneous Coronary Intervention (PCI)","surgical","Angioplasty and stent placement for coronary artery stenosis","92920",2.0,True),
        ("PR003","Haemodialysis","therapeutic","Renal replacement therapy for end-stage CKD","90935",0.25,False),
        ("PR004","Insulin Pump Therapy","therapeutic","Continuous subcutaneous insulin infusion for diabetes","95251",0.0,False),
        ("PR005","Pulmonary Rehabilitation","therapeutic","Exercise and education programme for COPD patients","94625",0.0,False),
        ("PR006","Chemotherapy Administration","therapeutic","Systemic cytotoxic drug infusion for cancer","96413",4.0,False),
        ("PR007","Bronchoscopy","diagnostic","Direct visualisation of airways; biopsy for lung cancer","31622",0.5,True),
        ("PR008","Defibrillation / Cardioversion","therapeutic","Electrical shock to restore normal cardiac rhythm","92960",0.5,True),
    ]
    for pid, name, ptype, desc, cpt, dur, anes in procs:
        uv(conn, "Procedure", pid, {
            "name": name, "procedure_type": ptype, "description": desc,
            "cpt_code": cpt, "avg_duration_hours": dur, "requires_anesthesia": anes,
        })
    print(f"    {len(procs)} procedures seeded.")


def seed_symptoms(conn):
    print("  Seeding Symptom …")
    symptoms = [
        ("S001","Chest Pain","Cardiovascular",0.9,"sudden","transient",False),
        ("S002","Shortness of Breath","Respiratory",0.85,"gradual","persistent",False),
        ("S003","Fatigue","General/Systemic",0.4,"gradual","persistent",False),
        ("S004","Fever","General/Systemic",0.6,"sudden","transient",False),
        ("S005","Headache","Neurological",0.5,"sudden","episodic",False),
        ("S006","Dizziness","Neurological",0.55,"sudden","episodic",False),
        ("S007","Cough","Respiratory",0.5,"gradual","persistent",False),
        ("S008","Nausea","Gastrointestinal",0.45,"sudden","transient",False),
        ("S009","Leg Oedema","Cardiovascular",0.75,"gradual","persistent",False),
        ("S010","Palpitations","Cardiovascular",0.7,"sudden","episodic",False),
        ("S011","Polyuria","Endocrine",0.65,"gradual","persistent",False),
        ("S012","Polydipsia","Endocrine",0.65,"gradual","persistent",False),
        ("S013","Unintentional Weight Loss","General/Systemic",0.7,"gradual","persistent",False),
        ("S014","Night Sweats","General/Systemic",0.5,"gradual","persistent",False),
        ("S015","Joint Pain","Musculoskeletal",0.6,"gradual","persistent",False),
        ("S016","Blurred Vision","Ophthalmological",0.7,"gradual","persistent",False),
        ("S017","Wheezing","Respiratory",0.8,"sudden","episodic",False),
        ("S018","Confusion / Cognitive Decline","Neurological",0.75,"gradual","persistent",False),
        ("S019","Jaundice","Hepatic",0.8,"gradual","persistent",True),
        ("S020","Haemoptysis","Respiratory",0.85,"sudden","episodic",True),
        ("S021","Pallor","Hematologic",0.5,"gradual","persistent",False),
        ("S022","Hypertension (elevated BP)","Cardiovascular",0.8,"gradual","persistent",False),
        ("S023","Tachycardia","Cardiovascular",0.7,"sudden","episodic",False),
        ("S024","Muscle Weakness","Musculoskeletal",0.5,"gradual","persistent",False),
        ("S025","Memory Loss","Neurological",0.75,"gradual","persistent",False),
        ("S026","Urinary Frequency","Renal",0.55,"gradual","persistent",False),
        ("S027","Abdominal Pain","Gastrointestinal",0.6,"sudden","episodic",False),
        ("S028","Peripheral Neuropathy (tingling)","Neurological",0.65,"gradual","persistent",False),
        ("S029","Dry Skin / Pruritus","Dermatological",0.35,"gradual","persistent",False),
        ("S030","Exercise Intolerance","Cardiovascular",0.75,"gradual","persistent",False),
    ]
    for sid, name, bsys, sw, onset, dur, path in symptoms:
        uv(conn, "Symptom", sid, {
            "name": name, "body_system": bsys, "severity_weight": sw,
            "onset_pattern": onset, "duration_pattern": dur, "is_pathognomonic": path,
        })
    print(f"    {len(symptoms)} symptoms seeded.")


def seed_side_effects(conn):
    print("  Seeding SideEffect …")
    ses = [
        ("SE001","Hypoglycaemia","severe","common","early",True,"Endocrine"),
        ("SE002","Nausea / GI Upset","mild","very_common","early",True,"Gastrointestinal"),
        ("SE003","Dry Cough","mild","common","early",True,"Respiratory"),
        ("SE004","Hyperkalaemia","moderate","uncommon","delayed",True,"Renal"),
        ("SE005","Rhabdomyolysis","severe","rare","delayed",False,"Musculoskeletal"),
        ("SE006","Haemorrhage / Bleeding","severe","uncommon","delayed",True,"Hematologic"),
        ("SE007","Acute Kidney Injury","severe","uncommon","early",True,"Renal"),
        ("SE008","Anaphylaxis","life-threatening","very_rare","immediate",True,"Hematologic"),
        ("SE009","QT Prolongation","severe","rare","delayed",True,"Cardiovascular"),
        ("SE010","Hepatotoxicity","severe","rare","delayed",False,"Hepatic"),
        ("SE011","Cardiotoxicity","life-threatening","uncommon","delayed",False,"Cardiovascular"),
        ("SE012","Thrombocytopenia","moderate","uncommon","delayed",True,"Hematologic"),
        ("SE013","Peripheral Oedema","mild","common","delayed",True,"Cardiovascular"),
        ("SE014","Bradycardia","moderate","common","early",True,"Cardiovascular"),
        ("SE015","Headache","mild","common","early",True,"Neurological"),
        ("SE016","Fatigue","mild","common","early",True,"General/Systemic"),
        ("SE017","Lactic Acidosis","life-threatening","very_rare","delayed",False,"Metabolic"),
        ("SE018","Angioedema","life-threatening","rare","immediate",True,"Dermatological"),
        ("SE019","Hot Flashes","mild","very_common","early",True,"Endocrine"),
        ("SE020","Myalgia (Muscle Pain)","mild","common","delayed",True,"Musculoskeletal"),
    ]
    for eid, name, sev, freq, onset, rev, bsys in ses:
        uv(conn, "SideEffect", eid, {
            "name": name, "severity": sev, "frequency": freq,
            "onset_time": onset, "reversible": rev, "body_system": bsys,
        })
    print(f"    {len(ses)} side effects seeded.")


def seed_diseases(conn):
    print("  Seeding Disease …")
    diseases = [
        # id, name, icd10, snomed, omim, severity, category, desc, prev, mort, onset, hereditary, contagious, complexity
        ("D001","Type 2 Diabetes Mellitus","E11","44054006","MIM:125853","moderate","Endocrine",
         "Insulin resistance and progressive beta-cell dysfunction",6900.0,0.05,"chronic",True,False,3),
        ("D002","Essential Hypertension","I10","59621000","MIM:145500","moderate","Cardiovascular",
         "Persistently elevated systemic arterial blood pressure",29000.0,0.08,"chronic",True,False,2),
        ("D003","Coronary Artery Disease","I25","53741008","MIM:607339","severe","Cardiovascular",
         "Atherosclerotic narrowing of the coronary arteries",6400.0,0.15,"chronic",True,False,3),
        ("D004","Heart Failure","I50","84114007","","severe","Cardiovascular",
         "Inability of the heart to meet the body's circulatory demands",1900.0,0.20,"chronic",False,False,4),
        ("D005","Chronic Kidney Disease","N18","709044004","","moderate","Renal",
         "Progressive loss of kidney function over months to years",15000.0,0.12,"chronic",False,False,3),
        ("D006","COPD","J44","13645005","MIM:606963","moderate","Respiratory",
         "Progressive, largely irreversible airflow obstruction from tobacco/pollution",3900.0,0.10,"chronic",True,False,3),
        ("D007","Asthma","J45","195967001","MIM:600807","mild","Respiratory",
         "Chronic inflammatory airway disease with reversible bronchoconstriction",7500.0,0.01,"chronic",True,False,2),
        ("D008","Alzheimer's Disease","G30","26929004","MIM:104300","severe","Neurological",
         "Progressive neurodegenerative disorder causing memory and cognitive decline",1400.0,0.35,"chronic",True,False,4),
        ("D009","Atrial Fibrillation","I48","49436004","MIM:613980","moderate","Cardiovascular",
         "Irregular rapid electrical activity of the atria",3700.0,0.06,"chronic",True,False,3),
        ("D010","Hyperlipidaemia","E78","13644009","MIM:143890","mild","Endocrine",
         "Elevated plasma cholesterol and/or triglycerides",31000.0,0.03,"chronic",True,False,1),
        ("D011","Acute Myocardial Infarction","I21","57054005","","critical","Cardiovascular",
         "Irreversible myocardial cell death due to coronary artery occlusion",330.0,0.08,"acute",False,False,5),
        ("D012","Type 1 Diabetes Mellitus","E10","46635009","MIM:222100","moderate","Endocrine",
         "Autoimmune destruction of pancreatic beta cells causing absolute insulin deficiency",700.0,0.04,"chronic",True,False,4),
        ("D013","Non-Alcoholic Fatty Liver Disease","K76.0","197321007","","mild","Hepatic",
         "Hepatic steatosis not attributable to alcohol; associated with metabolic syndrome",24000.0,0.03,"chronic",False,False,2),
        ("D014","Osteoarthritis","M19","396275006","","moderate","Musculoskeletal",
         "Degenerative joint disease with cartilage breakdown",18000.0,0.01,"chronic",True,False,2),
        ("D015","Rheumatoid Arthritis","M05","69896004","MIM:180300","moderate","Musculoskeletal",
         "Chronic autoimmune inflammatory joint disease",1000.0,0.05,"chronic",True,False,3),
        ("D016","Breast Cancer","C50","254837009","MIM:114480","severe","Oncologic",
         "Malignant tumour arising from breast epithelial tissue",12600.0,0.22,"chronic",True,False,4),
        ("D017","Lung Cancer","C34","93880001","","critical","Oncologic",
         "Malignant lung tumour; predominantly associated with smoking",4200.0,0.55,"chronic",False,False,5),
        ("D018","Ischaemic Stroke","I63","422504002","","critical","Neurological",
         "Brain infarction from arterial occlusion due to thrombosis or embolism",800.0,0.25,"acute",False,False,5),
        ("D019","Cirrhosis","K74","19943007","","severe","Hepatic",
         "End-stage liver fibrosis from chronic liver injury",500.0,0.30,"chronic",False,False,4),
        ("D020","Diabetic Nephropathy","N08","127013003","","severe","Renal",
         "Kidney damage caused by longstanding diabetes-related vascular injury",2500.0,0.18,"chronic",False,False,4),
    ]
    for row in diseases:
        (did, name, icd, snomed, omim, sev, cat, desc, prev, mort, onset, hered, cont, compl) = row
        uv(conn, "Disease", did, {
            "name": name, "icd10_code": icd, "snomed_code": snomed, "omim_id": omim,
            "severity": sev, "category": cat, "description": desc,
            "prevalence_per_100k": prev, "mortality_rate": mort, "onset_type": onset,
            "is_hereditary": hered, "is_contagious": cont, "treatment_complexity": compl,
        })
    print(f"    {len(diseases)} diseases seeded.")


def seed_drugs(conn):
    print("  Seeding Drug …")
    drugs = [
        # id, name, generic, drug_class, status, formula, t½_h, route, preg_cat, bbw, max_dose, controlled
        ("DR001","Metformin","Metformin HCl","Biguanide","approved","C4H11N5",6.5,"oral","B",False,2550.0,False),
        ("DR002","Lisinopril","Lisinopril","ACE Inhibitor","approved","C21H31N3O5",12.0,"oral","D",False,40.0,False),
        ("DR003","Atorvastatin","Atorvastatin calcium","Statin","approved","C33H35FN2O5",14.0,"oral","X",False,80.0,False),
        ("DR004","Aspirin","Acetylsalicylic acid","NSAID/Antiplatelet","approved","C9H8O4",0.3,"oral","C",False,4000.0,False),
        ("DR005","Warfarin","Warfarin sodium","Anticoagulant","approved","C19H16O4",40.0,"oral","X",True,10.0,False),
        ("DR006","Metoprolol","Metoprolol tartrate","Beta Blocker","approved","C15H25NO3",3.5,"oral","C",False,400.0,False),
        ("DR007","Furosemide","Furosemide","Loop Diuretic","approved","C12H11ClN2O5S",2.0,"oral/IV","C",False,600.0,False),
        ("DR008","Amlodipine","Amlodipine besylate","Calcium Channel Blocker","approved","C20H25ClN2O5",35.0,"oral","C",False,10.0,False),
        ("DR009","Omeprazole","Omeprazole","Proton Pump Inhibitor","approved","C17H19N3O3S",1.0,"oral","C",False,40.0,False),
        ("DR010","Albuterol","Salbutamol","Beta-2 Agonist","approved","C13H21NO3",3.0,"inhaled","C",False,16.0,False),
        ("DR011","Insulin Glargine","Insulin glargine","Insulin","approved","C267H404N72O78S6",24.0,"SC","B",False,0.0,False),
        ("DR012","Rivaroxaban","Rivaroxaban","Factor Xa Inhibitor","approved","C19H18ClN3O5S",9.0,"oral","X",True,20.0,False),
        ("DR013","Ibuprofen","Ibuprofen","NSAID","approved","C13H18O2",2.0,"oral","C",False,3200.0,False),
        ("DR014","Donepezil","Donepezil HCl","AChE Inhibitor","approved","C24H29NO3",70.0,"oral","C",False,23.0,False),
        ("DR015","Clopidogrel","Clopidogrel bisulfate","Antiplatelet","approved","C16H16ClNO2S",6.0,"oral","B",True,75.0,False),
        ("DR016","Ramipril","Ramipril","ACE Inhibitor","approved","C23H32N2O5",13.0,"oral","D",False,10.0,False),
        ("DR017","Spironolactone","Spironolactone","Aldosterone Antagonist","approved","C24H32O4S",20.0,"oral","C",False,400.0,False),
        ("DR018","Azithromycin","Azithromycin","Macrolide Antibiotic","approved","C38H72N2O12",68.0,"oral","B",False,500.0,False),
        ("DR019","Doxorubicin","Doxorubicin HCl","Anthracycline","approved","C27H29NO11",26.7,"IV","D",True,550.0,False),
        ("DR020","Tamoxifen","Tamoxifen citrate","SERM","approved","C26H29NO",192.0,"oral","D",True,40.0,False),
    ]
    for row in drugs:
        (did, name, gen, cls, status, formula, t_half, route, preg, bbw, maxd, ctrl) = row
        uv(conn, "Drug", did, {
            "name": name, "generic_name": gen, "drug_class": cls,
            "approval_status": status, "molecular_formula": formula,
            "half_life_hours": t_half, "route": route,
            "pregnancy_category": preg, "black_box_warning": bbw,
            "max_daily_dose_mg": maxd, "controlled_substance": ctrl,
        })
    print(f"    {len(drugs)} drugs seeded.")


def seed_patients(conn):
    print("  Seeding Patient …")
    patients = [
        ("P001","John Smith",65,"male","A+",27.5,"former","moderate","White","10001"),
        ("P002","Mary Johnson",58,"female","O+",31.2,"never","none","White","10002"),
        ("P003","Robert Chen",72,"male","B+",24.8,"former","moderate","Asian","10003"),
        ("P004","Sarah Davis",45,"female","AB-",26.1,"never","none","Hispanic","10004"),
        ("P005","Ahmed Hassan",55,"male","O-",29.3,"never","moderate","Middle Eastern","10005"),
    ]
    for pid, name, age, gender, blood, bmi, smoke, alc, eth, zip in patients:
        uv(conn, "Patient", pid, {
            "name": name, "age": age, "gender": gender, "blood_type": blood,
            "bmi": bmi, "smoking_status": smoke, "alcohol_use": alc,
            "ethnicity": eth, "zip_code": zip,
        })
    print(f"    {len(patients)} patients seeded.")


# ════════════════════════════════════════════════════════════════════════════════
# EDGE DATA
# ════════════════════════════════════════════════════════════════════════════════

def seed_symptom_body_system_edges(conn):
    print("  Seeding ORIGINATES_FROM (Symptom → BodySystem) …")
    edges = [
        ("S001","BS001"),("S009","BS001"),("S010","BS001"),("S022","BS001"),("S023","BS001"),("S030","BS001"),
        ("S002","BS002"),("S007","BS002"),("S017","BS002"),("S020","BS002"),
        ("S005","BS003"),("S006","BS003"),("S018","BS003"),("S025","BS003"),("S028","BS003"),
        ("S008","BS004"),("S027","BS004"),
        ("S011","BS005"),("S012","BS005"),
        ("S015","BS006"),("S024","BS006"),
        ("S021","BS007"),
        ("S026","BS008"),("S029","BS008"),
        ("S003","BS013"),("S004","BS013"),("S013","BS013"),("S014","BS013"),("S016","BS011"),("S019","BS012"),
    ]
    for sid, bsid in edges:
        ue(conn, "Symptom", sid, "ORIGINATES_FROM", "BodySystem", bsid, {"is_primary": True})
    print(f"    {len(edges)} edges.")


def seed_disease_system_edges(conn):
    print("  Seeding AFFECTS_SYSTEM (Disease → BodySystem) …")
    edges = [
        ("D001","BS005"),("D001","BS008"),("D001","BS001"),
        ("D002","BS001"),("D002","BS008"),("D002","BS003"),
        ("D003","BS001"),("D004","BS001"),("D004","BS008"),
        ("D005","BS008"),("D005","BS001"),
        ("D006","BS002"),("D007","BS002"),
        ("D008","BS003"),
        ("D009","BS001"),("D010","BS001"),("D010","BS005"),
        ("D011","BS001"),("D012","BS005"),
        ("D013","BS012"),("D014","BS006"),
        ("D015","BS006"),("D015","BS007"),
        ("D016","BS010"),("D017","BS002"),
        ("D018","BS003"),("D019","BS012"),
        ("D020","BS008"),("D020","BS001"),
    ]
    for did, bsid in edges:
        ue(conn, "Disease", did, "AFFECTS_SYSTEM", "BodySystem", bsid,
           {"is_primary": True})
    print(f"    {len(edges)} edges.")


def seed_has_symptom_edges(conn):
    print("  Seeding HAS_SYMPTOM (Disease ↔ Symptom) …")
    # (disease_id, symptom_id, frequency, weight)
    edges = [
        # T2DM
        ("D001","S011","always",0.85),("D001","S012","always",0.85),
        ("D001","S013","often",0.6),("D001","S016","often",0.65),
        ("D001","S003","often",0.5),("D001","S028","sometimes",0.6),
        # Hypertension
        ("D002","S022","always",0.9),("D002","S005","sometimes",0.4),
        ("D002","S006","sometimes",0.4),
        # CAD
        ("D003","S001","often",0.85),("D003","S030","often",0.8),
        ("D003","S003","often",0.5),("D003","S002","often",0.7),
        # Heart Failure
        ("D004","S002","always",0.9),("D004","S009","always",0.85),
        ("D004","S003","always",0.8),("D004","S030","always",0.85),
        ("D004","S023","often",0.7),
        # CKD
        ("D005","S003","often",0.6),("D005","S009","often",0.6),
        ("D005","S026","often",0.65),("D005","S024","sometimes",0.5),
        ("D005","S029","sometimes",0.5),
        # COPD
        ("D006","S007","always",0.9),("D006","S002","always",0.85),
        ("D006","S017","often",0.8),("D006","S003","often",0.7),
        # Asthma
        ("D007","S017","always",0.9),("D007","S007","often",0.75),
        ("D007","S002","often",0.7),("D007","S001","sometimes",0.5),
        # Alzheimer's
        ("D008","S025","always",0.95),("D008","S018","always",0.9),
        ("D008","S003","often",0.5),
        # Atrial Fibrillation
        ("D009","S010","always",0.9),("D009","S002","often",0.7),
        ("D009","S003","often",0.6),("D009","S006","sometimes",0.5),
        # Hyperlipidaemia  (often silent)
        ("D010","S003","sometimes",0.2),
        # AMI
        ("D011","S001","always",0.95),("D011","S002","always",0.8),
        ("D011","S008","often",0.6),("D011","S023","often",0.7),
        # T1DM
        ("D012","S011","always",0.9),("D012","S012","always",0.9),
        ("D012","S013","often",0.75),("D012","S003","often",0.6),
        # NAFLD
        ("D013","S027","sometimes",0.4),("D013","S003","sometimes",0.3),
        # Osteoarthritis
        ("D014","S015","always",0.9),("D014","S024","often",0.6),
        # RA
        ("D015","S015","always",0.9),("D015","S003","often",0.6),
        ("D015","S004","sometimes",0.5),
        # Breast Cancer
        ("D016","S013","often",0.65),("D016","S003","often",0.5),
        # Lung Cancer
        ("D017","S007","often",0.7),("D017","S020","sometimes",0.8),
        ("D017","S013","often",0.7),("D017","S002","often",0.6),
        # Stroke
        ("D018","S005","often",0.7),("D018","S018","often",0.8),
        ("D018","S006","often",0.7),
        # Cirrhosis
        ("D019","S019","often",0.8),("D019","S027","often",0.6),
        ("D019","S003","often",0.5),
        # Diabetic Nephropathy
        ("D020","S026","often",0.7),("D020","S009","often",0.6),
        ("D020","S003","often",0.5),
    ]
    for did, sid, freq, wt in edges:
        ue(conn, "Disease", did, "HAS_SYMPTOM", "Symptom", sid,
           {"frequency": freq, "weight": wt})
    print(f"    {len(edges)} edges.")


def seed_symptom_overlap_edges(conn):
    print("  Seeding SYMPTOM_OVERLAP …")
    edges = [
        ("S001","S010",0.7),("S001","S002",0.65),("S002","S007",0.6),
        ("S002","S017",0.7),("S003","S016",0.55),("S011","S012",0.9),
        ("S011","S013",0.6),("S022","S001",0.5),("S009","S002",0.65),
        ("S010","S023",0.75),("S025","S018",0.85),("S015","S024",0.6),
    ]
    for s1, s2, score in edges:
        ue(conn, "Symptom", s1, "SYMPTOM_OVERLAP", "Symptom", s2,
           {"correlation_score": score})
    print(f"    {len(edges)} edges.")


def seed_comorbid_edges(conn):
    print("  Seeding COMORBID_WITH (Disease ↔ Disease) …")
    edges = [
        ("D001","D002",0.72,"UKPDS/NHS Digital"),
        ("D001","D010",0.68,"Framingham Heart Study"),
        ("D001","D003",0.55,"ACC/AHA Guidelines"),
        ("D001","D020",0.48,"ADVANCE trial"),
        ("D001","D013",0.62,"NASH/T2DM literature"),
        ("D002","D003",0.65,"ESC/ESH Guidelines"),
        ("D002","D004",0.55,"ESC HF Guidelines"),
        ("D002","D009",0.45,"AFFIRM trial"),
        ("D002","D018",0.58,"Stroke prevention literature"),
        ("D002","D005",0.42,"CKD-Hypertension link"),
        ("D003","D004",0.70,"PARADIGM-HF"),
        ("D003","D009",0.52,"AF in CAD patients"),
        ("D003","D018",0.48,"Cardioembolic stroke"),
        ("D009","D004",0.60,"ESC AF Guidelines"),
        ("D009","D018",0.55,"AF stroke risk CHADS2"),
        ("D010","D003",0.65,"Framingham risk score"),
        ("D005","D004",0.50,"CRS type 3"),
        ("D005","D020",0.80,"T2DM→CKD progression"),
        ("D006","D007",0.35,"GINA/GOLD overlap (ACO)"),
        ("D013","D019",0.45,"NASH→Cirrhosis"),
        ("D015","D003",0.40,"RA cardiovascular risk"),
        ("D001","D004",0.38,"Diabetic cardiomyopathy"),
    ]
    for d1, d2, rate, src in edges:
        ue(conn, "Disease", d1, "COMORBID_WITH", "Disease", d2,
           {"comorbidity_rate": rate, "evidence_source": src})
    print(f"    {len(edges)} edges.")


def seed_progression_edges(conn):
    print("  Seeding PROGRESSES_TO (Disease → Disease) …")
    edges = [
        # source, target, progression_rate, avg_years, preventable
        ("D001","D020",0.40,10.0,True),
        ("D001","D004",0.25,15.0,True),
        ("D001","D018",0.20,12.0,True),
        ("D002","D004",0.30,12.0,True),
        ("D002","D018",0.25,10.0,True),
        ("D002","D005",0.20,15.0,True),
        ("D003","D011",0.35,5.0,True),
        ("D003","D004",0.45,8.0,True),
        ("D005","D003",0.30,8.0,False),  # CKD worsens CVD
        ("D010","D003",0.40,10.0,True),
        ("D013","D019",0.20,15.0,True),
        ("D019","D004",0.15,5.0,False),
        ("D009","D018",0.35,5.0,True),
        ("D009","D004",0.40,8.0,True),
        ("D006","D004",0.20,10.0,False),
        ("D017","D002",0.25,3.0,False),
        ("D020","D005",0.60,5.0,True),
    ]
    for src, tgt, rate, yrs, prev in edges:
        ue(conn, "Disease", src, "PROGRESSES_TO", "Disease", tgt, {
            "progression_rate": rate,
            "avg_years_to_progress": yrs,
            "prevention_possible": prev,
        })
    print(f"    {len(edges)} edges.")


def seed_treats_edges(conn):
    print("  Seeding TREATS (Drug → Disease) …")
    edges = [
        # drug, disease, efficacy, evidence, first_line, duration_days
        ("DR001","D001",0.80,"A",True,0),
        ("DR001","D013",0.45,"B",False,0),
        ("DR002","D002",0.82,"A",True,0),
        ("DR002","D004",0.78,"A",True,0),
        ("DR002","D003",0.70,"A",True,0),
        ("DR002","D020",0.65,"A",True,0),
        ("DR003","D010",0.88,"A",True,0),
        ("DR003","D003",0.72,"A",True,0),
        ("DR004","D003",0.70,"A",True,0),
        ("DR004","D011",0.68,"A",True,0),
        ("DR004","D018",0.55,"A",True,0),
        ("DR005","D009",0.75,"A",True,0),
        ("DR006","D002",0.78,"A",True,0),
        ("DR006","D004",0.80,"A",True,0),
        ("DR006","D003",0.72,"A",True,0),
        ("DR007","D004",0.85,"A",True,0),
        ("DR007","D002",0.65,"B",False,0),
        ("DR008","D002",0.80,"A",True,0),
        ("DR008","D003",0.68,"A",False,0),
        ("DR009","D013",0.55,"C",False,0),
        ("DR010","D007",0.90,"A",True,0),
        ("DR010","D006",0.78,"A",True,0),
        ("DR011","D012",0.92,"A",True,0),
        ("DR011","D001",0.70,"A",False,0),
        ("DR012","D009",0.82,"A",True,0),
        ("DR013","D014",0.70,"B",True,30),
        ("DR013","D015",0.60,"B",False,0),
        ("DR014","D008",0.55,"A",True,0),
        ("DR015","D003",0.75,"A",True,0),
        ("DR015","D009",0.70,"A",False,0),
        ("DR016","D004",0.82,"A",True,0),
        ("DR016","D002",0.80,"A",True,0),
        ("DR017","D004",0.75,"A",True,0),
        ("DR017","D002",0.65,"B",False,0),
        ("DR018","D007",0.60,"C",False,5),
        ("DR019","D016",0.70,"A",True,0),
        ("DR019","D017",0.65,"A",True,0),
        ("DR020","D016",0.78,"A",True,0),
    ]
    for drug, disease, eff, ev, fl, dur in edges:
        ue(conn, "Drug", drug, "TREATS", "Disease", disease, {
            "efficacy_score": eff, "evidence_level": ev,
            "first_line": fl, "treatment_duration_days": dur,
        })
    print(f"    {len(edges)} edges.")


def seed_drug_interactions(conn):
    print("  Seeding INTERACTS_WITH (Drug ↔ Drug) …")
    edges = [
        # drug1, drug2, type, severity, mechanism, clinical_effect
        ("DR005","DR004","pharmacodynamic","dangerous","additive anticoagulation",
         "Increased risk of major bleeding; avoid concurrent use"),
        ("DR005","DR013","pharmacodynamic","dangerous","additive anticoagulation",
         "Ibuprofen potentiates warfarin anticoagulation causing severe bleeding"),
        ("DR005","DR018","pharmacokinetic","major","CYP2C9 inhibition by azithromycin",
         "Azithromycin elevates warfarin levels; monitor INR closely"),
        ("DR004","DR013","pharmacodynamic","moderate","COX-1 competition",
         "Ibuprofen blunts aspirin's irreversible platelet inhibition"),
        ("DR002","DR017","pharmacodynamic","moderate","additive hyperkalemia",
         "Combined ACE inhibitor + spironolactone increases K+ risk"),
        ("DR006","DR009","pharmacokinetic","minor","CYP2D6 / P-gp",
         "Omeprazole may slightly increase metoprolol exposure"),
        ("DR012","DR004","pharmacodynamic","major","additive anticoagulation",
         "Concurrent rivaroxaban + aspirin significantly increases bleeding"),
        ("DR012","DR013","pharmacodynamic","major","additive anticoagulation",
         "NSAIDs increase bleeding risk with rivaroxaban"),
        ("DR003","DR009","pharmacokinetic","minor","CYP3A4 competition",
         "PPIs have minimal effect on atorvastatin exposure"),
        ("DR019","DR020","pharmacodynamic","moderate","competing ER pathway",
         "Monitor cardiac function when combining cytotoxics with hormonal therapy"),
        ("DR001","DR007","pharmacodynamic","moderate","volume depletion",
         "Loop diuretics increase lactic acidosis risk with metformin in dehydration"),
        ("DR018","DR006","pharmacokinetic","minor","QTc monitoring",
         "Both can prolong QTc; use with caution in arrhythmia"),
    ]
    for d1, d2, itype, sev, mech, effect in edges:
        ue(conn, "Drug", d1, "INTERACTS_WITH", "Drug", d2, {
            "interaction_type": itype, "severity": sev,
            "mechanism": mech, "clinical_effect": effect,
        })
    print(f"    {len(edges)} edges.")


def seed_side_effect_edges(conn):
    print("  Seeding CAUSES_SIDE_EFFECT (Drug → SideEffect) …")
    edges = [
        # drug, side_effect, probability, dose_dependent
        ("DR001","SE002",0.20,True),("DR001","SE017",0.00003,True),
        ("DR002","SE003",0.15,False),("DR002","SE018",0.001,False),("DR002","SE004",0.05,True),
        ("DR003","SE005",0.001,True),("DR003","SE020",0.05,True),("DR003","SE010",0.001,True),
        ("DR004","SE006",0.02,True),("DR004","SE007",0.03,True),("DR004","SE002",0.10,True),
        ("DR005","SE006",0.08,True),("DR005","SE012",0.005,False),
        ("DR006","SE014",0.15,True),("DR006","SE016",0.10,True),
        ("DR007","SE004",0.05,True),("DR007","SE007",0.03,True),
        ("DR008","SE013",0.10,True),("DR008","SE015",0.05,True),
        ("DR009","SE015",0.05,True),("DR009","SE016",0.05,False),
        ("DR010","SE016",0.08,False),("DR010","SE015",0.05,False),
        ("DR011","SE001",0.15,True),
        ("DR012","SE006",0.07,True),("DR012","SE002",0.08,True),
        ("DR013","SE002",0.15,True),("DR013","SE007",0.04,True),("DR013","SE006",0.02,True),
        ("DR014","SE002",0.20,True),("DR014","SE016",0.10,False),
        ("DR015","SE006",0.04,True),("DR015","SE002",0.08,True),
        ("DR016","SE003",0.15,False),("DR016","SE004",0.05,True),("DR016","SE018",0.001,False),
        ("DR017","SE004",0.07,True),("DR017","SE002",0.10,True),
        ("DR018","SE002",0.15,True),("DR018","SE009",0.001,False),
        ("DR019","SE011",0.05,True),("DR019","SE012",0.10,True),("DR019","SE002",0.60,True),
        ("DR020","SE019",0.40,False),("DR020","SE006",0.01,False),
    ]
    for drug, se, prob, dd in edges:
        ue(conn, "Drug", drug, "CAUSES_SIDE_EFFECT", "SideEffect", se, {
            "probability": prob, "dose_dependent": dd,
        })
    print(f"    {len(edges)} edges.")


def seed_contraindication_edges(conn):
    print("  Seeding CONTRAINDICATED_IN (Drug → Disease) …")
    edges = [
        ("DR001","D005","absolute","eGFR < 30 mL/min: lactic acidosis risk"),
        ("DR001","D004","relative","decompensated HF causes tissue hypoxia → lactic acidosis risk"),
        ("DR002","D016","relative","ACE inhibitors may worsen angioedema; avoid in breast cancer with oedema"),
        ("DR003","D019","absolute","Active liver disease or unexplained elevated transaminases"),
        ("DR004","D019","relative","NSAID effect on platelet function worsens cirrhotic bleeding"),
        ("DR005","D019","relative","Warfarin erratic in liver disease; use LMWH instead"),
        ("DR013","D005","relative","NSAIDs worsen renal perfusion; avoid in CKD stages 3-5"),
        ("DR013","D004","relative","NSAID fluid retention worsens heart failure"),
        ("DR013","D002","relative","NSAIDs antagonise antihypertensive effect and cause Na+ retention"),
        ("DR012","D019","relative","Rivaroxaban impaired elimination in severe liver disease"),
        ("DR003","D016","relative","Statins may theoretically increase statin-drug interactions with tamoxifen"),
        ("DR017","D005","relative","Spironolactone accumulates in severe renal impairment → hyperkalaemia"),
        ("DR006","D007","relative","Beta blockers can precipitate bronchospasm in reactive airway disease"),
        ("DR006","D006","relative","Non-selective beta blockers worsen airflow obstruction in COPD"),
    ]
    for drug, disease, sev, reason in edges:
        ue(conn, "Drug", drug, "CONTRAINDICATED_IN", "Disease", disease, {
            "severity": sev, "reason": reason,
        })
    print(f"    {len(edges)} edges.")


def seed_drug_class_edges(conn):
    print("  Seeding BELONGS_TO_CLASS (Drug → DrugClass) …")
    edges = [
        ("DR001","DC006",True),("DR002","DC002",True),("DR003","DC004",True),
        ("DR004","DC001",False),("DR004","DC011",False),
        ("DR005","DC005",True),("DR006","DC003",True),
        ("DR007","DC007",True),("DR008","DC008",True),("DR009","DC009",True),
        ("DR010","DC010",True),("DR011","DC006",False),
        ("DR012","DC012",True),("DR013","DC001",False),
        ("DR014","DC013",True),("DR015","DC011",True),
        ("DR016","DC002",False),("DR017","DC005",False),
        ("DR018","DC005",False),("DR019","DC014",True),("DR020","DC015",True),
    ]
    for drug, cls, proto in edges:
        ue(conn, "Drug", drug, "BELONGS_TO_CLASS", "DrugClass", cls,
           {"is_prototype": proto})
    print(f"    {len(edges)} edges.")


def seed_gene_disease_edges(conn):
    print("  Seeding ASSOCIATED_WITH (Gene → Disease) …")
    edges = [
        # gene, disease, strength, type, variant
        ("G001","D002",0.75,"risk","ACE I/D polymorphism"),
        ("G002","D010",0.80,"causative","PCSK9 gain-of-function"),
        ("G002","D003",0.72,"risk","PCSK9 loss-of-function protective"),
        ("G005","D016",0.90,"causative","BRCA1 pathogenic variant"),
        ("G006","D008",0.85,"risk","APOE ε4 allele"),
        ("G006","D003",0.70,"risk","APOE ε4 increases CVD risk"),
        ("G007","D001",0.85,"risk","TCF7L2 rs7903146 T allele"),
        ("G007","D012",0.40,"risk","modest T1DM association"),
        ("G008","D009",0.65,"risk","F2 G20210A variant"),
        ("G009","D009",0.70,"pharmacogenomic","VKORC1 -1639G>A affects warfarin dose"),
        ("G010","D016",0.88,"causative","HER2 amplification/overexpression"),
        ("G011","D017",0.80,"risk","TP53 mutation in 50% of lung cancers"),
        ("G011","D016",0.75,"risk","TP53 mutations in triple-negative breast cancer"),
        ("G012","D004",0.60,"risk","VEGF polymorphisms in HF angiogenesis"),
        ("G001","D003",0.60,"risk","ACE DD genotype increases CAD risk"),
    ]
    for gene, disease, strength, atype, variant in edges:
        ue(conn, "Gene", gene, "ASSOCIATED_WITH", "Disease", disease, {
            "evidence_strength": strength, "association_type": atype, "variant": variant,
        })
    print(f"    {len(edges)} edges.")


def seed_gene_drug_edges(conn):
    print("  Seeding TARGETS_GENE and METABOLIZED_BY (Drug → Gene) …")
    targets = [
        ("DR002","G001","inhibitor",0.90),
        ("DR003","G002","inhibitor",0.85),
        ("DR005","G009","substrate",0.95),
        ("DR005","G008","inhibitor",0.80),
        ("DR006","G003","substrate",0.80),
        ("DR014","G006","modulator",0.60),
        ("DR020","G010","antagonist",0.88),
        ("DR019","G011","modulator",0.70),
        ("DR015","G003","substrate",0.75),
    ]
    for drug, gene, mech, aff in targets:
        ue(conn, "Drug", drug, "TARGETS_GENE", "Gene", gene, {
            "mechanism": mech, "binding_affinity": aff,
        })

    metabolised = [
        # drug, gene (CYP), type, impact
        ("DR003","G004","substrate","none"),
        ("DR005","G003","substrate","reduced"),  # CYP2D6 poor metabolisers: warfarin toxicity
        ("DR005","G004","substrate","none"),
        ("DR006","G003","substrate","increased"),  # CYP2D6 PM → higher metoprolol exposure
        ("DR008","G004","substrate","none"),
        ("DR013","G004","substrate","none"),
        ("DR014","G003","substrate","reduced"),
        ("DR015","G003","substrate","reduced"),   # CYP2D6 PM → clopidogrel prodrug not activated
        ("DR019","G004","substrate","reduced"),
        ("DR020","G003","substrate","reduced"),
    ]
    for drug, gene, mtype, impact in metabolised:
        ue(conn, "Drug", drug, "METABOLIZED_BY", "Gene", gene, {
            "metabolism_type": mtype, "impact_on_efficacy": impact,
        })
    print(f"    {len(targets)+len(metabolised)} edges.")


def seed_gene_pathway_edges(conn):
    print("  Seeding INVOLVED_IN (Gene → Pathway) …")
    edges = [
        ("G001","PW001","catalyst"),("G002","PW002","regulator"),
        ("G007","PW004","regulator"),("G008","PW005","catalyst"),
        ("G009","PW005","substrate"),("G010","PW009","catalyst"),
        ("G011","PW008","regulator"),("G012","PW010","catalyst"),
        ("G006","PW001","regulator"),
    ]
    for gene, pw, role in edges:
        ue(conn, "Gene", gene, "INVOLVED_IN", "Pathway", pw, {"role": role})

    print("  Seeding DISRUPTS_PATHWAY (Disease → Pathway) …")
    d_edges = [
        ("D001","PW004","downregulation"),("D001","PW007","upregulation"),
        ("D002","PW001","upregulation"),("D003","PW001","upregulation"),
        ("D003","PW002","upregulation"),("D004","PW001","upregulation"),
        ("D010","PW002","upregulation"),("D008","PW008","downregulation"),
        ("D016","PW009","upregulation"),("D017","PW008","mutation"),
        ("D009","PW005","upregulation"),
    ]
    for dis, pw, dtype in d_edges:
        ue(conn, "Disease", dis, "DISRUPTS_PATHWAY", "Pathway", pw,
           {"disruption_type": dtype})
    print(f"    {len(edges)+len(d_edges)} edges.")


def seed_biomarker_edges(conn):
    print("  Seeding biomarker edges …")
    # DIAGNOSED_BY (Disease → MedicalTest)
    diag = [
        ("D001","MT003",True,0.92,0.95),("D001","MT010",True,0.85,0.90),
        ("D002","MT009",False,0.75,0.80),
        ("D003","MT004",True,0.95,0.98),("D003","MT002",False,0.80,0.85),("D003","MT009",False,0.70,0.75),
        ("D004","MT002",True,0.88,0.92),("D004","MT009",False,0.80,0.82),
        ("D005","MT011",False,0.75,0.85),("D005","MT001",False,0.70,0.75),
        ("D006","MT007",True,0.92,0.95),("D006","MT006",False,0.75,0.85),("D006","MT015",False,0.82,0.88),
        ("D007","MT007",True,0.88,0.92),
        ("D008","MT005",True,0.85,0.90),
        ("D009","MT009",True,0.95,0.98),
        ("D010","MT013",True,0.98,0.99),
        ("D011","MT014",True,0.98,0.95),("D011","MT009",False,0.80,0.90),
        ("D012","MT003",True,0.95,0.97),("D012","MT010",False,0.88,0.90),
        ("D016","MT006",False,0.70,0.75),
        ("D017","MT015",True,0.85,0.90),("D017","MT007",False,0.70,0.80),
        ("D018","MT005",True,0.92,0.95),
        ("D019","MT008",True,0.90,0.95),
    ]
    for dis, test, gold, sens, spec in diag:
        ue(conn, "Disease", dis, "DIAGNOSED_BY", "MedicalTest", test, {
            "is_gold_standard": gold, "sensitivity": sens, "specificity": spec,
        })

    # MONITORED_VIA (Disease → Biomarker)
    mon = [
        ("D001","BM001","every 3 months",7.0),
        ("D001","BM013","daily",180.0),
        ("D002","BM010","weekly",180.0),
        ("D003","BM002","every 3 months",190.0),
        ("D004","BM011","every 3 months",900.0),
        ("D004","BM010","weekly",140.0),
        ("D005","BM009","every 3 months",30.0),
        ("D005","BM005","every 3 months",2.0),
        ("D009","BM003","every 4 weeks",3.5),
        ("D010","BM002","every 6 months",130.0),
        ("D010","BM014","every 6 months",240.0),
        ("D019","BM012","monthly",80.0),
    ]
    for dis, bm, freq, thresh in mon:
        ue(conn, "Disease", dis, "MONITORED_VIA", "Biomarker", bm, {
            "monitoring_frequency": freq, "critical_threshold": thresh,
        })

    # ELEVATES_BIOMARKER (Disease → Biomarker)
    elev = [
        ("D001","BM001","up"),("D001","BM013","up"),
        ("D002","BM010","up"),
        ("D003","BM002","up"),("D003","BM008","up"),
        ("D004","BM011","up"),
        ("D005","BM005","up"),("D005","BM010","up"),
        ("D010","BM002","up"),("D010","BM014","up"),
        ("D011","BM004","up"),
        ("D013","BM012","up"),
        ("D019","BM012","up"),
        ("D020","BM005","up"),("D020","BM009","down"),
    ]
    for dis, bm, direction in elev:
        ue(conn, "Disease", dis, "ELEVATES_BIOMARKER", "Biomarker", bm, {
            "elevation_factor": 2.0 if direction == "up" else 0.5,
            "directionality": direction,
        })

    # REQUIRES_MONITORING (Drug → Biomarker)
    drug_mon = [
        ("DR001","BM001",90,"HbA1c every 3 months to assess glycemic control"),
        ("DR001","BM009",90,"Monitor eGFR — stop if eGFR < 30"),
        ("DR003","BM002",180,"LDL every 6 months"),
        ("DR003","BM012",30,"ALT at baseline and if symptoms"),
        ("DR005","BM003",28,"INR every 4 weeks for warfarin dose titration"),
        ("DR007","BM005",30,"Creatinine and electrolytes monthly"),
        ("DR007","BM009",30,"eGFR monthly in at-risk patients"),
        ("DR002","BM005",30,"Creatinine and K+ at baseline and 1 month"),
        ("DR002","BM009",30,"eGFR monitor for ACE inhibitor"),
        ("DR017","BM005",30,"Creatinine / K+ monthly — hyperkalemia risk"),
        ("DR019","BM004",90,"Cardiac troponin for cardiotoxicity monitoring"),
    ]
    for drug, bm, interval, reason in drug_mon:
        ue(conn, "Drug", drug, "REQUIRES_MONITORING", "Biomarker", bm, {
            "monitoring_interval_days": interval, "reason": reason,
        })

    print(f"    {len(diag)+len(mon)+len(elev)+len(drug_mon)} edges.")


def seed_risk_factor_edges(conn):
    print("  Seeding INCREASES_RISK (RiskFactor → Disease) …")
    edges = [
        # risk, disease, relative_risk, evidence, dose_response
        ("RF001","D017",15.0,"A",True),
        ("RF001","D006",5.0,"A",True),
        ("RF001","D003",2.5,"A",True),
        ("RF001","D016",2.0,"A",True),
        ("RF002","D001",3.0,"A",True),
        ("RF002","D002",2.5,"A",True),
        ("RF002","D003",2.2,"A",True),
        ("RF002","D010",2.8,"A",True),
        ("RF002","D013",3.5,"A",True),
        ("RF003","D001",2.0,"B",True),
        ("RF003","D003",1.8,"B",False),
        ("RF004","D002",2.0,"A",True),
        ("RF005","D003",2.5,"A",False),
        ("RF005","D011",3.0,"A",False),
        ("RF006","D008",4.0,"A",False),
        ("RF006","D003",2.0,"A",False),
        ("RF007","D003",2.5,"A",False),
        ("RF007","D018",2.0,"A",False),
        ("RF008","D018",3.0,"A",False),
        ("RF008","D004",2.5,"A",False),
        ("RF009","D019",7.0,"A",True),
        ("RF009","D013",3.5,"A",True),
        ("RF010","D006",2.0,"B",True),
        ("RF010","D017",1.5,"B",True),
        ("RF011","D003",3.5,"A",True),
        ("RF011","D018",2.5,"A",False),
        ("RF012","D016",5.0,"A",False),
        ("RF013","D003",1.8,"B",True),
        ("RF014","D003",3.0,"A",False),
        ("RF015","D003",1.8,"B",False),
    ]
    for rf, dis, rr, ev, dr in edges:
        ue(conn, "RiskFactor", rf, "INCREASES_RISK", "Disease", dis, {
            "relative_risk": rr, "evidence_level": ev, "dose_response": dr,
        })
    print(f"    {len(edges)} edges.")


def seed_procedure_edges(conn):
    print("  Seeding TREATED_BY_PROCEDURE (Disease → Procedure) …")
    edges = [
        ("D003","PR001",0.92,"A"),
        ("D003","PR002",0.88,"A"),
        ("D005","PR003",0.85,"A"),
        ("D001","PR004",0.80,"A"),
        ("D012","PR004",0.90,"A"),
        ("D006","PR005",0.70,"A"),
        ("D016","PR006",0.65,"A"),
        ("D017","PR006",0.55,"A"),
        ("D009","PR008",0.78,"A"),
        ("D011","PR002",0.90,"A"),
    ]
    for dis, proc, rate, ev in edges:
        ue(conn, "Disease", dis, "TREATED_BY_PROCEDURE", "Procedure", proc, {
            "success_rate": rate, "evidence_level": ev,
        })
    print(f"    {len(edges)} edges.")


def seed_patient_edges(conn):
    print("  Seeding patient edges …")

    # DIAGNOSED_WITH
    from datetime import datetime
    d = lambda s: datetime.strptime(s, "%Y-%m-%d")

    diag = [
        # patient, disease, date, status, confirmed_by
        ("P001","D002",d("2018-03-15"),"chronic","GP"),
        ("P001","D003",d("2020-07-22"),"active","Cardiologist"),
        ("P002","D001",d("2016-11-10"),"chronic","Endocrinologist"),
        ("P002","D010",d("2019-04-01"),"active","GP"),
        ("P003","D009",d("2017-08-30"),"active","Cardiologist"),
        ("P003","D004",d("2021-01-12"),"active","Cardiologist"),
        ("P003","D002",d("2015-05-20"),"chronic","GP"),
        ("P004","D007",d("2010-02-14"),"chronic","Pulmonologist"),
        ("P004","D014",d("2022-09-01"),"active","GP"),
        ("P005","D001",d("2014-06-01"),"chronic","Endocrinologist"),
        ("P005","D002",d("2015-03-10"),"chronic","GP"),
        ("P005","D005",d("2023-01-20"),"active","Nephrologist"),
    ]
    for pid, did, date, status, conf in diag:
        ue(conn, "Patient", pid, "DIAGNOSED_WITH", "Disease", did, {
            "diagnosis_date": date, "status": status, "confirmed_by": conf,
        })

    # TAKES_DRUG
    today = datetime(2026, 1, 1)
    meds = [
        ("P001","DR002",today,"10mg once daily","once_daily","D002"),
        ("P001","DR004",today,"75mg once daily","once_daily","D003"),
        ("P001","DR006",today,"50mg once daily","once_daily","D002"),
        ("P002","DR001",today,"500mg twice daily","twice_daily","D001"),
        ("P002","DR003",today,"20mg once daily","once_daily","D010"),
        ("P003","DR005",today,"5mg once daily","once_daily","D009"),
        ("P003","DR007",today,"40mg once daily","once_daily","D004"),
        ("P003","DR002",today,"5mg once daily","once_daily","D004"),
        ("P004","DR010",today,"2 puffs PRN","PRN","D007"),
        ("P004","DR013",today,"400mg three times daily","three_daily","D014"),
        ("P005","DR001",today,"1000mg twice daily","twice_daily","D001"),
        ("P005","DR008",today,"5mg once daily","once_daily","D002"),
    ]
    for pid, did, sdate, dosage, freq, reason in meds:
        ue(conn, "Patient", pid, "TAKES_DRUG", "Drug", did, {
            "dosage": dosage, "frequency": freq,
            "start_date": sdate, "prescribed_for": reason,
        })

    # HAS_RISK_FACTOR
    rfactors = [
        ("P001","RF005","high"),("P001","RF001","moderate"),("P001","RF011","moderate"),
        ("P002","RF002","high"),("P002","RF003","moderate"),
        ("P003","RF001","moderate"),("P003","RF006","high"),("P003","RF011","high"),
        ("P004","RF010","low"),
        ("P005","RF007","high"),("P005","RF008","high"),("P005","RF014","moderate"),
    ]
    for pid, rid, sev in rfactors:
        ue(conn, "Patient", pid, "HAS_RISK_FACTOR", "RiskFactor", rid, {
            "severity_level": sev, "since_date": today,
        })

    # ALLERGIC_TO
    allergies = [
        ("P001","DR013","anaphylaxis","severe",True),   # John allergic to ibuprofen — dangerous when prescribed
        ("P003","DR016","rash","mild",True),             # Robert allergic to ramipril
        ("P004","DR004","GI","moderate",False),           # Sarah GI intolerant to aspirin
    ]
    for pid, did, rtype, sev, verified in allergies:
        ue(conn, "Patient", pid, "ALLERGIC_TO", "Drug", did, {
            "reaction_type": rtype, "severity": sev, "verified": verified,
        })

    # HAS_VARIANT (pharmacogenomics)
    variants = [
        ("P001","G003","CYP2D6*2/*4","poor_metabolizer",True),   # Poor metoprolol/clopidogrel metaboliser
        ("P002","G009","VKORC1 -1639A/A","increased_sensitivity",True),
        ("P003","G004","CYP3A4*22","slow_metabolizer",True),     # Slow statin/warfarin metabolism
        ("P005","G007","TCF7L2 rs7903146 T/T","high_risk",True),
    ]
    for pid, gid, geno, pheno, ver in variants:
        ue(conn, "Patient", pid, "HAS_VARIANT", "Gene", gid, {
            "genotype": geno, "phenotype": pheno, "verified": ver,
        })

    print(f"    Patient edges seeded.")


# ════════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════════

def main():
    conn = connect()

    print("\n[1/4] Seeding vertex data …")
    seed_body_systems(conn)
    seed_drug_classes(conn)
    seed_pathways(conn)
    seed_genes(conn)
    seed_biomarkers(conn)
    seed_risk_factors(conn)
    seed_medical_tests(conn)
    seed_procedures(conn)
    seed_symptoms(conn)
    seed_side_effects(conn)
    seed_diseases(conn)
    seed_drugs(conn)
    seed_patients(conn)

    print("\n[2/4] Seeding structural edges …")
    seed_symptom_body_system_edges(conn)
    seed_disease_system_edges(conn)
    seed_has_symptom_edges(conn)
    seed_symptom_overlap_edges(conn)

    print("\n[3/4] Seeding clinical knowledge edges …")
    seed_comorbid_edges(conn)
    seed_progression_edges(conn)
    seed_treats_edges(conn)
    seed_drug_interactions(conn)
    seed_side_effect_edges(conn)
    seed_contraindication_edges(conn)
    seed_drug_class_edges(conn)
    seed_gene_disease_edges(conn)
    seed_gene_drug_edges(conn)
    seed_gene_pathway_edges(conn)
    seed_biomarker_edges(conn)
    seed_risk_factor_edges(conn)
    seed_procedure_edges(conn)

    print("\n[4/4] Seeding patient clinical records …")
    seed_patient_edges(conn)

    print("\n✓ Seed data complete.")
    print("  Run the setup.py script to install queries, then test the API.")


if __name__ == "__main__":
    main()
