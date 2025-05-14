import slixmpp
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

class SendMsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        super().__init__(jid, password)
        self.recipient = recipient
        self.msg = message

        self.add_event_handler("session_start", self.start)
        #self.add_event_handler("disconnected", self.disconnected)

    async def start(self, event):
        print("start")
        self.send_presence()
        await self.get_roster()

        self.send_message(
            mto=self.recipient,
            mbody=self.msg,
            mtype='chat'
        )

        print(f"Message sent to {self.recipient}")
        self.disconnect()

# ==== KONFIGURATION HIER ANPASSEN ====
jid = "max@fhcampus.com"
password = "max"
recipient = "sepp@fhcampus.com"
message = "Hallo vom Slixmpp-Bot!"

xmpp = SendMsgBot(jid, password, recipient, message)
xmpp.enable_starttls = False
xmpp.enable_direct_tls = False
xmpp.use_ipv6 = False
print("pre connect")
#xmpp.connect(("fhcampus.com", 5222), use_ssl=False, force_starttls=False, disable_starttls=True)
#xmpp.connect("fhcamus.com", 5222)
print("after connect")
#asyncio.get_event_loop().run_until_complete(xmpp.disconnected)

import socket

xml_payload = """
<message
       from='juliet@example.com/balcony'
       id='ktx72v49'
       to='romeo@example.net'
       type='chat'
       xml:lang='en'>
     <body>Art thou not Romeo, and a Montague?</body>
   </message>
"""

pres = """
<presence from='juliet@example.com'
                 id='ign291v5'
                 to='romeo@example.net'
                 type='probe'/>
"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("10.0.0.12", 5222))
    s.sendall(pres.encode("utf-8"))