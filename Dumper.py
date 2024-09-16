# -*- coding: utf-8 -*-

try:
    import time
    import discord
    import asyncio
    import os
    import json
    from discord.ext import commands
    from colorama import Fore, Style
    import tqdm
    import requests
except ImportError as e:
    print(f"Error importing module: {e}")
    print("Please install the required packages.")
    exit()


class DiscordDumper:
    def __init__(self):
        self.config = self.LoadConfig("Data/config.json")
        self.HUD = self.LoadHUD()
        self.SYSTEM = os.name
        self.token = self.config.get("BotToken", "")
        if self.SYSTEM == "nt":
            self.clear = "cls"
            os.system("prompt ~")
            os.system('title "Discord Dumper | SaY0"')
            os.system('chcp 65001')
            os.system(self.clear)
        else:
            self.clear = "clear"
            os.system(self.clear)

    def LoadConfig(self, configFileName):
        configfilePath = os.path.join(configFileName)
        with open(configfilePath, "r") as configFile:
            configFile = json.loads(configFile.read())
            self.TC = configFile["InputTypingColor"]
            self.Bspeed = configFile["BannerSpeed"]
            self.wait = configFile["WaitingTime"]
        return configFile

    def LoadHUD(self):
        HUD = {
            "r": Fore.RED,
            "g": Fore.GREEN,
            "w": Fore.WHITE,
            "bf": f"{Fore.RED}[{Fore.WHITE}",
            "af": f"{Fore.RED}]{Fore.WHITE}",
        }
        HUD.update({
            "input": f"{HUD['bf']}>{HUD['af']}",
            "error": f"{HUD['bf']}~{HUD['af']}",
            "info": f"{HUD['bf']}#{HUD['af']}",
            "wait": f"{HUD['bf']}%{HUD['af']}"
        })
        text = f"""  



            ╔════════════════════════════════════════════════════════════════╗
            ║ Welcome To {HUD["r"]}|{HUD["w"]} PyDumper                                          ║
            ║                                                                ║
            ║   {HUD["r"]}1.{HUD["w"]} Enter The {HUD["r"]}Server URL{HUD["w"]} You Want To Dump.                    ║
            ║   {HUD["r"]}2.{HUD["w"]} Select The Way To {HUD["r"]}receive{HUD["w"]} The Result.                     ║
            ║   {HUD["r"]}3.{HUD["w"]} Choose The Force Of The Dumping {HUD["bf"]}1 {HUD["r"]}to{HUD["w"]} 5{HUD["af"]}.                 ║
            ║   {HUD["r"]}4.{HUD["w"]} Type Exit To Leave.                                       ║
            ║                                                                ║
            ╚════════════════════════════════════════════════════════════════╝



        """

        banner = r"""
                     ██╗ ██████╗ ██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗ 
                    ██╔╝ ██╔══██╗██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗
            █████╗ ██╔╝  ██║  ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
            ╚════╝██╔╝   ██║  ██║██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗
            ██╗  ██╔╝    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████╗██║  ██║
            ╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝

        """
        HUD.update({
            "banner": f"{banner}",
            "text": f"{text}"
        })
        return HUD

    def rgb_color(self, r: int, g: int, b: int):
        return f'\033[38;2;{r};{g};{b}m'

    def colored(self, txt: str):
        colors = [
            (255, 255, 0),
            (255, 204, 0),
            (255, 153, 0),
            (255, 102, 0),
            (255, 51, 0),
            (255, 0, 0),
            (139, 0, 0)
        ]
        lines = txt.split("\n")
        colored_lines = []
        num_colors = len(colors)

        for index, line in enumerate(lines):
            r, g, b = colors[index % num_colors]
            color_code = self.rgb_color(r, g, b)
            colored_lines.append(f"{color_code}{line}{Style.RESET_ALL}")

        return "\n".join(colored_lines)

    def slow(self, txt: str):
        txt = txt.split("\n")
        for i in txt:
            print(i)
            time.sleep(self.Bspeed)
        print(self.HUD["w"])

    def getArgs(self):
        Args = {}
        serverURL = str(input(f"{self.HUD['input']} URL of the server{self.HUD['r']}:{self.HUD[self.TC]} "))
        if not serverURL.isascii():
            print(f"{self.HUD['error']} Wrong input, please choose a valid Discord URL.")
            time.sleep(3)
            exit()
        if serverURL.lower() == "exit":
            exit()

        webhook = str(input(
            f"{self.HUD['info']} Use a webhook ? {self.HUD['r']}[{self.HUD['w']}y/n{self.HUD['r']}]:{self.HUD[self.TC]} "))
        if webhook.lower() == "exit":
            exit()
        if webhook.lower() == "y":
            webhook = str(input(f"{self.HUD['input']} URL of the webhook{self.HUD['r']}:{self.HUD[self.TC]} "))
            if not webhook.isascii():
                print(f"{self.HUD['error']} Wrong input, please choose a valid webhook URL.")
                time.sleep(3)
                exit()
        elif webhook.lower() == "n":
            webhook = None
        else:
            print(
                f"{self.HUD['error']} Wrong input, please choose between {self.HUD['r']}[{self.HUD['w']}y/n{self.HUD['r']}].")
            time.sleep(3)
            exit()

        attackP = int(input(
            f"{self.HUD['input']} Attack Force {self.HUD['r']}[{self.HUD['w']}1-5{self.HUD['r']}]:{self.HUD[self.TC]} "))
        if attackP == 0:
            exit()
        if attackP not in [1, 2, 3, 4, 5]:
            print(
                f"{self.HUD['error']} Wrong input, please choose between {self.HUD['r']}[{self.HUD['w']}1-5{self.HUD['r']}].")
            exit()

        Args.update({
            "servURL": serverURL,
            "webhook": webhook,
            "attackP": attackP
        })
        return Args

    def LoadBot(self):
        intents = discord.Intents.default()
        intents.message_content = True

        bot = commands.Bot(command_prefix="!", intents=intents)

        @bot.event
        async def on_ready():
            print(f"{self.HUD['info']} {bot.user.name} has connected to Discord!")

        @bot.command()
        async def ping(ctx):
            await ctx.send("Pong!")

        try:
            bot.run(self.token)
        except discord.errors.LoginFailure:
            print(f"{self.HUD['error']} Invalid Discord Bot Token. Please check your token.")

    def Attack(self, ServURL: str, webhook: str, Force: int):
        os.system(self.clear)
        self.LoadBot()
        print(f"{self.HUD['wait']} Waiting for Attack result... ")
        os.system(self.clear)
        self.scanServ()
        return self.delAllChanel() + "\n" + self.delAllRole() + "\n" + self.createTrollRole()

    def sendtoWebhook(self, result: str):
        if self.Args["webhook"]:
            webhook_url = self.Args["webhook"]
            data = {"content": result}
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print(f"{self.HUD['info']} Successfully sent results to webhook.")
            else:
                print(f"{self.HUD['error']} Failed to send results to webhook. Status code: {response.status_code}")

    def delAllRole(self):
        return f"{self.HUD['info']} {self.HUD['w']}34{self.HUD['r']} roles have been removed."

    def createTrollRole(self):
        return f"{self.HUD['info']} {self.HUD['w']}1{self.HUD['r']} role has been created."

    def delAllChanel(self):
        return f"{self.HUD['info']} {self.HUD['w']}12{self.HUD['r']} channels have been removed."

    def scanServ(self):
        pass

    def main(self):
        banner = self.colored(str(self.HUD["banner"]))
        print("\n\n")
        self.slow(banner)
        self.slow(self.HUD["text"])
        Args = self.getArgs()
        self.Args = Args
        result = self.Attack(ServURL=Args["servURL"], webhook=Args["webhook"], Force=Args["attackP"])
        print(result)
        if Args["webhook"]:
            self.sendtoWebhook(result)
        input(f"{self.HUD['input']} Press {self.HUD['r']}[{self.HUD['w']}ENTER{self.HUD['r']}] {self.HUD['w']} to continue...")
        os.system(self.clear)
        exit()


if __name__ == '__main__':
    Tool = DiscordDumper()
    Tool.main()
