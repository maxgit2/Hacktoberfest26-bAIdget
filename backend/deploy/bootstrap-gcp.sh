#!/usr/bin/env bash
# One-time GCP setup for the bAIdget backend (run by a project owner).
# Creates: Artifact Registry repo (auto-cleanup), runtime + deployer service accounts (least privilege),
# Secret Manager secret for the Gemini key, Workload Identity Federation for GitHub Actions (this repo only),
# GitHub repo variables, and a 1 EUR budget alert.
# Usage: CLOUDSDK_ACTIVE_CONFIG_NAME=baidget bash deploy/bootstrap-gcp.sh
set -euo pipefail

P=${GCP_PROJECT_ID:-baidget-a6230}
REG=${GCP_REGION:-europe-west1}
REPO=${GITHUB_REPO:-maxgit2/Hacktoberfest26-bAIdget}
BILLING=${BILLING_ACCOUNT:-01BD58-E07740-997706}
PN=$(gcloud projects describe "$P" --format='value(projectNumber)')
API=baidget-api@$P.iam.gserviceaccount.com
DEP=baidget-deployer@$P.iam.gserviceaccount.com
exists() { "$@" >/dev/null 2>&1; }

echo "== Artifact Registry"
exists gcloud artifacts repositories describe baidget --location="$REG" --project="$P" ||
  gcloud artifacts repositories create baidget --repository-format=docker --location="$REG" --project="$P"
policy=$(mktemp)
cat >"$policy" <<'EOF'
[{"name":"keep-3","action":{"type":"Keep"},"mostRecentVersions":{"keepCount":3}},
 {"name":"delete-old","action":{"type":"Delete"},"condition":{"olderThan":"86400s"}}]
EOF
gcloud artifacts repositories set-cleanup-policies baidget --location="$REG" --project="$P" --policy="$policy" --no-dry-run -q >/dev/null
rm -f "$policy"

echo "== Service accounts"
exists gcloud iam service-accounts describe "$API" --project="$P" ||
  gcloud iam service-accounts create baidget-api --display-name="bAIdget API runtime" --project="$P"
exists gcloud iam service-accounts describe "$DEP" --project="$P" ||
  gcloud iam service-accounts create baidget-deployer --display-name="bAIdget GitHub deployer" --project="$P"

# Runtime: Firestore read/write only.
gcloud projects add-iam-policy-binding "$P" --member="serviceAccount:$API" --role=roles/datastore.user --condition=None -q >/dev/null
# Deployer: deploy Cloud Run, push images, deploy Firestore rules/indexes.
for role in roles/run.admin roles/artifactregistry.writer roles/firebaserules.admin roles/datastore.indexAdmin roles/serviceusage.serviceUsageConsumer; do
  gcloud projects add-iam-policy-binding "$P" --member="serviceAccount:$DEP" --role="$role" --condition=None -q >/dev/null
done
gcloud iam service-accounts add-iam-policy-binding "$API" --project="$P" \
  --member="serviceAccount:$DEP" --role=roles/iam.serviceAccountUser -q >/dev/null

echo "== Secret (value added separately, never in this script)"
exists gcloud secrets describe gemini-api-key --project="$P" ||
  gcloud secrets create gemini-api-key --replication-policy=automatic --project="$P"
gcloud secrets add-iam-policy-binding gemini-api-key --project="$P" \
  --member="serviceAccount:$API" --role=roles/secretmanager.secretAccessor -q >/dev/null

echo "== Workload Identity Federation (only $REPO)"
exists gcloud iam workload-identity-pools describe github --location=global --project="$P" ||
  gcloud iam workload-identity-pools create github --location=global --display-name=GitHub --project="$P"
exists gcloud iam workload-identity-pools providers describe github-repo --location=global --workload-identity-pool=github --project="$P" ||
  gcloud iam workload-identity-pools providers create-oidc github-repo --location=global --workload-identity-pool=github --project="$P" \
    --issuer-uri=https://token.actions.githubusercontent.com \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref" \
    --attribute-condition="assertion.repository=='$REPO'"
gcloud iam service-accounts add-iam-policy-binding "$DEP" --project="$P" --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$PN/locations/global/workloadIdentityPools/github/attribute.repository/$REPO" -q >/dev/null

echo "== GitHub repo variables"
gh variable set GCP_PROJECT_ID -R "$REPO" -b "$P"
gh variable set GCP_REGION -R "$REPO" -b "$REG"
gh variable set WIF_PROVIDER -R "$REPO" -b "projects/$PN/locations/global/workloadIdentityPools/github/providers/github-repo"
gh variable set DEPLOY_SA -R "$REPO" -b "$DEP"

echo "== Budget alert (1 EUR, alerts at 50/90/100%)"
gcloud billing budgets list --billing-account="$BILLING" --format='value(displayName)' | grep -qx baidget-budget ||
  gcloud billing budgets create --billing-account="$BILLING" --display-name=baidget-budget \
    --budget-amount=1EUR --filter-projects="projects/$P" \
    --threshold-rule=percent=0.5 --threshold-rule=percent=0.9 --threshold-rule=percent=1.0

echo "Done. Next: add the Gemini key with
  read -rs K && printf %s \"\$K\" | gcloud secrets versions add gemini-api-key --data-file=- --project=$P; unset K"
