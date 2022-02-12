import streamlit as st
from transformers import pipeline


@st.cache(allow_output_mutation=True)
def get_pipeline():
    model_path = "./trained_models"
    model_name = "beomi/kcgpt2"
    return pipeline('text-generation', model=model_path, tokenizer=model_name)

st.title("음식리뷰 생성기")

select_types = ('긍정적 리뷰', '부정적리뷰')
positive = st.radio(
     "만들 음식 리뷰의 유형을 골라주세요",
     select_types
     )
positive = positive == select_types[0]

prefix = st.text_input("리뷰의 시작 텍스트를 입력해주세요", "이 가게 음식은")

def generate_review(reviewer, prefix, positive):
    text = "긍정 : " if positive else "부정 : "
    text += prefix
    return reviewer(text, num_return_sequences=5)
    
with st.spinner("리뷰를 작성중이에요..."):
    reviewer = get_pipeline()

refresh = st.button("새로고침")

for text in generate_review(reviewer, prefix, positive):
    text = text["generated_text"]
    text = text.split("\n")[0]
    
    if positive:
        st.success(text)
    else:
        st.error(text)