### MISSION
a Discord bot that serves as
- proxy commander: forward imagine, upscale, variate, and reroll interactions to a [paid Midjourney account](https://docs.midjourney.com/docs/plans)
- reactive listener: collect output messages from Midjourney Bot then process accordingly (interpret/persist/broadcast)

### GETTING STARTED
- Make a Discord bot, so called **mjr-bot**, [get its token and install it into your Discord server](https://www.writebots.com/discord-bot-token/) of choice
- Grab [the Discord user token](https://linuxhint.com/get-discord-token/) of the Discord account that is [on a paid subscription to Midjourney](https://docs.midjourney.com/docs/plans)
- Clone .env-without-consul.example into your own .env and fill in correct values
  ```bash
  cp .env-without-consul.example .env
  vi .env
  ```
- Install requirements (preferably within a virtualenv of python 3.11)
  ```bash
  pip3 install -r requirements.txt 
  ```
- Run the main program 
  ```bash
  python3 main.py
  ```
- In a Discord channel where the **mjr-bot** is invited to, invoke command 

   ```/lucky_imagine: a hippo is skating on an ice field, ultra realistic```
  
### CONTAINERIZATION
- Build docker image
  ```bash
  docker build -t mj-remit:latest -f Dockerfile .
  ```
- Run within a container
  ```bash
  docker run -d -ti --name mj-remit-prod --restart=always --env-file=.env --network="host" mj-remit:latest
  ```

### DEVOPS NOTES
- I use [consul](https://www.consul.io/) as the secret keeper here (check the example) but apparently you can run with your .env so please ignore the consul-example.json and .env-with-consul.example if not applicable
- More work needs to be done to handle the queue limits stated in Midjourney Standard/Pro plan https://docs.midjourney.com/docs/plans
- Feel free to make your own docker-compose.yml to incorporate all dependent services like mongodb and rabbitmq to simplify the deployment to production

### DEFAULT SETTINGS
- `BROADCAST_AND_PERSIST_ENABLED = False` means results are not persisted to db / published to msg queue. If you change this value to `True`, be sure to configure your mongodb & rabbitmq correctly.
- `USE_MESSAGED_CHANNEL = True` means mjr bot will post the results into which ever guild-channel it was talked to, so in case of private channels, be sure it's invited & granted permissions to
