#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # Exit on error

echo "Setting up environment variables for build..."

# If VITE_API_BASE_URL is not set, construct it based on Render environment
if [ -z "$VITE_API_BASE_URL" ]; then
  if [ "$IS_PULL_REQUEST" = "true" ]; then
    # For preview environments, construct the backend URL using the current branch
    # Render preview URLs follow the pattern: servicename-pr-{number}.onrender.com
    # Extract the PR number or branch suffix from this service's URL
    if [ -n "$RENDER_EXTERNAL_HOSTNAME" ]; then
      # Extract the PR suffix (e.g., "pr-4" from "bonoai-frontend-pr-4.onrender.com")
      # Use sed with -E for extended regex (portable across GNU and BSD sed)
      PR_SUFFIX=$(echo "$RENDER_EXTERNAL_HOSTNAME" | sed -E 's/.*-(pr-[0-9]+).*/\1/')
      if [ -n "$PR_SUFFIX" ]; then
        export VITE_API_BASE_URL="https://bonoai-backend-${PR_SUFFIX}.onrender.com"
        echo "Preview environment detected: Using backend at $VITE_API_BASE_URL"
      else
        # Fallback to production backend
        export VITE_API_BASE_URL="https://bonoai-backend.onrender.com"
        echo "Warning: Could not determine PR number, using production backend"
      fi
    else
      export VITE_API_BASE_URL="https://bonoai-backend.onrender.com"
      echo "Using production backend: $VITE_API_BASE_URL"
    fi
  else
    # Production deployment
    export VITE_API_BASE_URL="https://bonoai-backend.onrender.com"
    echo "Production environment: Using backend at $VITE_API_BASE_URL"
  fi
else
  echo "VITE_API_BASE_URL already set to: $VITE_API_BASE_URL"
fi

echo "Building frontend..."
npm run build

echo "Build completed successfully!"
