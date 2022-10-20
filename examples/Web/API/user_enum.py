from asyncio import run
from pyhtools.attackers.web.api.discover import APIdiscover


discoverer = APIdiscover(
    base_url='https://target-api.domain?', # requires question mark at the end
    match_codes=[200,301,],
    rate_limit=20,
    delay=0.05,
    output_file_path=r'output_file_path'
)

run(
    discoverer.start_enum_id(ending_id=40, param_name='userId')
)
