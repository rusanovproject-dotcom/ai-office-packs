#!/usr/bin/env bash
# AI Office Packs — universal installer
# Usage:
#   curl -sL https://raw.githubusercontent.com/rusanovproject-dotcom/ai-office-packs/main/install.sh | bash -s <pack-name>
#
# Examples:
#   curl -sL ...install.sh | bash -s telegram       # Telegram Tools
#   curl -sL ...install.sh | bash -s designer       # Designer agent
#   curl -sL ...install.sh | bash -s list           # Show available packs

set -e

PACK="${1:-}"
REPO="rusanovproject-dotcom/ai-office-packs"
REPO_URL="https://github.com/${REPO}.git"
TMP_DIR="/tmp/ai-office-packs-install-$$"

# ────────── Colors ──────────
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${BLUE}→${NC} $1"; }
ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
err()  { echo -e "${RED}✗${NC} $1" >&2; }

# ────────── Validate ──────────
if [[ -z "$PACK" ]]; then
    cat <<EOF

AI Office Packs — установщик

Usage:
  curl -sL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash -s <pack>

Packs:
  telegram     — Telegram Tools (парсинг каналов, дайджесты, HTML-экспорт)
  designer     — Дизайнер-агент (Brand Book + Claude Design + Claude Code)
  list         — показать все доступные паки

Repo: https://github.com/${REPO}

EOF
    exit 1
fi

# ────────── list ──────────
if [[ "$PACK" == "list" ]]; then
    cat <<EOF

Доступные паки:

  Agent-packs (агенты-помощники):
    designer     — Дизайнер (Brand Book + Claude Design + Claude Code + Vercel-деплой)

  Tool-packs (инструменты):
    telegram     — Telegram Tools (парсинг публичных каналов, дайджесты, HTML-экспорт)

Установка:
  curl -sL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash -s <name>

EOF
    exit 0
fi

# ────────── Check dependencies ──────────
if ! command -v git >/dev/null 2>&1; then
    err "git не установлен. Установи Git и попробуй снова."
    exit 1
fi

# ────────── Clone ──────────
info "Скачиваю ai-office-packs..."
git clone --depth=1 --quiet "$REPO_URL" "$TMP_DIR" 2>/dev/null || {
    err "Не смог склонировать репо. Проверь интернет и попробуй снова."
    exit 1
}

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

# ────────── Installers ──────────

install_telegram() {
    info "Устанавливаю Telegram Tools Pack..."

    local SRC="$TMP_DIR/_tool-packs/telegram"
    local SKILL_DIR="$HOME/.claude/skills/telegram-channel-parser"
    local EXTRAS_DIR="$HOME/workspace/tools/telegram"

    if [[ ! -d "$SRC" ]]; then
        err "Пак telegram не найден в репо. Проверь название."
        exit 1
    fi

    # Skill
    mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/config" "$SKILL_DIR/assets" "$SKILL_DIR/cache"
    cp -rf "$SRC/skills/telegram-channel-parser/"* "$SKILL_DIR/"
    chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true
    ok "Скилл установлен: $SKILL_DIR"

    # Extras
    mkdir -p "$EXTRAS_DIR"
    cp -f "$SRC/extras/parse-html-export/parse_telegram.py" "$EXTRAS_DIR/"
    cp -f "$SRC/extras/parse-html-export/README.md" "$EXTRAS_DIR/"
    ok "Парсер HTML-экспорта: $EXTRAS_DIR"

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ Telegram Tools установлены${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    cat <<EOF

Что попробовать прямо сейчас (в Claude Code / Cursor):

  • дайджест канала @linear.app за неделю
  • топ-10 постов из @notion за месяц
  • найди упоминания НейроШтаб в каналах X, Y, Z
  • сравни активность каналов A и B

Настройка категорий дайджестов (опционально):
  cp $SKILL_DIR/config/.env.example $SKILL_DIR/config/.env
  и отредактируй $SKILL_DIR/config/.env

Парсинг HTML-экспорта своего канала:
  смотри $EXTRAS_DIR/README.md

EOF
}

install_designer() {
    info "Устанавливаю Designer agent pack..."

    local SRC="$TMP_DIR/_agent-packs/designer"
    local INSTALL_SKILL_SRC="$TMP_DIR/.claude/skills/install-agent/SKILL.md"

    if [[ ! -d "$SRC" ]]; then
        err "Пак designer не найден."
        exit 1
    fi

    # Install-agent skill (для будущих установок по фразе)
    mkdir -p "$HOME/.claude/skills/install-agent"
    cp -f "$INSTALL_SKILL_SRC" "$HOME/.claude/skills/install-agent/SKILL.md"
    ok "Install-agent скилл готов"

    # Определяем целевой офис (CWD или $CLAUDE_OFFICE_PATH)
    local OFFICE="${CLAUDE_OFFICE_PATH:-$PWD}"
    if [[ ! -f "$OFFICE/CLAUDE.md" ]]; then
        warn "Не нашёл CLAUDE.md в текущей папке. Укажи путь к офису:"
        echo "  export CLAUDE_OFFICE_PATH=/path/to/your/office"
        echo "  и запусти скрипт снова"
        exit 1
    fi

    mkdir -p "$OFFICE/_agent-packs/designer"
    cp -rf "$SRC/"* "$OFFICE/_agent-packs/designer/"
    ok "Designer pack скопирован в $OFFICE/_agent-packs/designer/"

    echo ""
    cat <<EOF
${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}
${GREEN}✓ Designer pack скачан${NC}
${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}

Финальный шаг — в Claude Code / Cursor в своём офисе скажи:

  установи дизайнера

Install-agent skill развернёт агента: обновит AGENTS.md, корневой CLAUDE.md,
Director core.md. Через 30 секунд Дизайнер — в команде.

EOF
}

# ────────── Route ──────────
case "$PACK" in
    telegram)  install_telegram ;;
    designer)  install_designer ;;
    *)
        err "Неизвестный пак: $PACK"
        echo ""
        echo "Доступные: telegram, designer"
        echo "Список: curl -sL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash -s list"
        exit 1
        ;;
esac
