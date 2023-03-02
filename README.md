## MISSION
a Discord bot that serves as
- proxy commander: forward imagine, upscale, variate, and reroll interactions to a paid Midjourney account
- reactive listener: collect output messages from Midjourney Bot then process accordingly (interpret/persist/broadcast)

## DEVOPS NOTES
- I use Hashi Corp consul as secret keepers here (check the example) but alternatively you can run with a .env file
- More work needs to be done to handle the queue limits stated in Midjourney Standard/Pro plan https://docs.midjourney.com/docs/plans
