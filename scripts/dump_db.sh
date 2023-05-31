sudo docker exec english_bot_mongo_1 sh -c 'mongodump --authenticationDatabase admin -h localhost:27017 -d english_bot -u root  -p example --out=/data/backup'
