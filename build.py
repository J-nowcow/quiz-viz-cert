#!/usr/bin/env python3
"""Build index.html by embedding quiz_data.json into the HTML template."""
import json

with open('quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

# Minify JSON for embedding
quiz_json = json.dumps(quiz_data, ensure_ascii=False, separators=(',', ':'))

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>경영정보시각화 퀴즈</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --primary: #4F46E5; --primary-light: #818CF8; --success: #10B981;
  --danger: #EF4444; --warning: #F59E0B; --bg: #F9FAFB; --card: #fff;
  --text: #111827; --text-light: #6B7280; --border: #E5E7EB;
  --radius: 12px; --shadow: 0 1px 3px rgba(0,0,0,.1);
}}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100dvh; }}
.container {{ max-width: 720px; margin: 0 auto; padding: 16px; }}
h1 {{ font-size: 1.5rem; font-weight: 700; text-align: center; padding: 20px 0 8px; }}
h2 {{ font-size: 1.15rem; font-weight: 600; margin-bottom: 12px; }}
.subtitle {{ text-align: center; color: var(--text-light); font-size: .9rem; margin-bottom: 24px; }}
.card {{ background: var(--card); border-radius: var(--radius); padding: 20px; margin-bottom: 16px; box-shadow: var(--shadow); }}
.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 12px 24px; border-radius: 8px; border: none; font-size: 1rem;
  font-weight: 600; cursor: pointer; transition: all .15s; text-decoration: none; }}
