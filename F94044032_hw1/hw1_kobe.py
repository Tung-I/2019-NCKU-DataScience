import csv
from collections import defaultdict
import heapq
from operator import itemgetter



# load the csv file
with open('kobe.csv', 'rt') as fin:
	cin = csv.reader(fin)
	kobe = [row for row in cin]

# 以欄位名稱為key 每一row視作一個字典組合一個list
rows = []
for i in range(1, len(kobe)):
	cnt = 0
	info = {}
	for mark in kobe[0]:
		info[mark] = kobe[i][cnt]
		cnt+=1
	rows.append(info)




def question1():
	# a defaultdict using opponent as key 
	rows_by_opponent = defaultdict(list)
	for row in rows:
		rows_by_opponent[row['opponent']].append(row)
	# select the opponent
	opponent_chosen = 'HOU'
	num_2PT = 0
	denom_2PT = 0
	num_3PT = 0
	denom_3PT = 0
	for row in rows_by_opponent[opponent_chosen]:
		if row['shot_type'] == '2PT Field Goal':
			denom_2PT+=1
			if row['shot_made_flag'] == '1':
				num_2PT+=1
		elif row['shot_type'] == '3PT Field Goal':
			denom_3PT+=1
			if row['shot_made_flag'] == '1':
				num_3PT+=1
	print("Kobe 對戰火箭隊(HOU)的平均兩分球與三分球命中率")
	print("average 2PT FG% : "+str(num_2PT/denom_2PT))
	print("average 3PT FG% : "+str(num_3PT/denom_3PT))

def question2():
	# a defaultdict using opponent as key 
	rows_by_opponent = defaultdict(list)
	for row in rows:
		rows_by_opponent[row['opponent']].append(row)
	# 紀錄Kobe對上不同對手的平均得分
	avg_point = []
	for opponent in rows_by_opponent.keys():
		info = {}
		n_of_point = 0
		n_of_game = 0
		game_id_remain = '0'
		for row in rows_by_opponent[opponent]:
			if game_id_remain!=row['game_id']:
				n_of_game+=1
				game_id_remain = row['game_id']
			if row['shot_made_flag']=='1':
				if row['shot_type']=='2PT Field Goal':
					n_of_point+=2
				elif row['shot_type']=='3PT Field Goal':
					n_of_point+=3
		info['opponent'] = opponent
		info['avg_point'] = float(n_of_point)/n_of_game
		avg_point.append(info)
	# select top 5 
	top_5 = heapq.nsmallest(5, avg_point, key = lambda s:s['avg_point'])
	print("使得 Kobe 平均得分最低的前五支球隊")
	for i in range(5):
		print(top_5.pop())

def question3():
	# a defaultdict using game_id as key (只收錄季後賽第四節的出手)
	rows_by_game = defaultdict(list)
	for row in rows:
		if row['playoffs']=='1' and row['period']=='4':
			rows_by_game[row['game_id']].append(row)
	# 紀錄game_id & point
	top_5 = []
	for game_id in rows_by_game.keys():
		n_of_point = 0
		info = {}
		for row in rows_by_game[game_id]:
					if row['minutes_remaining']=='2' or row['minutes_remaining']=='1' or row['minutes_remaining']=='0':
						if row['shot_made_flag']=='1':
							if row['shot_type']=='2PT Field Goal':
								n_of_point+=2
							elif row['shot_type']=='3PT Field Goal':
								n_of_point+=3
		info['game_id'] = game_id
		info['point'] = n_of_point
		top_5.append(info)
	# select top 5
	top_5 = heapq.nlargest(5, top_5, key = lambda s:s['point'])
	print("Kobe 在季後賽最後 3 分鐘內得分最高的前五場球賽")
	for i in range(5):
		print(top_5.pop())

def question4():
	# 以球季做區分(只收錄季後賽)
	rows_by_season = defaultdict(list)
	for row in rows:
		if row['playoffs']=='1':
			rows_by_season[row['season']].append(row)
	percentage_season = []
	seasons = []
	shot_made_2000 = 0
	num_of_shot_2000 = 0
	for season in rows_by_season.keys():
		info = {}
		shot_made = 0
		num_of_shot = 0
		for row in rows_by_season[season]:
			# less than 1 minute & jump shot
			if not(season.startswith('1')):
				if row['minutes_remaining']=='0' and row['action_type']=='Jump Shot':
					num_of_shot_2000+=1
					if row['shot_made_flag']=='1':
						shot_made_2000+=1
			else:
				if row['minutes_remaining']=='0' and row['action_type']=='Jump Shot':
					num_of_shot+=1
					if row['shot_made_flag']=='1':
						shot_made+=1
		if season.startswith('1'):
			info['season'] = season
			info['Jump Shot%'] = float(shot_made)/num_of_shot
			percentage_season.append(info)

	info = {}
	info['season'] = "2000-01"
	info['Jump Shot%'] = float(shot_made_2000)/num_of_shot_2000
	percentage_season.append(info)
	percentage_season.reverse()
	print("各球季季後賽中，比賽最後 1 分鐘內的 Jump Shot 命中率")
	for i in range(len(percentage_season)):
		print (percentage_season.pop())

