# Screenshots Guide

Capture these screenshots for your portfolio README, LinkedIn, or resume site.

## 1. Passing Test Run

```bash
make up
make test
```

Capture terminal output showing all tests passed (green dots or `PASSED` lines).

**What to highlight:** test count, execution time, zero failures.

## 2. Coverage Report

```bash
make coverage
open reports/coverage/index.html
```

Capture:

- Terminal coverage summary (`--cov-report=term-missing`)
- HTML coverage page showing tested modules

## 3. HTML Test Report (Optional)

```bash
make report
open reports/report.html
```

Capture the pytest-html summary page with pass/fail table.

## 4. GitHub Actions Workflow

After pushing to GitHub:

1. Open **Actions** tab
2. Select the latest **API Tests** run
3. Screenshot the green check and step list

Also screenshot the workflow file in the repo for YAML visibility.

## 5. Sample API Swagger UI

With services running, open:

```
http://localhost:8000/docs
```

Capture the OpenAPI Swagger page listing health, auth, users, and items endpoints.

## 6. Docker Containers Running

```bash
docker compose ps
```

Capture containers `api-test-postgres` and `api-test-sample-api` in healthy/running state.

## Suggested README Layout

| Screenshot | Caption |
|------------|---------|
| Test run | Automated API regression suite |
| Coverage | Test suite coverage report |
| GitHub Actions | CI pipeline on every PR |
| Swagger | Sample FastAPI service under test |
| Docker | Local zero-cost test environment |

## Tips

- Use light mode for readability in portfolio pages
- Crop terminal noise; keep command + result visible
- Blur or omit local paths if sharing publicly
