# Copywriter Pack — Design Research

Проектное исследование курсовой версии копирайтера. Дата: 2026-04-27. Авторы: Sergey + Claude (Демиург-режим).

---

## 1. Контекст задачи

**Проблема:** копирайтер в `ai-office-v2/office/agents/copywriter/` заточен под голос Никиты лично (исповедальный бунт, бунтарь с дневником). Не переиспользуем для других людей.

**Цель:** адаптировать копирайтера так, чтобы (а) был качественный универсальный движок, (б) при заходе в новый офис клиента сам собирал Voice DNA владельца, (в) писал в его голосе так, чтобы подписчики не отличали.

**Магазин:** `ai-office-packs/_agent-packs/` (есть designer, telegram). Копирайтер ещё не вынесен.

---

## 2. Аудит существующего копирайтера

Прочитан полностью: системка (298 строк) + 5 файлов knowledge + 9 скиллов + 6 файлов dendygandy.

### Что брать как есть (~60% объёма)

Универсальные движки, работают на любом голосе:

- `knowledge/dendygandy/INDEX.md` — концепция «голос автора + палитра тонов поверх»
- `knowledge/dendygandy/viralnost.md` — 5-этапный QA-чекер (12 критериев хука + 11 типов AI-маркеров + связность + 3 читателя + скальпель)
- `knowledge/dendygandy/temy-system.md` — 11 кластеров переживаний + 5 фильтров
- `knowledge/dendygandy/styles/` — 3 стиля-референса (Дерзкий/Лёгкий/Сторителлинг — переименовать без имён авторов)
- `skills/check-virality/SKILL.md`
- `skills/write-thread/SKILL.md` — Content Web хуки, формулы фасцинации
- `skills/content-factory/SKILL.md` — конвейер темы→стили→тексты→QA
- `skills/write-longread/SKILL.md` + 2 knowledge-базы (longreads + US-experts на 54К символов)
- `skills/review-longread/SKILL.md` — 3 линзы (Хормози + рунет + US-эксперты)
- `skills/write-landing/SKILL.md` — структура блоков универсальна
- 9 заповедей в CLAUDE.md (строки 281-289) — готовая методичка
- `FAILURES.md` как формат + 6 failures как **демо-кейс для курса**

### Что обобщить (~30%)

Хорошая логика, но завязано на Никиту:

- `CLAUDE.md` строки 1-15, 220-243 — заменить «голос Никиты», «исповедальный бунт» на слоты `{{CLIENT_NAME}}`, `{{VOICE_ARCHETYPE}}`
- Строка 28: путь `~/workspace/knowledge/brand/brief-for-methodologist.md` — критический баг, у клиента не будет
- `knowledge/style-dna.md` (264 строки) — превратить в `style-dna-template.md` (пустой каркас) + конкретный заполняется через `voice-dna-discovery`
- `knowledge/audience.md` — удалить (дубль с артефактом Маркетолога в `hub/marketing/audience.md`)
- `knowledge/examples.md` — превратить в `examples-template.md`, заполняется автоматически
- `knowledge/anti-patterns.md` — 75% универсально, чистить 25% про Никиту
- `skills/write-post`, `write-ad`, `write-landing`, `image-gen` — заменить примеры Life-OS на нейтральные

### Что выкинуть

- `MEMORY.md` записи Никиты (Татьяна-риэлторы, presell-лонгрид, Core Offer) — личный лог
- Жёсткие пути `~/workspace/...` — заменить на `office/...`

### Гениальные фишки Никиты для курса (продают курс)

Чего нет в массовых копирайтинг-курсах:

1. **Стили = палитра тонов поверх голоса автора** — синтез «найди свой голос» + «копируй известных»
2. **5-этапный QA с виральным скальпелем** — уровень редакции газеты внутри AI-агента
3. **Скоринг 35/50 как gate** — формализация чуйки в 5 параметров
4. **Stop-slop ≠ кастрация** — никто не предупреждает что чистка убивает живость
5. **3-линзовое ревью лонгридов** (Хормози + рунет + US) — фильтр западных фреймворков через скепсис рунета
6. **Тандем write-longread + review-longread** — compound engineering на копирайтинге
7. **Контент-фабрика** — конвейер темы→стили→тексты→QA в одном промпте
8. **9 заповедей** — готовая методичка на одну страницу
9. **FAILURES.md** — методология исправляет себя через зафиксированные ошибки
10. **Шаг -1 анализ ЦА** — без него текст не пишется

---

## 3. Главная дыра — Voice DNA Discovery

### Что есть

`knowledge/style-dna.md` собран Демиургом ВРУЧНУЮ из 400+ постов и 350+ анкет. У клиента такого ресурса не будет.

