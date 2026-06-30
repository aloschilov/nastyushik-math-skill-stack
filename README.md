# nastyushik-math-skill-stack

Лёгкий репозиторий для ведения **capability matrix** по математике: какие навыки уже держатся, какие требуют коротких повторений, и какие задания выдавать дальше.

> Privacy note: репозиторий лучше создавать **private**. Внутри есть персонализированная обратная связь для ребёнка; при публикации замените имя/никнейм на нейтральное `student`.

## Для кого

- Ребёнок: Настюшик.
- Родитель/проверяющий: быстро видит, что проверять и на что делать акцент.
- Формат: маленькие дневные итерации, без перегруза и без резкого ухода в новые темы.

## Текущий фокус

К концу Дня 38 базовые уравнения, раскрытие скобок, особые случаи и текстовые задачи в целом держатся. Основной риск теперь не концептуальный, а операционный:

1. последний шаг в уравнении: если получилось `2x = 8`, нужно писать `x = 8 : 2 = 4`;
2. десятичные коэффициенты со знаками;
3. неравенства с отрицательным множителем, где знак нужно перевернуть;
4. смешанные задания без подсказки типа.

## Структура

```text
nastyushik-math-skill-stack/
├── MATRIX.md                         # основная capability matrix
├── artifacts/generated/              # задания, ответы, обратная связь
├── artifacts/source_uploads/          # исходные решения, фото, контрольные
├── artifacts/nastyushik_repo_artifacts_full.zip
├── data/capability_matrix.csv         # табличная версия матрицы
├── data/artifacts_manifest.csv        # inventory файлов из полной сессии
├── docs/index.html                    # GitHub Pages dashboard
├── docs/day-notes.md                  # краткая история итераций
├── docs/skill-gates.md                # критерии: когда навык считать закреплённым
├── docs/parent-review-checklist.md    # чек-лист для проверки тетради
├── prompts/next-day-template.md       # шаблон запроса для следующего дня
├── prompts/session-prompts.md         # prompts исходной ChatGPT-сессии
├── scripts/generate_dashboard.py      # сборка GitHub Pages dashboard
├── scripts/validate_matrix.py         # простая проверка CSV
└── .github/workflows/                 # CI-проверка и GitHub Pages deploy
```

Структура намеренно похожа на skill-stack подход: есть явная матрица возможностей, критерии прохождения и короткий цикл проверки.

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
6. Пересобрать dashboard и прогнать проверки:

```bash
python3 scripts/generate_dashboard.py
python3 scripts/validate_matrix.py
```

## Рекомендуемое имя GitHub-репозитория

```text
aloschilov/nastyushik-math-skill-stack
```

Рекомендуемая видимость: **private**.
