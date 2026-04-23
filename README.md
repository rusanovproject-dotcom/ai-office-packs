# AI Office — Agent Packs

Модульные паки помощников и инструментов для AI-офисов. Устанавливаются **одной командой в терминале**.

## Быстрый старт — одна строка

```bash
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s telegram
```

Это установит Telegram Tools. Вместо `telegram` — любое имя пака (см. ниже).

## Доступные команды

```bash
# Список всех паков
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s list

# Telegram Tools (парсинг публичных каналов, дайджесты)
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s telegram

# Designer agent (Brand Book + Claude Design + Vercel-деплой)
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s designer
```

После установки пака — открываешь свой AI-офис в Claude Code и сразу пользуешься.

## Что это

У клиента есть базовый AI-офис (Director + Strategist + Architect). Дополнительные помощники и инструменты — паки, которые ставятся по мере нужды.

**Два типа паков:**
- **Agent-packs** — помощники-агенты (Дизайнер, Копирайтер, Продажник). Получают свою папку в `office/agents/`.
- **Tool-packs** — наборы скиллов/утилит (Telegram-инструменты, SEO, аналитика). Копируются в `.claude/skills/` и `tools/`.

## Как это работает

1. Ученик запускает `install.sh` с именем пака
2. Скрипт делает `git clone` этого репо во временную папку
3. Читает нужный пак, копирует файлы в правильные места
4. Делает `chmod +x` на скрипты, создаёт папки кэша
5. Удаляет временную папку, показывает что дальше

Для agent-packs — скрипт кладёт `install-agent` skill в `.claude/skills/`, и дальше в Claude Code можно говорить «установи дизайнера» — агент активируется в офисе.

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
