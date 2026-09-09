import os
import base64
import re
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Load knowledge base
with open("knowledge_base.txt", "r", encoding="utf-8") as file:
    knowledge_base = file.read()


# -----------------------------------
# RAG: Retrieve relevant guidance
# -----------------------------------
def retrieve_guidance(user_text):
    sections = knowledge_base.split("\n\n")
    keywords = user_text.lower().split()

    relevant_sections = []

    for section in sections:
        section_lower = section.lower()
        score = 0

        for keyword in keywords:
            if len(keyword) > 3 and keyword in section_lower:
                score += 1

        if score > 0:
            relevant_sections.append((score, section))

    relevant_sections.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    top_sections = relevant_sections[:3]

    if top_sections:
        return "\n\n".join(
            section for score, section in top_sections
        )

    return (
        "No directly relevant guidance was retrieved. "
        "Use general responsible e-waste principles only."
    )


# -----------------------------------
# Safety detection
# -----------------------------------
def detect_safety_risk(condition):
    condition_lower = condition.lower()

    danger_words = [
        "swollen",
        "swelling",
        "leaking",
        "leakage",
        "overheating",
        "overheated",
        "burning",
        "smoke",
        "fire",
        "ruptured",
        "damaged battery",
        "bulging battery"
    ]

    for word in danger_words:
        if word in condition_lower:
            return True

    return False


# -----------------------------------
# Extract recommended pathway
# -----------------------------------
def extract_pathway(result):
    result_lower = result.lower()

    # Normalize spacing around "/" so that:
    # Donate/Refurbish
    # Donate / Refurbish
    # Donate/ Refurbish
    # Donate /Refurbish
    # are treated the same.
    normalized_result = re.sub(
        r"\s*/\s*",
        "/",
        result_lower
    )

    # Look specifically near "Recommended Pathway"
    match = re.search(
        r"recommended pathway\s*:?\s*(.{0,150})",
        normalized_result
    )

    if match:
        recommended_text = match.group(1)

        if "responsible disposal" in recommended_text:
            return "Responsible Disposal"

        if "donate/refurbish" in recommended_text:
            return "Donate/Refurbish"

        if "donate or refurbish" in recommended_text:
            return "Donate/Refurbish"

        if "recycle" in recommended_text:
            return "Recycle"

        if "reuse" in recommended_text:
            return "Reuse"

        if "repair" in recommended_text:
            return "Repair"

    # Fallback checks
    if "responsible disposal" in normalized_result:
        return "Responsible Disposal"

    if "donate/refurbish" in normalized_result:
        return "Donate/Refurbish"

    if "donate or refurbish" in normalized_result:
        return "Donate/Refurbish"

    if "recycle" in normalized_result:
        return "Recycle"

    if "reuse" in normalized_result:
        return "Reuse"

    if "repair" in normalized_result:
        return "Repair"

    return "Unknown"


# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="E-Waste Assistant",
    page_icon="♻️",
    layout="centered"
)

st.title("♻️ E-Waste Assistant")

st.write(
    "Get an AI-powered recommendation for what to do "
    "with your electronic device."
)


# -----------------------------------
# Device information
# -----------------------------------
device = st.selectbox(
    "What type of device is it?",
    [
        "Phone",
        "Laptop",
        "Tablet",
        "TV",
        "Battery",
        "Headphones",
        "Smartwatch",
        "Other"
    ]
)

age = st.number_input(
    "How old is the device? (years)",
    min_value=0,
    max_value=30,
    value=2
)

working = st.selectbox(
    "Is the device working?",
    [
        "Yes",
        "Partially",
        "No"
    ]
)

condition = st.text_area(
    "What is the condition/problem?",
    placeholder=(
        "Example: Battery drains quickly and "
        "the screen has a small crack."
    )
)


# -----------------------------------
# Image upload
# -----------------------------------
st.subheader("🖼️ Device Image")

