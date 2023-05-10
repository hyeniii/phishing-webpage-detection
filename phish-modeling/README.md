## Docker Instructions

- ### Build Docker image for pipeline
    ```bash
    docker build -t <image-name> -f dockerfiles/pipeline.Dockerfile .
    ```

- ### Run Docker image for pipeline
    ```bash
    docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=<user_profile> --name <container-name> <image-name>
    ```