### Что нужно построить

Скилл `/voice-dna-discovery` — зеркало `brand-onboarding` у дизайнера. Главный новый скилл, без которого пак неработоспособен на чужом голосе.

---

## 4. Индустриальные практики Voice DNA

Синтез из Mailchimp, Nielsen Norman Group, Jasper Brand Voice, Writer.com, Premium Ghostwriting Academy (Cole), ship30for30, copyhackers (Joanna Wiebe).

### 15 категорий профиля голоса

1. **Archetype** — 12 архетипов Mark&Pearson; обычно гибрид: Justin Welsh = Sage+Everyman, Dan Koe = Rebel+Magician
2. **Tone-axes** (Nielsen Norman Group) — 4 слайдера 1-5: Funny↔Serious, Formal↔Casual, Respectful↔Irreverent, Matter-of-fact↔Enthusiastic
3. **Lexicon** — power-words, banned-words, замены
4. **Syntax** — средняя длина предложения, fragments
5. **Rhythm** — длина абзаца, паттерн «1-3-1» (Cole в ship30)
6. **Hooks** — 5 формул открытий
7. **Closings** — 5 формул финалов + подпись
8. **Themes** — 5 core + 5 taboo
9. **Метафоры** — из какой области
10. **Story types** — соотношение я/клиент/абстрактное
11. **Emotional range** — как звучит когда злится/радуется
12. **Humor type** — самоирония / сухой / сарказм / observational
13. **POV** — я/мы/ты
14. **Cultural references** — кого цитирует
15. **Formatting** — emoji, bold, CAPS, bullets

### Три рабочих workflow

**A. Premium Ghostwriting Academy (Cole)** — золотой стандарт. 4 шага, ~2 недели:
1. Voice Mining (50-100 постов + голосовые)
2. Voice Decoding Interview (2 часа)
3. Pattern Extraction (ручная разметка 30-50 постов)
4. Validation Loop (5-10 итераций, drop rate 60% → 5-10%)

**B. Jasper / Writer.com** — AI-инструмент. JSON profile + few-shot + RAG style guide. Под капотом промпт-сэндвич:
```
[SYSTEM] Voice profile JSON
[USER] Brief
[EXAMPLES] 3-5 best posts (few-shot verbatim)
[CONSTRAINTS] banned words, required patterns
```

**C. Joanna Wiebe / Copyhackers** — Voice of Customer + Author Voice. Голос автора = голос клиента + добавки автора. Mining реальных слов клиентов из reviews/support/sales calls.

### Stop-slop актуальный 2026 (русский)

**Слова-флаги:** в современном мире, играет ключевую роль, тонкости и нюансы, многогранный, безусловно, уникальный, погрузиться, раскрыть потенциал, комплексный подход.

**Главные фразы:**
- «Не просто X, а Y» — топ-маркер 2025-2026
- «Стоит отметить, что…», «Важно понимать, что…», «Давайте разберёмся»

**Структурные:** em-dashes (—) в избытке, идеально симметричные абзацы по 3-4 строки, bullet lists всегда по 5, идеальные topic sentences.

**Семантические:** отсутствие конкретики, hedging («может быть», «как правило»), морализаторские концовки.

### Что Никита делает лучше индустрии

| Фишка | Индустрия | Никита |
|---|---|---|
| Скоринг текста | Нет / абстрактный | Жёсткий 35/50 gate |
| Anti-AI чистка | Чистят и отдают | Stop-slop ≠ кастрация |
| QA перед публикацией | Один проход | 5-этапный (хуки + AI + связность + 3 читателя + скальпель) |
| Ревью лонгрида | Хормози ИЛИ рунет ИЛИ US | 3 линзы одновременно + 100-балльный скоринг |
| Стили | «Найди свой голос» ИЛИ «копируй известных» | Палитра тонов ПОВЕРХ голоса автора |
| Обучение методологии | Слайды + теория | FAILURES.md — реальные ошибки в реальном времени |

---

## 5. Концепция онбординга — 5 этапов

```
ЭТАП 1: ВХОД + РАЗВИЛКА          (3-5 мин)
   ↓
ЭТАП 2: VOICE MINING             (15-30 мин)
   ├── Путь A: анализ текстов клиента
   ├── Путь B: 13 живых вопросов
   └── Путь C: «веди сам» (заготовка по нише)
   ↓
ЭТАП 3: ARCHETYPE + TONE-AXES    (5-10 мин)
   ↓
ЭТАП 4: ВАЛИДАЦИЯ                (15-20 мин)
   └── 3 варианта тестового текста → выбор → правка DNA
   ↓
ЭТАП 5: ФИНАЛИЗАЦИЯ              (5 мин)
   └── voice-dna.md + 5 артефактов готовы
```

