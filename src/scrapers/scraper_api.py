import aiofiles, json, os
from aiohttp.client import ClientSession


async def get_assets(number_of_results: int):
    try:
        headers = {
        'Authorization': f'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyR3JvdXBzIjpbImFzc2V0U3RvcmVVc2VycyJdLCJzZWFyY2hIdWIiOiJBc3NldHN0b3JlX1NlYXJjaCIsInY4Ijp0cnVlLCJ0b2tlbklkIjoieG5udnh5d2hnaXhiYm81eTRpcHZ5dmtwZWEiLCJvcmdhbml6YXRpb24iOiJ1bml0eXRlY2hub2xvZ2llc3Byb2R1Y3Rpb25ta2FodGVhdiIsInVzZXJJZHMiOlt7InR5cGUiOiJVc2VyIiwibmFtZSI6ImFub255bW91cyIsInByb3ZpZGVyIjoiRW1haWwgU2VjdXJpdHkgUHJvdmlkZXIifV0sInJvbGVzIjpbInF1ZXJ5RXhlY3V0b3IiXSwiaXNzIjoiU2VhcmNoQXBpIiwiZXhwIjoxNzM5MTM0MjUxLCJpYXQiOjE3MzkwNDc4NTF9.q9IcR3TGIQCf9HKG-R2NjtOEWeDkfZ5WzRmO5bblNSQ',
        'Content-Type': 'application/json'
    }   
        results_path = os.path.join(os.getcwd(), 'src', 'scrapers', 'parse_results', 'result_post.json')
        payload_path = os.path.join(os.getcwd(), 'src', 'scrapers', 'payload.json')
        async with ClientSession(headers=headers) as session:
            async with aiofiles.open(payload_path, 'r', encoding='utf-8') as file:
                payload = json.loads((await file.read()))
                payload["numberOfResults"] = number_of_results
            async with session.post(url="https://unitytechnologiesproductionmkahteav.org.coveo.com/rest/search/v2?organizationId=unitytechnologiesprod", json=payload) as resp:
                if resp.status == 200:
                    async with aiofiles.open(results_path, 'w', encoding='utf-8') as file:
                        await file.write(await resp.text())
                else:
                    return
    except Exception as e:
        raise e
    