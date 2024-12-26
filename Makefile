.PHONY: demo

demo:
	docker build -f ./demo/Dockerfile -t demo .
	docker run -it --rm demo
