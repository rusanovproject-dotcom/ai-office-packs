# Telegram Tools Pack — install manifest

Машиночитаемые метаданные для установки пака через промт-инструкцию в Claude Code.

## Metadata

```yaml
pack_id: telegram-tools
pack_type: tool-pack            # не agent, а набор скиллов/утилит
pack_name_human: Telegram Tools
short_role: Парсинг публичных Telegram-каналов, дайджесты, разбор HTML-экспорта
version: 1.0.0
requires: []
optional_deps:
  - curl (обычно уже есть)
  - awk, sed, grep (обычно уже есть)
  - python3 (для extras/parse-html-export)
  - beautifulsoup4 (только для extras; pip install beautifulsoup4)
```

## Files to copy

Источник: `_tool-packs/telegram/` в репозитории `github.com/rusanovproject-dotcom/ai-office-packs`
Цель: офис клиента (пути ниже)

```yaml
files:
  # Главный скилл — парсер публичных каналов
  - src: skills/telegram-channel-parser/SKILL.md
    dest: .claude/skills/telegram-channel-parser/SKILL.md
  - src: skills/telegram-channel-parser/scripts/
    dest: .claude/skills/telegram-channel-parser/scripts/
    recursive: true
  - src: skills/telegram-channel-parser/config/.env.example
    dest: .claude/skills/telegram-channel-parser/config/.env.example
  - src: skills/telegram-channel-parser/config/README.md
    dest: .claude/skills/telegram-channel-parser/config/README.md
  - src: skills/telegram-channel-parser/assets/
    dest: .claude/skills/telegram-channel-parser/assets/
    recursive: true
  - src: skills/telegram-channel-parser/.gitignore
    dest: .claude/skills/telegram-channel-parser/.gitignore

  # Extras — парсер HTML-экспорта (не скилл, а standalone скрипт)
  - src: extras/parse-html-export/parse_telegram.py
    dest: tools/telegram/parse_telegram.py

folders:
  # Создать пустые папки для кэша (они в .gitignore)
  - path: .claude/skills/telegram-channel-parser/cache
```

## Post-install steps

```yaml
post_install:
  - action: chmod_executable
    targets:
      - .claude/skills/telegram-channel-parser/scripts/*.sh
  - action: print_message
    message: |
      Готово. В офисе появились Telegram Tools.

      Что можно делать прямо сейчас:
      — «Дайджест канала @linear.app за неделю»
      — «Топ-10 постов из @notion за месяц»
      — «Найди все упоминания X в каналах Y и Z»
      — «Сравни активность двух каналов»

      Хочешь настроить категории для быстрых дайджестов?
      Скажи: «настрой дайджесты» — я помогу прописать .env.

      Для приватных каналов нужен отдельный MCP-сервер с повышенными
      требованиями безопасности. Подробности — в README пака.
```

## Message to client (after install)

```
Готово. В команде появились Telegram Tools.

Что умеет:
— парсить любой публичный TG-канал (посты, метрики, реакции)
— делать дайджесты по категориям (настраивается через конфиг)
— разобрать HTML-экспорт твоего канала в структурированные данные

Без токенов, без API, без настройки — работает сразу.

Попробуй прямо сейчас — скажи «дайджест @linear.app за неделю»
или назови свой любимый канал.
```

## Uninstall

```yaml
uninstall:
  remove_folders:
    - .claude/skills/telegram-channel-parser/
    - tools/telegram/
```
