old_urls = []
my_urls = [1, 2, 3]
other_urls = []
for i in range(10):
    if other_urls:
        my_urls = other_urls
    other_urls = []
    for i in my_urls:
        a = i + 1
        other_urls.append(a)
    old_urls += other_urls