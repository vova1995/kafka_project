#
# Makefile for appservice
#



.PHONY: usage
usage:
	@echo
	@echo 'Usage: make <action>'
	@echo
	@echo '    consumer     run consumer'
	@echo '    producer     run producer'
	@echo '
	@echo '    run          run producer and consumer'
	@echo


producer:
	(cd appservice ; python producer_run.py)

consumer:
	(cd appservice ; python consumer_run.py)

run:
	gnome-terminal -e "bash -c \"make consumer; exec bash\""
	gnome-terminal -e "bash -c \"make producer; exec bash\""
	python appservice/run.py
