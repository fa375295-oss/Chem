
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="رحلة الزمن الكيميائية", layout="centered")

# --- Data: Stations (scripted "AI" responses & quiz) ---
STATIONS = [
    {
        "year": "800s (الخيمياء الإسلامية)",
        "scientist": "جابر بن حيان",
        "intro": "أهلاً بك في مختبر الخيميائي! أنا جابر بن حيان، أبحث عن طرق لتحويل المواد وفهم التفاعلات.",
        "talk": [
            "في عصرنا كنا نُجري تجارب على التقطير والتسخين لاستخراج المواد.",
            "الكيمياء كانت قريبة من الفلسفة والطب — كنا نحاول فهم خواص المواد.",
        ],
        "quiz": {
            "question": "ما اسم أداة كان الخيميائيون يستخدمونها لفصل السوائل عبر التسخين والتكثيف؟",
            "answer": "التقطير"
        }
    },
    {
        "year": "1660s",
        "scientist": "روبرت بويل",
        "intro": "أنا روبرت بويل، أحب التجارب والقياس. أُعتبر أحد مؤسسي الكيمياء الحديثة.",
        "talk": [
            "قانون بويل يصف علاقة ضغط الغاز بحجمه عند ثبوت درجة الحرارة.",
            "نؤمن بالتجربة الدقيقة والقياس لتحديد قوانين الطبيعة."
        ],
        "quiz": {
            "question": "ماذا يصف قانون بويل؟ (اختر: أ- علاقة الضغط بالحجم، ب- قانون الحركة، ج- تركيب الذرة)",
            "answer": "أ"
        }
    },
    {
        "year": "1803",
        "scientist": "جون دالتون",
        "intro": "أنا جون دالتون، اقترحت فكرة أن المادة مكونة من ذرات صغيرة.",
        "talk": [
            "فكرة الذرات ساعدت على تفسير نسب التراكيب الكيميائية.",
            "تخيل أن كل عنصر له نوع من الجسيمات الصغيرة (الذرات)."
        ],
        "quiz": {
            "question": "ما الذي اقترحه دالتون عن المادة؟",
            "answer": "الذرات"
        }
    },
    {
        "year": "1869",
        "scientist": "ديميتري مندليف",
        "intro": "أنا مندليف، رتبت العناصر في جدول دوري مبكر يُظهر خواصًا متشابهة.",
        "talk": [
            "ترتيبي سمح بتوقع عناصر لم تُكتشف بعد — تركت فراغات.",
            "الجدول الدوري يُسهل رؤية الأنماط بين العناصر."
        ],
        "quiz": {
            "question": "ما الفائدة من ترك فراغات في الجدول الدوري الذي أنشأته مندليف؟",
            "answer": "توقُع عناصر جديدة"
        }
    },
    {
        "year": "1897",
        "scientist": "ج.ج. طومسون",
        "intro": "أنا طومسون، اكتشفت الإلكترون وأعدت التفكير في بنية الذرة.",
        "talk": [
            "اكتشاف الإلكترون بيّن أن للذرة أجزاء أصغر.",
            "هذا فتح الباب لفيزياء وكيمياء الذرة الحديثة."
        ],
        "quiz": {
            "question": "ما الجزئ الموجود داخل الذرة الذي اكتشفه طومسون؟",
            "answer": "الإلكترون"
        }
    },
    {
        "year": "1903-1911",
        "scientist": "ماري كوري",
        "intro": "أنا ماري كوري، درست النشاط الإشعاعي وفزت بجائزة نوبل.",
        "talk": [
            "عملت على عناصر مشعة مثل الراديوم والبولونيوم.",
            "البحث العلمي يتطلب شجاعة وصبرًا طويلاً."
        ],
        "quiz": {
            "question": "بأي مجال حصلت ماري كوري على جائزة نوبل؟ (اختر: أ- الكيمياء، ب- الأدب، ج- الرياضيات)",
            "answer": "أ"
        }
    }
]

# --- Helpers ---
def reset():
    st.session_state.stage = "intro"
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.history = []

if "stage" not in st.session_state:
    reset()

# --- UI ---
st.title("🕰️ رحلة عبر الزمن مع علماء الكيمياء")
st.write("نشاط تفاعلي لمدرسي وطلاب المدارس — تحدث مع علماء من عصور مختلفة، أجب على تحدياتهم، وتقدّم في الزمن!")

