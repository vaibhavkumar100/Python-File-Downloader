import requests
import sys
import time

units = {
	'B':{'size':1, 'speed':'B/s'},
	'KB':{'size':1024, 'speed':'KB/s'},
	'MB':{'size':1024*1024, 'speed':'MB/s'},
	'GB':{'size':1024*1024*1024, 'speed':'GB/s'}
	}

def check_unit(length):
	if length < units['KB']['size']:
		return 'B'
	elif length >= units['KB']['size'] and length <= units['MB']['size']:
		return 'KB'
	elif length >= units['MB']['size'] and length <= units['GB']['size']:
		return 'MB'
	elif length > units['GB']['size']:
		return 'GB'

def downloadFile(url, directory) :
	localFilename = url.split('/')[-1]
	with open(directory + '/' + localFilename, 'wb') as f:
		print ("Downloading . . .\n")
		start = time.time()
		r = requests.get(url, stream=True)
		total_length = float(r.headers.get('content-length'))
		d = 0
		if total_length is None: # no content length header
			f.write(r.content)
		else:
			for chunk in r.iter_content(8192):
				d += float(len(chunk))
				f.write(chunk)
				tl = total_length / units[check_unit(total_length)]['size']
				trs = d//(time.time() - start)
				speed = units[check_unit(trs)]['speed']

				done = 100 * d / total_length
				sys.stdout.write("\r%6.2f %s [%s%s] %7.2f %s/%7.2f %s  %7.2f %s" % (
					float(done), '%',
					'*' * int(done/2), 
					'_' * int(50-done/2), 
					d/units[check_unit(d)]['size'], check_unit(d), 
					tl, check_unit(total_length), 
					trs/units[check_unit(trs)]['size'], speed))

				sys.stdout.flush()
	return (time.time() - start)

def main() :
	directory = '.'
	if len(sys.argv) > 1 :
		url = sys.argv[1]
		if len(sys.argv) > 2:
			directory = sys.argv[2]
		total_time = downloadFile(url, directory)
		print ('')
		print ("Download complete...")
		print ("\rTime Elapsed: %.2fs" % total_time)
	else :
		print("No link found!")

if __name__ == "__main__" :
	main()
