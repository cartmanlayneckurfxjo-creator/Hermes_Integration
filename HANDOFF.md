# Hermes & Antigravity Integration — Handoff

**Дата актуализации:** 2026-09-04  
**Проект:** `C:\Users\may\.gemini\antigravity-ide\scratch\Hermes_Integration`  
**GitHub:** [cartmanlayneckurfxjo-creator/Hermes_Integration](https://github.com/cartmanlayneckurfxjo-creator/Hermes_Integration)  
**Текущий статус:** ACP протокол отлажен, дедлоки устранены, бот `antigravity` создан, проект задеплоен на GitHub, встроен статус-бар в Antigravity IDE.

---

## 1. Архитектура интеграции

```
┌──────────────────────────────────────────────────────────┐
│                   Antigravity IDE                        │
│   • Главный архитектор / Оркестратор                     │
│   • Status Bar: $(hubot) Hermes [antigravity] ⚡        │
│   • Extension: hermes-statusbar-1.0.0-universal          │
└──────────────────────────┬───────────────────────────────┘
                           │ Agent Client Protocol (ACP)
                           │ stdio (JSON-RPC 2.0 streaming)
                           ▼
┌──────────────────────────────────────────────────────────┐
│                hermes_acp_runner.py                      │
│   • Python ACP клиент (авто-одобрение, парсер файлов)    │
│   • Динамический поиск HERMES_DIR и HERMES_PYTHON        │
│   • Флаги: --save-file, --profile                        │
└──────────────────────────┬───────────────────────────────┘
                           │ subprocess (python -m acp_adapter)
                           │ env: HERMES_HOME=profiles/<name>
                           ▼
┌──────────────────────────────────────────────────────────┐
│                   Hermes Agent                           │
│   (Автономный агент / специализированные бот-профили)   │
│   • Profile: antigravity (<HERMES_DIR>/profiles/antigravity)│
│   • SOUL.md: Роль выделенного ко-пилота для Antigravity  │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTP / OpenAI API
                           ▼
┌──────────────────────────────────────────────────────────┐
│             Локальный / Внешний AI-шлюз                  │
│       (Провайдеры, Combos, fallback, квоты)             │
└──────────────────────────────────────────────────────────┘
```

---

## 2. Что сделано и зафиксировано

1. **Решение проблемы зависаний (Deadlock в Windows):**
   - Прямой запуск: `python.exe -m acp_adapter` из `hermes_acp_runner.py` без батников и утечек дескрипторов CMD.
   - Опция `--save-file <filename>`: сохранение кода из ACP-потока на диск клиентом за **~5 секунд** в обход виртуального bash-окружения на Windows.

2. **Поддержка бот-профилей (Hermes Bot Mode):**
   - Создан бот-профиль `antigravity` (`profiles/antigravity/SOUL.md`).
   - Поддержка переключения ботов через `--profile <name>`. Отклик: **4.6 сек**.

3. **Портативность путей:**
   - Код раннера и документация очищены от жестких путей.
   - Внедрен автопоиск через `HERMES_DIR` и `HERMES_PYTHON` (fallback на локальные пути).

4. **Деплой на GitHub:**
   - Репозиторий: **[https://github.com/cartmanlayneckurfxjo-creator/Hermes_Integration](https://github.com/cartmanlayneckurfxjo-creator/Hermes_Integration)**.
   - Чистый `README.md` без привязки к конкретным путям и локальным сервисам.

5. **Расширение статус-бара для Antigravity IDE:**
   - Установлено в: `C:\Users\may\.antigravity\extensions\hermes-statusbar-1.0.0-universal`.
   - Исходники в репозитории: `vscode-extension/`.
   - Функции: отображение активного бота и статуса шлюза, меню быстрого запуска задач ACP, переключение ботов.

---

## 3. Команды запуска

### Базовый запуск:
```bash
python hermes_acp_runner.py "Твой запрос" "путь_к_проекту"
```

### Генерация файла со сквозным сохранением:
```bash
python hermes_acp_runner.py "Напиши скрипт..." "путь_к_проекту" --save-file "myscript.py"
```

### Запрос к конкретному боту:
```bash
python hermes_acp_runner.py "Твоя задача" "путь_к_проекту" --profile antigravity
```

---

## 4. Следующие шаги
- Перезагрузить окно Antigravity (`Developer: Reload Window`) для отображения статус-бара.
- Настроить Combos / Fallback моделей при необходимости добавления нескольких нейросетей.
- Использовать бота `antigravity` для автономных исследовательских и тестовых задач.
