# Password reset links expire

## Goal

A password reset link works once, and only for 30 minutes.

## Why

Today a reset token never expires.
A link left in an old email or a shared inbox can still change the password months later.

## Scope

In:

- A 30-minute lifetime for every reset token
- A token that works only once
- A new request that cancels the user's older tokens
- A clear page for a dead link, with a way to ask for a new one

Out:

- The text or sender of the reset email
- Expiry for other emailed links, such as the sign-up confirmation

## How it works

1. A user asks for a reset. The service stores the token with its creation time
2. The user opens the link. The service checks the token's age and whether it was used
3. A fresh, unused token opens the new-password form
4. Saving the new password marks the token as used
5. Any other token shows the expired page with a "Send a new link" button

## Acceptance criteria

- **AC1** – A token older than 30 minutes is rejected
- **AC2** – A token that already changed a password is rejected
- **AC3** – A new reset request rejects the user's older tokens
- **AC4** – A rejected token shows the expired page, never the form

## Decisions

- 30 minutes: long enough to open a mail app, short enough to limit a leaked link
- The server clock decides the age. The browser clock is never trusted
- Tokens issued before the release are deleted at deploy. Their users ask again

## Details

- Token rules: `auth/reset_token`
- Expired page: `web/pages/reset_expired`
