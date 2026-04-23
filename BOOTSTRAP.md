# Как установить пак — одной командой

Открой **терминал** (Terminal на macOS / iTerm / Warp / встроенный терминал Cursor).

Скопируй нужную команду, вставь, нажми Enter. Установка — ~30 секунд.

---

## Telegram Tools — парсинг каналов, дайджесты

```bash
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s telegram
```

**После установки** — открой свой AI-офис в Claude Code / Cursor и попробуй:

- *«дайджест канала @linear.app за неделю»*
- *«топ-10 постов из @notion за месяц»*
- *«найди упоминания X в каналах Y, Z»*
- *«сравни активность каналов A и B»*

Без токенов, без настройки. Работает сразу.

---

## Designer — дизайнер-агент

```bash
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s designer
```

**Перед запуском** установи переменную `CLAUDE_OFFICE_PATH` — путь к твоему AI-офису (или просто запусти `cd` в папку офиса):

```bash
cd ~/workspace/my-office
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s designer
```

**После установки** в Claude Code в своём офисе скажи:

> *установи дизайнера*

Через 30 секунд Дизайнер — в команде. Дальше:

- *«собери мне Brand Book для моего проекта»*
- *«сделай лендинг под услугу»*
- *«обложка для Telegram канала»*
- *«выложи этот сайт на живой URL»* (Vercel-деплой)

---

## Список всех паков

```bash
curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s list
```

Покажет что доступно прямо сейчас.

---

## Что если нет доступа к GitHub

В странах где GitHub заблокирован — используй VPN или Cloudflare WARP. Репозиторий публичный, доступен со всего мира.

## Если установка сломалась

1. Проверь что установлен `git`: `git --version`
2. Проверь интернет: `curl -I https://github.com`
3. Запусти с debug: `bash -x` вместо `bash`:
   ```bash
   curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -x -s telegram
   ```
4. Напиши Никите с логом ошибки.

---

## Безопасность

Скрипт `install.sh` — публичный, читай перед запуском:
https://github.com/rusanovproject-dotcom/ai-office-packs/blob/main/install.sh

Он делает только:
- `git clone` этого репо во временную папку
- Копирует файлы в `~/.claude/skills/` и `~/workspace/tools/` (или `CLAUDE_OFFICE_PATH`)
- `chmod +x` на bash-скрипты
- Удаляет временную папку

**Ничего не отправляет наружу, не просит права root, не устанавливает системные пакеты.**
