# Resume Bullets

Copy and adapt these bullets for QA, SDET, backend, and software engineering roles.

## QA / SDET

- Built a reusable API testing automation framework with Pytest, HTTPX, schema validation, test data factories, database checks, and CI execution.
- Automated positive, negative, authentication, CRUD, and database validation tests for a FastAPI sample service.
- Integrated coverage reporting and GitHub Actions workflow to support repeatable regression testing.
- Designed JSON Schema contract checks to detect breaking API response changes before release.
- Implemented environment-based test configuration for local and CI execution without paid tooling.

## Backend / Software Engineer

- Improved API reliability by implementing automated tests for authentication, payload validation, protected routes, and persistence behavior.
- Designed reusable API client abstractions and test fixtures to simplify endpoint-level validation across services.
- Validated JWT-protected CRUD workflows with database assertions to confirm API and persistence layer consistency.
- Containerized sample API and PostgreSQL with Docker Compose for reproducible local and CI test environments.

## DevOps-Adjacent

- Created GitHub Actions pipeline that builds services, waits for readiness, runs regression tests, and publishes coverage artifacts.
- Standardized local developer workflow with Makefile targets for up, test, coverage, and reset.

## Interview Talking Points

- Why API tests sit in the middle of the test pyramid
- How schema validation reduces integration risk
- Difference between API response validation and database validation
- How client abstractions reduce duplication across test suites
- How to port this framework to an existing microservice in one afternoon
