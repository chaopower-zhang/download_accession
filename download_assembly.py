# -*- coding: utf-8 -*-
#chao
#2019/7/6


import argparse
import re,os,sys
from ftplib import FTP

def get_path(num):
	match_p = re.compile(r'GC[AF]_0+([1-9]\d+)\.\d')
	match = match_p.match(num)
	if not match:
		print("UNCOTTECT %s" % num)
		return
	else :
		num1 = match.group(1)
		path = "/genomes/all/%s/%s/%s/%s/%s_ASM%sv%s/"\
		       % (num[0:3],num[4:7],num[7:10],num[10:13],num,num1[:-1],num[-1])
	return path


def connect():
	ftp = FTP()
	try:
		ftp.connect("ftp.ncbi.nlm.nih.gov", 21)
	except:
		print("Can not connect NCBI.")
	else:
		ftp.login()
	return ftp


def download(ftp,path):
	try :
		ftp.cwd(path)
	except:
		print("Can not cwd %s ." % path)
	filelist = ftp.nlst()
	n = 1
	for file in filelist:
		wfile = open(file, 'wb')
		ftp.retrbinary('RETR %s' % file, wfile.write)
		wfile.close()
		view_download(n,len(filelist))
		n += 1


def view_download(num, total):
	'''显示进度条'''

	rate = float(num)/float(total)
	rate_num = int(rate * 100)
	number=int(50*rate)
	r = '\r[%s%s]%d%%' % ("#"*number, " "*(50-number), rate_num)
	sys.stdout.write(r)
	sys.stdout.flush()
	if num == total:
		print


def run(num):
	com_path = os.getcwd()
	rem_path = get_path(num)
	if rem_path:
		if not os.path.exists(com_path+"/"+num):
			os.makedirs(num)
		os.chdir(num)
		ftp = connect()
		print("Donwloading %s" % num)
		download(ftp,rem_path)
		os.chdir(com_path)


def main():
	parse = argparse.ArgumentParser("Download file form NCBI assembly ftpsite by using accession number.")
	parse.add_argument('-i','--input',type=file,required=True,help="Files with accession numbers for pep line.")
	args = parse.parse_args()
	with open(args.input) as in_file:
		info = in_file.readlines()
		if info:
			for num in info:
				run(num.strip())
		else:
			print("NO accession number in your file")


if __name__ == '__main__':
	main()