# LaTeX Workflow

Новые дневные PDF собираются из Markdown через Pandoc и XeLaTeX. Это основной путь для Дня 45 и дальше.

## Структура

```text
artifacts/generated/source/dayNN/
├── feedback_child.md
├── feedback_parent.md
├── tasks.md
└── answers.md
```

Каждый файл начинается с front matter:

```yaml
---
title: "День NN. Задания"
subtitle: "Для Настюшика. Время: 45-55 минут."
output: "artifacts/generated/tasks/denNN_zadaniya_Nastyushik.pdf"
footer-left: "Настюшик - математика, 7 класс"
---
```

## Формулы

- Inline: `\( ... \)`.
- Display: `\[ ... \]`.
- Десятичные дроби: `\(1{,}5x\)`.
- Не сдавать PDF, где видны буквальные `\(`, `\le`, `\Rightarrow`, `\circ`, `\cdot`.
- В пользовательских PDF не использовать длинные Markdown backticks для имён файлов или технических ссылок: они рендерятся monospace и могут портить верстку.

## Сборка

```bash
python3 scripts/build_day_pdfs.py --day NN --update-manifest --render-preview
```

Скрипт:

- собирает все `*.md` из `artifacts/generated/source/dayNN/`;
- использует `templates/day-material.tex`;
- обновляет PDF по путям из `output:`;
- проверяет количество страниц через `pdfinfo`;
- проверяет отсутствие сырых LaTeX-маркеров через `pdftotext`;
- при `--render-preview` кладёт PNG-превью в `tmp/pdfs/rendered_check/`;
- при `--update-manifest` обновляет `data/artifacts_manifest.csv`.

После сборки нужно визуально посмотреть PNG-превью и пересобрать dashboard:

```bash
python3 scripts/generate_dashboard.py
python3 scripts/validate_matrix.py
git diff --check
```

## Зависимости

Локально уже доступны `pandoc`, `xelatex`, `latexmk`, `pdftotext`, `pdftoppm` и `pdfinfo`.

Шаблон предпочитает `PT Serif` для основного текста и `PT Sans` для заголовков. Если этих шрифтов нет, используются системные fallback-шрифты с кириллицей.

ReportLab-генераторы в `scripts/generated/` остаются историческими. Для новых дней использовать Markdown/Pandoc/XeLaTeX, если нет отдельной причины делать иначе.
