

f = open("/Users/vikramchhikara/PycharmProjects/Project/log_avg_pooling.txt")
g = open("/Users/vikramchhikara/PycharmProjects/Project/extracted_avg_pool.txt", 'w')
lines = f.readlines()

for line in lines:
    line = line[34:38]
    g.write(line)
    # g.writelines('/n')

f.close()
g.close()