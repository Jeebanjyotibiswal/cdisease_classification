from flask import Flask, render_template, request, make_response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

symptoms = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering',
    'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting',
    'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain',
    'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness',
    'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever',
    'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache',
    'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm',
    'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion',
    'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements',
    'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness',
    'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels',
    'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties',
    'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech',
    'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
    'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine',
    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
    'belly_pain', 'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes',
    'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum',
    'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
    'history_of_alcohol_consumption', 'blood_in_sputum', 'prominent_veins_on_calf',
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
    'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
    'blister', 'red_sore_around_nose', 'yellow_crust_ooze'
]

disease_data = {
    "Fungal infection": {
        "description": "An infection caused by fungi, affecting skin, nails, or internal organs.",
        "precautions": ["Keep skin dry", "Avoid tight clothing", "Maintain hygiene"],
        "treatment": "Antifungal creams, powders, or oral medication."
    },
    "Hepatitis C": {
        "description": "A viral infection causing liver inflammation.",
        "precautions": ["Avoid sharing needles", "Practice safe sex", "Get tested regularly"],
        "treatment": "Antiviral medications prescribed by a doctor."
    },
    "Hepatitis E": {
        "description": "A waterborne viral liver disease.",
        "precautions": ["Drink clean water", "Maintain hygiene", "Avoid raw meat"],
        "treatment": "Supportive care and hydration."
    },
    "Alcoholic hepatitis": {
        "description": "Liver inflammation caused by excessive alcohol intake.",
        "precautions": ["Avoid alcohol", "Eat a healthy diet", "Regular check-ups"],
        "treatment": "Alcohol cessation, medications, and nutritional support."
    },
    "Tuberculosis": {
        "description": "A serious infectious disease affecting the lungs.",
        "precautions": ["Wear masks", "Cover mouth when coughing", "Avoid close contact"],
        "treatment": "A long-term antibiotic regimen as prescribed."
    },
    "Common Cold": {
        "description": "A mild viral infection of the nose and throat.",
        "precautions": ["Wash hands often", "Avoid close contact", "Boost immunity"],
        "treatment": "Rest, fluids, and over-the-counter medications."
    },
    "Pneumonia": {
        "description": "Lung infection causing inflammation in the air sacs.",
        "precautions": ["Get vaccinated", "Practice good hygiene", "Avoid smoking"],
        "treatment": "Antibiotics or antivirals, hospitalization if severe."
    },
    "Dimorphic hemmorhoids(piles)": {
        "description": "Swollen veins in the lower rectum and anus.",
        "precautions": ["Eat high-fiber diet", "Drink plenty of water", "Avoid straining"],
        "treatment": "Topical treatments, lifestyle changes, or surgery."
    },
    "Heart attack": {
        "description": "Blockage of blood flow to the heart muscle.",
        "precautions": ["Quit smoking", "Control blood pressure", "Exercise regularly"],
        "treatment": "Emergency care, medications, and possibly surgery."
    },
    "Varicose veins": {
        "description": "Swollen, twisted veins often in the legs.",
        "precautions": ["Avoid standing long hours", "Exercise regularly", "Elevate legs"],
        "treatment": "Compression stockings, sclerotherapy, or surgery."
    },
    "Hypothyroidism": {
        "description": "Thyroid hormone deficiency.",
        "precautions": ["Regular thyroid checkups", "Healthy balanced diet", "Avoid stress"],
        "treatment": "Thyroid hormone replacement therapy."
    },
    "Hyperthyroidism": {
        "description": "Excess thyroid hormone production.",
        "precautions": ["Regular monitoring", "Avoid iodine-rich food", "Manage stress"],
        "treatment": "Antithyroid medications or radioactive iodine."
    },
    "Hypoglycemia": {
        "description": "Low blood sugar levels.",
        "precautions": ["Eat small frequent meals", "Avoid excess alcohol", "Monitor blood sugar"],
        "treatment": "Immediate sugar intake and medical supervision."
    },
    "Osteoarthristis": {
        "description": "Degenerative joint disease causing pain and stiffness.",
        "precautions": ["Maintain healthy weight", "Exercise gently", "Avoid joint stress"],
        "treatment": "Pain relievers, physiotherapy, or joint replacement."
    },
    "Arthritis": {
        "description": "Inflammation of joints causing pain and stiffness.",
        "precautions": ["Exercise moderately", "Eat anti-inflammatory foods", "Avoid injury"],
        "treatment": "Pain management, medications, and physical therapy."
    },
    "(vertigo) Paroymsal Positional Vertigo": {
        "description": "A condition causing brief dizziness spells.",
        "precautions": ["Avoid sudden head movements", "Get up slowly", "Do vestibular exercises"],
        "treatment": "Positional maneuvers, medications if needed."
    },
    "Acne": {
        "description": "A skin condition causing pimples and inflammation.",
        "precautions": ["Clean face regularly", "Avoid oily products", "Use non-comedogenic makeup"],
        "treatment": "Topical creams, antibiotics, or retinoids."
    },
    "Urinary tract infection": {
        "description": "Bacterial infection affecting the urinary tract.",
        "precautions": ["Drink plenty of water", "Wipe front to back", "Avoid holding urine"],
        "treatment": "Antibiotics prescribed by a doctor."
    },
    "Psoriasis": {
        "description": "Chronic autoimmune skin disease causing red, scaly patches.",
        "precautions": ["Keep skin moisturized", "Avoid stress", "Avoid triggers like smoking"],
        "treatment": "Topical treatments, phototherapy, or immunosuppressants."
    },
    "Hepatitis D": {
        "description": "A liver infection that occurs only with hepatitis B.",
        "precautions": ["Avoid sharing needles", "Safe sex practices", "Vaccinate for hepatitis B"],
        "treatment": "Supportive care and antiviral medications."
    },
    "Hepatitis B": {
        "description": "A serious liver infection caused by the hepatitis B virus.",
        "precautions": ["Avoid sharing personal items", "Get vaccinated", "Safe sex practices"],
        "treatment": "Antiviral drugs and regular monitoring."
    },
    "Allergy": {
        "description": "An immune system reaction to foreign substances.",
        "precautions": ["Avoid known allergens", "Carry antihistamines", "Use air purifiers"],
        "treatment": "Antihistamines, decongestants, or epinephrine for severe cases."
    },
    "hepatitis A": {
        "description": "A viral liver infection spread through contaminated food and water.",
        "precautions": ["Drink clean water", "Get vaccinated", "Maintain hygiene"],
        "treatment": "Rest, hydration, and supportive care."
    },
    "GERD": {
        "description": "Gastroesophageal reflux disease causing heartburn.",
        "precautions": ["Avoid spicy food", "Eat small meals", "Elevate head while sleeping"],
        "treatment": "Antacids, lifestyle changes, or surgery."
    },
    "Chronic cholestasis": {
        "description": "Reduction or stoppage of bile flow.",
        "precautions": ["Avoid fatty food", "Regular liver function tests", "Avoid alcohol"],
        "treatment": "Bile acid medications, vitamins, or surgery."
    },
    "Drug Reaction": {
        "description": "An adverse response to medications.",
        "precautions": ["Inform doctor about allergies", "Read medicine labels carefully", "Avoid self-medication"],
        "treatment": "Discontinue drug, antihistamines, or steroids."
    },
    "Peptic ulcer diseae": {
        "description": "Sores that develop on the stomach lining.",
        "precautions": ["Avoid NSAIDs", "Limit spicy foods", "Manage stress"],
        "treatment": "Antibiotics, antacids, and lifestyle changes."
    },
    "AIDS": {
        "description": "A chronic, potentially life-threatening condition caused by HIV.",
        "precautions": ["Practice safe sex", "Avoid sharing needles", "Regular HIV tests"],
        "treatment": "Antiretroviral therapy (ART)."
    },
    "Diabetes": {
        "description": "A disease causing high blood sugar levels.",
        "precautions": ["Monitor sugar regularly", "Exercise daily", "Eat balanced diet"],
        "treatment": "Insulin therapy and oral medications."
    },
    "Gastroenteritis": {
        "description": "An intestinal infection marked by diarrhea, cramps, and vomiting.",
        "precautions": ["Drink clean water", "Wash hands often", "Avoid street food"],
        "treatment": "Rehydration and antibiotics if necessary."
    },
    "Bronchial Asthma": {
        "description": "A respiratory condition marked by spasms in the bronchi.",
        "precautions": ["Avoid triggers", "Use inhaler as prescribed", "Keep environment clean"],
        "treatment": "Bronchodilators and corticosteroids."
    },
    "Hypertension": {
        "description": "High blood pressure.",
        "precautions": ["Reduce salt intake", "Exercise daily", "Avoid stress"],
        "treatment": "Antihypertensive medications and lifestyle modifications."
    },
    "Migraine": {
        "description": "A severe, throbbing headache usually on one side of the head.",
        "precautions": ["Avoid loud noise", "Get adequate sleep", "Manage stress"],
        "treatment": "Pain relievers and preventive medications."
    },
    "Cervical spondylosis": {
        "description": "Age-related wear and tear affecting spinal disks in the neck.",
        "precautions": ["Avoid prolonged sitting", "Do neck exercises", "Use ergonomic pillows"],
        "treatment": "Pain relievers, physiotherapy, or surgery."
    },
    "Paralysis (brain hemorrhage)": {
        "description": "Loss of muscle function caused by bleeding in the brain.",
        "precautions": ["Control blood pressure", "Avoid head injuries", "Regular check-ups"],
        "treatment": "Emergency care, physiotherapy, and medications."
    },
    "Jaundice": {
        "description": "Yellowing of skin and eyes due to high bilirubin.",
        "precautions": ["Avoid alcohol", "Maintain liver-friendly diet", "Get regular check-ups"],
        "treatment": "Depends on cause; may involve medications and supportive care."
    },
    "Chicken pox": {
        "description": "A highly contagious viral infection causing itchy rash and blisters.",
        "precautions": ["Isolate infected person", "Avoid scratching", "Maintain hygiene"],
        "treatment": "Antiviral medications and symptom relief."
    },
    "Dengue": {
        "description": "A mosquito-borne viral disease causing high fever.",
        "precautions": ["Use mosquito nets", "Remove stagnant water", "Use repellents"],
        "treatment": "Supportive care and fluids."
    },
    "Typhoid": {
        "description": "A serious bacterial infection.",
        "precautions": ["Wash hands", "Avoid street food", "Drink boiled water"],
        "treatment": "Antibiotics prescribed by doctor."
    },
    "Impetigo": {
        "description": "A highly contagious bacterial skin infection.",
        "precautions": ["Maintain hygiene", "Avoid sharing personal items", "Cover wounds"],
        "treatment": "Antibiotic creams and oral antibiotics."
    }
}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    visible_symptoms = symptoms[:20]
    other_symptoms = symptoms[20:]
    return render_template(
        'predict.html',
        visible_symptoms=visible_symptoms,
        other_symptoms=other_symptoms
    )

