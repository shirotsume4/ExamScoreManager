fix:
	isort -rc -sl .
	autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables .
	black .
	isort -rc -m 3 .
run:
	python src/run.py