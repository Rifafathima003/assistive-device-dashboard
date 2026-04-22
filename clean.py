import pandas as pd

def load_and_clean_data(path= None):
    url="https://docs.google.com/spreadsheets/d/e/2PACX-1vTh9RBFi-hMFzAmCekGFnHjhgn0ZMTZVuqSHYHsV3qanHKbXN29QMPHKBGFDkKS_ioXsrJLU-zvgBSV/pub?gid=139800674&single=true&output=csv"
    # ---------------- LOAD DATA ----------------
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    

# Remove extra description inside brackets
    df.columns = df.columns.str.replace(r"\(.*\)", "", regex=True)

# Remove newlines
    df.columns = df.columns.str.replace("\n", " ")

    df.columns = df.columns.str.strip()

    # ---------------- USE EXISTING SCHOOL CODE ----------------
    df['School ID'] = df['School ID'].astype(str).str.strip().str.upper()
    school_id = "School ID"   
    # Create standard school name using School ID
    df['School Name'] = df['School Name'].astype(str).str.strip().str.title() 
    school_map = df.groupby(school_id)['School Name'].agg(lambda x: x.value_counts().index[0])
    
# Apply standardized name
    df['School_Name'] = df[school_id].map(school_map)

    # ---------------- CLEAN MEASUREMENTS ----------------
    df['Palm Width'] = pd.to_numeric(df['Palm Width'], errors='coerce')
    df['Palm Length'] = pd.to_numeric(df['Palm Length'], errors='coerce')

    # Keep measurements within plausible human-hand ranges while preserving true sub-2 cm widths.
    df['Palm Width Cleaned'] = df['Palm Width'].where(df['Palm Width'].between(1.0, 5.0)).round(2)
    df['Palm Length Cleaned'] = df['Palm Length'].where(df['Palm Length'].between(4.0, 15.0)).round(2)

    #cleaning district names and standardizing them
    df['District'] = df['District'].astype(str).str.strip().str.title()

    #cleaning gender values and standardizing them
    df['Gender'] = df['Gender'].astype(str).str.strip().str.title()
    df['Gender'] = df['Gender'].astype(str).str.strip().str.lower()
    gender_map = {'male': 'Male', 'female': 'Female', 'm' : 'Male', 'f': 'Female','nale':'Male', 'Nale':'Male', 'Femal':'Female','M' :'Male', 'F' :'Female'}
    df['Gender'] = df['Gender'].map(gender_map).fillna('Other')

    
    # ---------------- CLEAN DISABILITY (NOT USED IN DASHBOARD) ----------------
    disability_col = [col for col in df.columns if "primary disability" in col.lower()][0]

    def clean_disability(text):
        text = str(text).strip().lower()

        if "cp" in text or "cerebral" in text:
            return "Cerebral Palsy"
        elif "id" in text or "intellectual" in text or "idd" in text or "ied" in text or "mr" in text or "mental" in text:
            return "Intellectual Disability"
        elif "vision" in text or "visual" in text or "blind" in text:
            return "Visual Impairment"
        elif "hearing" in text or "deaf" in text:       
            return "Hearing Impairment"
        elif "speech" in text or "dumb" in text or "communication" in text:
            return "Speech Impairment"
        elif "learning" in text or "ld" in text:
            return "Learning Disability"
        elif "autism" in text or "asd" in text:
            return "Autism"
        elif "adhd" in text or "attention" in text:
            return "ADHD"
        elif "down syndrome" in text or "ds" in text or "downs" in text or "down's" in text or "down" in text:
            return "Down Syndrome"
        elif "dwarfism" in text or "dwarf" in text:
            return "Dwarfism"   
        elif "seizure" in text or "epilepsy" in text:
            return "Epilepsy"   
        elif "neurological" in text or "glutoria" in text:
            return "Neurological Condition"
        elif "bed ridden" in text or "bedridden" in text:
            return "Bedridden"
        elif "emotionally unstable" in text or "emotional disorder" in text:
            return "Emotional Disorder"
        elif "global development delay" in text or "gdd" in text:
            return "Global Developmental Delay"
        else:
            return "Other"
    
    df["disability_cleaned"] = df[disability_col].apply(clean_disability) 
    
    
    df["disability_cleaned"].value_counts()

    # ---------------- CLEAN DEVICE NAMES ----------------
    
    # ---------------- DEVICE RESHAPING ----------------
    device_cols = ['Device Priority 1', 'Device Priority 2', 'Device Priority 3']

    df_devices = df.melt(
        id_vars=[
            'District',
            'School_Name',
            school_id,
            'Student Name',
            'Gender',
            'Social Category',
            'disability_cleaned',
            'Palm Width Cleaned',
            'Palm Length Cleaned',
        ],
        value_vars=device_cols,
        var_name="Priority",
        value_name='Device'
    )
    df_devices["Priority"] = df_devices["Priority"].str.replace("Device Priority ", "")
    df_devices['Device'] = df_devices['Device'].astype(str).str.strip().str.lower()
    df_devices['Device'] = df_devices['Device'].replace(['nan', 'not applicable', 'none', " "], pd.NA)
    df_devices = df_devices[df_devices['Device'].notna()&(df_devices['Device'] != '')&(df_devices['Device'] != 'nan')&(df_devices['Device'] != 'none')]

    device_map = {
        "wheel chair": "wheelchair",
        "wheel-chair": "wheelchair",
        "hearing aid device": "hearing aid",
        "hearing machine": "hearing aid",
        "walking stick": "walking aid",
        "walker": "walking aid"
    }

    df_devices['Device'] = df_devices['Device'].replace(device_map)

    measurement_based_devices = {
        'utensil holder',
        'palm pen holder',
        'toothbrush holder',
    }
    fixed_measurement_mask = ~df_devices['Device'].isin(measurement_based_devices)
    df_devices.loc[fixed_measurement_mask, ['Palm Width Cleaned', 'Palm Length Cleaned']] = pd.NA

    
    device_category_map = {
    "wheelchair": "Mobility",
    "crutches": "Mobility",
    "walking aid": "Mobility",
    "prosthetic limb": "Mobility",
    "orthotic device": "Mobility",

    "visual aid": "Assistive",
    "button aid": "Assistive",
    "braille": "Assistive",
    "hearing aid": "Assistive",
    "reading bar": "Assistive",
    "palm pen holder": "Assistive",
    "utensil holder": "Assistive",
    "toothbrush holder": "Assistive",
    "adaptive pencil grip": "Assistive",
    "braille kit": "Assistive",

    "communication device": "Cognitive",
    "maze": "Cognitive",
    "tetris": "Cognitive",
    "low profile switch": "Assistive",
    "communication board": "Cognitive",
    "speech device": "Cognitive"
    }

    df_devices['Device Category'] = df_devices['Device'].map(device_category_map)

    # ---------------- SAVE CLEANED FILE ----------------
    try:
        df_devices.to_csv("data/cleaned_data.csv", index=False)
    except PermissionError:
        pass

    return df_devices
# ---------------- RUN FILE ----------------
if __name__ == "__main__":
    df_devices=load_and_clean_data()
    print("✅Cleaned file saved as data/cleaned_data.csv")
    print(df_devices.head())
    print(df_devices['School ID'].unique())
