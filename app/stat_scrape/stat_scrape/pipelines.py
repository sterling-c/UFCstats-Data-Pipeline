from stat_scrape.items import Event, Fight, Fighter
from dotenv import load_dotenv
from datetime import date

import logging
import psycopg
import os


class StatScrapePipeline:
    def __init__(self):
        logging.basicConfig(
            format="%(levelname)s: %(message)s",
            level=logging.DEBUG,
        )

        load_dotenv()
        hostname = os.environ.get("POSTGRES_HOST", "Hostname not found")
        username = os.environ.get("POSTGRES_USER", "Username not found")
        password = os.environ.get("POSTGRES_PASSWORD", "Password not found")
        database = os.environ.get("POSTGRES_DB", "Database name not found")
        port = os.environ.get("POSTGRES_PORT", "Port not found")

        logging.debug("Connecting to database...")

        try:
            self.connection = psycopg.connect(
                host=hostname,
                user=username,
                password=password,
                dbname=database,
                port=port,
            )
            self.cursor = self.connection.cursor()
            logging.info("Connected to database.")
        except:
            logging.error("Could not connect to database.")
            raise

        self.cursor.execute(
            open("stat_scrape/sql/create_events_table.sql", "r").read())
        self.cursor.execute(
            open("stat_scrape/sql/create_fights_table.sql", "r").read())
        self.cursor.execute(
            open("stat_scrape/sql/create_fighters_table.sql", "r").read()
        )

    def process_item(self, item, spider):
        if isinstance(item, Event):
            logging.debug("Inserting event into database...")
            try:
                self.cursor.execute(
                    open("stat_scrape/sql/insert_into_events.sql", "r").read(),
                    (item.id, item.name, item.date, item.location, item.link),
                )
                logging.debug("Inserted event into database.")
            except Exception as e:
                logging.error(f"Could not insert event into database: {e}")
                raise
        elif isinstance(item, Fight):
            logging.debug("Inserting fight into database...")
            try:
                self.cursor.execute(
                    open("stat_scrape/sql/insert_into_fights.sql", "r").read(),
                    (
                        item.id,
                        item.event_id,
                        item.red_id,
                        item.blue_id,
                        item.winner,
                        item.loser,
                        item.division,
                        item.time_format,
                        item.ending_round,
                        item.ending_time,
                        item.method,
                        item.details,
                        item.referee,
                        item.title_fight,
                        item.perf_bonus,
                        item.fotn_bonus,
                        item.red_kd,
                        item.blue_kd,
                        item.red_sig_strike,
                        item.blue_sig_strike,
                        item.red_sig_attempt,
                        item.blue_sig_attempt,
                        item.red_takedown,
                        item.blue_takedown,
                        item.red_takedown_attempt,
                        item.blue_takedown_attempt,
                        item.red_sub,
                        item.blue_sub,
                        item.red_reversal,
                        item.blue_reversal,
                        item.red_control,
                        item.blue_control,
                        item.red_head,
                        item.blue_head,
                        item.red_head_attempt,
                        item.blue_head_attempt,
                        item.red_body,
                        item.blue_body,
                        item.red_body_attempt,
                        item.blue_body_attempt,
                        item.red_leg,
                        item.blue_leg,
                        item.red_leg_attempt,
                        item.blue_leg_attempt,
                        item.red_dist,
                        item.blue_dist,
                        item.red_dist_attempt,
                        item.blue_dist_attempt,
                        item.red_clinch,
                        item.blue_clinch,
                        item.red_clinch_attempt,
                        item.blue_clinch_attempt,
                        item.red_ground,
                        item.blue_ground,
                        item.red_ground_attempt,
                        item.blue_ground_attempt,
                        item.link,
                    ),
                )
                logging.debug("Inserted fight into database.")
            except Exception as e:
                logging.error(f"Could not insert fight into database: {e}")
                raise
        elif isinstance(item, Fighter):
            if (
                len(
                    self.cursor.execute(
                        open("stat_scrape/sql/select_fighters.sql", "r").read(),
                        (item.id,),
                    ).fetchall()
                )
                != 0
            ):
                logging.debug("Fighter already in database. Updating...")
                try:
                    self.cursor.execute(
                        open("stat_scrape/sql/update_fighters.sql", "r").read(),
                        (
                            item.first_name,
                            item.last_name,
                            item.t_wins,
                            item.t_losses,
                            item.t_draws,
                            item.t_no_contests,
                            item.nickname,
                            item.ufc_wins,
                            item.ufc_losses,
                            item.ufc_draws,
                            item.ufc_no_contests,
                            item.height,
                            item.reach,
                            item.stance,
                            item.sig_strike_landed,
                            item.sig_strike_acc,
                            item.sig_strike_abs,
                            item.strike_def,
                            item.takedown_avg,
                            item.takedown_acc,
                            item.takedown_def,
                            item.sub_avg,
                            item.id,
                        ),
                    )
                    logging.debug("Updated fighter in database.")
                except Exception as e:
                    logging.error(f"Could not update fighter in database: {e}")
                    raise

            else:
                logging.debug("Inserting fighter into database...")
                try:
                    self.cursor.execute(
                        open("stat_scrape/sql/insert_into_fighters.sql", "r").read(),
                        (
                            item.id,
                            item.first_name,
                            item.last_name,
                            item.t_wins,
                            item.t_losses,
                            item.t_draws,
                            item.t_no_contests,
                            item.nickname,
                            item.ufc_wins,
                            item.ufc_losses,
                            item.ufc_draws,
                            item.ufc_no_contests,
                            item.height,
                            item.reach,
                            item.stance,
                            item.date_of_birth,
                            item.sig_strike_landed,
                            item.sig_strike_acc,
                            item.sig_strike_abs,
                            item.strike_def,
                            item.takedown_avg,
                            item.takedown_acc,
                            item.takedown_def,
                            item.sub_avg,
                            item.link,
                        ),
                    )
                    logging.debug("Inserted fighter into database.")
                except Exception as e:
                    logging.error(f"Could not insert fighter into database: {e}")
                    raise

        self.connection.commit()
        return item

    def open_spider(self, spider):
        spider.last_event_date = date(1, 1, 1)
        logging.debug("Getting last event date from database...")
        if len(self.cursor.execute("SELECT * from events;").fetchall()) != 0:
            spider.last_event_date = self.cursor.execute(
                "SELECT MAX(date) FROM events;"
            ).fetchone()[0]
        logging.debug(f"Last event date: {spider.last_event_date}")

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