Итого: **45-70 минут**. Можно разбить на 2 захода.

### Этап 1 — Вход + развилка

Развилка как в `brand-onboarding`:

```
А. У тебя есть свои тексты — кинь 5-10 штук.
   Я сам вытащу паттерны. Самый точный путь.

Б. Текстов мало или их нет — ответь на 13 вопросов.
   По одному, минут 25-30.

В. «Веди сам» — дашь нишу и 1-2 имени-якоря.
   Соберу заготовку, потом уточним на тестах.
```

Все три пути сходятся в Этапе 4 (валидация).

### Этап 2 — Voice Mining

Главный этап. См. отдельный файл [voice-dna-questions.md](voice-dna-questions.md) — 13 вопросов с обоснованиями, принципами и анти-паттернами.

**Путь A (анализ текстов)** — silent mining:
- Лексика (топ-30 нестандартных слов)
- Фразы-маркеры (открытия/связки/финалы)
- Синтаксис, ритм
- Эмоциональный профиль
- Любимые приёмы
- Темы-якоря и табу
- Противоречия (если стиль разный в разных каналах)

**Путь B (13 вопросов)** — рассказы вместо рефлексии. Принцип: голос невозможно узнать, спросив про голос — спрашиваем про утро, про шарлатанов в нише, про последний срыв.

**Путь C (веди сам)** — собираем заготовку по нише + якорям из knowledge-базы.

### Этап 3 — Archetype + Tone-axes

Не абстрактный опросник. Показываем 8 архетипов как пары авторов:

```
🧙 Мудрец (Naval) — афоризмы, спокойствие
🦹 Бунтарь (Dan Koe) — провокация, гнев на mediocrity
👨 Простой парень (Justin Welsh) — без понтов
🧝 Маг (Tim Ferriss) — лайфхаки, эксперименты
🃏 Шут (Marie Forleo) — самоирония
🦸 Герой (David Goggins) — преодоление
⚓ Заботливый — «ты не один»
🔮 Творец — концепции, картины будущего
```

У эксперта обычно гибрид 2 архетипов.

**Tone-axes** (4 слайдера 1-5) — желательно визуально HTML-страничкой.

**Tone matrix** (Mailchimp) — голос один, тон вариативен по контексту:

| Контекст | Funny | Casual | Irreverent | Enthusiastic |
|---|---|---|---|---|
| Пост ТГ | 3 | 5 | 4 | 4 |
| Лендинг | 2 | 4 | 3 | 5 |
| Email | 2 | 4 | 2 | 3 |
| Коммент | 4 | 5 | 4 | 3 |

### Этап 4 — Валидация (изобретаем сами)

Этого нет нигде в индустрии. Voice ≠ Brand Book — голос проверяется только на тексте.

**3 итерации максимум:**

**Итерация 1:**
- Копирайтер берёт нейтральную тему
- Пишет 3 коротких поста (~500 знаков), каждый — слегка разный микс DNA
- Клиент даёт реакцию: ✅ Mine / 🟡 Близко но... / ❌ Fake

**Итерация 2:**
- Берём правки, обновляем DNA, помечаем в `## История эволюции`
- Пишем ЕЩЁ 2 текста на новой теме
- Цель: 80%+ совпадение

**Итерация 3 (если нужна):**
- Сложный тест: пишем в выбранном тоне из tone matrix

**Drop rate** правок (от Cole) — метрика готовности: с 60% упасть до 5-10% за 3 итерации.

**Артефакт:** `voice-dna-validation.log.md` — все 5-9 тестовых текстов + реакции + diff. Это **обучающий датасет** для будущих few-shot промптов.

### Этап 5 — Финализация

5 артефактов на выходе:

```
office/agents/copywriter/knowledge/
├── voice-dna.md                  # ⭐ главный — 19 секций
├── voice-samples/                # сырые тексты клиента (Путь A)
├── examples.md                   # 7-10 дословных цитат + few-shot
├── voice-dna-validation.log.md   # тестовые тексты + diff (датасет)
└── voice-evolution.md            # append-only история изменений
```

См. шаблон в [templates/voice-dna-template.md](templates/voice-dna-template.md).

---

## 6. Структура курсового пака

