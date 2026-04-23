# AI Office — Agent Packs

Модульные паки помощников для клиентских AI-офисов. Устанавливаются одной командой в Cursor / Claude Code.

## Что это

У клиента есть базовый AI-офис (Director + Strategist + Architect). Когда нужен дополнительный помощник — Дизайнер, Копирайтер, Продажник, Tech Lead — его не надо создавать руками. Он уже собран как **пак** в этом репозитории.

Клиент пишет в чате Claude Code / Cursor:

> *установи дизайнера*

И через 30 секунд в его офисе появляется рабочий Дизайнер с полным стеком знаний и скилов.

## Как это работает

### Если у клиента уже есть `install-agent` skill

```
установи дизайнера
```

Скилл:
1. Проверяет локальный `_agent-packs/designer/` — если нет, качает с GitHub
2. Копирует файлы в `office/agents/designer/`
3. Обновляет `office/AGENTS.md`, корневой `CLAUDE.md`, Director core.md
4. Оповещает клиента живым языком

### Если скилла `install-agent` ещё нет (первая установка)

Клиент копирует **bootstrap-промт** в Cursor / Claude Code — Claude сам скачивает скилл + первый пак с GitHub, ставит в офис, запускает установку.

Bootstrap-промт: см. `BOOTSTRAP.md` в этом репозитории.

## Структура репозитория

```
ai-office-packs/
├── README.md                 ← этот файл
├── BOOTSTRAP.md              ← готовый промт для первой установки
├── _agent-packs/             ← паки помощников-агентов
│   └── designer/             ← пак Дизайнера (Brand Book + Claude Design + Claude Code)
├── _tool-packs/              ← паки инструментов (не агенты, утилиты)
│   └── telegram/             ← Telegram Tools (парсинг каналов, дайджесты)
│       ├── install.md
│       ├── README.md
│       ├── skills/telegram-channel-parser/
│       └── extras/parse-html-export/
└── .claude/
    └── skills/
        └── install-agent/    ← универсальный установщик для agent-packs
            └── SKILL.md
```

## Доступные паки

### Agent-packs (помощники)
| Пак | Что делает | Статус |
|-----|------------|--------|
| `designer` | Brand Book + сам делает лендинги/обложки/презентации + Vercel-деплой | ✅ готов (v2.3) |
| `copywriter` | Тексты, посты, лендинги, рассылки | 🔜 в разработке |
| `sales` | КП, follow-up, продающие созвоны | 🔜 |
| `tech-lead` | Код, инфра, деплой | 🔜 |

### Tool-packs (инструменты)
| Пак | Что делает | Статус |
|-----|------------|--------|
| `telegram` | Парсинг публичных TG-каналов, дайджесты по категориям, разбор HTML-экспорта | ✅ готов (v1.0) |

## Как добавить новый пак

1. Создать `_agent-packs/<name>/` со структурой как у `designer/`
2. Написать `install.md` с метаданными (manifest)
3. Push в этот репозиторий
4. Пак автоматически доступен клиентам через `/install-agent <name>`

Подробные принципы интеграции — в исходном клиентском шаблоне: `office/AGENT-INTEGRATION-PRINCIPLES.md`.

## Raw URLs для bootstrap

Все файлы доступны через:
```
https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/<path>
```

Пример:
```
https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/.claude/skills/install-agent/SKILL.md
https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/_agent-packs/designer/install.md
```

## Автор

Никита Русанов, проект НейроШтаб. 2026.
