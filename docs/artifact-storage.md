# Artifact archive storage

The complete session artifact bundle is intended to be stored with Git LFS for integrity.

Expected archive path:

```text
artifacts/nastyushik_repo_artifacts_full.zip
```

The archive has also been unpacked into repo-facing locations:

```text
artifacts/generated/tasks/            # generated worksheets
artifacts/generated/answers/          # answer keys and checking accents
artifacts/generated/feedback_child/   # child-facing feedback
artifacts/generated/feedback_parent/  # parent-facing feedback
artifacts/source_uploads/pdfs/        # uploaded solutions and target control
artifacts/source_uploads/images/      # uploaded photos/screenshots
prompts/session-prompts.md            # user prompts from the ChatGPT session
scripts/generated/                    # helper scripts from the session
data/artifacts_manifest.csv           # original archive inventory
```

The target control / objective artifact for the dashboard is:

```text
artifacts/source_uploads/pdfs/Экзамен по математике Настюшик.pdf
```

Expected SHA-256:

```text
56bca25bd89dec8ced6d3d74b70c82269e0b03f3c5bdb3dc7a25ca948736e488  artifacts/nastyushik_repo_artifacts_full.zip
```

Recommended local upload flow:

```bash
git clone git@github.com:aloschilov/nastyushik-math-skill-stack.git
cd nastyushik-math-skill-stack

git lfs install
git lfs track "*.zip"

mkdir -p artifacts
cp /path/to/nastyushik_repo_artifacts_full.zip artifacts/
shasum -a 256 artifacts/nastyushik_repo_artifacts_full.zip > artifacts/nastyushik_repo_artifacts_full.zip.sha256

git add .gitattributes artifacts/nastyushik_repo_artifacts_full.zip artifacts/nastyushik_repo_artifacts_full.zip.sha256
git commit -m "Add complete session artifact archive"
git push
```

Integrity check after clone:

```bash
git lfs pull
shasum -a 256 -c artifacts/nastyushik_repo_artifacts_full.zip.sha256
```

Regenerate the GitHub Pages dashboard after changing artifacts or matrix data:

```bash
python3 scripts/generate_dashboard.py
python3 scripts/validate_matrix.py
```
