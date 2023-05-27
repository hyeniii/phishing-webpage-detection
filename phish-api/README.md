# FAST API


## Containerize

### Build Image in local
```bash
docker build -t phish-api -f Dockerfile.dev
```

### Run Container
```bash
docker run -p 80:80 -v ~/.aws:/root/.aws -e AWS_PROFILE=personal-sso-admin phish-api
```