import logging
import re

from scrapy import Spider, Request
from scrapy.utils.log import configure_logging 
from datetime import datetime, time
from stat_scrape.items import Event, Fight, Fighter

def clean_text(response, path):
    return [data.strip() for data in response.xpath(path).getall() if data.strip()]

def convert_height(height):
    clean_height = height.translate({ord(i): None for i in ["\'", '\"']}).split()
    return int(clean_height[0]) * 12 + int(clean_height[1]) 

class UFCStatsSpider(Spider):
    name = "ufcstatspider"
    start_urls = ["http://ufcstats.com/statistics/events/completed?page=all"]
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    def parse(self, response):
        date_format = "%B %d, %Y"
        for row in response.xpath('//*[@class="b-statistics__table-events"]//tbody//tr')[3:]:
            content  =  row.xpath('td[1]//text() | td[1]//@href').getall()
            event = Event(
                id = content[2].split('/')[-1],
                name = ' '.join(content[3].split()),
                date = datetime.strptime(' '.join(content[5].split()), date_format),
                location =  ' '.join(row.xpath('td[2]//text()').getall()[0].split()),
                link = content[2]
            )
            yield event
            yield Request(event.link, callback=self.parse_event, dont_filter=False)
            
            

    def parse_event(self, response):
        for row in response.xpath('//*[@class="b-fight-details__table b-fight-details__table_style_margin-top b-fight-details__table_type_event-details js-fight-table"]//tbody//tr'):
            fight_link = row.xpath("td//a/@href").getall()[0]
            yield Request(fight_link, callback=self.parse_fight, dont_filter=False)

    def parse_fight(self, response):
        event_link = response.xpath('//*[@class="b-content__title"]//a/@href').get()
        fighter_links = response.xpath('//*[@class="b-fight-details__person"]//a/@href').getall()
        special_marks = response.xpath('//*[@class="b-fight-details__fight-head"]//img/@src').getall() 
        winner = None
        loser = None
        for fighter in response.xpath('//*[@class="b-fight-details__persons clearfix"]/div'):
            if re.search('W', ''.join(fighter.xpath('i//text()').get().split())):
                winner = fighter.xpath('//*[@class="b-fight-details__person-text"]/h3/a/@href').get().split()[-1]
            elif re.search('L', ''.join(fighter.xpath('i//text()').get().split())):
                loser = fighter.xpath('//*[@class="b-fight-details__person-text"]/h3/a/@href').get().split()[-1]

        fight_division = response.xpath('normalize-space(//*[@class="b-fight-details__fight-head"])').get()
        fight_details = clean_text(response, '//*[@class="b-fight-details__content"]//text()')
        fight_stats = response.xpath('//*[@class="b-fight-details__table-body"]/tr')
        total_stats = clean_text(fight_stats[0], ('td//text()'))
        red_control = time()
        if re.search(r"^[0-5]?\d:[0-5]\d$", total_stats[18]):
            red_control = time(minute=int(total_stats[18].split(":")[0]), second=int(total_stats[18].split(":")[1]))
        else:
            red_control = None
        
        blue_control = time()
        if re.search(r"^[0-5]?\d:[0-5]\d$", total_stats[19]):
            blue_control = time(minute=int(total_stats[19].split(":")[0]), second=int(total_stats[19].split(":")[1]))
        else:
            blue_control = None

        significant_stats = clean_text(fight_stats[int(len(fight_stats)/2)], ('td//text()'))
        fight = Fight(
            id = response.url.split()[-1],
            event_id = event_link.split()[-1],
            red_id = fighter_links[0].split()[-1],
            blue_id = fighter_links[1].split()[-1],
            winner = winner,
            loser = loser,
            division = fight_division,
            time_format = fight_details[7],
            ending_round = fight_details[3],
            ending_time = time(minute=int(fight_details[5].split(":")[0]), 
                               second=int(fight_details[5].split(":")[1])),
            method = fight_details[1],
            details = ' '.join(fight_details[11:]),
            referee = fight_details[9],
            title_fight = "http://1e49bc5171d173577ecd-1323f4090557a33db01577564f60846c.r80.cf1.rackcdn.com/belt.png" in special_marks,
            perf_bonus = "http://1e49bc5171d173577ecd-1323f4090557a33db01577564f60846c.r80.cf1.rackcdn.com/perf.png" in special_marks,
            fotn_bonus = "	http://1e49bc5171d173577ecd-1323f4090557a33db01577564f60846c.r80.cf1.rackcdn.com/fight.png"in special_marks,
            red_kd = total_stats[2],
            blue_kd = total_stats[3],
            red_sig_strike = int(total_stats[4].split(' of ')[0]),
            blue_sig_strike = int(total_stats[5].split(' of ')[0]),
            red_sig_attempt = int(total_stats[4].split(' of ')[1]),
            blue_sig_attempt = int(total_stats[5].split(' of ')[1]),
            red_takedown = int(total_stats[10].split(' of ')[0]),
            blue_takedown = int(total_stats[11].split(' of ')[0]),
            red_takedown_attempt = int(total_stats[10].split(' of ')[1]),
            blue_takedown_attempt = int(total_stats[11].split(' of ')[1]),
            red_sub = int(total_stats[14]),
            blue_sub = int(total_stats[15]),
            red_reversal = int(total_stats[16]),
            blue_reversal = int(total_stats[17]),
            red_control = red_control,
            blue_control = blue_control,
            red_head = int(significant_stats[6].split(' of ')[0]),
            blue_head = int(significant_stats[7].split(' of ')[0]),
            red_head_attempt = int(significant_stats[6].split(' of ')[1]),
            blue_head_attempt = int(significant_stats[7].split(' of ')[1]),
            red_body = int(significant_stats[8].split(' of ')[0]),
            blue_body = int(significant_stats[9].split(' of ')[0]),
            red_body_attempt = int(significant_stats[8].split(' of ')[1]),
            blue_body_attempt = int(significant_stats[9].split(' of ')[1]),
            red_leg = int(significant_stats[10].split(' of ')[0]),
            blue_leg = int(significant_stats[11].split(' of ')[0]),
            red_leg_attempt = int(significant_stats[10].split(' of ')[1]),
            blue_leg_attempt = int(significant_stats[11].split(' of ')[1]),
            red_dist = int(significant_stats[12].split(' of ')[0]),
            blue_dist = int(significant_stats[13].split(' of ')[0]),
            red_dist_attempt = int(significant_stats[12].split(' of ')[1]),
            blue_dist_attempt = int(significant_stats[13].split(' of ')[1]),
            red_clinch = int(significant_stats[14].split(' of ')[0]),
            blue_clinch = int(significant_stats[15].split(' of ')[0]),
            red_clinch_attempt = int(significant_stats[14].split(' of ')[1]),
            blue_clinch_attempt = int(significant_stats[15].split(' of ')[1]),
            red_ground = int(significant_stats[16].split(' of ')[0]),
            blue_ground = int(significant_stats[17].split(' of ')[0]),
            red_ground_attempt = int(significant_stats[16].split(' of ')[1]),
            blue_ground_attempt = int(significant_stats[17].split(' of ')[1]),
            link = response.url
        )
        yield fight
        for fighter in fighter_links:
            yield Request(fighter, callback=self.parse_fighter, dont_filter=False)

    def parse_fighter(self,response):
        date_format = "%b %d, %Y"
        
        header = clean_text(response, '//*[@class="b-content__title"]//text()')
        first_name = None
        last_name = None
        if len(header[0].split()) < 2: 
            first_name = header[0][0]
        else: 
            first_name, last_name = header[0][0], header[0][-1]
        
        
        record = re.findall(r'\d+', header[1])
        t_wins = int(record[0])
        t_losses = int(record[1])
        t_draws = int(record[2])
        t_no_contests = 0
        if len(record) > 3: 
            t_no_contests = int(record[3])  
        
        nickname = ' '.join(response.xpath('//*[@class="b-content__Nickname"]//text()').get().split())
        
        basic_info = clean_text(response, '//*[@class="b-list__info-box b-list__info-box_style_small-width js-guide"]//text()')
        height = None
        reach = None
        stance = None
        date_of_birth = None
        if basic_info[1] != '--': 
            height = convert_height(basic_info[1])
        if basic_info[5] != '--': 
            reach = int(basic_info[5].replace('\"', ''))
        if basic_info[7] in ['Orthodox', 'Southpaw', 'Switch']: 
            stance = basic_info
        if  basic_info[-1] != '--': 
            date_of_birth = datetime.strptime(' '.join(basic_info[-1].split()), date_format)

        career_stats = clean_text(response, '//*[@class="b-list__info-box b-list__info-box_style_middle-width js-guide clearfix"]//text()')
        ufc_results = clean_text(response, '//*[@class="b-flag__text"]//text()')
        

        fighter = Fighter(
            id = response.url.split()[-1],
            first_name = first_name,
            last_name = last_name,
            t_wins = t_wins,
            t_losses = t_losses,
            t_draws = t_draws,
            t_no_contests = t_no_contests,
            nickname = nickname,
            ufc_wins = ufc_results.count('win'),
            ufc_losses = ufc_results.count('loss'),
            ufc_draws = ufc_results.count('draw'),
            ufc_no_contests = ufc_results.count('nc'),
            height = height,
            reach = reach,
            stance = stance,
            date_of_birth = date_of_birth,
            sig_strike_landed = float(career_stats[2]),
            sig_strike_acc = int(career_stats[4].replace('%', '')),
            sig_strike_abs = float(career_stats[6]),
            strike_def = int(career_stats[8].replace('%', '')),
            takedown_avg = float(career_stats[10]),
            takedown_acc = int(career_stats[12].replace('%', '')),
            takedown_def = int(career_stats[14].replace('%', '')),
            sub_avg = float(career_stats[16]),
            link = response.url
        )

        yield fighter


        


