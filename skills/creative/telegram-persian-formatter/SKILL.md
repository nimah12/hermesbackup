---
name: telegram-persian-formatter
description: Format Persian replies as beautiful Telegram channel posts.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags:
      - Telegram
      - Persian
      - Formatting
      - Creative
---

# Telegram Persian Formatter

Format all Persian responses to resemble beautiful Telegram channel posts with a consistent subscribe header, clean typography, and channel-style formatting. Works with any content type — answers, lists, code, media descriptions.

## When to Use
- Every response to user "Nima" (Persian speaker, Iranian)
- Any Persian-language output destined for Telegram delivery
- When you want channel-branded, visually consistent Persian messages

## Prerequisites
- Active Telegram connection (platform handles delivery)
- No external dependencies — pure Markdown formatting

## How to Run
Apply the formatting rules below to every Persian response. No tool invocation needed — this is a response-style skill.

## Quick Reference
| Element | Markdown Pattern |
|---------|------------------|
| Subscribe header | `**📢 کانال ما را در تلگرام جستجو کنید: @YourChannel**` |
| Section header | `## 📌 عنوان بخش` |
| Bullet points | `• متن مورد نظر` |
| Bold emphasis | `**متن مهم**` |
| Code inline | `` `code` `` |
| Code block | ```lang\ncode\n``` |
| Divider | `---` |
| Footer | `🔗 **منبع:** [لینک](url) • **کانال:** @YourChannel` |

## Procedure
1. **Start every Persian response with the subscribe header**  
   `**📢 کانال ما را در تلگرام جستجو کنید: @YourChannel**`  
   (Replace `@YourChannel` with actual channel username if known)

2. **Add a blank line after header** for visual separation

3. **Structure content with clear section headers** using `## 📌` prefix

4. **Use bullet points (•) for lists** instead of dashes or numbers

5. **Emphasize key data with bold** — prices, dates, model names, actions

6. **Wrap code/technical terms in backticks** for inline, fenced blocks for multi-line

7. **Separate major sections with `---` horizontal rules**

8. **End with footer** containing source link (if applicable) and channel reference  
   `🔗 **منبع:** [لینک](url) • **کانال:** @YourChannel`

9. **Keep language 100% Persian** — no English unless user explicitly asks

10. **Use Telegram-supported Markdown only**: bold, italic, strikethrough, spoiler, inline code, code blocks, links, headers

## Pitfalls
- Telegram Markdown does NOT support: tables, task lists, HTML, custom CSS, emoji reactions
- Long messages (>4096 chars) get truncated — split into multiple messages if needed
- Channel username placeholder `@YourChannel` must be replaced with real handle
- Do not use `###` or deeper headers — `##` renders best on mobile
- Avoid excessive formatting; clean > cluttered

## Verification
Send a test Persian response to Telegram and verify:
- Subscribe header appears at top
- Sections render with clear hierarchy
- Bold/italic/code render correctly
- Footer shows at bottom
- Entire message reads naturally in Persian