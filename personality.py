import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV2


personality_insights = PersonalityInsightsV2(
    username='deb6b9e4-0853-4b73-aa17-71efddce9ab9',
    password='NM461uOwgTb8')

with open('personality.txt') as personality_text:
    dump = json.dumps(personality_insights.profile(
        text=personality_text.read()), indent=2)

#art = dump["tree"]["children"][0]["children"][0]["children"][0]["children"]
art = json.loads(dump)
a = art["tree"]["children"][0]["children"][0]["children"][0]["children"]
for i in range(len(a)):
	if a[i]['id'] == 'Artistic interests':
		print a[i]['percentage']