uploaded_image = st.file_uploader(
    "Upload a photo of the device (optional)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:
    st.image(
        uploaded_image,
        caption="Uploaded Device Image",
        use_container_width=True
    )


# -----------------------------------
# Analyze Device
# -----------------------------------
if st.button("🔍 Analyze Device"):

    if not condition.strip():

        st.warning(
            "Please describe the device condition."
        )

    else:

        # -----------------------------------
        # Safety check BEFORE AI
        # -----------------------------------
        safety_risk = detect_safety_risk(condition)

        # -----------------------------------
        # RAG retrieval
        # -----------------------------------
        user_text = f"""
        Device: {device}
        Age: {age} years
        Working status: {working}
        Condition: {condition}
        """

        retrieved_guidance = retrieve_guidance(
            user_text
        )


        # -----------------------------------
        # AI prompt
        # -----------------------------------
        prompt = f"""
You are an AI-powered E-Waste Sustainability Assistant.

Your task is to recommend the most appropriate
and sustainable pathway for the user's electronic device.

USER INFORMATION
----------------
Device type: {device}
Age: {age} years
Working status: {working}
Condition/problem: {condition}

RETRIEVED TRUSTED GUIDANCE
--------------------------
{retrieved_guidance}

Choose ONE primary pathway:

1. Repair
2. Reuse
3. Donate/Refurbish
4. Recycle
5. Responsible Disposal

Provide:

Recommended Pathway:
State exactly ONE pathway.

Why This Pathway:
Explain why it is suitable based on the user's
information and retrieved guidance.

Alternative Pathway:
Give one reasonable alternative.

Practical Next Steps:
Give 2-4 safe, high-level actions.

Safety Warning:
Mention relevant safety concerns.

Sustainability Benefit:
Explain how the recommendation supports sustainable
consumption and reduces e-waste.

IMPORTANT SAFETY RULES:

- Do NOT provide step-by-step DIY repair instructions.
- Do NOT tell the user how to open, dismantle, modify,
  or repair a device.
- Recommend qualified or authorized professionals
  for repairs when appropriate.
- Do not recommend putting electronics or batteries
  in normal household waste.
- Do not invent information that the user did not provide.
- Never describe the device as fully functional unless
  the user selected "Yes".
- Never claim a battery is safe merely because swelling
  is not visible in an image.
- Make uncertainty clear when visual evidence is limited.
- If the user's condition mentions a swollen, leaking,
  overheating, burning, smoking, ruptured, or damaged
  battery, DO NOT recommend Repair.
- For a hazardous battery condition, prioritize safety,
  professional handling, and responsible disposal/recycling.
- Keep the response clear and easy to understand.
"""


        # -----------------------------------
        # AI analysis
        # -----------------------------------
        with st.spinner(
            "🤖 Retrieving guidance and analyzing device..."
        ):

            try:

                if uploaded_image is not None:

                    image_bytes = uploaded_image.getvalue()

                    image_base64 = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    mime_type = uploaded_image.type

                    image_data_url = (
                        f"data:{mime_type};base64,{image_base64}"
                    )

                    response = client.chat.completions.create(
                        model="google/gemini-2.5-flash",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": image_data_url
                                        }
                                    }
                                ]
                            }
                        ]
                    )

                    image_used = True

                else:

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    image_used = False


                # -----------------------------------
                # Get AI result
                # -----------------------------------
                result = (
                    response.choices[0]
                    .message.content
                )

                # -----------------------------------
                # SAFETY OVERRIDE
                # -----------------------------------
                if safety_risk:

                    result = f"""
**Recommended Pathway:**
**Responsible Disposal / Professional Handling**

**Why This Pathway:**
The information provided indicates a potentially hazardous
battery condition. Safety takes priority over repair or reuse.

**Alternative Pathway:**
**Responsible Recycling** through an appropriate e-waste
facility that accepts damaged batteries.

**Practical Next Steps:**

1. Stop using the device if it is overheating, leaking,
   smoking, or otherwise unsafe.
2. Do not open, dismantle, puncture, or attempt to repair
   the battery.
3. Contact an authorized service provider or appropriate
   e-waste facility for professional handling.
4. Keep the device away from heat and ignition sources
   while waiting for professional guidance.

**Safety Warning:**
A swollen, leaking, overheating, smoking, or visibly damaged
battery can present a serious safety risk. Do not attempt
DIY handling.

**Sustainability Benefit:**
Professional recycling or responsible handling helps prevent
hazardous materials from entering the environment while
allowing appropriate components and materials to be recovered.
"""


                # -----------------------------------
                # AI Recommendation
                # -----------------------------------
                st.subheader(
                    "🤖 AI Recommendation"
                )

                st.write(result)


                # -----------------------------------
                # Determine actual pathway
                # -----------------------------------
                if safety_risk:

                    actual_pathway = "Responsible Disposal"

                else:

                    actual_pathway = extract_pathway(
                        result
                    )


                # -----------------------------------
                # Sustainability Impact
                # -----------------------------------
                st.subheader(
                    "🌱 Sustainability Impact"
                )

                if actual_pathway == "Repair":

                    st.success(
                        "High positive impact potential: "
                        "repairing the device can extend its "
                        "useful life and delay replacement."
                    )

                elif actual_pathway == "Reuse":

                    st.success(
                        "Positive impact potential: reusing "
                        "the device keeps it in circulation "
                        "and reduces premature disposal."
                    )

                elif actual_pathway == "Donate/Refurbish":

                    st.success(
                        "Positive impact potential: donation "
                        "or refurbishment can extend the "
                        "device's useful life for another user."
                    )

                elif actual_pathway == "Recycle":

                    st.info(
                        "Positive impact potential: responsible "
                        "recycling helps recover useful materials "
                        "and prevents improper disposal."
                    )

                elif actual_pathway == "Responsible Disposal":

                    st.warning(
                        "Safety-first impact: responsible handling "
                        "helps prevent hazardous electronic waste "
                        "from entering normal household waste."
                    )

                else:

                    st.info(
                        "The sustainability impact depends on the "
                        "final pathway selected after assessment."
                    )

                st.caption(
                    "Impact level is a qualitative estimate for "
                    "awareness and is not a scientific "
                    "carbon-footprint calculation."
                )


                # -----------------------------------
                # Retrieved guidance
                # -----------------------------------
                with st.expander(
                    "📚 Retrieved Guidance Used"
                ):

                    st.write(
                        retrieved_guidance
                    )


                # -----------------------------------
                # Image analysis
                # -----------------------------------
                if image_used:

                    st.subheader(
                        "👁️ Visual Analysis"
                    )

                    st.success(
                        "The uploaded device image was analyzed "
                        "by a vision-capable AI model."
                    )

                    st.caption(
                        "Visual analysis provides supporting evidence "
                        "and should not replace professional inspection."
                    )


            except Exception as e:

                st.error(
                    "Something went wrong while analyzing "
                    "the device."
                )

                st.caption(
                    f"Error: {e}"
                )


# -----------------------------------
# Responsible AI
# -----------------------------------
st.divider()

st.subheader("🛡️ Responsible AI")

st.markdown("""
**Safety:** The assistant uses a rule-based safety check before
accepting an AI recommendation for potentially hazardous battery
conditions.

**Transparency:** Recommendations are AI-generated decision support
and are not professional certification.

**Human Oversight:** Users should consult qualified professionals
when technical inspection or safety assessment is required.

**Privacy:** Do not enter personal, confidential, or sensitive
information.

**Fairness & Reliability:** Recommendations depend on the information
provided and may contain errors. Important decisions should be
independently verified.

**Image Limitations:** Image analysis cannot reliably determine hidden
internal damage, battery health, or electrical safety.
""")