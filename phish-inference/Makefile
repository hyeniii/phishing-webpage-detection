package:
	pip install -r requirements.txt --target ./package

package.zip:
	cd package && zip -r ../package.zip . && cd .. && zip -r package.zip src/ config/ && zip package.zip lambda_handler.py 

zip: package.zip