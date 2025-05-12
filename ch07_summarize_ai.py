import streamlit as st
from openai import OpenAI

sample_text = """프롬프트 엔지니어링이란 무엇인가요?
프롬프트 엔지니어링은 생성형 AI로부터 원하는 결과를 얻기 위한 질문의 기술입니다. 생성형 AI는 인간을 모방하려고 시도하지만 고품질의 결과를 만들어내려면 자세한 지침이 필요합니다. 프롬프트 엔지니어링은 생성형 AI가 사용자와 더 의미 있게 상호작용할 수 있도록 가장 적절한 형식, 구문, 단어, 기호를 사용하게 해줍니다. 사용자가 창의력을 발휘하면서도 여러 번의 시행착오를 거쳐 최적의 결과물을 얻을 수 있게 합니다.
프롬프트란 무엇인가요?
프롬프트는 특정 작업을 수행하도록 생성형 AI에 요청하는 자연어 텍스트입니다. 생성형 AI는 스토리, 대화, 동영상, 이미지, 음악과 같은 새로운 콘텐츠를 만들어내는 인공지능 솔루션으로, 방대한 양의 데이터로 사전 훈련된 심층 신경망을 사용하는 대규모 기계 학습(ML) 모델을 기반으로 합니다.
"""

# main() 함수 선언
def main():
	# 메인 화면 구성
	st.set_page_config(layout="wide")
	st.title("문서 요약 프로그램")
	st.caption("스트림릿과 OpenAI API를 활용한 간단한 요약 프로그램")
	# 사이드바 구성
	with st.sidebar:
		st.subheader("OpenAI API Key 설정")
		# 입력 위젯 유형 설정(비밀번호)
		openai_api_key = st.text_input("OpenAI API Key", type="password")
		st.write("[OpenAI API Key 받기](https://platform.openai.com/account/api-keys)")
		# OpenAI 클라이언트 생성
		if openai_api_key:
			client = OpenAI(api_key=openai_api_key)
	# 문서 요약 함수
	def summarize_text(prompt, text):
		content = prompt + "\n" + text
		response = client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[{"role": "user", "content": content}],
		)
		return response.choices[0].message.content
	st.write("### 요약할 문서와 프롬프트 입력")
	# 문서 입력 위젯
	text = st.text_area(
		"문서 입력:",
		height=300,
		placeholder="요약하고 싶은 문서를 여기에 입력하세요.",
		value=sample_text,
	)
	# 프롬프트 입력 위젯
	start_prompt = """다음 문서를 개조식으로 요약해주세요.
- ~음, ~했음 등의 어조를 사용하세요.
- 가장 중요한 내용을 중심으로 간결하게 요약하세요.
- 마크다운을 이용해 구조화된 요약 결과를 보여주세요.
"""
	prompt = st.text_area(
		"프롬프트 입력:",
		height=100,
		value=start_prompt,
	)
	# 요약 버튼 생성 및 결과 표시
	if st.button("요약"):
		if not client:
			st.error("유효한 API Key를 입력하세요.")
		elif not text.strip():
			st.error("문서를 입력하세요.")
		else:
			with st.spinner("요약 중입니다..."):
				# 문서 요약 함수 호출 및 결과 출력
				try:
					summary = summarize_text(prompt, text)
					st.subheader("요약 결과")
					st.write(summary)
				except Exception as e:
					st.error(f"오류가 발생했습니다: {e}")

# main 함수 실행
if __name__ == "__main__":
	main()