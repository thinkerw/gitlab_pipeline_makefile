export docker_tag = 1.0.0
docker_tag = $(VERSION)
image = gitlab-outsourcing-users
harbor = harbor.dev.21vianet.com/osam/gitlab-outsourcing-users
tag = $(harbor):$(docker_tag)	
latest = $(image):latest
build:
	@echo "Build the image"
	docker build -t $(tag) .
	docker tag $(tag) $(harbor):latest
	docker push $(harbor)
deploy:	
	@echo "Deploy to production server"
	# - kubectl apply -f /home/thinkerw/pods/pod-gitlab-outsourcing-users.yaml
	kubectl apply -f pod-gitlab-outsourcing-users.yaml
runJob: deploy
	kubectl exec -i -n gitlab pod-gitlab-outsourcing-users python app/gitlab-outsourcing-users.py
