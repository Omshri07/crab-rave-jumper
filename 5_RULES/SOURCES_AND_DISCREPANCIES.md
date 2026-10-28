# Where each fact came from, and where sources disagreed

The only authoritative source is the organizer's event page (see `OFFICIAL_RULES.md`). Everything
else is secondhand. Searched and read on 2026-10-28.

## Official
- Event page, English: https://beunlimited.me/en/events/crab-robot-challenge-2026
  Read in the built-in browser. A plain text fetch only returns a "loading / local preview
  with fictional sample projects" placeholder, which is a rendering artifact, not the rules.
- Chinese page: https://beunlimited.me/events/crab-robot-challenge-2026 (same placeholder in a
  plain fetch).
- Organizer's product page: https://kingkong.tech/en/jumper and https://kingkong.tech/jumper
  (points to the event page and the community; no rules of its own).
- Repo README: https://github.com/KingKongRobotics/jumper ("Get a free Jumper!" banner linking to
  the event page).

## Secondhand, and what they got right or wrong
| Source | Said | Verdict against the official page |
|---|---|---|
| Chinese news (china.com, Sohu, Sina, Baidu, 2026-09-30) | Douyin only; tags 螃蟹机器人开源动作大赛 and 螃蟹机器人; @梁不歪 @金钢科技; over 15 s; 60/40 judging; 100 engineering units; Chinese entrants must use the toolkit; no closing date | matches the China route. Written before the overseas route and the Oct 30 date were published. |
| pasqualepillitteri.it article | Douyin; "screen recording"; no overseas rule found; no closing date | outdated. The official page has an X or YouTube route for overseas. "Screen recording" is not in the rules: a video is enough. |
| Search summaries and other entrants' READMEs (nik1t7n/crab-challenge, a DEV Community post) | Overseas on X or YouTube; round 1 closes 2026-10-30; originality enforced; music licensing on the entrant; IP infringement disqualifies | all confirmed by the official page. |
| Early search summary | a "raffle" of 100 robots | not accurate: robots go to 100 selected outstanding projects, judged 60 % audience and 40 % expert. |
| Early reports | hashtag lists with extra tags (#手搓万物 in one summary) | the official page lists only the two China tags above. |

## Known conflicts, resolved
- Prize wording "give away 100" (news headline) versus "100 outstanding open-source projects
  will be selected" (official page): use the official wording.
- Deadline: news gave no closing date; the official page and other entrants give round 1 =
  2026-10-30 and the whole contest = 2026-09-30 to 2026-11-30.
- Platform for overseas entrants: news says Douyin only; official page says X or YouTube.

## Facts about the repos that touch the rules
- The toolkit docs say the dance music is not included, because "its source could not be
  established". The repos hold no statement about music in contest videos.
- The repos' README clips are "without audio".
- One other entrant skipped the repo's branded skins because the contest disqualifies IP
  infringement; the official page confirms the originality and IP rule.
- Library skins with third-party characters in `jumper-design` keep their own licenses (see its
  `NOTICE.md`); we used none of them.
