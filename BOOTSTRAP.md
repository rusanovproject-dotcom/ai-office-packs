# Bootstrap — первая установка в уже работающий офис

Этот промт — **однократный bootstrap** для клиентов у которых уже есть базовый AI-офис, но ещё нет скилла `install-agent`. После применения этого промта — дальше всё работает обычной командой.

## Как использовать

1. Открой свой AI-офис в Cursor или Claude Code (папка с `CLAUDE.md`, `office/` и т.д.)
2. Скопируй промт ниже
3. Вставь в чат Claude
4. Claude скачает всё нужное и подключит Дизайнера

## Промт для копирования

```
Задача: подключить мне в офис Дизайнера из репозитория ai-office-packs.

Сделай следующее:

1. Создай папку .claude/skills/install-agent/ если её нет.

2. Скачай файл:
   https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/.claude/skills/install-agent/SKILL.md
   в .claude/skills/install-agent/SKILL.md

3. Создай папку _agent-packs/designer/ если её нет.

4. Скачай все файлы пака Дизайнера с GitHub в _agent-packs/designer/.
   Структура пака:
   - install.md
   - CLAUDE.md, core.md, overrides.md, memory.md, failures.md
   - knowledge/ (INDEX.md, design-catalog.md, design-stack-2026.md, landing-frameworks.md, edge-cases.md, how-to-design.md)
   - skills/ (brand-onboarding/SKILL.md, brand-revise/SKILL.md, claude-code-artifact/SKILL.md, claude-design-prompt/SKILL.md, creative-brief/SKILL.md)
   - templates/ (brand-book.md, design-brief.md)

   Базовый URL:
   https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/_agent-packs/designer/<путь-к-файлу>

   Используй GitHub API для получения списка файлов:
   https://api.github.com/repos/rusanovproject-dotcom/ai-office-packs/contents/_agent-packs/designer

   Или просто скачай все файлы из структуры выше через curl/wget.

5. После установки файлов — запусти /install-agent designer чтобы активировать Дизайнера в офисе.

6. Оповести меня одной фразой: "Дизайнер подключён, давай начнём с Brand Book?"

Важно:
- Не затирай overrides.md если он уже существует (клиентские правки)
- Не затирай memory.md и failures.md (накопленная память агента)
- Используй bash с curl для скачивания
```

## Что произойдёт

1. Claude создаст две папки — `.claude/skills/install-agent/` и `_agent-packs/designer/`
2. Скачает SKILL.md установщика и все файлы пака Дизайнера (~20 файлов)
3. Запустит `/install-agent designer` — активирует Дизайнера
4. Скажет живой фразой что готово

Время: ~30–60 секунд.

## После первой установки

Всё. Больше bootstrap не нужен — теперь в офисе есть скилл `install-agent`. Любой следующий пак ставится одной фразой:

> *установи копирайтера*

Когда будут готовы новые паки.

## Если что-то пошло не так

- Если Claude не может скачать — попроси его использовать `gh` CLI или `git clone`
- Если `install-agent` скилл не активируется после установки — перезапусти сессию Claude Code / Cursor
- Если остались ошибки — напиши Никите, разберёмся