```
_agent-packs/copywriter/
│
├── CLAUDE.md                           # @core.md @overrides.md (3 строки)
├── core.md                             # системка обобщённая
├── overrides.md                        # клиентские правила, не затирается
├── memory.md, failures.md              # пустые шаблоны
├── install.md                          # манифест + first-task + message-to-client
├── CREDITS.md                          # источники
│
├── knowledge/
│   ├── INDEX.md                        # карта клиенту: 5 вещей
│   ├── style-dna.md                    # ПУСТОЙ ШАБЛОН
│   ├── examples.md                     # ПУСТОЙ ШАБЛОН
│   ├── anti-patterns.md                # обобщённые
│   ├── fallback-voice.md               # дженерик-голос
│   │
│   └── styles/                         # переименовано из dendygandy/, без имён
│       ├── INDEX.md
│       ├── viralnost.md
│       ├── temy-system.md
│       ├── derzky.md / derzky-examples.md
│       ├── lyogkiy.md / lyogkiy-examples.md
│       └── storyteller.md / storyteller-examples.md
│
├── skills/
│   ├── voice-dna-discovery/            # ⭐ НОВЫЙ — главное
│   ├── voice-dna-revise/               # НОВЫЙ — апдейт DNA
│   ├── write-post / write-thread / write-ad / write-landing / image-gen
│   ├── write-longread/ + 2 knowledge-базы
│   └── review-longread, content-factory, check-virality
│
└── templates/
    ├── voice-dna-template.md           # каркас для discovery (19 секций)
    ├── tone-axes-slider.html           # визуальный слайдер
    ├── post-frontmatter.md
    ├── longread-skeleton.md
    └── ad-3-variants.md
```

---

## 7. Подача в курсе — 7 уроков

1. **5 мин** — `/install-agent copywriter`
2. **15-30 мин** — `/voice-dna-discovery` → собираем голос
3. **15 мин** — первый пост → `/check-virality`
4. **10 мин** — палитра стилей (дерзкий/лёгкий/сторителлинг)
5. **20 мин** — `/content-factory [ниша], 7, посты` → пакет на неделю
6. **1 час** — `/write-longread` presell + `/review-longread`
7. **10 мин** — `overrides.md` + `failures.md` как личная методичка

За 2-3 часа клиент выходит на полный продакшн-цикл. **Это и есть демка курса.**

---

## 8. Источники

### Индустриальные

**Style guides (open source):**
- styleguide.mailchimp.com — золотой стандарт
- primer.style/brand/content — GitHub
- atlassian.design/content/voice-and-tone

**Frameworks:**
- nngroup.com/articles/tone-of-voice-dimensions — 4 tone-axes
- *The Hero and the Outlaw* (Mark & Pearson, 2001) — 12 архетипов

**Ghostwriting:**
- *The Art and Business of Ghostwriting* (Nicolas Cole, 2023)
- ship30for30.com — Cole + Dickie Bush
- copyhackers.com — Joanna Wiebe, Voice of Customer

**AI-tools docs:**
- jasper.ai/features/brand-voice
- writer.com/product/brand-voice

### Vоice discovery / interview techniques

- Rob Fitzpatrick *The Mom Test* (2013) — конкретный случай вместо обобщения
- Dan McAdams *The Stories We Live By* (1993) — Life Story Interview
- James Pennebaker *The Secret Life of Pronouns* (2011) — function words
- Indi Young *Practical Empathy* (2015), *Time to Listen* (2022)
- Bob Moesta *Demand-Side Sales 101* (2020) — JTBD forensic interview
- William Labov — структура нарратива (1972)
- Tim Ferriss *Tools of Titans* (2016) — sensory ritual questions
- Studs Terkel *Working* (1974) — народное интервью через детали
- Sally Hogshead *How the World Sees You* (2014) — Anthem methodology
- Donald Miller *Building a StoryBrand* (2017) — BrandScript
- Miller & Rollnick *Motivational Interviewing* (4-е изд., 2023)

### Локальные источники для миграции

- `ai-office-v2/office/agents/copywriter/` — основа
- `ai-office-v2/demiurg/knowledge/examples/copywriter-v1.md` — архитектурный образец (562 строки)
- `project-x/products/quiz-chat/NIKITA-VOICE-GUIDE.md` — эмпирический voice guide (375 строк, 20+ реальных постов)
- `ai-office-packs/_agent-packs/designer/` — образец структуры пакета
- `neuroshtab-template-client/.claude/skills/strategist-intake/` — образец сбора по одному вопросу
- `neuroshtab-template-client/.claude/skills/interview/` — образец вопросов строящихся друг на друге

---

## 9. Что дальше

1. **Пилот онбординга** на реальном клиенте → проверить буксует ли где-то
2. По итогам — собрать `skills/voice-dna-discovery/SKILL.md` целиком
3. Параллельно — мигрировать универсальные части (`dendygandy/`, `check-virality`, `write-longread`) в структуру пака
4. Обобщить системку (`CLAUDE.md` → `core.md`) — параметризовать `{{CLIENT_NAME}}`
5. Написать `install.md` (манифест установки) по образцу designer-пака
6. После этого — пак готов к включению в каталог `/install-agent copywriter`
