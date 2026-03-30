import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import tempfile

st.title("📒 오답노트 생성기")

# 세션 저장
if "notes" not in st.session_state:
    st.session_state.notes = []

# ===== 입력 =====
category = st.selectbox("계열 선택", ["국어", "수학", "탐구", "영어", "기타"])
subject = st.text_input("세부 과목 (예: 언어와 매체, 확률과 통계, 생활과 윤리, 지구과학 1, 한국사...)")
unit = st.text_input("단원")
question = st.text_area("문제")

uploaded_file = st.file_uploader("문제 사진 업로드", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, caption="문제 이미지", use_container_width=True)

my_answer = st.text_input("내가 작성한 답")
correct_answer = st.text_input("정답")

reason = st.selectbox("틀린 이유", ["개념 부족", "실수", "시간 부족", "이해 부족"])
detail_reason = st.text_input("세부 이유 (선택)")

# ===== 저장 =====
if st.button("오답 저장"):
    if my_answer != correct_answer:
        st.session_state.notes.append({
            "계열": category,
            "과목": subject,
            "단원": unit,
            "문제": question,
            "이미지": uploaded_file,
            "내 답": my_answer,
            "정답": correct_answer,
            "이유": reason,
            "세부 이유": detail_reason
        })
        st.success("오답 저장 완료!")
    else:
        st.warning("정답입니다!")

# ===== 오답 출력 =====
st.markdown("---")
st.subheader("📒 오답노트")

for i, n in enumerate(st.session_state.notes):
    st.write(f"{i+1}. {n['계열']} - {n['과목']} - {n['단원']}")
    st.write(f"문제: {n['문제']}")
    st.write(f"이유: {n['이유']} / {n['세부 이유']}")
    st.markdown("---")

# ===== 통계 =====
st.subheader("📊 오답 분석")

stats = {"개념 부족":0, "실수":0, "시간 부족":0, "이해 부족":0}

for n in st.session_state.notes:
    if n["이유"] in stats:
        stats[n["이유"]] += 1

for key, value in stats.items():
    st.write(f"{key}: {value}회")

# ===== 피드백 =====
st.subheader("📌 맞춤 피드백")

if stats.get("개념 부족", 0) > 0:
    st.write("개념 복습이 필요합니다.")
if stats.get("실수", 0) > 0:
    st.write("문제를 꼼꼼히 읽고, 검토하는 습관을 들이세요.")
if stats.get("시간 부족", 0) > 0:
    st.write("시간 관리 연습이 필요합니다.")
if stats.get("이해 부족", 0) > 0:
    st.write("문제의 조건을 해석하는 연습이 필요합니다.")

# 과목별 피드백
if category == "국어":
    st.write("지문을 이해할 수 있도록 구조화하며 읽어보세요!")
elif category == "수학":
    st.write("오답 유형과 유사한 문제를 다양하게 접해보세요!")
elif category == "탐구":
    st.write("틀린 선지를 따로 모아 분석해보세요!")
elif category == "영어":
    st.write("모르는 어휘를 모아 암기하며 다시 독해해보세요!")

# ===== PDF 생성 (한글 지원 + 이미지 포함) =====
pdfmetrics.registerFont(TTFont('NanumGothic', 'fonts/NanumGothic.ttf'))

korean_style = ParagraphStyle(
    name='Korean',
    fontName='NanumGothic',
    fontSize=12,
    leading=15
)

def make_pdf(notes):
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_pdf.name)
    elements = []

    for i, n in enumerate(notes):
        elements.append(Paragraph(f"{i+1}번", korean_style))
        elements.append(Paragraph(f"과목: {n['계열']} - {n['과목']}", korean_style))
        elements.append(Paragraph(f"단원: {n['단원']}", korean_style))
        elements.append(Paragraph(f"문제: {n['문제']}", korean_style))
        elements.append(Paragraph(f"내 답: {n['내 답']}", korean_style))
        elements.append(Paragraph(f"정답: {n['정답']}", korean_style))
        elements.append(Paragraph(f"이유: {n['이유']} ({n['세부 이유']})", korean_style))
        elements.append(Spacer(1, 10))

        if n["이미지"] is not None:
            img_temp = tempfile.NamedTemporaryFile(delete=False)
            img_temp.write(n["이미지"].getvalue())
            img_temp.close()
            elements.append(Image(img_temp.name, width=300, height=200))
            elements.append(Spacer(1, 20))

    doc.build(elements)

    with open(temp_pdf.name, "rb") as f:
        return f.read()

pdf_data = make_pdf(st.session_state.notes)

st.download_button(
    label="📥 오답노트 다운로드 (PDF)",
    data=pdf_data,
    file_name="오답노트.pdf",
    mime="application/pdf"
)

# ===== 하단 링크 =====
st.markdown("---")
st.markdown("내가 틀린 문제를 남들은 얼마나 틀렸을까? 전국연합학력평가 정답률 확인")
st.markdown("[👉 EBSi 바로가기](https://www.ebsi.co.kr)")

# ===== 하단 링크 =====
st.markdown("---")
st.markdown("내가 틀린 문제를 남들은 얼마나 틀렸을까? 전국연합학력평가 정답률 확인")
st.markdown("[👉 EBSi 바로가기](https://www.ebsi.co.kr)")
