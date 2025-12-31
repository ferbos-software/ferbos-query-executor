# Branch Protection Configuration

This document describes the branch protection rules that should be configured in GitHub for this repository.

## Required Settings

### Protected Branches
- `main`
- `develop` (if used)

### Protection Rules

#### 1. Require Pull Request Reviews
- ✅ **Required**: Yes
- **Required number of reviewers**: 2
- **Dismiss stale pull request approvals when new commits are pushed**: Yes
- **Require review from Code Owners**: Yes (if CODEOWNERS file exists)

#### 2. Require Status Checks to Pass
- ✅ **Required**: Yes
- **Required status checks**:
  - `lint` - Lint Code
  - `unit-tests` - Unit Tests (all Python versions)
  - `integration-tests` - Integration Smoke Tests
  - `validate-manifest` - Validate Manifest
  - `check-hacs` - Check HACS Configuration
- **Require branches to be up to date before merging**: Yes

#### 3. Require Conversation Resolution Before Merging
- ✅ **Required**: Yes

#### 4. Require Signed Commits (Optional but Recommended)
- ⚠️ **Recommended**: Yes (if your project requires signed commits)

#### 5. Require Linear History (Optional)
- ⚠️ **Optional**: No (unless your team prefers linear history)

#### 6. Include Administrators
- ✅ **Recommended**: Yes (apply rules to administrators)

## How to Configure

1. Go to your GitHub repository
2. Navigate to **Settings** → **Branches**
3. Click **Add rule** or edit existing rule
4. Configure the settings as described above
5. Save the rule

## Verification

After setting up branch protection, verify it works by:
1. Creating a test PR
2. Ensuring that:
   - PR cannot be merged without 2 approvals
   - PR cannot be merged if CI checks fail
   - PR cannot be merged if there are unresolved conversations

## CI Status Checks

The following status checks are created by the CI workflow:
- `lint` - Code linting
- `unit-tests (3.10)` - Unit tests on Python 3.10
- `unit-tests (3.11)` - Unit tests on Python 3.11
- `unit-tests (3.12)` - Unit tests on Python 3.12
- `integration-tests` - Integration smoke tests
- `validate-manifest` - Manifest validation
- `check-hacs` - HACS configuration check

All of these must pass before a PR can be merged.

## Artifacts

The CI pipeline generates the following artifacts:
- **PR Approvals**: Tracked in GitHub PR interface
- **CI Logs**: Available in GitHub Actions tab
- **Coverage Reports**: Uploaded to Codecov (if configured)

## Troubleshooting

### Status checks not appearing
- Ensure the workflow file is in `.github/workflows/ci.yml`
- Check that the workflow runs on pull_request events
- Verify job names match the required status checks

### Cannot merge despite approvals
- Check that all required status checks have passed
- Ensure branch is up to date with base branch
- Verify no unresolved conversations


