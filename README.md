## Introduction
this is a mock api to simulate clusters , machines and tags in a cloud env.
where each cluster can have zero or more machines, a machine can have zero or more tags.

## Database design
     Cluster table
|----+----------+--------------|
| id | name     | cloud region |
|----+----------+--------------|
|  1 | cluster1 | us-east-1    |
|----+----------+--------------|

    Machine table ( cluster id as fk)
|----+-------+-------------+---------------+------------|
| id | name  |  ip address | instance type | cluster_id |
|----+-------+-------------+---------------+------------|
|  1 | node1 | 10.10.10.10 | c3.xlarge     |          1 |
|----+-------+-------------+---------------+------------|

    Tag table ( machine id as fk)
|----+------+------------|
| id | name | machine_id |
|----+------+------------|
|  1 | tag1 |          1 |
|----+------+------------|


## how to run locally
import the api-flask postman collection,
It has some testing with environment variables setting and url setting.
It has some predefined API's which are not complete.
for example tags/<str:name> PUT is deleting the machines which is simulation of stop.
