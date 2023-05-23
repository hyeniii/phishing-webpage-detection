package:
	pip install -r requirements.txt --target ./package

package.zip:
	zip -r package.zip package/ src/ config/ lambda_function.py

zip: package.zip