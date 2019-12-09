import autocomplete_me as ac
import time
import statistics as s

def build_time():
	build_time_start = time.time()
	pokemon = ac.build_trie('Data/trademarks.txt')
	build_time_end = time.time()
	build_duration = build_time_end - build_time_start
	print("Build Trie takes %f seconds to finish" %build_duration)
	# return build_duration

# build_time()
trademarks = ac.build_trie('Data/trademarks.txt')

def suggestion_time():
	slow_time_start = time.time()
	ac.slowComplete('Par', 'Data/trademarks.txt',3)
	slow_time_end = time.time()
	slow_duration = slow_time_end - slow_time_start
	auto_time_start = time.time()
	ac.autoComplete('Par', trademarks, 3)
	auto_time_end = time.time()
	auto_duration = auto_time_end - auto_time_start
	# print("Slow Complete takes %f seconds to get the result, and Auto Complete takes %f seconds to get the result" %(slow_duration, auto_duration))
	return slow_duration, auto_duration


def main():
	slow_list = []
	auto_list = []
	for i in range(50):
		slow_time, auto_time = suggestion_time()
		slow_list.append(slow_time)
		auto_list.append(auto_time)
	print(s.mean(slow_list), s.mean(auto_list))

main()


