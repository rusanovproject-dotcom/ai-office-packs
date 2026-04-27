# Copywriter Pack — Draft (in design)

Курсовая версия копирайтера для магазина `_agent-packs/`. Адаптация существующего копирайтера из `ai-office-v2/office/agents/copywriter/` под мультитенант: чтобы устанавливался любому клиенту и при первом заходе сам собирал Voice DNA владельца.

## Статус

🟡 **In design, not built yet.** Здесь только research и концепт. Реальная реализация (`core.md`, `skills/`, `install.md`) ещё не написана.

## Что внутри

- **[design-research.md](design-research.md)** — полное проектное исследование (что брать из текущего копирайтера, что обобщить, что построить, индустриальные практики, концепция онбординга в 5 этапов)
- **[voice-dna-questions.md](voice-dna-questions.md)** — 13 вопросов для онбординга (рассказы вместо рефлексии) + 7 принципов + анти-паттерны + bonus
- **[templates/voice-dna-template.md](templates/voice-dna-template.md)** — шаблон артефакта `voice-dna.md` (19 секций)

## Откуда брать готовое

При имплементации копировать (с обобщением личных привязок):
- Системка: [`ai-office-v2/office/agents/copywriter/CLAUDE.md`](../../../ai-office-v2/office/agents/copywriter/CLAUDE.md)
- Скиллы: write-post, write-thread, write-ad, write-landing, write-longread (+2 knowledge), review-longread, content-factory, check-virality, image-gen
- Knowledge: dendygandy/ (стили + viralnost + temy-system), anti-patterns.md (75% универсально)
- Шаблон структуры пакета: [`_agent-packs/designer/`](../../_agent-packs/designer/)

## Что построить с нуля

- `skills/voice-dna-discovery/SKILL.md` — главный новый скилл (онбординг по 13 вопросам)
- `skills/voice-dna-revise/SKILL.md` — апдейт DNA по ходу работы (зеркало `brand-revise`)
- `templates/voice-dna-template.md` — каркас артефакта (19 секций)
- `templates/tone-axes-slider.html` — визуальный слайдер для Этапа 3 (4 оси Nielsen Norman Group)
- `knowledge/fallback-voice.md` — дженерик-голос пока DNA не собран

## Следующий шаг

Пилот онбординга на реальном клиенте → отладка вопросов → собрать `voice-dna-discovery/SKILL.md` целиком.
