*skill-repair — REPAIR_OK_FIXED*

Target: heartbeat

Root cause: Priority Brief branch attempts Resend API call without guarding against empty RESEND_API_KEY, causing gateway cascade failure.

Fix: Added explicit guard check to skip email cleanly when email is unconfigured (20 lines, LOW risk).

PR: https://github.com/ildus650-pixel/aeon/pull/22

Verify: Run skill=heartbeat var=brief