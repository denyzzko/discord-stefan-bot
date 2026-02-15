import asyncio
import logging
from datetime import datetime, timedelta, time, date
import pytz
import random

import discord
from discord.ext import commands, tasks

from src.utils.config_manager import ConfigManager
from src.utils.pet_schedule_manager import PetScheduleManager
from src.utils.strings import CSStrings

logger = logging.getLogger("stefan-bot")

GREEN_CHECK = "✅"
RED_X = "❌"

FILTER_INTERVAL_DAYS = 2
FILTER_MAX_STEPS = 3   # Wed, Fri, Sun (3 reminders per week)
TANK_INTERVAL_DAYS = 7 # weekly reminders

class PetsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_manager
        self.state = bot.pet_schedule
        self.tz = pytz.timezone(self.config.get_timezone())

        # runtime cache for open message IDs
        self.feed_msg_id = None
        self.filter_msg_id = None
        self.tank_msg_id = None

        self.feed_loop.start()
        self.maintenance_loop.start()

    def cog_unload(self):
        self.feed_loop.cancel()
        self.maintenance_loop.cancel()

    # Utility to get channel
    async def get_pets_channel(self):
        channel_id = self.config.get_channel_id()
        guild = self.bot.get_guild(self.config.get_guild_id()) if self.config.get_guild_id() else None
        if channel_id:
            ch = self.bot.get_channel(channel_id)
            if isinstance(ch, discord.TextChannel):
                return ch
        # search by name under guild if provided
        if guild:
            for ch in guild.text_channels:
                if ch.name == self.config.get_channel_name():
                    return ch
        # fallback: global search by name
        for ch in self.bot.get_all_channels():
            if isinstance(ch, discord.TextChannel) and ch.name == self.config.get_channel_name():
                return ch
        return None

    # ---------- FEEDING ----------
    @tasks.loop(minutes=1.0)
    async def feed_loop(self):
        try:
            now = datetime.now(self.tz)
            today = now.date()
            today_str = today.isoformat()

            # Reset state at midnight if needed
            if self.state.data.get("feed", {}).get("date") != today_str:
                self.state.reset_feed_for_today(today_str)
                self.feed_msg_id = None

            # Feeding can be turned off via /pet-reminders-off
            if not self.state.reminders_enabled():
                return

            # At configured feeding time: post initial reminder if not yet posted
            # Default: 13:00
            feed_time_str = self.config.get_time("feeding", "13:00")
            hh, mm = [int(x) for x in feed_time_str.split(":")]
            start_dt = self.tz.localize(datetime.combine(today, time(hh, mm)))

            # Send the start message at start_dt
            if now >= start_dt and not self.state.data["feed"].get("message_id") and not self.state.data["feed"].get("done"):
                channel = await self.get_pets_channel()
                if not channel:
                    logger.warning("Pets channel not found")
                    return
                msg = await channel.send(random.choice(CSStrings.FEED_STARTS))
                try:
                    await msg.add_reaction(GREEN_CHECK)
                except Exception:
                    pass
                self.state.data["feed"]["message_id"] = msg.id
                self.state.data["feed"]["reminder_step"] = 0  # 0 = no reminders sent yet
                self.state.save()
                self.feed_msg_id = msg.id
                return

            # Remind every 4 hours after the start (17:00, 21:00) and then stop
            # Two reminders max.
            if self.state.data["feed"].get("message_id") and not self.state.data["feed"].get("done"):
                step = int(self.state.data["feed"].get("reminder_step", 0))
                if step < 2:
                    target = start_dt + timedelta(hours=4 * (step + 1))
                    if now >= target:
                        channel = await self.get_pets_channel()
                        if channel:
                            await channel.send(random.choice(CSStrings.FEED_REMINDERS))
                        self.state.data["feed"]["reminder_step"] = step + 1
                        self.state.save()
        except Exception as e:
            logger.exception("feed_loop error: %s", e)

    # ---------- WEEKLY & MONTHLY MAINTENANCE ----------
    @tasks.loop(minutes=5.0)
    async def maintenance_loop(self):
        try:
            now = datetime.now(self.tz)
            ch = await self.get_pets_channel()
            if not ch:
                return

            # ----------------- Filter (weekly) -----------------
            post_time_str = self.config.get_post_time("filter_clean", "10:00")
            ph, pm = [int(x) for x in post_time_str.split(":")]
            post_t = time(ph, pm)

            # Post a new assignment strictly on Monday at post_time
            if now.weekday() == 0:
                week = now.isocalendar().week
                year = now.isocalendar().year
                week_str = f"{year}-W{week:02d}"
                if self.state.data["filter"].get("week") != week_str and now.time() >= post_t:
                    self.state.start_week(week_str)
                    await self._post_filter_assignment(ch)

            # Reminders any day: Wed/Fri/Sun at the same post_time
            filt = self.state.data["filter"]
            if self.state.reminders_enabled() and filt.get("week") and not filt.get("done"):
                # derive Monday date of that ISO week
                try:
                    y_s, w_s = filt["week"].split("-W")
                    y_i, w_i = int(y_s), int(w_s)
                    monday_date = date.fromisocalendar(y_i, w_i, 1)
                except Exception:
                    monday_date = now.date()  # fallback

                base_dt = self.tz.localize(datetime.combine(monday_date, post_t))
                step = int(filt.get("reminder_step", 0))
                if step < FILTER_MAX_STEPS:
                    target_dt = base_dt + timedelta(days=FILTER_INTERVAL_DAYS * (step + 1))
                    if now >= target_dt:
                        assignee = await self._current_filter_assignee_mention(ch.guild)
                        await ch.send(CSStrings.FILTER_REMINDER.format(assignee=assignee))
                        self.state.data["filter"]["reminder_step"] = step + 1
                        self.state.save()

            # ----------------- Tank (monthly) -----------------
            t_post_time_str = self.config.get_post_time("tank_clean", "10:00")
            th, tm = [int(x) for x in t_post_time_str.split(":")]
            t_post_t = time(th, tm)

            # Post a new assignment strictly on the 1st at post_time
            if now.day == 1:
                month_str = now.strftime("%Y-%m")
                if self.state.data["tank"].get("month") != month_str and now.time() >= t_post_t:
                    self.state.start_month(month_str)
                    await self._post_tank_assignment(ch)

            # Reminders any day: every 7 days after the 1st at the same post_time
            tank = self.state.data["tank"]
            if self.state.reminders_enabled() and tank.get("month") and not tank.get("done"):
                try:
                    y_s, m_s = tank["month"].split("-")
                    y_i, m_i = int(y_s), int(m_s)
                    first_of_month = date(y_i, m_i, 1)
                except Exception:
                    first_of_month = date(now.year, now.month, 1)

                base_dt = self.tz.localize(datetime.combine(first_of_month, t_post_t))
                step = int(tank.get("reminder_step", 0))
                target_dt = base_dt + timedelta(days=TANK_INTERVAL_DAYS * (step + 1))
                if now >= target_dt:
                    assignee = await self._current_tank_assignee_mention(ch.guild)
                    await ch.send(CSStrings.TANK_REMINDER.format(assignee=assignee))
                    self.state.data["tank"]["reminder_step"] = step + 1
                    self.state.save()

        except Exception as e:
            logger.exception("maintenance_loop error: %s", e)

    # Helpers to get current assignee mention
    async def _current_filter_assignee_mention(self, guild):
        rotation = self.config.get_rotation("filter_clean")
        idx = self.state.data["filter"].get("assignee_index", 0) % max(1, len(rotation))
        if not rotation:
            return "`(není nastavená rotace)`"
        uid = rotation[idx]
        member = guild.get_member(uid)
        return member.mention if member else f"<@{uid}>"

    async def _current_tank_assignee_mention(self, guild):
        rotation = self.config.get_rotation("tank_clean")
        idx = self.state.data["tank"].get("assignee_index", 0) % max(1, len(rotation))
        if not rotation:
            return "`(není nastavená rotace)`"
        uid = rotation[idx]
        member = guild.get_member(uid)
        return member.mention if member else f"<@{uid}>"

    async def _post_filter_assignment(self, channel: discord.TextChannel):
        guild = channel.guild
        rotation = self.config.get_rotation("filter_clean")
        if not rotation:
            await channel.send("⚠️ Není nastavená rotace pro čištění filtru v `config.json`.")
            return

        def eligible(uid):
            return not self.state.get_vacation(uid)

        current_idx = self.state.data["filter"].get("assignee_index", 0)
        uid, idx = self.state.next_in_rotation(rotation, current_idx, eligible)
        if uid is None:
            await channel.send("⚠️ Nikdo není aktuálně způsobilý (dovolené?).")
            return

        self.state.data["filter"]["assignee_index"] = idx
        self.state.save()

        member = guild.get_member(uid)
        mention = member.mention if member else f"<@{uid}>"
        msg = await channel.send(CSStrings.FILTER_ASSIGN.format(assignee=mention))
        try:
            await msg.add_reaction(GREEN_CHECK)
            await msg.add_reaction(RED_X)
        except Exception:
            pass
        self.state.data["filter"]["message_id"] = msg.id
        self.state.save()
        self.filter_msg_id = msg.id

    async def _post_tank_assignment(self, channel: discord.TextChannel):
        guild = channel.guild
        rotation = self.config.get_rotation("tank_clean")
        if not rotation:
            await channel.send("⚠️ Není nastavená rotace pro čištění akvárka v `config.json`.")
            return

        def eligible(uid):
            return not self.state.get_vacation(uid)

        current_idx = self.state.data["tank"].get("assignee_index", 0)
        uid, idx = self.state.next_in_rotation(rotation, current_idx, eligible)
        if uid is None:
            await channel.send("⚠️ Nikdo není aktuálně způsobilý (dovolené?).")
            return

        self.state.data["tank"]["assignee_index"] = idx
        self.state.save()

        member = guild.get_member(uid)
        mention = member.mention if member else f"<@{uid}>"
        msg = await channel.send(CSStrings.TANK_ASSIGN.format(assignee=mention))
        try:
            await msg.add_reaction(GREEN_CHECK)
            await msg.add_reaction(RED_X)
        except Exception:
            pass
        self.state.data["tank"]["message_id"] = msg.id
        self.state.save()
        self.tank_msg_id = msg.id

    # Reactions handler
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # only react to our own messages in the pets channel
        channel = await self.get_pets_channel()
        if not channel or payload.channel_id != channel.id:
            return
        if payload.user_id == self.bot.user.id:
            return

        # fetch the message to know what it is
        try:
            msg = await channel.fetch_message(payload.message_id)
        except Exception:
            return

        emoji = str(payload.emoji)

        # FEEDING flow
        if self.state.data["feed"].get("message_id") == msg.id:
            if emoji == GREEN_CHECK and not self.state.data["feed"].get("done"):
                self.state.mark_fed()
                thanks = random.choice(CSStrings.FEED_THANKS)
                await channel.send(thanks.format(mention=f"<@{payload.user_id}>"))
            return

        # FILTER flow
        if self.state.data["filter"].get("message_id") == msg.id:
            rotation = self.config.get_rotation("filter_clean")
            idx = self.state.data["filter"].get("assignee_index", 0) % max(1, len(rotation)) if rotation else 0
            current_uid = rotation[idx] if rotation else None

            if emoji == GREEN_CHECK and not self.state.data["filter"]["done"]:
                self.state.mark_filter_done()
                await channel.send(CSStrings.FILTER_DONE.format(mention=f"<@{payload.user_id}>"))
                # move index to next for next week
                if rotation:
                    self.state.advance_rotation_index("filter", len(rotation))
                return

            if emoji == RED_X and payload.user_id == current_uid and not self.state.data["filter"]["done"]:
                # reassign to next eligible
                def eligible(uid):
                    return not self.state.get_vacation(uid) and uid != current_uid
                uid, new_idx = self.state.next_in_rotation(rotation, (idx+1) % len(rotation), eligible) if rotation else (None, idx)
                if uid is not None:
                    self.state.data["filter"]["assignee_index"] = new_idx
                    self.state.save()
                    member = channel.guild.get_member(uid)
                    mention = member.mention if member else f"<@{uid}>"
                    new_msg = await channel.send(CSStrings.FILTER_ASSIGN.format(assignee=mention))
                    try:
                        await new_msg.add_reaction(GREEN_CHECK); await new_msg.add_reaction(RED_X)
                    except Exception:
                        pass
                    self.state.data["filter"]["message_id"] = new_msg.id
                    self.state.save()
                return

        # TANK flow
        if self.state.data["tank"].get("message_id") == msg.id:
            rotation = self.config.get_rotation("tank_clean")
            idx = self.state.data["tank"].get("assignee_index", 0) % max(1, len(rotation)) if rotation else 0
            current_uid = rotation[idx] if rotation else None

            if emoji == GREEN_CHECK and not self.state.data["tank"]["done"]:
                self.state.mark_tank_done()
                await channel.send(CSStrings.TANK_DONE.format(mention=f"<@{payload.user_id}>"))
                if rotation:
                    self.state.advance_rotation_index("tank", len(rotation))
                return

            if emoji == RED_X and payload.user_id == current_uid and not self.state.data["tank"]["done"]:
                def eligible(uid):
                    return not self.state.get_vacation(uid) and uid != current_uid
                uid, new_idx = self.state.next_in_rotation(rotation, (idx+1) % len(rotation), eligible) if rotation else (None, idx)
                if uid is not None:
                    self.state.data["tank"]["assignee_index"] = new_idx
                    self.state.save()
                    member = channel.guild.get_member(uid)
                    mention = member.mention if member else f"<@{uid}>"
                    new_msg = await channel.send(CSStrings.TANK_ASSIGN.format(assignee=mention))
                    try:
                        await new_msg.add_reaction(GREEN_CHECK); await new_msg.add_reaction(RED_X)
                    except Exception:
                        pass
                    self.state.data["tank"]["message_id"] = new_msg.id
                    self.state.save()
                return

    # Commands
    @commands.hybrid_command(name="pet-status", description="Zobrazí stav krmení, filtru a akvárka.")
    async def pet_status(self, ctx: commands.Context):
        ch = await self.get_pets_channel()
        if not ch:
            await ctx.reply(CSStrings.NO_CHANNEL)
            return

        guild = ctx.guild
        # feeding
        feed_done = self.state.data.get("feed", {}).get("done", False)
        # filter
        rotation_f = self.config.get_rotation("filter_clean")
        idx_f = self.state.data["filter"].get("assignee_index", 0) % max(1, len(rotation_f)) if rotation_f else 0
        uid_f = rotation_f[idx_f] if rotation_f else None
        assignee_f = (guild.get_member(uid_f).mention if guild and uid_f else "`nenastaveno`")
        filter_done = self.state.data["filter"].get("done", False)
        # tank
        rotation_t = self.config.get_rotation("tank_clean")
        idx_t = self.state.data["tank"].get("assignee_index", 0) % max(1, len(rotation_t)) if rotation_t else 0
        uid_t = rotation_t[idx_t] if rotation_t else None
        assignee_t = (guild.get_member(uid_t).mention if guild and uid_t else "`nenastaveno`")
        tank_done = self.state.data["tank"].get("done", False)

        embed = discord.Embed(title=CSStrings.STATUS_TITLE, color=0x00B2B2)
        embed.add_field(name="🍽️ Krmení (dnes)", value=CSStrings.STATUS_FEED.format(done=("✅" if feed_done else "❌")), inline=False)
        embed.add_field(name="🧽 Filtr (týden)", value=CSStrings.STATUS_FILTER.format(assignee=assignee_f, done=("✅" if filter_done else "❌")), inline=False)
        embed.add_field(name="🪣 Akvárko (měsíc)", value=CSStrings.STATUS_TANK.format(assignee=assignee_t, done=("✅" if tank_done else "❌")), inline=False)
        await ctx.reply(embed=embed, ephemeral=False)

    
    @commands.hybrid_command(name="pet-reminders-off", description="Vypne připomínky (krmení úplně, úklidy jen bez připomínek).")
    async def pet_reminders_off(self, ctx: commands.Context):
        self.state.set_reminders_enabled(False)
        await ctx.reply("🔕 Připomínky jsou vypnuté.")

    @commands.hybrid_command(name="pet-reminders-on", description="Zapne připomínky.")
    async def pet_reminders_on(self, ctx: commands.Context):
        self.state.set_reminders_enabled(True)
        await ctx.reply("🔔 Připomínky jsou zapnuté.")

    @commands.hybrid_command(name="pet-vacation", description="Nastaví/odstraní dovolenou uživatele v rotaci.")
    async def pet_vacation(self, ctx: commands.Context, member: discord.Member, stav: str):
        on = stav.lower() in ("on","true","1","ano","zapnout","zapnuto")
        self.state.set_vacation(member.id, on)
        if on:
            await ctx.reply(CSStrings.VACATION_ON.format(mention=member.mention))
        else:
            await ctx.reply(CSStrings.VACATION_OFF.format(mention=member.mention))

