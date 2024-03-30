
getLogMatter :
	@echo "retreiving all the logs of the matter-server container"
	@chmod +x ./scripts/getLogMatter.sh
	@./scripts/getLogMatter.sh

getLogHA :
	@echo "retreiving all the logs of the homeassistant container"
	@chmod +x ./scripts/getLogHA.sh
	@./scripts/getLogHA.sh

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
