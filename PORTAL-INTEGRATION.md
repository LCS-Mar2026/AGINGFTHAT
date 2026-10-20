# AFT portal integration for Eva and Walter

Portal origin: https://aft-client-portal-v1-review.cheery-pixie-7406.chatgpt.site

This guide contains no credentials or client records.

The live portal is an authenticated Worker with private R2 storage. The marketing
website is a separate GitHub repository. Neither is a WordPress migration.

## Prospect and client files

`POST /api/admin/prospects` accepts `{name,email,programme,start_date}`. It saves a
draft prospect without assessment folders. The signed fact-find opens the file
and creates the programme assessment stages. Existing client creation and typed
historical signatures remain supported for compatibility.

Save the fact-find with `PUT /api/admin/clients/{id}/fact-find`. A new prospect's
signed submission includes matching `full_name`, `consent_name`,
`consent_signature`, `consent_date`, `explicit_health_consent: "Yes"` and a drawn
PNG `signature_png`. Every save preserves a separate timestamped original with a
content digest. A drawing is a signing record, not independent identity proof.

## Folders and originals

Create a named folder with `POST /api/admin/clients/{id}/folders`, `{name}`.
Upload each original to `POST /api/admin/uploads` with raw file bytes and actual
Content-Type. Query fields: `assessment`, `name`, `category`, optional `folder`,
`title`, and `captured_date` (YYYY-MM-DD). The API returns the source file `id`.
The UI supports multiple files, displays per-file failures and retains successes.
Client/file/folder ownership is checked server-side.

## Eva and Walter report pipeline

Eva's email monitoring remains in Marblism. This repository does not connect to
her mailbox or perform PDF extraction. Walter must extract and validate the
source values, then use the portal API. Never put service credentials in source,
client-side JavaScript, emails, URLs or article content.

1. Match the report's named person to the correct client and assessment. If the
   identity or report date is ambiguous, hold for review; never guess.
2. Upload the original and retain its returned file ID.
3. Get the JSON contract at `GET /api/admin/report-import/schema`.
4. Preview with `POST /api/admin/report-import/preview`.
5. Apply with `POST /api/admin/report-import` using the same payload. Different
   existing values return a conflict unless `replace: true` is explicitly set
   following review. Reusing the same import ID/content is idempotent; changing
   its content is rejected.

Authenticated administrator requests use the session CSRF token. A configured
server-side Marblism integration may instead use the existing `X-AFT-Service-Key`
header. The portal's runtime service secret must be supplied securely by the
owner; this change does not establish a Marblism connection.

Supported types: `DEXA`, `VO2`, `RENPHO`, `blood`, `posture`. Numeric measurements
include `{value,unit}`. Preserve laboratory units and reference intervals. DEXA
lean soft tissue is not RENPHO estimated muscle; DEXA visceral area (cm2) is not a
RENPHO visceral index. Source dates, files, units and imported values are retained
in the import history. RENPHO data is not fed into the DEXA age model. The Level 1
age-reference calculation is still pending approval; this update does not invent
a new scoring method.

## Share a client login

The administrator's Share login by email button generates a random temporary
password and uses the client's email as their username. Clients must choose their
own password before accessing files. Existing access is replaced only after an
explicit reset acknowledgement, and old sessions are invalidated.

This currently prepares an addressed email for the administrator's email app;
it does not send an email. No outbound mail service is connected to this Worker.
The UI distinguishes prepared from sent. No real client invitation is sent by
deployment or tests. Add a supported outbound mail integration before promising
unattended delivery. Share-login responses must never be logged or cached.

## Publication and images

Marketing publication imports and verifies supplied Marblism artwork into
site-owned assets. New blog HTML and images are included automatically; missing
images fail publication. Preserve the site-owned files in a future migration.
Legacy reports remain in place at the owner's direction.
