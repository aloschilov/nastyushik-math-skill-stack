# nastyushik-math-skill-stack

Лёгкий репозиторий для ведения **capability matrix** по математике: какие навыки уже держатся, какие требуют коротких повторений, и какие задания выдавать дальше.

[GitHub Pages dashboard](https://aloschilov.github.io/nastyushik-math-skill-stack/)

> Privacy note: репозиторий лучше создавать **private**. Внутри есть персонализированная обратная связь для ребёнка; при публикации замените имя/никнейм на нейтральное `student`.

## Для кого

- Ребёнок: Настюшик.
- Родитель/проверяющий: быстро видит, что проверять и на что делать акцент.
- Формат: маленькие дневные итерации, без перегруза и без резкого ухода в новые темы.

## Текущий фокус

К концу Дня 38 базовые уравнения, раскрытие скобок, особые случаи и текстовые задачи в целом держатся. Основной риск теперь не концептуальный, а операционный:

1. последний шаг в уравнении: если получилось \(2x = 8\), нужно писать \(x = 8 : 2 = 4\);
2. десятичные коэффициенты со знаками;
3. неравенства с отрицательным множителем, где знак нужно перевернуть;
4. смешанные задания без подсказки типа.

## Структура

```text
nastyushik-math-skill-stack/
├── AGENTS.md                         # repo-level инструкции для Codex
├── MATRIX.md                         # основная capability matrix
├── artifacts/generated/              # задания, ответы, обратная связь
├── artifacts/generated/source/dayNN/ # Markdown-исходники новых дневных PDF
├── artifacts/source_uploads/          # исходные решения, фото, контрольные
├── artifacts/nastyushik_repo_artifacts_full.zip
├── data/capability_matrix.csv         # табличная версия матрицы
├── data/artifacts_manifest.csv        # inventory файлов из полной сессии
├── docs/index.html                    # GitHub Pages dashboard
├── docs/day-notes.md                  # краткая история итераций
├── docs/latex-workflow.md             # Markdown -> Pandoc/XeLaTeX -> PDF
├── docs/skill-gates.md                # критерии: когда навык считать закреплённым
├── docs/parent-review-checklist.md    # чек-лист для проверки тетради
├── prompts/next-day-template.md       # шаблон запроса для следующего дня
├── prompts/session-prompts.md         # prompts исходной ChatGPT-сессии
├── scripts/build_day_pdfs.py          # сборка дневных PDF из Markdown
├── scripts/generate_dashboard.py      # сборка GitHub Pages dashboard
├── scripts/validate_matrix.py         # простая проверка CSV
└── .github/workflows/                 # CI-проверка и GitHub Pages deploy
```

Структура намеренно похожа на skill-stack подход: есть явная матрица возможностей, критерии прохождения и короткий цикл проверки.

## Формат формул

Repo-level правило для будущих генераций описано в [AGENTS.md](AGENTS.md): новые математические выражения задаются в LaTeX-нотации, например \(x^2\), \(-3x \le 12 \Rightarrow x \ge -4\), \(0{,}5x \cdot 8x^2 = 4x^3\).

Текущий стандарт: LaTeX-исходник в Markdown и отрендеренные формулы в PDF. В итоговых PDF ребёнок не должен видеть сырые маркеры вроде `\(`, `\le`, `\Rightarrow`. Локально уже доступны TeX-инструменты `pandoc`, `xelatex`, `latexmk`, `latex`, `dvipng`, `dvisvgm` и Poppler; устанавливать отдельный LaTeX-дистрибутив для этой конвенции не нужно.

Новые дневные комплекты собираются через [docs/latex-workflow.md](docs/latex-workflow.md): Markdown-исходники лежат в `artifacts/generated/source/dayNN/`, а PDF пересобираются командой:

```bash
python3 scripts/build_day_pdfs.py --day 44 --update-manifest --render-preview
```

## GitHub Pages dashboard

Dashboard публикуется из `docs/index.html`:

```text
https://aloschilov.github.io/nastyushik-math-skill-stack/
```

Публикация выполняется автоматически workflow `.github/workflows/pages.yml` при каждом push в `master` (а также вручную через `workflow_dispatch`). GitHub Pages доступен, потому что репозиторий публичный — на free plan Pages не поддерживается для приватных репозиториев.

Страница собирается командой:

```bash
python3 scripts/generate_dashboard.py
```

Она показывает capability matrix, ссылки на дневные задания/ответы, исходные решения Настюшика, prompts сессии и целевую контрольную:

```text
artifacts/source_uploads/pdfs/Экзамен по математике Настюшик.pdf
```

Крупные PDF, изображения и полный ZIP хранятся через Git LFS. Dashboard использует GitHub blob-ссылки на эти артефакты, чтобы Pages не нужно было тащить 1+ GB файлов в статический сайт.

## Как обновлять после нового дня

1. Добавить строку в `docs/day-notes.md`.
2. Обновить `MATRIX.md` и `data/capability_matrix.csv`, если изменился статус навыка.
3. Разложить новые PDF/фото в `artifacts/generated/` или `artifacts/source_uploads/`.
4. Обновить `data/artifacts_manifest.csv`, если добавились новые артефакты.
5. Сгенерировать следующий день по шаблону из `prompts/next-day-template.md`.
6. Для новых дневных PDF использовать Markdown/XeLaTeX workflow:

```bash
python3 scripts/build_day_pdfs.py --day NN --update-manifest --render-preview
```

7. Пересобрать dashboard и прогнать проверки:

```bash
python3 scripts/generate_dashboard.py
python3 scripts/validate_matrix.py
```

## Рекомендуемое имя GitHub-репозитория

```text
aloschilov/nastyushik-math-skill-stack
```

Рекомендуемая видимость: **private**.
