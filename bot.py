from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from time import time
import stripe
from time import perf_counter
import requests
import random as rnd



bot = Client(
   "CARDER GUNNU",
    api_id = "18314318",
    api_hash = "bfd149250f0b9b9a9308b6d94ee68b3c",
    bot_token = "5358913248:AAGzxNxMU0y8cxKyg5xkV6lGvelfRb2YWOc"
)


GROUP = ["liveccbinchat"]   #array
WELCOME_MESSAGE = "<b>Hey there {}, and welcome to Hunter Bot</b>"
WELCOME_MESSAGE1 = "<b>It's good {}, to see you go!</b>"
cmds_text = "<b>Which commands would you like to check?</b>"

start_button = [
    [InlineKeyboardButton('🔥Join LIVE CC BIN', url='https://t.me/Live_CC_Bin')]
]


#start
@bot.on_message(filters.command('start') & filters.private)
def start(bot, message):  
    username = message.chat.username 
    bot.send_message(message.chat.id, f"""<b>Greetings @{username},

For more commands use /cmds

Join Official Channel <a href="https://t.me/Live_CC_Bin">LIVE CC BIN</a></b>""", disable_web_page_preview=True) 


#cmds
@bot.on_message(filters.command('cmds'))
def cmds(bot, message):
    cmds_buttons = [
    [InlineKeyboardButton('💳 CC Checker Gates', callback_data=f"check_{message.chat.id}_{message.message_id}")],
    [InlineKeyboardButton('🛠 Other Commands', callback_data=f"other_{message.chat.id}_{message.message_id}")]
]
    reply_markup = InlineKeyboardMarkup(cmds_buttons)
    text = cmds_text
    message.reply(
        text = text,
        reply_markup = reply_markup
    )

@bot.on_callback_query()
def cb_data(bot, cb: CallbackQuery):
    cb_data = str(cb.data).split("_")[0]
    cb_chat = int(str(cb.data).split("_")[1])
    cb_message = int(str(cb.data).split("_")[2])

    if cb_data == "checker" and cb_chat == cb.message.chat.id:
        bot.edit_message_text(chat_id = cb_chat, message_id = cb_message, text="**heyya**")

    if cb_data == "other" and cb_chat == cb.message.chat.id:
        bot.send_message(cb.message.chat.id, "**heyya**")
    
##############################################################################################

#leftmember
@bot.on_message(filters.chat(GROUP) & filters.left_chat_member)
def leftmember(client, message):
    left_members = [u.mention for u in message.left_chat_members]
    text = WELCOME_MESSAGE1.format("".join(left_members))
    message.reply_text(text, disable_web_page_preview=True)

#ban
@bot.on_message(filters.command('ban') & filters.group)
def ban(bot, message):
 if message.from_user.id == 1649362800:
    bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    message.reply_text(f"<b>{message.reply_to_message.from_user.mention} Banned!!</b>")
 else:
    message.reply_text("<b>Requires Admin Privilage</b>")
    


#mute
@bot.on_message(filters.command('mute') & filters.group)
def mute(bot, message):
 if message.from_user.id == 1649362800:
    bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(), int(time() + 86400))
    message.reply_text(f"<b>{message.reply_to_message.from_user.mention} Muted!!</b>")
 else:
      message.reply_text("<b>Requires Admin Privilage</b>")


#promote
@bot.on_message(filters.command('promote'))
def promote(bot, message):
 if message.from_user.id == 1649362800:
    bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_manage_chat=True,can_delete_messages=True,can_invite_users=True,can_manage_voice_chats=True)
    message.reply_text(f"<b>{message.reply_to_message.from_user.mention} Promoted!!</b>")
 else:
      message.reply_text("<b>Requires Admin Privilage</b>")

#demote   
@bot.on_message(filters.command('demote'))
def demote(bot, message):
 if message.from_user.id == 1649362800:
    bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_manage_chat=False)
    message.reply_text(f"<b>{message.reply_to_message.from_user.mention} Demoted!!</b>")
 else:
      message.reply_text("<b>Requires Admin Privilage</b>")

@bot.on_message(filters.command('chk'))
def chk(bot,message):
    amoun = int(str(message.text).split()[1])
    amou = amoun * 100
    tic = perf_counter()
    pips = str(message.text).split()[2]
    cc = str(pips).split("|")[0]
    month = str(pips).split("|")[1]
    year = str(pips).split("|")[2]
    cvv = str(pips).split("|")[3]
    stripe.api_key = "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"
    BLACKLISTED = ['489504', '41528505', '51546200', '559558', '543816', '529750', '512319', '519479', '554642', '429304']
    BIN = cc[:6]
    if BIN in BLACKLISTED:
        return message.reply_text(
            "<b>BLACKLISTED BIN</b>"
            )
    if amoun is None:
     amoun=1
    
    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
    token = stripe.Token.create(
  card={
    "number": f"{cc}",
    "exp_month": month,
    "exp_year": year,
    "cvc": f"{cvv}",
  },
)
    charge =   stripe.Charge.create(
    amount=amou,
    currency="usd",
    source=token,
    description="Hunter Donation",
 )
    toc = perf_counter() 
    message.reply_text(f"""
    **CC** ->> `{pips}`
**Status** ->> ✅Approved cvv
**Message** ->> Charged [Receipt]({charge.receipt_url})
**Time** ->> {toc - tic:0.4f}s
**Checked By** ->> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
**Bot By** ->> [Ak Developer](t.me/Owner_Of_Dogeonmmoon)
    """)



#unmute
@bot.on_message(filters.command('unmute') & filters.group)
def unnmute(bot, message):
 if message.from_user.id == 1649362800:
    bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(can_add_web_page_previews=True, can_send_messages=True, can_invite_users=True, can_send_media_messages=True))
    message.reply_text(f"<b>{message.reply_to_message.from_user.mention} Unmuted!!</b>")
 else:
      message.reply_text("<b>Requires Admin Privilage</b>")


#unban
@bot.on_message(filters.command('unban') & filters.group)
def ban(bot, message):
 if message.from_user.id == 1649362800:
    bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    bot.send_message(message.chat.id, f"<b>{message.reply_to_message.from_user.mention} Unbanned, {message.reply_to_message.from_user.mention} can join again!!</b>")
 else:
     message.reply_text("<b>Requires Admin Privilage</b>")

#id
@bot.on_message(filters.command('id'))
def id_reply(bot, message): 
    user_firstname = messag_user.username
    user_id = message.from_user.idm_user.username
    user_id = message.from_user.id
    chat_id = message.chat.id
    message.reply_text(f"""
    **This Chat's id is:** `{chat_id}`
**[{user_firstname}](t.me/{username})'s id is:** `{user_id}`""",
    disable_web_page_preview=True,
    parse_mode = "Markdown"
 )


#welcomebot
@bot.on_message(filters.group & filters.new_chat_members)
def welcome(client, message):
    new_members = [u.mention for u in message.new_chat_members]
    text = WELCOME_MESSAGE.format("".join(new_members))
    message.reply_text(
        text, 
        disable_web_page_preview=True,
        reply_markup = InlineKeyboardMarkup(start_button)
    )

#delmessage
@bot.on_message(filters.text)
def deletetxt(bot, message):
    wordlists = ['fuck', 'wtf', 'pay', 'pussy', 'abuse',  'vagina', 'dick', 'ass', 'lowde', 'bsdk', 'bhenchod', 'madarchod', 'lowda']
    if message.text in wordlists :
        bot.delete_messages(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "<b>MESSAGE Deleted because it contained a BlackListed word</b>")



print('Bot Started')
bot.run()
