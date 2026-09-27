# ClipMe video claims sheet (verified 2026-09-26, updated 2026-09-27)

Sources: admin.clipme.com screenshots (customer LIVE page, operator Clip Control dashboard),
clip-control repo (clip_live_any.sh, live_clip_now.sh, CHAT-VELOCITY-BROKEN-2026-09-07.md).

## OK to say
- ClipMe's engine clips LIVE streams on Kick, Twitch and YouTube — records the live feed in windows, clips land during the stream.
- ClipMe clips finished VODs: paste a VOD link or upload a file (self-serve in the app today).
- Ranks moments with a proprietary multi-signal model. Chat activity is one signal on Kick and Twitch.
- Output: captioned 9:16 on every plan; Pro adds 4:5, 1:1 and native. Blur / black / white fill.
- Chat is ONE ranking signal (Kick & Twitch only). Never 'ranked by chat' / 'chat spike = clip'.
- Starter free (ClipMe watermark). Pro $29/mo. Priced per VOD, no per-minute credit meter.
- Starter specifics, per clipme-landing src/app/pricing/page.js + faqs.js (@26916d6): "Free forever. No card, no credits."; 1 VOD a month, under 5 hours; "Full 1080p · ClipMe watermark"; the full AI picker, same as the paid plans. (Known site inconsistency: checkout.js FREE_STREAMS=3 — flagged to the founder; videos follow /pricing.)
- "Chat velocity" is the public term (site page /chat-velocity-clipping). Kick scraper fixed 2026-09-07 and Twitch implemented (CHAT-VELOCITY-BROKEN-2026-09-07.md). Always "one signal", never the ranking itself.
- CTA: "Paste a VOD — try it free" → the matching clipme.com page.

## Do NOT say
- "The second it happens" / instant / real-time per moment.
- That a customer can switch on live clipping themselves in the app (customer LIVE page: "not supported yet").
- Chat signal on YouTube (no YouTube chat implementation).
- Any signal count.
- Auto-posting to TikTok/Reels/Shorts (founder's call, unverified).

## Competitor facts (verified by the 2026-09-26 research workflow — cite the source on screen)
- OpusClip: help center says uploading while still streaming isn't supported; its free plan doesn't take Twitch links (paid plans only — don't name which).
- OpusClip: credits are charged per whole minute of video (help.opus.pro "How Do Credits Work?", checked 2026-09-27).
- Twitch: "Clip That" captures the preceding 60s; Auto Clips is in limited testing (beta signups since May 2026). Twitch auto-makes PORTRAIT clips and shares to Shorts — never call Twitch clips horizontal.
- Eklipse: processes after the stream ends; its site says clips typically land 20–60 min after, longer when the queue is busy. Eklipse calls itself a paid app — don't cite a free plan.
- StreamLadder: ClipGPT (AI finder) gated at $27/mo.
- AutoStreamPro: discontinued — never list as a rival.
- YouTube: the viewer Clip button was retired on April 17, 2026 (TeamYouTube). Never describe it as current.

## Viewer-facing rule
- The only thing a viewer can do today is paste a VOD. Live clipping is always ClipMe's engine, never an instruction ('clip your live stream', 'Live or VOD', 'the fix is to clip live').
