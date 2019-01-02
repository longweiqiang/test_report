### Windows启动定时任务命令

- celery -A test_report worker  --pool=solo

- celery -A test_report beat -l debug

### 初始化sql

```
CREATE TABLE `bug_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `bug_id` int(11) NOT NULL DEFAULT '0' COMMENT '页面id',
  `name` varchar(200) DEFAULT NULL COMMENT '缺陷标题',
  `priority` varchar(20) DEFAULT NULL COMMENT '优先级',
  `status` varchar(20) DEFAULT NULL COMMENT '状态',
  `developer` varchar(50) DEFAULT NULL COMMENT '开发人员',
  `tester` varchar(50) DEFAULT NULL COMMENT '测试人员',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '最后修改时间',
  `upload_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
```
