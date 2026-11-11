# Prompt Engineering Lab

## Hebrew

### תיאור הפרויקט
פרויקט זה מציג תהליך של Prompt Engineering מעשי: המרת הוראה בשפה טבעית לפקודת שורת פקודה של Windows, תוך שמירה על עקביות, אבטחה ויכולת ניתוח של טעויות בפרומפט.

המטרה המרכזית היא לא רק להפיק פקודה נכונה, אלא גם להבין כיצד ניסוח הפרומפט משפיע על התוצאה, כיצד מזהים מקרים שבהם המודל "נשבר", ומה צריך להוסיף כדי לשפר את הדיוק והבטיחות.

### מטרות הלמידה
- לבנות agent קטן שמקבל הוראה טבעית ומחזיר פקודת CLI
- לבדוק את השפעת ניסוח הפרומפט על איכות התשובה
- להעריך תוצאות על פי מדדים עקביים
- להוסיף שכבת אבטחה כדי לחסום פקודות מסוכנות
- להציג תהליך איטרטיבי של ניסוי, מדידה ושיפור

### ארגון הפרויקט
- `src/prompt_engineering_lab/agent.py` — הגדרת הפרומפטים ולוגיקת המרת המשפטים לפקודות
- `src/prompt_engineering_lab/app.py` — ממשק Gradio
- `src/prompt_engineering_lab/sandbox.py` — בדיקת אבטחה ומסנן פקודות מסוכנות
- `src/prompt_engineering_lab/llm_client.py` — אינטגרציה אופציונלית ל-OpenAI
- `prompt_iteration_1.csv` — איטרציה ראשונה
- `prompt_iteration_2.csv` — איטרציה שנייה
- `prompt_iteration_3.csv` — איטרציה שלישית

### דוגמאות לפקודות שנמצאות בתמיכה
- `ipconfig`
- `tasklist`
- `dir /o-s`
- `whoami`
- `hostname`
- `ver`

### שלבי הפיתוח
#### שלב א' — MVP ראשוני
- בניית גרסה בסיסית שמקבלת הוראה טבעית
- החזרת פקודת Windows אחת
- תיעוד התנהגות ראשונית

#### שלב ב' — ניתוח ושיפור
- זיהוי סוגי הוראות שהמנוע טועה בהם
- בדיקת פורמט, אבטחה ודיוק
- תיקון פרומפטים עם מיקוד בבעיה אחת
- הוספת מדדים כמו תקינות פורמט, תקינות תחבירית ואבטחה

### חוכמת הלקחים
הניסיון הראה כי:
- ניסוחים עמומים דורשים פירוט ברור יותר
- שינויים קטנים בפרומפט יכולים לשפר משמעותית את הדיוק
- הוספת כללים ברורים לגבי פלט יחיד, פורמט, וגם אבטחה, מפחיתה טעויות
- פקודות מסוכנות צריכות להידחות מוקדם, לפני שמגיעים להוצאה לפועל

### הפעלה
```bash
cd prompt-engineering-lab
uv run python -m prompt_engineering_lab.app
```

### הרצת בדיקות
```bash
cd prompt-engineering-lab
uv run pytest -q
```

### שכבת אבטחה
הפרויקט כולל שכבת בדיקה בסגנון sandbox שמעריכה כל פקודה לפי מצב:
- safe
- blocked
- requires_confirmation

דוגמאות לפקודות שנסגרות:
- `format`
- `shutdown`
- `restart`
- `rm -rf`
- מחיקת קבצים בצורה כללית ומסוכנת

---

## English

### Project Overview
This project demonstrates a practical Prompt Engineering workflow for converting natural-language instructions into safe Windows CLI commands.

The main goal is not only to generate a valid command, but also to understand how prompt wording affects model behavior, how to detect edge cases where the model fails, and how to improve reliability and safety through iterative refinement.

### Learning Goals
- Build a small agent that receives a natural-language instruction and returns a CLI command
- Examine how prompt wording influences response quality
- Evaluate outputs using consistent metrics
- Add a safety layer to block dangerous commands
- Demonstrate an iterative process of testing, measuring, and improving

### Project Structure
- `src/prompt_engineering_lab/agent.py` — prompt definitions and command-mapping logic
- `src/prompt_engineering_lab/app.py` — Gradio interface
- `src/prompt_engineering_lab/sandbox.py` — safety validation and blocked-command filtering
- `src/prompt_engineering_lab/llm_client.py` — optional OpenAI integration for real-model testing
- `prompt_iteration_1.csv` — first evaluation batch
- `prompt_iteration_2.csv` — second iteration
- `prompt_iteration_3.csv` — third iteration

### Supported command examples
- `ipconfig`
- `tasklist`
- `dir /o-s`
- `whoami`
- `hostname`
- `ver`

### Development Stages
#### Stage A — Initial MVP
- Create a basic version that accepts natural-language input
- Return exactly one Windows command
- Capture initial model behavior and failure patterns

#### Stage B — Analysis and Improvement
- Identify which types of requests are frequently misunderstood
- Check format, syntax, safety, and correctness
- Refine the prompt by addressing one issue at a time
- Add evaluation dimensions such as format consistency, syntax validity, and security

### Lessons Learned
The process showed that:
- Vague wording often leads to inconsistent outputs
- Small prompt changes can noticeably improve accuracy
- Clear instructions about output format and safety reduce errors
- Dangerous tasks should be rejected before execution is attempted

### Run the app
```bash
cd prompt-engineering-lab
uv run python -m prompt_engineering_lab.app
```

### Run tests
```bash
cd prompt-engineering-lab
uv run pytest -q
```

### Safety Layer
The project includes a sandbox-style validation layer that classifies each generated command as:
- safe
- blocked
- requires_confirmation

Examples of blocked patterns include:
- `format`
- `shutdown`
- `restart`
- `rm -rf`
- broad or recursive deletion patterns

### Final Assessment
This project is a strong example of an iterative Prompt Engineering workflow: it combines prompt design, testing, evaluation, and safety-aware behavior in a compact, understandable implementation suitable for coursework and demonstration purposes.