@app.route('/result', methods=['POST'])
def result_page():
    selected_symptoms = request.form.getlist('symptoms')
    name = request.form.get('name', '')
    age = request.form.get('age', '')
    blood_group = request.form.get('blood_group', '')
    
    input_vector = [1 if symptom in selected_symptoms else 0 for symptom in symptoms]
    prediction = model.predict([input_vector])[0]

    data = disease_data.get(prediction, {
        "description": "Information not found.",
        "precautions": ["Consult a doctor"],
        "treatment": "Get medical checkup immediately."
    })

    return render_template(
        'result.html',
        disease=prediction,
        description=data['description'],
        precautions=data['precautions'],
        treatment=data['treatment'],
        name=name,
        age=age,
        blood_group=blood_group
    )

@app.route('/download_report', methods=['POST'])
def download_report():
    # Get all data from form
    disease = request.form.get('disease', 'Unknown Disease')
    description = request.form.get('description', 'No description available')
    treatment = request.form.get('treatment', 'Consult your doctor')
    precautions = request.form.getlist('precautions')
    name = request.form.get('name', 'Not provided')
    age = request.form.get('age', 'Not provided')
    blood_group = request.form.get('blood_group', 'Not provided')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1,
        spaceAfter=20,
        textColor='#4e73df'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        spaceAfter=20,
        textColor='#666666'
    )
    
    content = []
    
    # Add title and patient info
    content.append(Paragraph(f"HealthAI Report: {disease}", title_style))
    content.append(Paragraph(f"Report generated on: {current_time}", subtitle_style))
    content.append(Spacer(1, 0.3*inch))
    
    # Patient details section
    content.append(Paragraph("<b>Patient Details</b>", styles['Heading2']))
    content.append(Paragraph(f"<b>Name:</b> {name}", styles['Normal']))
    content.append(Paragraph(f"<b>Age:</b> {age}", styles['Normal']))
    content.append(Paragraph(f"<b>Blood Group:</b> {blood_group}", styles['Normal']))
    content.append(Spacer(1, 0.3*inch))
    
    # Add disease info
    content.append(Paragraph("<b>About the Disease</b>", styles['Heading2']))
    content.append(Paragraph(description, styles['Normal']))
    content.append(Spacer(1, 0.3*inch))
    
    # Add treatment
    content.append(Paragraph("<b>Treatment Options</b>", styles['Heading2']))
    content.append(Paragraph(treatment, styles['Normal']))
    content.append(Spacer(1, 0.3*inch))
    
    # Add precautions
    content.append(Paragraph("<b>Precautions</b>", styles['Heading2']))
    precaution_items = [ListItem(Paragraph(p, styles['Normal'])) for p in precautions]
    content.append(ListFlowable(precaution_items, bulletType='bullet'))
    
    doc.build(content)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=HealthAI_Report_{disease}_{name}.pdf'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)