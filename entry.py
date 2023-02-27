import os
from pytz import timezone
import datetime
import driver
from dateutil import parser

TZ = timezone(os.getenv('TZ', default='UTC'))


class Entry:
    def __init__(self, dict) -> None:
        self.marked_for_deletion = False
        self.parse(dict)
        self.process_complex_properties()
        self.deleted_on_database = False

    def __str__(self) -> str:
        return f" Entry <{self.id}: {self.title()}> LE = {self.last_edited_time}. MFD = {self.marked_for_deletion}"

    def title(self):
        try:
            return self.properties['Name']['title'][0]['text']['content']
        except Exception as ex:
            print(ex)
            return "<NAME NOT REACHABLE>"

    def older_than(self, days):
        today = datetime.datetime.now(TZ)
        past_day = today - datetime.timedelta(days=days)

        return self.last_edition_time < past_day

    def newer_than(self, days):
        today = datetime.datetime.now(TZ)
        past_day = today - datetime.timedelta(days=days)

        return self.last_edition_time > past_day

    def between(self, days_start, days_end):
        today = datetime.datetime.now(TZ)
        past_day_start = today - datetime.timedelta(days=days_start)
        past_day_end = today - datetime.timedelta(days=days_end)

        return self.last_edition_time > past_day_start and self.last_edition_time < past_day_end

    def parse(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def process_complex_properties(self):
        try:
            self.last_edition_time = parser.parse(self.last_edited_time)
            self.marked_for_deletion = self.properties['Marked for deletion']['checkbox']
        except Exception as ex:
            print('ERROR parsing properties.', type(ex).__name__, ex)

    def mark_for_deletion(self, value):
        self.marked_for_deletion = driver.set_marked_for_deletion(
            self.id, value)

    def delete_on_database(self):
        print('DELETING', self)
        self.deleted_on_database = driver.delete_entry(self.id)

    def add_comment_on_database(self, comment):
        print('COMMENTING on', self, comment)
        return driver.comment_entry(self.id, comment)

    @classmethod
    def parse_many(klass, items_dicts):
        all = []
        for dict_item in items_dicts:
            all.append(klass(dict_item))

        return all

    @classmethod
    def print_many(klass, items, title='Entries:'):
        print(title)
        for item in items:
            print(item)

    @classmethod
    def list_older_than(klass, items, days):
        today = datetime.datetime.now(TZ)
        past_day = today - datetime.timedelta(days=days)
        result = []
        for entry in items:
            if past_day > entry.last_edition_time:
                result.append(entry)

        return result
