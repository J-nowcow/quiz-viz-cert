#!/usr/bin/env python3
"""Parse quiz markdown files into JSON for the web app."""
import re
import json
import sys

def parse_md(filepath, exam_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    questions = []
    subject = 0
    subject_names = {
        1: "경영정보 일반",
        2: "데이터 해석 및 활용",
        3: "경영정보시각화 디자인"
    }

    # Split by ### Q pattern
    parts = re.split(r'### Q(\d+)\n', content)
    # parts[0] = header, parts[1] = "1", parts[2] = Q1 content, parts[3] = "2", parts[4] = Q2 content, ...

    for i in range(1, len(parts) - 1, 2):
        q_num = int(parts[i])
        q_content = parts[i + 1]

        # Determine subject based on question number
        if q_num <= 20:
            subject = 1
        elif q_num <= 40:
            subject = 2
        else:
            subject = 3

        # Extract answer number from the success callout
        answer_match = re.search(r'>\s*\*\*([①②③④])', q_content)
        if answer_match:
            symbol = answer_match.group(1)
            answer_map = {'①': 1, '②': 2, '③': 3, '④': 4}
            answer = answer_map.get(symbol, 0)
        else:
            print(f"WARNING: No answer found for {exam_name} Q{q_num}", file=sys.stderr)
            answer = 0

        # Extract explanation (everything after the answer symbol line in the callout)
        expl_match = re.search(r'>\s*\*\*[①②③④].*?\*\*\s*(?:—\s*)?(.+?)?\n(?:>\s*(.+?))?(?:\n|$)', q_content)
        explanation = ""
        # Get all lines in the success callout after the answer line
        callout_match = re.search(r'> \[!success\]- 정답\n((?:>.*\n?)*)', q_content)
        if callout_match:
            callout_lines = callout_match.group(1).strip().split('\n')
            # First line has the answer, check for explanation after closing **
            first_line = callout_lines[0]
            # Pattern: > **④ text** — explanation  OR  > **② text**
            after_close = re.search(r'\*\*\s*(?:—\s*)?(.+)$', first_line)
            if after_close:
                expl_text = after_close.group(1).strip()
                # Remove any remaining markdown bold markers
                expl_text = expl_text.replace('**', '').strip()
                if expl_text:
                    explanation = expl_text
            # Additional explanation lines
            for line in callout_lines[1:]:
                line = line.lstrip('> ').strip().replace('**', '')
                if line:
                    if explanation:
                        explanation += " " + line
                    else:
                        explanation = line

        # Split content before the callout to get question text and choices
        before_callout = q_content.split('> [!success]')[0].strip()

        # Remove trailing ---
        before_callout = re.sub(r'\n---\s*$', '', before_callout).strip()

        # Extract choices
        choices = []
        choice_pattern = re.compile(r'^([①②③④])\s*(.+)$', re.MULTILINE)
        choice_matches = list(choice_pattern.finditer(before_callout))

        for cm in choice_matches:
            choices.append(cm.group(2).strip())

        # Question text is everything before the first choice
        if choice_matches:
            q_text = before_callout[:choice_matches[0].start()].strip()
        else:
            q_text = before_callout.strip()

        # Clean up question text - remove leading/trailing whitespace and normalize quotes
        # Handle blockquotes in question text (context)
        q_text = q_text.strip()

        questions.append({
            "exam": exam_name,
            "subject": subject,
            "subjectName": subject_names[subject],
            "questionNumber": q_num,
            "text": q_text,
            "choices": choices,
            "answer": answer,
            "explanation": explanation
        })

    return questions


def main():
    base = "/Users/hyunwoo/Documents/FirstBrain/20_Resources/Studies/경영정보시각화"
    files = [
        (f"{base}/문제 - 모의고사 A형.md", "모의고사 A형"),
        (f"{base}/문제 - 모의고사 B형.md", "모의고사 B형"),
        (f"{base}/문제 - 2024 제1회 기출.md", "2024 제1회 기출"),
    ]

    all_questions = []
    for filepath, exam_name in files:
        qs = parse_md(filepath, exam_name)
        print(f"{exam_name}: {len(qs)} questions parsed", file=sys.stderr)
        all_questions.extend(qs)

    print(f"Total: {len(all_questions)} questions", file=sys.stderr)

    # Verify answer distribution
    for exam_name in ["모의고사 A형", "모의고사 B형", "2024 제1회 기출"]:
        exam_qs = [q for q in all_questions if q["exam"] == exam_name]
        no_answer = [q for q in exam_qs if q["answer"] == 0]
        no_choices = [q for q in exam_qs if len(q["choices"]) != 4]
        if no_answer:
            print(f"  {exam_name}: {len(no_answer)} questions missing answers: {[q['questionNumber'] for q in no_answer]}", file=sys.stderr)
        if no_choices:
            print(f"  {exam_name}: {len(no_choices)} questions without 4 choices: {[q['questionNumber'] for q in no_choices]}", file=sys.stderr)

    # Output JSON
    print(json.dumps(all_questions, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
