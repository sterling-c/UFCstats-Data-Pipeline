# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

from datetime import datetime, time
import time 
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Event(scrapy.Item):
    id: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    date: Optional[datetime] = field(default=None)
    location: Optional[str] = field(default=None)
    link: Optional[str] = field(default=None)


@dataclass(frozen=True)
class Fight(scrapy.Item):
    id: Optional[str] = field(default=None)
    event_id: Optional[str] = field(default=None)
    red_id: Optional[str] = field(default=None)
    blue_id: Optional[str] = field(default=None)
    winner: Optional[str] = field(default=None)
    loser: Optional[str] = field(default=None)
    division: Optional[str] = field(default=None)
    time_format: Optional[str] = field(default=None)
    ending_round: Optional[int] = field(default=None)
    ending_time: Optional[datetime] = field(default=None)
    method: Optional[str] = field(default=None)
    details: Optional[str] = field(default=None)
    referee: Optional[str] = field(default=None)
    title_fight: bool = field(default=False)
    perf_bonus: bool = field(default=False)
    fotn_bonus: bool = field(default=False)
    red_kd: Optional[int] = field(default=None)
    blue_kd: Optional[int] = field(default=None)
    red_sig_strike: Optional[int] = field(default=None)
    blue_sig_strike: Optional[int] = field(default=None)
    red_sig_attempt: Optional[int] = field(default=None)
    blue_sig_attempt: Optional[int] = field(default=None)
    red_takedown: Optional[int] = field(default=None)
    blue_takedown: Optional[int] = field(default=None)
    red_takedown_attempt: Optional[int] = field(default=None)
    blue_takedown_attempt: Optional[int] = field(default=None)
    red_sub: Optional[int] = field(default=None)
    blue_sub: Optional[int] = field(default=None)
    red_reversal: Optional[int] = field(default=None)
    blue_reversal: Optional[int] = field(default=None)
    red_control: Optional[datetime] = field(default=None)
    blue_control: Optional[datetime] = field(default=None)
    red_head: Optional[int] = field(default=None)
    blue_head: Optional[int] = field(default=None)
    red_head_attempt: Optional[int] = field(default=None)
    blue_head_attempt: Optional[int] = field(default=None)
    red_body: Optional[int] = field(default=None)
    blue_body: Optional[int] = field(default=None)
    red_body_attempt: Optional[int] = field(default=None)
    blue_body_attempt: Optional[int] = field(default=None)
    red_leg: Optional[int] = field(default=None)
    blue_leg: Optional[int] = field(default=None)
    red_leg_attempt: Optional[int] = field(default=None)
    blue_leg_attempt: Optional[int] = field(default=None)
    red_dist: Optional[int] = field(default=None)
    blue_dist: Optional[int] = field(default=None)
    red_dist_attempt: Optional[int] = field(default=None)
    blue_dist_attempt: Optional[int] = field(default=None)
    red_clinch: Optional[int] = field(default=None)
    blue_clinch: Optional[int] = field(default=None)
    red_clinch_attempt: Optional[int] = field(default=None)
    blue_clinch_attempt: Optional[int] = field(default=None)
    red_ground: Optional[int] = field(default=None)
    blue_ground: Optional[int] = field(default=None)
    red_ground_attempt: Optional[int] = field(default=None)
    blue_ground_attempt: Optional[int] = field(default=None)
    link: Optional[str] = field(default=None)


@dataclass(frozen=True)
class Fighter(scrapy.Item):
    id: Optional[str] = field(default=None)
    first_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)
    t_wins: Optional[int] = field(default=None)
    t_losses: Optional[int] = field(default=None)
    t_draws: Optional[int] = field(default=None)
    t_no_contests: Optional[int] = field(default=None)
    nickname: Optional[str] = field(default=None)
    ufc_wins: Optional[int] = field(default=None)
    ufc_losses: Optional[int] = field(default=None)
    ufc_draws: Optional[int] = field(default=None)
    ufc_no_contests: Optional[int] = field(default=None)
    height: Optional[int] = field(default=None)
    reach: Optional[int] = field(default=None)
    stance: Optional[str] = field(default=None)
    date_of_birth: Optional[datetime] = field(default=None)
    sig_strike_landed: Optional[float] = field(default=None)
    sig_strike_acc: Optional[int] = field(default=None)
    sig_strike_abs: Optional[float] = field(default=None)
    strike_def: Optional[int] = field(default=None)
    takedown_avg: Optional[float] = field(default=None)
    takedown_acc: Optional[int] = field(default=None)
    takedown_def: Optional[int] = field(default=None)
    sub_avg: Optional[float] = field(default=None)
    link: Optional[str] = field(default=None)