if st.session_state.stage == "intro":
    st.markdown("""
    **طريقة اللعب:**  
    - ستزورون محطات زمنية (عصور مختلفة).  
    - في كل محطة ستقابل عالمًا وتقرأ مقدمة قصيرة.  
    - تحدث مع العالم (اكتب سؤالك أو ردك) أو اختر الإجابة الصحيحة في التحدي.  
    - عند الإجابة الصحيحة تفتح محطة جديدة وتكسب نقاط.
    """)
    col1, col2 = st.columns(2)
    with col1:
        students = st.text_input("أسماء الطلاب (مثال: فاطمة، علي)", key="students")
    with col2:
        mode = st.radio("وضع التشغيل:", ("وضع مُبرمج (بدون إنترنت)", "الوضع الذكي مع OpenAI (اختياري)"), index=0)
    if st.button("ابدأ الرحلة"):
        st.session_state.mode = mode
        st.session_state.stage = "station"
        st.session_state.idx = 0
        st.session_state.score = 0
        st.session_state.history = []
        st.experimental_rerun()

# Station stage
if st.session_state.stage == "station":
    idx = st.session_state.idx
    station = STATIONS[idx]
    st.subheader(f"{station['scientist']} — {station['year']}")
    st.write(station["intro"])
    st.write("**ماذا تعرف عن هذا العالم؟**")
    for t in station["talk"]:
        st.info(t)
    # Simple chat-like interaction (scripted)
    st.write("---")
    st.write("💬 **تحدث مع العالم** (اكتب سؤالًا أو تعليقًا — سيتم الرد بردود مُبرمجة تعليمية)")
    user_msg = st.text_input("اكتب رسالتك هنا:", key=f"user_msg_{idx}")
    if st.button("أرسل المحادثة", key=f"send_{idx}"):
        # generate a simple scripted reply by echoing keywords
        reply = ""
        low = user_msg.lower()
        if any(k in low for k in ["لماذا", "كيف", "ما", "متى", "who", "why", "how"]):
            reply = station["talk"][0]
        else:
            reply = "شكرًا على تعليقك! هل تحب أن تجاوب التحدي الآن لتفتح بوابة الزمن التالية؟"
        st.session_state.history.append({"speaker": "student", "text": user_msg})
        st.session_state.history.append({"speaker": station["scientist"], "text": reply})
        st.experimental_rerun()

    # show chat history for this session
    if st.session_state.history:
        st.write("### سجل المحادثة")
        for item in st.session_state.history[-6:]:
            if item["speaker"] == "student":
                st.write(f"**أنت:** {item['text']}")
            else:
                st.write(f"**{item['speaker']}:** {item['text']}")

    st.write("---")
    st.write("🎯 **التحدي** — أجب على السؤال التالي لتنتقل للمحطة التالية:")
    st.markdown(f"**{station['quiz']['question']}**")
    answer = st.text_input("إجابتك:", key=f"answer_{idx}")
    if st.button("تحقق من الإجابة", key=f"check_{idx}"):
        user_ans = answer.strip()
        correct = station["quiz"]["answer"].strip()
        # Normalize simple Arabic choices
        if user_ans == "":
            st.warning("اكتب إجابة ثم اضغط تحقق.")
        else:
            is_correct = False
            if user_ans == correct:
                is_correct = True
            else:
                # handle simple choice letters
                if user_ans.lower() in ["أ", "ا", "a", "A"] and correct.lower() in ["أ", "ا", "a"]:
                    is_correct = True
                if user_ans.lower() in ["ب", "b"] and correct.lower() in ["ب", "b"]:
                    is_correct = True
            if is_correct:
                st.success("إجابة صحيحة! 🎉 تفتح بوابة الزمن...")
                st.session_state.score += 10
                st.session_state.idx += 1
                if st.session_state.idx >= len(STATIONS):
                    st.session_state.stage = "end"
                st.experimental_rerun()
            else:
                st.error("للأسف، هذه ليست الإجابة الصحيحة. حاول مرة أخرى أو اقرأ حديث العالم أعلاه.")

# End stage
if st.session_state.stage == "end":
    st.balloons()
    st.header("🎉 تهانينا — انتهت الرحلة!")
    st.write(f"الدرجة النهائية: **{st.session_state.score}**")
    st.write("أخبرنا أي محطة أعجبتك أكثر أو اطبع شهادة المشاركة.")
    name = st.text_input("اكتب اسم الطالب/الطلاب لطباعة الشهادة:", key="cert_name")
    if st.button("طباعة شهادة المشاركة"):
        if not name.strip():
            st.warning("اكتب اسمًا لطباعته على الشهادة.")
        else:
            st.markdown(f"""
            ### 🏅 شهادة مشاركة
            نمنح هذه الشهادة إلى **{name}**  
            لمشاركته/ها في **رحلة الزمن الكيميائية** والتعرف على علماء الكيمياء.
            \n> التاريخ: {datetime.now().strftime('%Y-%m-%d')}
            """)
    if st.button("ابدأ من جديد"):
        reset()
        st.experimental_rerun()

# Footer / credits
st.write("---")
st.write("مُصمم بواسطة: نشاط تعليمي تفاعلي — يمكن تعديل الكود ليتصل بواجهة OpenAI API لإجابات حقيقية (انظر README).")
