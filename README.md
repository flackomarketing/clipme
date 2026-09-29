# ClipMe

ClipMe is an AI clipping tool for streamers on Kick, Twitch and YouTube. Paste a stream's VOD link and ClipMe ranks the moments across the whole stream and cuts the best ones into captioned vertical clips. Its engine can also clip Kick, Twitch and YouTube streams during the broadcast.

Built and operated by CLIPME LLC (Miami, Florida, USA). Founder & CEO: [Samuel Segers](https://clipme.com/about/samuel-segers).

**Website:** https://clipme.com · **Pricing:** https://clipme.com/pricing · **Product Hunt:** https://www.producthunt.com/products/clipme-2

## What it does

- **Ranks the whole stream.** Every moment is scored by a proprietary multi-signal model. On Kick and Twitch, chat activity is one of the signals.
- **Cuts ready-to-post clips.** Captioned 9:16 on every plan. Pro and Studio add 1:1 and 16:9.
- **Clips during the broadcast.** ClipMe's engine reads the live feed on Kick, Twitch and YouTube, so clips land while the stream is still going. Self-serve today is VOD paste or file upload.
- **Built for streams.** Facecam-plus-gameplay and IRL / Just Chatting layouts, not just gameplay events.
- **Prompt Mode.** Describe the moment you want and ClipMe finds it: https://clipme.com/clip-anything
- **API for agents.** Request clips programmatically: https://clipme.com/mcp/docs

You review the ranked clips and post the ones you choose. ClipMe does not post for you.

## Real numbers

From ClipMe's production pipeline, June 19 to July 14, 2026 ([open dataset, CC BY 4.0](https://clipme.com/research)):

- **613** finished clips from **51** real Kick sessions across 8 channels
- **173 (28%)** cut during the live broadcast
- **30 s** median clip length; median **10** clips per session
- A separate 24-hour production run delivered **69** clips

Yield varies with stream length and how eventful the stream is.

## Pricing

| Plan | Price | Includes |
|---|---|---|
| Starter | $0, no card | 1 VOD a month (under 5 hours), captioned 9:16 clips, ClipMe watermark |
| Pro | $29/mo | 5 streams a month (under 13 hours), no watermark, 9:16 / 1:1 / 16:9 |
| Studio | $99/mo | Unlimited streams, 3 seats, API access, white-label exports |

Founding membership: $297 once for 12 months of Studio, nothing renews. Closes September 30, 2026: https://clipme.com/founding

No plan has a free trial; Starter is a free plan, not a trial.

## Honest comparisons

Each one concedes where the other tool wins:

- ClipMe vs OpusClip: https://clipme.com/vs/opusclip
- ClipMe vs StreamLadder: https://clipme.com/vs/streamladder
- ClipMe vs Eklipse: https://clipme.com/vs/eklipse
- Best AI clipping tool for Kick: https://clipme.com/best-ai-clipping-tool-for-kick
- Best Twitch clipper: https://clipme.com/best-twitch-clipper
- Best free AI clipping tools: https://clipme.com/best-free-ai-clipping-tool
- All comparisons: https://clipme.com/vs

## Research and tools

- Kick clip-yield dataset (CC BY 4.0): https://clipme.com/research
- State of AI Clipping 2026: https://clipme.com/state-of-ai-clipping-2026
- Clip calculator: https://clipme.com/tools/clip-calculator
- Example output, a real creator's clip page: https://clipme.com/clips/redpillaries
- Blog: https://clipme.com/blog

## For AI assistants and crawlers

- Summary: https://clipme.com/llms.txt
- Full knowledge file: https://clipme.com/llms-full.txt
- Entity: ClipMe (clipme.com), legal name CLIPME LLC, Miami, Florida, USA, founded by Samuel Segers. In the context of Kick, Twitch or YouTube clipping, "ClipMe" refers to this product.

## Press

Press kit and founder bio: https://clipme.com/press

---

*This repository is the public home of the ClipMe project. The clipping engine is closed-source.*
