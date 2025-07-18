import streamlit as st
import random
import time
import difflib  # 오타 허용을 위한 유사도 측정

# 문장 데이터
sentence_dict = {
    'a': "이 광대한 우주, 무한한 시간 속에서  당신과 같은 시간, 같은 행성 위에 살아가는 것을 기뻐하며.",
    'b': "미래는 공백이었다. 대홍수가 지나가고 난 뒤의 세상 같은 것이었다.",
    'c': "가장 화려한 꽃이 가장 처참하게 진다 네 사랑을 보아라 네 사랑을 밀물진 꽃밭에서서 보아라.",
    'd': "그날 눈사람은 텅 빈 욕조에 누워 있었다. 뜨거운 물을 틀기 전에 그는 더 살아야 하는지 말아야 하는지 곰곰이 생각해 보았다.",
    'e': "사람들은 오베가 세상을 흑백으로 본다고 말했다. 하지만 그녀는 색깔이었다. 그녀가 오베가 볼 수 있는 색깔의 전부였다.",
    'f': "죽느냐 사느냐, 그것이 문제로다. 가혹한 운명의 화살을 맞고도 죽은듯 참아야하는가.",
    'g': "비록 그 빛 안 보여도 존재의 끝과  영원한 영광에 내 영혼 이를 수 있는 그 도달할 수 있는 곳까지 사랑합니다.",
    'h': "닫힌 방 안의 공기처럼 모든 게 조용하고 가만히 있었다. 그게 나의 세계였다. 난 그게 좋았다.",
    'i': "부서져본 적 없는 사람의 걸음걸이를 흉내내어 여기까지 걸어왔다. 꿰매지 않은 자리마다 깨끗한 장막을 덧대 가렸다.",
    'j': "시간 틈에 밀려 잠시 덮기는 좋았으나  영영 지울 수 없는 사람아 너를 들이면 내 심장 위치를 안다.",
    'k': "초라한 골목이 어째서 해가 지기 직전의 그 잠시동안 황홀할정도로 아름다워지는지, 그 때 나는 이유를 알지 못했다.",
    'l': "밤 촛불은 스러지고, 유쾌한 낮의 신이 안개낀 산마루에 발끝으로 서있답니다. 나는 떠나서 살거나, 남아서 죽어야만 하겠지요."
}

SHOW_TIME = 20  # 문장 보여주는 시간 (초)
TOTAL_ROUNDS = 8
SIMILARITY_THRESHOLD = 0.80  # 유사도 기준 (0~1 사이)

# 초기 세션 상태 설정
if "started" not in st.session_state:
    st.session_state.started = False
if "round" not in st.session_state:
    st.session_state.round = 1
    st.session_state.correct_count = 0
    st.session_state.current_key = ""
    st.session_state.current_sentence = ""
    st.session_state.user_input = ""
    st.session_state.stage = "waiting"
    st.session_state.used_keys = set()

st.title("🧠 기억력 테스트 (오타 허용 + 실시간 타이머)")

# 시작 전 대기 화면
if not st.session_state.started:
    st.subheader("🎮 테스트를 시작하려면 아래 버튼을 눌러주세요!")
    if st.button("▶️ 시작하기"):
        st.session_state.started = True
        st.session_state.stage = "start"
        st.rerun()
    st.stop()  # 아직 시작하지 않았으면 더 이상 코드 실행 중단

# 테스트 시작
if st.session_state.stage == "start":
    remaining_keys = list(set(sentence_dict.keys()) - st.session_state.used_keys)
    if not remaining_keys:
        st.error("더 이상 남은 문장이 없습니다.")
    else:
        selected_key = random.choice(remaining_keys)
        st.session_state.current_key = selected_key
        st.session_state.current_sentence = sentence_dict[selected_key]
        st.session_state.used_keys.add(selected_key)
        st.session_state.stage = "show"
        st.rerun()

# 문장 보여주기
elif st.session_state.stage == "show":
    st.subheader("문장을 기억하세요 👀")

    countdown = st.empty()
    sentence_box = st.empty()

    for i in range(SHOW_TIME, 0, -1):
        countdown.markdown(f"⏱️ 남은 시간: **{i}초**")
        sentence_box.markdown(f"### 📖 {st.session_state.current_sentence}")
        time.sleep(1)

    st.session_state.stage = "input"
    st.rerun()

# 사용자 입력
elif st.session_state.stage == "input":
    st.subheader(f"Round {st.session_state.round} / {TOTAL_ROUNDS}")
    st.markdown("✍️ 방금 본 문장을 최대한 똑같이 입력하세요 (오타 약간 허용)")

    user_input = st.text_area("🔡 문장을 입력하세요:", key="user_input")

    if st.button("제출"):
        correct = st.session_state.current_sentence.strip()
        user = user_input.strip()

        similarity = difflib.SequenceMatcher(None, correct, user).ratio()

        if similarity >= SIMILARITY_THRESHOLD:
            st.success("✅ 정답! (오타 허용)")
            st.session_state.correct_count += 1
        else:
            st.error("❌ 오답!")
            st.markdown(f"**정답:** {correct}")
            st.markdown(f"**유사도:** {similarity:.2f}")
        st.session_state.stage = "result"
        st.rerun()

# 결과 단계
elif st.session_state.stage == "result":
    st.markdown(f"### 현재 정답 수: **{st.session_state.correct_count} / {st.session_state.round}**")

    if st.session_state.round >= TOTAL_ROUNDS:
        score = st.session_state.correct_count
        st.subheader("🎯 최종 결과")

        if score == 0:
            st.error("그냥 돌")
        elif score <= 2:
            st.warning("금붕어 수준")
        elif score <= 4:
            st.warning("🦍 침팬치 수준")
        elif score <= 6:
            st.info("👤 사람 수준")
        else:
            st.success("🤖 컴퓨터 수준")

        if st.button("🔁 다시 시작"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    else:
        if st.button("다음 문제"):
            st.session_state.round += 1
            st.session_state.stage = "start"
            st.session_state.user_input = ""
            st.rerun()

