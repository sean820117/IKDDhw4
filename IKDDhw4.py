# -*- coding: utf-8 -*-
import re
import numpy as np
import os

class PageRank:
	dead_node = []
	page = []
	page_tmp = []

	def __init__(self, page):
		page_tmp = []
		self.page = page
		for num_page in page:
			tmp = [num_page[0],re.findall('http://page\d.txt', num_page[1])]
			page_tmp.append(tmp)
		self.page_tmp = page_tmp

	def de_DeadEnd(self, page_tmp):
		dead_node = self.dead_node
		front = 0
		end = len(page_tmp)
		flag = 0
		while front < end:
			if len(page_tmp[front][1]) == 0:
				flag = 1
				tmp = page_tmp[front][0]
				page_tmp.pop(front)
				for y in range(0,len(page_tmp)):
					f = 0
					e = len(page_tmp[y][1]) - 1
					while f <= e:
						if cmp(tmp, page_tmp[y][1][f]) == 0:
							page_tmp[y][1].pop(f)
							e = e - 1
						else:
							f = f + 1
				end = end - 1
				dead_node.append(tmp)
			else :
				front = front + 1
		if flag == 1:
			page_tmp = self.de_DeadEnd(page_tmp)

		self.dead_node = dead_node
		return page_tmp

	def get_Rank(self):
		page_true = self.de_DeadEnd(self.page_tmp)
		P_matrix = []
		for k in range(0, len(page_true)):
			row = []
			t = 0
			count = 0.0
			for index_page in page_true:
				row.append(0)
				for j in range(0, len(page_true[k][1])):
					if cmp(index_page[0], page_true[k][1][j]) == 0:
						row[t] = 1.0
						count = count + 1.0
						break
				t = t + 1
			for a in range(0, len(row)):
				if count != 0.0:
					row[a] = row[a] / count
			P_matrix.append(row)

		P_matrix = np.array(P_matrix).transpose()
		Q_matrix = np.linspace(1.0/len(P_matrix),1.0/len(P_matrix),len(P_matrix)) 

		for i in range(40):
			Q_matrix = np.dot(P_matrix,Q_matrix)

		orig = []
		for num_page in self.page:
				tmp = [num_page[0],re.findall('http://page\d.txt', num_page[1])]
				orig.append(tmp)

		index = {}
		for d in range(0, len(page_true)):
			index[page_true[d][0]] = Q_matrix[d]

		for dead in self.dead_node:
			ans = self.recover_dead_node(dead,orig,index)	
			index[dead] = ans

		return index

	def recover_dead_node(self, dead, origin, index):
		result = []
		for node in origin:
			for link in node[1]:
				if cmp(dead, link) == 0:
					flag = 0
					for ii in self.dead_node:
						if cmp(ii, node[0]) == 0:
							flag = 1
					if flag == 1:
						result.append(self.recover_dead_node(node[0],origin,index))
					else :
						result.append(1.0/len(node[1])*index[node[0]])
		ans = 0
		for itera in result:
			ans = ans + itera
		return ans	

def main():
	page = []
	for root, dirs, files in os.walk("webpage_data_5/"):
		try:
			if len(files) == 0:
				exit()
			for p in files:
				path = 'webpage_data_5/'+ os.path.join(p)
				f = open(path,'r')
				file_cont = f.read()
				f.close()
				page.append(['http://' + os.path.join(p), file_cont])
		except:
			print "Open file error or no file!"
			exit()

	rk = PageRank(page)
	result_index = rk.get_Rank()

	while True:
		search_dict = {}
		search = raw_input('Search:')
		for num_page in page:
			result = re.findall(search,num_page[1])
			if len(result) != 0:
				if result_index.get(num_page[0]) != None:
					search_dict[num_page[0]] = result_index[num_page[0]]
				else:
					search_dict[num_page[0]] = 0	

		dict = sorted(search_dict.iteritems(), key = lambda d:d[1], reverse = True)
		print "Rank          Filename"
		print "-----------------------"
		tmp = [-1,-1]
		for s in range(0, len(dict)):
			if tmp[1] == dict[s][1]:
				print  "{0:<12}".format(tmp[0]),
				print dict[s][0][7:]
			else:
				print  "{0:<12}".format(s+1),
				print dict[s][0][7:]
				tmp = [s+1,dict[s][1]]

if __name__ == '__main__':
	main()