def question5():
	# 確認資料以時間排序
	row_by_date = sorted(rows, key = itemgetter('game_date'))
	# 收集同一場比賽的出手，以game_id為key做成字典
	rows_by_game = defaultdict(list)
	for row in row_by_date:
		rows_by_game[row['game_id']].append(row)
	# 計算每一場比賽的命中率
	rate_each_game = {}
	for game_id in rows_by_game.keys():
		shot_made_cnt = 0
		for row in rows_by_game[game_id]:
			if row['shot_made_flag']=='1':
				shot_made_cnt+=1
		hit_rate = float(shot_made_cnt)/len(rows_by_game[game_id])
		rate_each_game[game_id] = (hit_rate, row['game_date'])
	# 紀錄33%up命中率連續場數及場次
	record = []
	seq = False
	n = 0
	for game_id in rate_each_game.keys():
		rate, date= rate_each_game[game_id]
		if rate>=0.33:
			if seq==True:
				n+=1
				end_date = date
			else:
				n = 1
				start_date = date
				seq = True
		else:
			if seq==True:
				record.append((n, start_date, end_date))
			seq = False
			n = 0
	# 以連勝場數排序後取出前三
	record = sorted(record)
	print("得分命中率33%以上的最長連續場數 前 3 名")
	for i in range(3):
		n, start, end = record.pop()
		print("場數 : "+str(n)+"\n起迄日期 : "+start+"~"+end)



def question6():
	rows_by_game = defaultdict(list)
	for row in rows:
		rows_by_game[row['game_id']].append(row)
	#紀錄命中率，對手，上下半場得分
	record = []
	for game_id in rows_by_game.keys():
		first_half = 0
		second_half = 0
		shot_made_cnt = 0
		for row in rows_by_game[game_id]:
			if row['shot_made_flag']=='1':
				shot_made_cnt+=1
				if row['shot_type']=='2PT Field Goal':
					if row['period']=='1' or row['period']=='2':
						first_half+=2
					else:
						second_half+=2
				elif row['shot_type']=='3PT Field Goal':
					if row['period']=='1' or row['period']=='2':
						first_half+=3
					else:
						second_half+=3
		if first_half>second_half:
			hit_rate = float(shot_made_cnt)/len(rows_by_game[game_id])
			record.append((hit_rate, row['game_date'], row['opponent'], first_half, second_half))

	record = sorted(record)
	print("「上半場得分多於下半場」且命中率最低的前 3 名場次")
	for i in range(3):
		rate, date, oppo, fh, sh = record[i]
		print("命中率 : "+str(rate)+"\t日期 : "+date+"\t對手 : "+oppo+"\t得分差 : "+str(fh-sh))

def question7():
	rows_by_game = defaultdict(list)
	for row in rows:
		rows_by_game[row['game_id']].append(row)

	record = []
	for game_id in rows_by_game.keys():
		seq = False
		n_lost = 0
		max_lost = 0
		n_of_point = 0
		for row in rows_by_game[game_id]:
			#紀錄連續失手
			if row['shot_made_flag']=='0':
				if seq==True:
					n_lost+=1
				else:
					n_lost = 1
					seq = True
			else:
				if seq==True:
					if max_lost<n_lost:
						max_lost = n_lost
					n_lost = 0
				#記錄得分
				if row['shot_type']=='2PT Field Goal':
					n_of_point+=2
				elif row['shot_type']=='3PT Field Goal':
					n_of_point+=3
		record.append((row['game_date'], row['opponent'], max_lost, n_of_point))

	record = sorted(record, key = lambda record:record[2])
	print("「投籃連續失手最多球」之前 3 名場次")
	for i in range(3):
		date, oppo, lost, point = record.pop()
		print("日期 : "+date+"\t對手 : "+oppo+"\t連續失手次數 : "+str(lost)+"\t得分 : "+str(point))


question1()
question2()
question3()
question4()
question5()
question6()
question7()