.btn-primary {{ background: var(--primary); color: #fff; }}
.btn-primary:hover {{ background: #4338CA; }}
.btn-outline {{ background: transparent; color: var(--primary); border: 2px solid var(--primary); }}
.btn-outline:hover {{ background: var(--primary); color: #fff; }}
.btn-success {{ background: var(--success); color: #fff; }}
.btn-danger {{ background: var(--danger); color: #fff; }}
.btn-warning {{ background: var(--warning); color: #fff; }}
.btn-sm {{ padding: 8px 16px; font-size: .875rem; }}
.btn-block {{ width: 100%; }}
.btn:disabled {{ opacity: .5; cursor: not-allowed; }}
.btn-group {{ display: flex; gap: 8px; flex-wrap: wrap; }}

/* Home screen */
.mode-card {{ cursor: pointer; border: 2px solid var(--border); transition: all .2s; }}
.mode-card:hover {{ border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(79,70,229,.15); }}
.mode-icon {{ font-size: 2rem; margin-bottom: 8px; }}
.mode-title {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 4px; }}
.mode-desc {{ color: var(--text-light); font-size: .85rem; }}

/* Exam selector */
.exam-option {{ padding: 16px; border: 2px solid var(--border); border-radius: 8px;
  cursor: pointer; transition: all .15s; margin-bottom: 8px; }}
.exam-option:hover {{ border-color: var(--primary-light); }}
.exam-option.selected {{ border-color: var(--primary); background: #EEF2FF; }}
.exam-option .exam-name {{ font-weight: 600; }}
.exam-option .exam-info {{ color: var(--text-light); font-size: .85rem; }}

/* Question card fixed height */
.q-card-scroll {{ min-height: 420px; max-height: 60vh; overflow-y: auto; padding: 4px; }}

/* Question */
.q-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px; }}
.q-num {{ font-weight: 700; color: var(--primary); font-size: 1rem; }}
.q-subject {{ font-size: .8rem; color: var(--text-light); background: #F3F4F6; padding: 2px 10px; border-radius: 999px; }}
.q-text {{ font-size: 1rem; margin-bottom: 16px; white-space: pre-wrap; }}
.q-context {{ background: #F9FAFB; border-left: 3px solid var(--primary-light); padding: 12px 16px;
  margin-bottom: 16px; border-radius: 0 8px 8px 0; font-size: .95rem; color: #374151; }}
.choice {{ display: block; width: 100%; padding: 12px 16px; margin-bottom: 8px; border: 2px solid var(--border);
  border-radius: 8px; background: #fff; cursor: pointer; text-align: left; font-size: .95rem;
  transition: all .15s; }}
.choice:hover:not(.disabled) {{ border-color: var(--primary-light); background: #EEF2FF; }}
.choice.selected {{ border-color: var(--primary); background: #EEF2FF; }}
.choice.correct {{ border-color: var(--success); background: #ECFDF5; }}
.choice.wrong {{ border-color: var(--danger); background: #FEF2F2; }}
.choice.disabled {{ cursor: default; }}
.choice-num {{ font-weight: 600; margin-right: 8px; }}

/* Explanation */
.explanation {{ background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px;
  padding: 12px 16px; margin-top: 12px; font-size: .9rem; }}
.explanation strong {{ color: var(--success); }}

/* Timer */
.timer-bar {{ display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }}
.timer-display {{ font-size: 1.2rem; font-weight: 700; font-variant-numeric: tabular-nums; }}
.timer-display.warning {{ color: var(--danger); }}
.timer-toggle {{ font-size: .85rem; }}

/* Progress */
.progress-bar {{ height: 6px; background: var(--border); border-radius: 999px; overflow: hidden; margin-bottom: 16px; }}
.progress-fill {{ height: 100%; background: var(--primary); border-radius: 999px; transition: width .3s; }}
.progress-text {{ font-size: .8rem; color: var(--text-light); text-align: right; margin-bottom: 8px; }}

/* Result */
.result-summary {{ text-align: center; padding: 24px 0; }}
.result-score {{ font-size: 3rem; font-weight: 800; }}
.result-pass {{ color: var(--success); font-size: 1.3rem; font-weight: 700; margin: 8px 0; }}
.result-fail {{ color: var(--danger); font-size: 1.3rem; font-weight: 700; margin: 8px 0; }}
.subject-scores {{ margin-top: 16px; }}
.subject-row {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--border); }}
.subject-row:last-child {{ border-bottom: none; }}
.subject-name {{ font-weight: 500; }}
.subject-score {{ font-weight: 700; }}
.subject-score.pass {{ color: var(--success); }}
.subject-score.fail {{ color: var(--danger); }}

/* Navigation */
.nav-bar {{ display: flex; justify-content: space-between; align-items: center; padding-top: 16px; gap: 8px; }}
.back-btn {{ cursor: pointer; display: flex; align-items: center; gap: 4px; color: var(--primary);
  font-weight: 600; font-size: .95rem; background: none; border: none; padding: 8px 0; }}

/* Question grid (exam mode) */
.q-grid {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; margin: 16px 0; }}
.q-grid-item {{ width: 100%; aspect-ratio: 1; display: flex; align-items: center; justify-content: center;
  border-radius: 6px; font-size: .75rem; font-weight: 600; cursor: pointer;
  border: 1px solid var(--border); background: #fff; }}
.q-grid-item.answered {{ background: #EEF2FF; border-color: var(--primary-light); color: var(--primary); }}
.q-grid-item.current {{ background: var(--primary); color: #fff; border-color: var(--primary); }}

/* Filter chips */
.filter-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }}
.chip {{ padding: 6px 14px; border-radius: 999px; border: 1px solid var(--border);
  background: #fff; cursor: pointer; font-size: .85rem; transition: all .15s; }}
.chip.active {{ background: var(--primary); color: #fff; border-color: var(--primary); }}

/* Wrong answers badge */
.badge {{ display: inline-flex; align-items: center; justify-content: center; min-width: 22px;
  height: 22px; border-radius: 999px; background: var(--danger); color: #fff;
  font-size: .75rem; font-weight: 700; padding: 0 6px; margin-left: 6px; }}

/* Stats */
.stat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }}
.stat-item {{ text-align: center; padding: 12px; background: #F9FAFB; border-radius: 8px; }}
.stat-value {{ font-size: 1.5rem; font-weight: 800; color: var(--primary); }}
.stat-label {{ font-size: .75rem; color: var(--text-light); margin-top: 4px; }}

/* Scrollable review */
.review-list {{ max-height: 70vh; overflow-y: auto; }}

/* Responsive */
@media (max-width: 480px) {{
  .container {{ padding: 12px; }}
  h1 {{ font-size: 1.25rem; }}
  .q-grid {{ grid-template-columns: repeat(6, 1fr); }}
  .stat-grid {{ grid-template-columns: repeat(3, 1fr); gap: 8px; }}
  .stat-value {{ font-size: 1.2rem; }}
  .btn {{ padding: 10px 18px; }}
}}

.hidden {{ display: none !important; }}
</style>
</head>
<body>
<div class="container" id="app">

<!-- HOME SCREEN -->
<div id="screen-home">
  <h1>📊 경영정보시각화</h1>
  <p class="subtitle">자격증 시험 대비 퀴즈 (256문항)</p>

  <div id="home-stats" class="card">
    <div class="stat-grid">
      <div class="stat-item">
        <div class="stat-value" id="stat-total">0</div>
        <div class="stat-label">풀이한 문항</div>
      </div>
      <div class="stat-item">
        <div class="stat-value" id="stat-correct">0%</div>
        <div class="stat-label">정답률</div>
      </div>
      <div class="stat-item">
        <div class="stat-value" id="stat-wrong">0</div>
        <div class="stat-label">오답노트</div>
      </div>
    </div>
  </div>

  <div class="card mode-card" onclick="showExamSelect()">
    <div class="mode-icon">📝</div>
    <div class="mode-title">시험 모드</div>
    <div class="mode-desc">실제 시험과 동일 — 60문항, 60분 타이머, 제출 후 결과 확인</div>
  </div>

  <div class="card mode-card" onclick="startPractice()">
    <div class="mode-icon">💡</div>
    <div class="mode-title">연습 모드</div>
    <div class="mode-desc">한 문제씩 풀기 — 즉시 정답/해설 확인, 과목/시험 필터</div>
  </div>

  <div class="card mode-card" onclick="startWrongNotes()">
    <div class="mode-icon">📕</div>
    <div class="mode-title">오답노트 <span class="badge hidden" id="wrong-badge">0</span></div>
    <div class="mode-desc">틀린 문제만 모아서 재풀이</div>
  </div>

  <a href="notes.html" style="text-decoration:none;">
  <div class="card mode-card">
    <div class="mode-icon">📚</div>
    <div class="mode-title">이론 정리</div>
    <div class="mode-desc">3과목 핵심 개념 · 빈출 키워드 · 기출 포인트</div>
  </div>
  </a>

  <div style="text-align:center; margin-top:16px;">
    <button class="btn btn-sm btn-outline" onclick="if(confirm('모든 풀이 기록을 초기화할까요?'))resetAll()">기록 초기화</button>
  </div>
</div>

<!-- EXAM SELECT SCREEN -->
<div id="screen-exam-select" class="hidden">
  <button class="back-btn" onclick="goHome()">← 홈으로</button>
  <h2>시험 선택</h2>

  <div class="exam-option" data-exam="모의고사 A형" onclick="selectExam(this)">
    <div class="exam-name">📝 모의고사 A형</div>
    <div class="exam-info">3과목 60문항 · 해커스HRD 13차시+23차시</div>
  </div>
  <div class="exam-option" data-exam="모의고사 B형" onclick="selectExam(this)">
    <div class="exam-name">📝 모의고사 B형</div>
    <div class="exam-info">3과목 60문항 · 해커스HRD 14차시+24차시</div>
  </div>
  <div class="exam-option" data-exam="2024 제1회 기출" onclick="selectExam(this)">
    <div class="exam-name">📋 2024 제1회 기출</div>
    <div class="exam-info">3과목 60문항 · 실전 기출문제</div>
  </div>
  <div class="exam-option" data-exam="확인학습" onclick="selectExam(this)">
    <div class="exam-name">📖 확인학습</div>
    <div class="exam-info">이론 차시별 복습 76문항 · 빈칸/용어/O·X</div>
  </div>
  <div class="exam-option" data-exam="랜덤 혼합" onclick="selectExam(this)">
    <div class="exam-name">🎲 랜덤 혼합</div>
    <div class="exam-info">전체 256문항에서 과목별 20문제 랜덤 출제</div>
  </div>

  <div style="margin-top:16px;">
    <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
      <input type="checkbox" id="timer-toggle" checked>
      <span>⏱ 60분 타이머 사용</span>
    </label>
  </div>

  <button class="btn btn-primary btn-block" style="margin-top:16px;" id="btn-start-exam" disabled onclick="startExam()">
    시험 시작
  </button>
</div>

<!-- EXAM MODE SCREEN -->
<div id="screen-exam" class="hidden">
  <div class="timer-bar">
    <button class="back-btn" onclick="if(confirm('시험을 중단할까요? 진행상황이 사라집니다.'))goHome()">← 나가기</button>
    <div style="flex:1"></div>
    <div class="timer-display" id="exam-timer">60:00</div>
  </div>
  <div class="progress-text" id="exam-progress-text">1 / 60</div>
  <div class="progress-bar"><div class="progress-fill" id="exam-progress"></div></div>

  <div class="card" id="exam-question-card"></div>

  <div class="q-grid" id="exam-q-grid"></div>

  <div class="nav-bar">
    <button class="btn btn-outline btn-sm" id="exam-prev" onclick="examNav(-1)">← 이전</button>
    <button class="btn btn-success btn-sm" id="exam-submit" disabled onclick="submitExam()">제출하기 <span id="exam-submit-count"></span></button>
    <button class="btn btn-primary btn-sm" id="exam-next" onclick="examNav(1)">다음 →</button>
  </div>
</div>

<!-- PRACTICE MODE SCREEN -->
<div id="screen-practice" class="hidden">
  <button class="back-btn" onclick="goHome()">← 홈으로</button>
  <h2>연습 모드</h2>

  <div class="filter-row" id="practice-exam-filter"></div>
  <div class="filter-row" id="practice-subject-filter"></div>

  <div class="progress-text" id="practice-progress-text">1 / 180</div>
  <div class="progress-bar"><div class="progress-fill" id="practice-progress"></div></div>

  <div class="card" id="practice-question-card"></div>

  <div class="nav-bar">
    <button class="btn btn-outline btn-sm" id="practice-prev" onclick="practiceNav(-1)">← 이전</button>
    <button class="btn btn-primary btn-sm" id="practice-next" onclick="practiceNav(1)">다음 →</button>
  </div>
</div>

<!-- WRONG NOTES SCREEN -->
<div id="screen-wrong" class="hidden">
  <button class="back-btn" onclick="goHome()">← 홈으로</button>
  <h2>📕 오답노트 <span class="badge" id="wrong-count">0</span></h2>

  <div id="wrong-empty" class="card hidden" style="text-align:center; color:var(--text-light);">
    오답이 없습니다! 🎉
  </div>

  <div class="filter-row" id="wrong-subject-filter"></div>

  <div class="progress-text" id="wrong-progress-text"></div>
  <div class="progress-bar"><div class="progress-fill" id="wrong-progress"></div></div>

  <div class="card" id="wrong-question-card"></div>

  <div class="nav-bar" id="wrong-nav">
    <button class="btn btn-outline btn-sm" id="wrong-prev" onclick="wrongNav(-1)">← 이전</button>
    <button class="btn btn-primary btn-sm" id="wrong-next" onclick="wrongNav(1)">다음 →</button>
  </div>
</div>

<!-- RESULT SCREEN -->
<div id="screen-result" class="hidden">
  <button class="back-btn" onclick="goHome()">← 홈으로</button>

  <div class="card">
    <div class="result-summary">
      <div class="result-score" id="result-total-score">0점</div>
      <div id="result-pass-status"></div>
      <div style="color:var(--text-light); font-size:.9rem;" id="result-exam-name"></div>
    </div>

    <div class="subject-scores" id="result-subjects"></div>
  </div>

  <div style="margin:16px 0;">
    <button class="btn btn-primary btn-block" onclick="showResultReview()">틀린 문제 리뷰</button>
  </div>

  <div class="card hidden" id="result-review">
    <h2>틀린 문제 리뷰</h2>
    <div class="review-list" id="result-review-list"></div>
  </div>

  <div style="text-align:center; margin-top:16px;">
    <button class="btn btn-outline" onclick="goHome()">홈으로 돌아가기</button>
  </div>
</div>

</div>

<script>
// ── DATA ──
const QUIZ_DATA = {quiz_json};

const EXAMS = ["모의고사 A형", "모의고사 B형", "2024 제1회 기출", "확인학습"];
const SUBJECTS = [
  {{ id: 1, name: "경영정보 일반" }},
  {{ id: 2, name: "데이터 해석 및 활용" }},
  {{ id: 3, name: "경영정보시각화 디자인" }}
];
const CHOICE_LABELS = ["①", "②", "③", "④"];

// ── STATE ──
let state = {{
  screen: 'home',
  // Exam mode
  examName: null, examQuestions: [], examAnswers: {{}}, examIndex: 0,
  timerEnabled: true, timerSeconds: 3600, timerInterval: null,
  // Practice mode
  practicePool: [], practiceIndex: 0, practiceRevealed: false,
  practiceExamFilter: null, practiceSubjectFilter: null,
  // Wrong notes
  wrongPool: [], wrongIndex: 0, wrongRevealed: false, wrongSubjectFilter: null,
}};

// ── LOCAL STORAGE ──
function loadHistory() {{
  try {{ return JSON.parse(localStorage.getItem('quizHistory') || '{{}}'); }} catch {{ return {{}}; }}
}}
function saveHistory(h) {{ localStorage.setItem('quizHistory', JSON.stringify(h)); }}
function loadWrong() {{
  try {{ return JSON.parse(localStorage.getItem('quizWrong') || '[]'); }} catch {{ return []; }}
}}
function saveWrong(w) {{ localStorage.setItem('quizWrong', JSON.stringify(w)); }}
function getQKey(q) {{ return q.exam + '_' + q.questionNumber; }}

function recordAnswer(q, chosen, isCorrect) {{
  const h = loadHistory();
  const key = getQKey(q);
  h[key] = {{ correct: isCorrect, chosen, answer: q.answer, last: Date.now() }};
  saveHistory(h);

  let wrong = loadWrong();
  if (!isCorrect) {{
    if (!wrong.includes(key)) wrong.push(key);
  }} else {{
    wrong = wrong.filter(k => k !== key);
  }}
  saveWrong(wrong);
}}

function resetAll() {{
  localStorage.removeItem('quizHistory');
  localStorage.removeItem('quizWrong');
  updateHomeStats();
}}

// ── SCREENS ──
function showScreen(name) {{
  document.querySelectorAll('[id^="screen-"]').forEach(el => el.classList.add('hidden'));
  document.getElementById('screen-' + name).classList.remove('hidden');
  state.screen = name;
  window.scrollTo(0, 0);
}}

function goHome() {{
  if (state.timerInterval) {{ clearInterval(state.timerInterval); state.timerInterval = null; }}
  showScreen('home');
  updateHomeStats();
}}

function updateHomeStats() {{
  const h = loadHistory();
  const wrong = loadWrong();
  const total = Object.keys(h).length;
  const correct = Object.values(h).filter(v => v.correct).length;
  document.getElementById('stat-total').textContent = total;
  document.getElementById('stat-correct').textContent = total ? Math.round(correct / total * 100) + '%' : '0%';
  document.getElementById('stat-wrong').textContent = wrong.length;
  const badge = document.getElementById('wrong-badge');
  if (wrong.length > 0) {{ badge.textContent = wrong.length; badge.classList.remove('hidden'); }}
  else {{ badge.classList.add('hidden'); }}
}}

// ── EXAM MODE ──
function showExamSelect() {{
  showScreen('exam-select');
  document.querySelectorAll('.exam-option').forEach(el => el.classList.remove('selected'));
  document.getElementById('btn-start-exam').disabled = true;
  state.examName = null;
}}

function selectExam(el) {{
  document.querySelectorAll('.exam-option').forEach(e => e.classList.remove('selected'));
  el.classList.add('selected');
  state.examName = el.dataset.exam;
  document.getElementById('btn-start-exam').disabled = false;
}}

function shuffle(arr) {{
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }}
  return a;
}}

function startExam() {{
  if (!state.examName) return;
  if (state.examName === '랜덤 혼합') {{
    // Pick 20 random per subject from all 180
    let pool = [];
    for (const subj of SUBJECTS) {{
      const subjQs = QUIZ_DATA.filter(q => q.subject === subj.id);
      pool = pool.concat(shuffle(subjQs).slice(0, 20));
    }}
    state.examQuestions = pool;
  }} else {{
    state.examQuestions = QUIZ_DATA.filter(q => q.exam === state.examName);
  }}
  state.examAnswers = {{}};
  state.examIndex = 0;
  state.timerEnabled = document.getElementById('timer-toggle').checked;
  state.timerSeconds = 3600;

  showScreen('exam');
  buildExamGrid();
  renderExamQuestion();

  if (state.timerEnabled) {{
    updateTimerDisplay();
    state.timerInterval = setInterval(() => {{
      state.timerSeconds--;
      updateTimerDisplay();
      if (state.timerSeconds <= 0) {{
        clearInterval(state.timerInterval);
        state.timerInterval = null;
        alert('시간 종료! 자동 제출합니다.');
        submitExam();
      }}
    }}, 1000);
  }} else {{
    document.getElementById('exam-timer').textContent = '타이머 OFF';
  }}
}}

function updateTimerDisplay() {{
  const m = Math.floor(state.timerSeconds / 60);
  const s = state.timerSeconds % 60;
  const disp = document.getElementById('exam-timer');
  disp.textContent = `${{String(m).padStart(2,'0')}}:${{String(s).padStart(2,'0')}}`;
  disp.classList.toggle('warning', state.timerSeconds < 300);
}}

function buildExamGrid() {{
  const grid = document.getElementById('exam-q-grid');
  grid.innerHTML = '';
  state.examQuestions.forEach((q, i) => {{
    const div = document.createElement('div');
    div.className = 'q-grid-item';
    div.textContent = i + 1;
    div.onclick = () => {{ state.examIndex = i; renderExamQuestion(); }};
    grid.appendChild(div);
  }});
}}

function updateExamGrid() {{
  const items = document.querySelectorAll('#exam-q-grid .q-grid-item');
  items.forEach((el, i) => {{
    el.className = 'q-grid-item';
    if (state.examAnswers[i] !== undefined) el.classList.add('answered');
    if (i === state.examIndex) el.classList.add('current');
  }});
}}

function renderExamQuestion() {{
  const q = state.examQuestions[state.examIndex];
  const total = state.examQuestions.length;
  document.getElementById('exam-progress-text').textContent = `${{state.examIndex + 1}} / ${{total}}`;
  document.getElementById('exam-progress').style.width = `${{(state.examIndex + 1) / total * 100}}%`;

  const card = document.getElementById('exam-question-card');
  card.innerHTML = '<div class="q-card-scroll">' + renderQuestionHTML(q, state.examAnswers[state.examIndex], false) + '</div>';
  card.querySelector('.q-card-scroll').scrollTop = 0;
  card.querySelectorAll('.choice').forEach(btn => {{
    btn.onclick = () => {{
      const chosen = parseInt(btn.dataset.choice);
      state.examAnswers[state.examIndex] = chosen;
      renderExamQuestion();
    }};
  }});

  // Nav buttons
  document.getElementById('exam-prev').disabled = state.examIndex === 0;
  document.getElementById('exam-next').disabled = state.examIndex === total - 1;
  const answered = Object.keys(state.examAnswers).length;
  document.getElementById('exam-submit').disabled = answered < total;
  document.getElementById('exam-submit-count').textContent = answered < total ? `(${{answered}}/${{total}})` : '';

  updateExamGrid();
}}

function examNav(dir) {{
  const newIdx = state.examIndex + dir;
  if (newIdx >= 0 && newIdx < state.examQuestions.length) {{
    state.examIndex = newIdx;
    renderExamQuestion();
  }}
}}

function submitExam() {{
  if (state.timerInterval) {{ clearInterval(state.timerInterval); state.timerInterval = null; }}

  const qs = state.examQuestions;
  const answers = state.examAnswers;

  // Calculate scores
  let subjectScores = {{ 1: {{ correct: 0, total: 0 }}, 2: {{ correct: 0, total: 0 }}, 3: {{ correct: 0, total: 0 }} }};
  let totalCorrect = 0;

  qs.forEach((q, i) => {{
    const chosen = answers[i] || 0;
    const isCorrect = chosen === q.answer;
    if (isCorrect) {{ totalCorrect++; subjectScores[q.subject].correct++; }}
    subjectScores[q.subject].total++;
    recordAnswer(q, chosen, isCorrect);
  }});

  // Display result
  showScreen('result');
  const totalScore = Math.round(totalCorrect / qs.length * 100);
  document.getElementById('result-total-score').textContent = totalScore + '점';
  document.getElementById('result-exam-name').textContent = state.examName;

  // Check pass conditions
  let allSubjectsPass = true;
  const subjectsDiv = document.getElementById('result-subjects');
  subjectsDiv.innerHTML = '';

  for (const subj of SUBJECTS) {{
    const sc = subjectScores[subj.id];
    const score = sc.total > 0 ? Math.round(sc.correct / sc.total * 100) : 0;
    const pass = score >= 40;
    if (!pass) allSubjectsPass = false;

    const row = document.createElement('div');
    row.className = 'subject-row';
    row.innerHTML = `<span class="subject-name">${{subj.name}}</span>
      <span class="subject-score ${{pass ? 'pass' : 'fail'}}">${{score}}점 (${{sc.correct}}/${{sc.total}}) ${{pass ? '✓' : '✗ 과락'}}</span>`;
    subjectsDiv.appendChild(row);
  }}

  const overallPass = allSubjectsPass && totalScore >= 60;
  const statusDiv = document.getElementById('result-pass-status');
  statusDiv.className = overallPass ? 'result-pass' : 'result-fail';
  statusDiv.textContent = overallPass ? '🎉 합격!' : '😢 불합격';

  // Prepare review data
  document.getElementById('result-review').classList.add('hidden');
}}

function showResultReview() {{
  const review = document.getElementById('result-review');
  review.classList.remove('hidden');
  const list = document.getElementById('result-review-list');
  list.innerHTML = '';

  state.examQuestions.forEach((q, i) => {{
    const chosen = state.examAnswers[i] || 0;
    if (chosen === q.answer) return;

    const div = document.createElement('div');
    div.style.marginBottom = '20px';
    div.style.paddingBottom = '16px';
    div.style.borderBottom = '1px solid var(--border)';
    div.innerHTML = renderQuestionHTML(q, chosen, true);
    list.appendChild(div);
  }});

  if (list.children.length === 0) {{
    list.innerHTML = '<p style="text-align:center; color:var(--text-light);">모두 맞았습니다! 🎉</p>';
  }}
  review.scrollIntoView({{ behavior: 'smooth' }});
}}

// ── PRACTICE MODE ──
function startPractice() {{
  state.practiceExamFilter = null;
  state.practiceSubjectFilter = null;
  state.practiceIndex = 0;
  state.practiceRevealed = false;

  showScreen('practice');
  buildPracticeFilters();
  updatePracticePool();
}}

function buildPracticeFilters() {{
  const examFilter = document.getElementById('practice-exam-filter');
  examFilter.innerHTML = '<div class="chip active" onclick="setPracticeExamFilter(null, this)">전체</div>';
  EXAMS.forEach(e => {{
    examFilter.innerHTML += `<div class="chip" onclick="setPracticeExamFilter('${{e}}', this)">${{e}}</div>`;
  }});

  const subjectFilter = document.getElementById('practice-subject-filter');
  subjectFilter.innerHTML = '<div class="chip active" onclick="setPracticeSubjectFilter(null, this)">전체</div>';
  SUBJECTS.forEach(s => {{
    subjectFilter.innerHTML += `<div class="chip" onclick="setPracticeSubjectFilter(${{s.id}}, this)">${{s.name}}</div>`;
  }});
}}

function setPracticeExamFilter(val, el) {{
  state.practiceExamFilter = val;
  document.querySelectorAll('#practice-exam-filter .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  state.practiceIndex = 0;
  state.practiceRevealed = false;
  updatePracticePool();
}}

function setPracticeSubjectFilter(val, el) {{
  state.practiceSubjectFilter = val;
  document.querySelectorAll('#practice-subject-filter .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  state.practiceIndex = 0;
  state.practiceRevealed = false;
  updatePracticePool();
}}

function updatePracticePool() {{
  let pool = [...QUIZ_DATA];
  if (state.practiceExamFilter) pool = pool.filter(q => q.exam === state.practiceExamFilter);
  if (state.practiceSubjectFilter) pool = pool.filter(q => q.subject === state.practiceSubjectFilter);
  state.practicePool = shuffle(pool);
  if (state.practiceIndex >= pool.length) state.practiceIndex = 0;
  renderPracticeQuestion();
}}

function renderPracticeQuestion() {{
  const pool = state.practicePool;
  if (pool.length === 0) {{
    document.getElementById('practice-question-card').innerHTML = '<p style="text-align:center; color:var(--text-light);">해당 조건의 문제가 없습니다.</p>';
    return;
  }}
  const q = pool[state.practiceIndex];
  document.getElementById('practice-progress-text').textContent = `${{state.practiceIndex + 1}} / ${{pool.length}}`;
  document.getElementById('practice-progress').style.width = `${{(state.practiceIndex + 1) / pool.length * 100}}%`;

  const card = document.getElementById('practice-question-card');
  if (state.practiceRevealed) {{
    card.innerHTML = '<div class="q-card-scroll">' + renderQuestionHTML(q, state._practiceChosen, true) + '</div>';
  }} else {{
    card.innerHTML = '<div class="q-card-scroll">' + renderQuestionHTML(q, null, false) + '</div>';
    card.querySelectorAll('.choice').forEach(btn => {{
      btn.onclick = () => {{
        const chosen = parseInt(btn.dataset.choice);
        state._practiceChosen = chosen;
        state.practiceRevealed = true;
        recordAnswer(q, chosen, chosen === q.answer);
        renderPracticeQuestion();
      }};
    }});
  }}

  document.getElementById('practice-prev').disabled = state.practiceIndex === 0;
  document.getElementById('practice-next').disabled = state.practiceIndex === pool.length - 1;
}}

function practiceNav(dir) {{
  const newIdx = state.practiceIndex + dir;
  if (newIdx >= 0 && newIdx < state.practicePool.length) {{
    state.practiceIndex = newIdx;
    state.practiceRevealed = false;
    state._practiceChosen = null;
    renderPracticeQuestion();
  }}
}}

// ── WRONG NOTES MODE ──
function startWrongNotes() {{
  state.wrongSubjectFilter = null;
  state.wrongIndex = 0;
  state.wrongRevealed = false;

  showScreen('wrong');
  buildWrongFilters();
  updateWrongPool();
}}

function buildWrongFilters() {{
  const subjectFilter = document.getElementById('wrong-subject-filter');
  subjectFilter.innerHTML = '<div class="chip active" onclick="setWrongSubjectFilter(null, this)">전체</div>';
  SUBJECTS.forEach(s => {{
    subjectFilter.innerHTML += `<div class="chip" onclick="setWrongSubjectFilter(${{s.id}}, this)">${{s.name}}</div>`;
  }});
}}

function setWrongSubjectFilter(val, el) {{
  state.wrongSubjectFilter = val;
  document.querySelectorAll('#wrong-subject-filter .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  state.wrongIndex = 0;
  state.wrongRevealed = false;
  updateWrongPool();
}}

function updateWrongPool() {{
  const wrongKeys = loadWrong();
  let pool = QUIZ_DATA.filter(q => wrongKeys.includes(getQKey(q)));
  if (state.wrongSubjectFilter) pool = pool.filter(q => q.subject === state.wrongSubjectFilter);

  state.wrongPool = pool;
  document.getElementById('wrong-count').textContent = pool.length;

  if (pool.length === 0) {{
    document.getElementById('wrong-empty').classList.remove('hidden');
    document.getElementById('wrong-question-card').innerHTML = '';
    document.getElementById('wrong-progress-text').textContent = '';
    document.getElementById('wrong-progress').style.width = '0%';
    document.getElementById('wrong-nav').classList.add('hidden');
    return;
  }}

  document.getElementById('wrong-empty').classList.add('hidden');
  document.getElementById('wrong-nav').classList.remove('hidden');
  if (state.wrongIndex >= pool.length) state.wrongIndex = 0;
  renderWrongQuestion();
}}

function renderWrongQuestion() {{
  const pool = state.wrongPool;
  if (pool.length === 0) return;
  const q = pool[state.wrongIndex];

  document.getElementById('wrong-progress-text').textContent = `${{state.wrongIndex + 1}} / ${{pool.length}}`;
  document.getElementById('wrong-progress').style.width = `${{(state.wrongIndex + 1) / pool.length * 100}}%`;

  const card = document.getElementById('wrong-question-card');
  if (state.wrongRevealed) {{
    let inner = renderQuestionHTML(q, state._wrongChosen, true);
    if (state._wrongChosen === q.answer) {{
      inner += '<div style="text-align:center; margin-top:12px; color:var(--success); font-weight:600;">✓ 오답노트에서 제거되었습니다</div>';
    }}
    card.innerHTML = '<div class="q-card-scroll">' + inner + '</div>';
  }} else {{
    card.innerHTML = '<div class="q-card-scroll">' + renderQuestionHTML(q, null, false) + '</div>';
    card.querySelectorAll('.choice').forEach(btn => {{
      btn.onclick = () => {{
        const chosen = parseInt(btn.dataset.choice);
        state._wrongChosen = chosen;
        state.wrongRevealed = true;
        recordAnswer(q, chosen, chosen === q.answer);
        renderWrongQuestion();
      }};
    }});
  }}

  document.getElementById('wrong-prev').disabled = state.wrongIndex === 0;
  document.getElementById('wrong-next').disabled = state.wrongIndex === pool.length - 1;
}}

function wrongNav(dir) {{
  const newIdx = state.wrongIndex + dir;
  if (newIdx >= 0 && newIdx < state.wrongPool.length) {{
    state.wrongIndex = newIdx;
    state.wrongRevealed = false;
    state._wrongChosen = null;
    renderWrongQuestion();
  }}
}}

// ── RENDER HELPERS ──
function escapeHtml(str) {{
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}}

function renderQuestionHTML(q, chosen, showAnswer) {{
  let html = '<div class="q-header">';
  html += `<span class="q-num">${{q.exam}} Q${{q.questionNumber}}</span>`;
  html += `<span class="q-subject">${{q.subjectName}}</span>`;
  html += '</div>';

  // Parse question text for context blocks (lines starting with >)
  const lines = q.text.split('\\n');
  let mainText = [];
  let contextText = [];
  let inContext = false;
  for (const line of lines) {{
    if (line.startsWith('> ')) {{
      contextText.push(line.slice(2));
      inContext = true;
    }} else {{
      if (inContext) {{ inContext = false; }}
      mainText.push(line);
    }}
  }}

  html += `<div class="q-text">${{escapeHtml(mainText.join('\\n'))}}</div>`;
  if (contextText.length > 0) {{
    html += `<div class="q-context">${{escapeHtml(contextText.join('\\n'))}}</div>`;
  }}

  // Choices
  q.choices.forEach((c, i) => {{
    const num = i + 1;
    let cls = 'choice';
    if (showAnswer) {{
      cls += ' disabled';
      if (num === q.answer) cls += ' correct';
      else if (num === chosen) cls += ' wrong';
    }} else {{
      if (num === chosen) cls += ' selected';
    }}
    html += `<button class="${{cls}}" data-choice="${{num}}"${{showAnswer ? ' disabled' : ''}}>`;
    html += `<span class="choice-num">${{CHOICE_LABELS[i]}}</span> ${{escapeHtml(c)}}`;
    html += '</button>';
  }});

  // Explanation
  if (showAnswer && q.explanation) {{
    html += `<div class="explanation"><strong>해설:</strong> ${{escapeHtml(q.explanation)}}</div>`;
  }}

  return html;
}}

// ── INIT ──
updateHomeStats();
</script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"index.html generated ({len(html):,} bytes)")
