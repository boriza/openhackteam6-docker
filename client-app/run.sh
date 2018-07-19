docker build -t boriza/ohclient:1.0 .
docker run -itd --name ohclient --publish 8090:80 boriza/ohclient:1.0

(echo -n '{"image": "'; base64 ./test-image-carabiner.jpeg; echo '"}') |
curl -H "Content-Type: application/json" -d @-  http://localhost:5000/predict