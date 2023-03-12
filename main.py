import os
import driver
from dotenv import load_dotenv
from entry import Entry
import datetime
from pytz import timezone
from pdf_generation.generate_pdf import generate_gtd_report
from logging_tools import log

DATES_FORMAT = '%Y-%m-%d_%H:%M:%S'

load_dotenv()
TZ = timezone(os.getenv('TZ', default='UTC'))
today = datetime.datetime.now(TZ)

try:
    fr = open("last_execution.txt", "r")
    last_execution_date = datetime.datetime.strptime(fr.read(), DATES_FORMAT)
    last_execution_date = TZ.localize(last_execution_date)
    CRON_FREQUENCY_DAYS = int(os.getenv('CRON_FREQUENCY_DAYS', default=10))
    time_delta = datetime.timedelta(days=CRON_FREQUENCY_DAYS)
    fr.close()

    if last_execution_date > (today - time_delta):
        log('Execution skipped, last execution was at',
            last_execution_date.strftime(DATES_FORMAT))
        exit(0)

except Exception as ex:
    log('Error checking last execution', type(ex).__name__, ex)
    exit(1)

log('Script will be executed!')

results = []
query_result = driver.get_done_items()
# print(query_result)

try:
    results = query_result['results']
except Exception as ex:
    log('Error parsing query result', type(ex).__name__, ex)
    exit(1)

comment_days = int(os.environ.get('COMMENT_DAYS', default=5))
deletion_days = int(os.environ.get('DELETION_DAYS', default=10))

all_entries = Entry.parse_many(results)
entries_for_deletion = []
entries_for_comment = []

log(f'Processing {len(all_entries)} entries...')
for entry in all_entries:
    if entry.between(deletion_days, comment_days) and not entry.marked_for_deletion:
        time_delta = datetime.timedelta(days=deletion_days)
        tentative_deletion = entry.last_edition_time + time_delta
        tentative_deletion_str = tentative_deletion.strftime('%A. %d/%m/%Y')
        entry.mark_for_deletion(True)
        entry.add_comment_on_database(
            f"[MARKED] Will be deleted after {tentative_deletion_str}")
        entries_for_comment.append(entry)
    elif entry.older_than(deletion_days):
        entries_for_deletion.append(entry)

log(f'Deleting {len(entries_for_deletion)} entries...')

generate_gtd_report(entries_for_comment, entries_for_deletion, all_entries)

for entry in entries_for_deletion:
    entry.delete_on_database()

f = open("last_execution.txt", "w")
f.write(today.strftime(DATES_FORMAT))
f.close()
