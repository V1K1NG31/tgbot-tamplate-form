# Changelog

User-visible changes for bot operators and template users.  
Internal-only refactors are omitted.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).  
Latest release at the **top**.

## [Unreleased]

Move items here while developing; cut a dated release when you publish.

### Added

- Root `README.md` and `docs/PROJECT_OVERVIEW.md`.
- Pytest suite under `tests/` (keyboards, Fluent, settings, Telegram utils).

### Changed

- Demo copy and menu labels: fictional brand “Svetlitsa”, no bankruptcy niche.
- Package and Docker artifacts: `tgbot-template-form` instead of `bfl`; compose service `bot`.
- **English-only UI:** default locale `en`, strings in `app/locales/en.ftl`; code comments and docs in English.

---

## [0.1.0] — 2026-03-22

### Added

- Changelog file.
