
getMatterLog :
	@echo "retreiving all the logs of the matter-server container"
	@chmod +x ./scripts/getMatterLog.sh
	@./scripts/getMatterLog.sh

getHALog :
	@echo "retreiving all the logs of the homeassistant container"
	@chmod +x ./scripts/getHALog.sh
	@./scripts/getHALog.sh

install :
	@echo "installing the honeypot environment"
	@chmod +x ./scripts/install.sh
	@./scripts/install.sh

clean :
	@echo "cleaning the honeypot environment"
	@chmod +x ./scripts/clean.sh
	@./scripts/clean.sh

back-up :
	@tar -cvf ./back-ups/back-up$(shell date -d "now"  +"%Y-%m-%d-h%Hm%Ms%S").tar ./data ./logs > /dev/null
