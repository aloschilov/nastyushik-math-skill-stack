# Artifact archive storage

The complete session artifact bundle is intended to be stored with Git LFS for integrity.

Expected archive path:

```text
artifacts/nastyushik_repo_artifacts_full.zip
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
