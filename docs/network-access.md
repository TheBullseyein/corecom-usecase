# Network Access — Allowed Domains

This project relies on [Pixelbin](https://www.pixelbin.io/) for image storage and
delivery. Claude Code on the web sessions run in a sandbox whose outbound network
access is governed by the environment's **Network access** setting, so these
domains must be on the environment allowlist for the workflow to reach Pixelbin.

## Allowlisted domains

The canonical list is kept in [`.claude/allowed-domains.txt`](../.claude/allowed-domains.txt),
one domain per line, ready to paste into the environment's **Allowed domains**
field:

| Domain                 | Purpose                                        |
| ---------------------- | ---------------------------------------------- |
| `cdn.pixelbin.io`      | Pixelbin CDN — static asset / image serving    |
| `delivery.pixelbin.io` | Pixelbin delivery — transformed image delivery |

## How to apply

The domain allowlist for Claude Code on the web is configured on the **cloud
environment**, not in a committed file. Committing the list here only records the
requirement — an operator still has to apply it in the environment settings:

1. Open the cloud environment for editing (cloud icon → hover the environment →
   settings icon).
2. Set **Network access** to **Custom** (keep "include defaults" enabled to retain
   the Trusted package-registry allowlist).
3. In the **Allowed domains** field, add one domain per line:

   ```text
   cdn.pixelbin.io
   delivery.pixelbin.io
   ```

4. Save. The setup script re-runs to rebuild the cached environment when the
   allowed hosts change.

Changing the allowed hosts only affects **new** sessions created after the save;
existing sessions keep their original network policy.

Reference: <https://code.claude.com/docs/en/claude-code-on-the-web#network-access>
