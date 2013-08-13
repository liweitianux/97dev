wget http://mirror.bit.edu.cn/apache/lucene/solr/3.6.2/apache-solr-3.6.2.tgz -O solr.tgz
tar xzvf solr.tgz

# 使用方法
#生成schema.xml:
	#./manage.py build_solr_schema > env/apache-solr-3.6.2/example/solr/conf/schema.xml

#启动solr:
	#java -jar env/apache-solr-3.6.2/example/start.jar

#更新索引:
	#./manage.py update_index
